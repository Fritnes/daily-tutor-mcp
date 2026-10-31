"""Deterministic answer checking and answer-position control for the Daily Tutor.

Pure functions, no I/O, so they are easy to unit test.
"""
import random
import re

LETTERS = "ABCDE"
KEY_REQUIRED = {"multiple_choice", "multi_select", "true_false", "ordering", "match_pairs"}
ACCEPTED_TYPES = {"fill_blank", "command_challenge", "flashcard"}
AUTO_TYPES = KEY_REQUIRED | ACCEPTED_TYPES


# ------------------------------------------------------------------ keys
def normalize_text(s: str) -> str:
    s = (s or "").strip().strip("`'\".;:").strip()
    return re.sub(r"\s+", " ", s).lower()


def _letters(v, allowed: str = LETTERS) -> list[str]:
    items = re.findall(r"[A-Za-z]", v) if isinstance(v, str) else [str(x).strip() for x in v]
    out = sorted({x.upper() for x in items if x})
    if not out or any(x not in allowed for x in out):
        raise ValueError(f"options must be letters from {allowed}, got {v!r}")
    return out


def normalize_key(qtype: str, key) -> dict:
    """Validate and canonicalise an answer key. Raises ValueError with a fix hint."""
    key = dict(key or {})
    if qtype == "multiple_choice":
        c = _letters(key.get("correct", ""))
        if len(c) != 1:
            raise ValueError("multiple_choice needs answer_key {'correct': 'B'} (exactly one letter)")
        return {"correct": c[0]}
    if qtype == "multi_select":
        c = _letters(key.get("correct", []))
        if len(c) < 2:
            raise ValueError("multi_select needs answer_key {'correct': ['A','C']} (2+ letters)")
        return {"correct": c}
    if qtype == "true_false":
        v = key.get("verdict")
        if isinstance(v, str):
            v = {"true": True, "false": False}.get(v.strip().lower())
        if not isinstance(v, bool):
            raise ValueError("true_false needs answer_key {'verdict': true} or {'verdict': false}")
        return {"verdict": v}
    if qtype == "ordering":
        try:
            order = [int(x) for x in key.get("order", [])]
        except (TypeError, ValueError):
            raise ValueError("ordering needs answer_key {'order': [3,1,4,2]}") from None
        if not 3 <= len(order) <= 8 or sorted(order) != list(range(1, len(order) + 1)):
            raise ValueError("ordering 'order' must be a permutation of 1..n (3 <= n <= 8)")
        return {"order": order}
    if qtype == "match_pairs":
        raw = key.get("pairs") or {}
        pairs = {str(k).strip().upper(): str(v).strip() for k, v in raw.items()}
        n = len(pairs)
        if not 3 <= n <= 6 or sorted(pairs) != list("ABCDEF"[:n]) \
                or sorted(pairs.values()) != [str(i) for i in range(1, n + 1)]:
            raise ValueError("match_pairs needs answer_key {'pairs': {'A':'3','B':'1','C':'4','D':'2'}} "
                             "(letters A.., each number 1..n used once)")
        return {"pairs": pairs}
    if qtype in ACCEPTED_TYPES:
        acc = [str(a).strip() for a in (key.get("accepted") or []) if str(a).strip()]
        return {"accepted": acc} if acc else {}
    return {}


def keys_equal(a: dict, b: dict) -> bool:
    return a == b


def describe_key(qtype: str, key: dict) -> str:
    if qtype == "multiple_choice":
        return key["correct"]
    if qtype == "multi_select":
        return ", ".join(key["correct"])
    if qtype == "true_false":
        return "True" if key["verdict"] else "False"
    if qtype == "ordering":
        return ", ".join(str(x) for x in key["order"])
    if qtype == "match_pairs":
        return ", ".join(f"{k}-{v}" for k, v in sorted(key["pairs"].items()))
    if qtype in ACCEPTED_TYPES and key.get("accepted"):
        return " | ".join(key["accepted"])
    return ""


# ------------------------------------------------------------------ bias control
def dictate(qtype: str, rng=random):
    """Randomly dictate WHERE the correct answer goes, so the LLM cannot favour B/C."""
    if qtype == "multiple_choice":
        return {"correct": rng.choice("ABCD")}
    if qtype == "multi_select":
        return {"correct": sorted(rng.sample(LETTERS, rng.choice([2, 3])))}
    if qtype == "true_false":
        return {"verdict": rng.choice([True, False])}
    if qtype == "ordering":
        order = list(range(1, rng.choice([4, 5]) + 1))
        while order == sorted(order):
            rng.shuffle(order)
        return {"order": order}
    if qtype == "match_pairs":
        nums = ["1", "2", "3", "4"]
        while nums == ["1", "2", "3", "4"]:
            rng.shuffle(nums)
        return {"pairs": dict(zip("ABCD", nums, strict=True))}
    return None


