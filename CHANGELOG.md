# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Spec-driven development with GitHub Spec Kit (`specify-cli` 1.2.5, Claude Code integration): project
  constitution, templates and skills under `.specify/` and `.claude/skills/`; workflow documented in CONTRIBUTING.

## [0.3.0] - 2026-10-31

First public release.

### Added
- Multi-topic practice with per-topic levels, subtopics and mixed-topic questions.
- 13 question types, with server-side exact grading for the deterministic ones (`check_answer`).
- Anti-bias control: the server dictates the position of the correct answer and rejects duplicates and repeated concepts.
- Spaced repetition (1, 3, 7, 14, 30 days) and adaptive difficulty per topic.
- Sessions, XP, daily goal, streaks with freezes, hints, skip, weekly recap, mistake review.
- Certification tracks (CCNA, CKA, RHCSA, AWS SAA, Terraform Associate) with objective coverage.
- Own-material questions (`add_material`).
- Streamable HTTP transport with bearer-token auth and per-user isolation.
- Timezone-aware days (`set_settings`).
- Versioned SQLite migrations; existing databases migrate in place.
- Docker image (non-root), docker-compose, GitHub Actions CI, agent skill, 42 tests.
