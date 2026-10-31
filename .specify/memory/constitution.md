# Daily Tutor MCP Constitution

These principles are distilled from rules this repository already follows and enforces
(`docs/ARCHITECTURE.md`, `CONTRIBUTING.md`, `SECURITY.md`, CI and the test suite). Specs, plans and
tasks MUST comply with them. Unrealistic or aspirational rules do not belong here.

## Core Principles

### I. The Server Owns the Rules; the LLM Owns the Words
Anything an LLM can get wrong MUST be implemented in code, not in a prompt: grading, scheduling, counting,
streaks, difficulty, duplicate detection and the position of the correct answer. The model is used only to
write scenarios and explanations and to judge free-text answers against a rubric. A feature that moves a
deterministic decision into a prompt MUST be rejected or justified in the plan's Complexity Tracking.

### II. Behaviour Changes Ship With Tests
Every behaviour change MUST include automated tests in `tests/`. Time-dependent logic MUST read the clock
through `server._now` so tests can control it, and "today" MUST be computed in the user's timezone. Pure
logic (for example grading) MUST stay side-effect free in `grading.py` so it can be tested in isolation.
`make test lint` MUST pass before merge.

### III. Data Is Migrated, Never Broken
Schema changes MUST be new, idempotent functions appended to `MIGRATIONS`; an existing migration MUST NOT be
edited. Databases from earlier versions MUST upgrade in place without data loss, and migrations that change
meaning (for example streaks) MUST backfill from existing data.

### IV. Tenant Isolation and Authenticated Remote Access
Over HTTP the user identity MUST come from the verified bearer token, and any `user_id` argument MUST be
ignored. The server MUST refuse to start in HTTP mode without configured tokens. Tokens MUST be compared in
constant time. Per-user data MUST NOT be readable by another user through any tool.

### V. User Content Is Data, Never Instructions
Text supplied by users (for example materials) MUST be stored and presented to the model as data with an
explicit instruction not to follow directives inside it. New features that ingest external text MUST apply the
same rule.

### VI. Tool Docs Have One Source of Truth
Tool docstrings are the model's manual and generate `docs/TOOLS.md`. Every new tool MUST have a precise
docstring, be listed in `scripts/gen_tools_doc.py`, and leave `make docs` with no uncommitted diff (CI checks
this).

### VII. Keep It Simple and Operable
Prefer one SQLite file and no extra services. Add a dependency, service or abstraction only when the plan
justifies why a simpler option fails. The container MUST run as a non-root user with state confined to the
`/data` volume.

## Additional Constraints

- **Runtime**: Python 3.10+ for the package (CI matrix 3.10 to 3.13); `mcp` is pinned to `>=1.9,<2`.
- **Transports**: `stdio` (single local user) and Streamable HTTP with bearer-token auth. OAuth is roadmap work
  and MUST go through its own spec and security review.
- **Content accuracy**: certification objective lists MUST be based on the vendor's public exam guide, contain
  no commas inside an objective name, and be described as study outlines, not official blueprints.
- **Question quality**: the server MUST keep rejecting duplicate wording, repeated concepts and wrong answer
  positions; changes MUST NOT weaken these checks without replacing them.

## Development Workflow and Quality Gates

- Non-trivial features start with the Spec Kit flow: specify, clarify, plan, tasks, analyze, implement,
  converge. Small fixes, docs and dependency bumps MAY skip it.
- A change is mergeable only when CI is green: ruff, tests on all supported Python versions, generated docs
  up to date, and the Docker smoke test showing that authentication is enforced.
- Update `CHANGELOG.md` under **Unreleased**; use Conventional Commit titles.
- Plans MUST include a Constitution Check against Principles I to VII.

## Governance

This constitution supersedes other practices where they conflict. Amendments require a pull request that
states the reason, updates affected docs, and bumps the version (MAJOR: a principle removed or redefined;
MINOR: a principle or section added; PATCH: clarification). All reviews MUST verify compliance, and any
deviation MUST be recorded and justified in the relevant plan. Day-to-day guidance lives in `CONTRIBUTING.md`
and `docs/ARCHITECTURE.md`.

**Version**: 1.0.0 | **Ratified**: 2026-10-31 | **Last Amended**: 2026-10-31