def describe_required(qtype: str, key: dict) -> str:
    if qtype == "multiple_choice":
        return f"The correct option MUST be {key['correct']}. Make the other three plausible distractors."
    if qtype == "multi_select":
        return (f"Use options A-E. The correct options MUST be exactly: {', '.join(key['correct'])}. "
                "The rest are plausible distractors.")
    if qtype == "true_false":
        return f"The statement MUST be {'TRUE' if key['verdict'] else 'FALSE'}."
    if qtype == "ordering":
        n = len(key["order"])
        return (f"Show {n} steps in SHUFFLED display, labelled 1-{n}. Label them so the correct execution "
                f"order is exactly: {', '.join(str(x) for x in key['order'])} "
                f"(the step labelled {key['order'][0]} happens first).")
    if qtype == "match_pairs":
        return ("Items A-D, descriptions 1-4 (shuffled). The correct matches MUST be exactly: "
                + ", ".join(f"{k}-{v}" for k, v in sorted(key["pairs"].items())) + ".")
    return ""


# ------------------------------------------------------------------ grading
def _bad(msg):
    return {"status": "bad_format", "detail": msg}


def _done(result, detail):
    return {"status": "graded", "result": result, "detail": detail}


def _llm(**extra):
    return {"status": "needs_llm", **extra}


def parse_verdict(s: str):
    low = (s or "").lower()
    m = re.search(r"\b(true|false)\b", low) or re.search(r"\b(yes|no)\b", low)
    if m:
        return m.group(1) in ("true", "yes")
    m = re.match(r"\s*([tf])\b", low)
    return (m.group(1) == "t") if m else None


def grade(qtype: str, key: dict, answer: str) -> dict:
    """Return {'status': 'graded'|'needs_llm'|'bad_format', ...}."""
    a = answer or ""

    if qtype == "multiple_choice":
        m = re.search(r"\b([A-Ea-e])\b", a)
        if not m:
            return _bad("Reply with a single letter, e.g. B.")
        got = m.group(1).upper()
        return _done("correct" if got == key["correct"] else "wrong",
                     f"Picked {got}, answer is {key['correct']}.")

    if qtype == "multi_select":
        got = {x.upper() for x in re.findall(r"\b([A-Ea-e])\b", a)}
        if not got:
            return _bad("Reply with letters, e.g. A,C.")
        want = set(key["correct"])
        extras, missed = got - want, want - got
        if not extras and not missed:
            return _done("correct", "Exact set.")
        if (not extras and missed) or (len(extras) == 1 and not missed):
            return _done("partial", f"Missed: {sorted(missed) or '-'}; extra: {sorted(extras) or '-'}.")
        return _done("wrong", f"Missed: {sorted(missed) or '-'}; extra: {sorted(extras) or '-'}.")

    if qtype == "ordering":
        order = key["order"]
        nums = [int(x) for x in re.findall(r"\d+", a)]
        if sorted(nums) != sorted(order):
            return _bad(f"Use each step number 1-{len(order)} exactly once, e.g. "
                        f"{','.join(str(i) for i in range(1, len(order) + 1))}.")
        if nums == order:
            return _done("correct", "Exact order.")
        exp, got = set(zip(order, order[1:], strict=False)), set(zip(nums, nums[1:], strict=False))
        frac = len(exp & got) / len(exp)
        return _done("partial" if frac >= 0.6 else "wrong",
                     f"{len(exp & got)} of {len(exp)} adjacent steps in the right order.")

    if qtype == "match_pairs":
        want = key["pairs"]
        found = re.findall(r"([A-Fa-f])\s*(?:->|=>|→|-|:|=)+\s*(\d)", a)
        if not found:
            return _bad("Reply like: A-2, B-1, C-4, D-3.")
        given = {k.upper(): v for k, v in found}
        hits = sum(1 for k, v in want.items() if given.get(k) == v)
        if hits == len(want):
            return _done("correct", "All pairs right.")
        return _done("partial" if hits * 2 >= len(want) else "wrong", f"{hits} of {len(want)} pairs right.")

    if qtype == "true_false":
        verdict = parse_verdict(a)
        if verdict is None:
            return _bad("Start with True or False, then one line of reasoning.")
        if verdict != key["verdict"]:
            return _done("wrong", f"Verdict was {verdict}, correct is {key['verdict']}.")
        rest = re.sub(r"\b(true|false|yes|no)\b", "", a, flags=re.I)
        if len(re.findall(r"[A-Za-z0-9]+", rest)) < 3:
            return _done("partial", "Right verdict but no reasoning given.")
        return _llm(verdict_correct=True,
                    next_step="Verdict is right. Judge the REASON against key_points: sound = correct, "
                              "weak or wrong reason = partial. Then call record_result.")

    if qtype in ACCEPTED_TYPES:
        accepted = key.get("accepted") or []
        if normalize_text(a) in {normalize_text(x) for x in accepted}:
            return _done("correct", "Matches an accepted answer.")
        return _llm(accepted_answers=accepted,
                    next_step="No exact match. Judge whether the answer is an equivalent that WORKS "
                              "(different flags order, long/short options, synonyms). Then call record_result.")

    return _llm(next_step="Free-text answer: judge it against key_points and the grading guide, "
                          "then call record_result.")
