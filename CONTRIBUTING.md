# Contributing

This is currently a small personal experiment maintained by **fritnes**. External contributions and pull requests
are not being accepted at this time; this policy may change in the future. This guide documents the development
workflow for the maintainer.

## Setup

```bash
git clone https://github.com/fritnes/daily-tutor-mcp.git && cd daily-tutor-mcp
python -m venv .venv && source .venv/bin/activate
make install
make test lint
```

## Ground rules

- **Tests are required** for behaviour changes. Time-dependent code takes the clock from `server._now`; tests patch it.
- `make lint` must pass (ruff). `make docs` must leave `docs/TOOLS.md` unchanged (CI checks this).
- **Never edit an old migration.** Append a new function to `MIGRATIONS` in `server.py`; migrations must be idempotent.
- Anything the LLM might get wrong (grading, scheduling, positions, counting) belongs in code, not in a prompt.
- User-supplied text (materials) is **data, never instructions**. Keep it that way.
- Keep tool docstrings clear: they are the model's manual, and they generate `docs/TOOLS.md`.

## Recipes

**Add a question type**
1. Add it to `QTYPES` in `server.py` (`levels`, `reply`, `write`, `grade`).
2. If it can be graded exactly, add key normalisation, `grade()` and (if the answer position matters) `dictate()` in `grading.py`, and list it in `KEY_REQUIRED` or `ACCEPTED_TYPES`.
3. Add tests in `tests/test_tutor.py`, then `make docs`.

**Add a certification track**: add an entry to `tracks.py` (no commas inside objective names). Base it on the vendor's public exam guide and say so in the PR.

**Add a tool**: write it in `server.py` with a precise docstring, add it to `GROUPS` in `scripts/gen_tools_doc.py`, add tests, run `make docs`.

## Spec-driven development (Spec Kit)

Non-trivial features start as a spec, using [GitHub Spec Kit](https://github.github.com/spec-kit/). The project is
already initialised (`.specify/` and `.claude/skills/`), and our rules live in
[`.specify/memory/constitution.md`](.specify/memory/constitution.md). Plans are checked against it.

```bash
# one-time: install the CLI (needs Python 3.11+; the package itself supports 3.10+)
uv tool install specify-cli          # or: pipx install specify-cli
specify version
```

In Claude Code, run the skills in order (the Claude integration names them with hyphens):

| Step | Skill | Result |
|---|---|---|
| 1 | `/speckit-specify <what and why>` | `specs/<NNN-feature>/spec.md` |
| 2 | `/speckit-clarify` (optional) | ambiguities resolved in the spec |
| 3 | `/speckit-plan` | design, checked against the constitution |
| 4 | `/speckit-tasks` then `/speckit-analyze` | task list and cross-artifact consistency check |
| 5 | `/speckit-implement` | code and tests |
| 6 | `/speckit-converge` | gaps appended as tasks until done |

Tips: describe the **compatibility boundaries** too (for example "existing databases must migrate in place");
keep the first change small; review the generated spec, plan and code together in the PR. Commit the whole
feature folder under `specs/`. Other agents are supported: `specify init --here --force --integration <key>`.
Small fixes, docs and dependency bumps do not need a spec.

## Pull requests

- Small, focused PRs. Describe the behaviour change and how you tested it.
- Use [Conventional Commits](https://www.conventionalcommits.org/) style titles (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- Update `CHANGELOG.md` under **Unreleased**.

By contributing you agree your work is licensed under the [MIT License](LICENSE).
