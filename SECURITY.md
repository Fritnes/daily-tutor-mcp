# Security Policy

## Reporting a vulnerability

Please **do not open a public issue**. Use GitHub's
[private vulnerability reporting](https://github.com/fritnes/daily-tutor-mcp/security/advisories/new)
(Security tab, "Report a vulnerability"). You will get an acknowledgement within a few days.

## Supported versions

Only the latest release receives security fixes.

## Threat model and design notes

- **Authentication.** HTTP mode requires `TUTOR_API_TOKENS`; the server refuses to start without them. Tokens are
  static bearer tokens compared in constant time. Treat them like passwords: long, random, rotated, never committed.
- **Tenant isolation.** In HTTP mode the user id comes from the verified token. The `user_id` tool argument is
  ignored, so one user cannot address another's data. In stdio mode there is a single local user.
- **Transport.** The server speaks plain HTTP. Run it behind a TLS-terminating reverse proxy and set
  `TUTOR_ALLOWED_HOSTS` to your hostname.
- **Prompt injection.** Text added with `add_material` is stored as data and handed to the model with an explicit
  instruction to ignore directives inside it. This reduces, but cannot eliminate, injection risk: do not add
  material from sources you do not trust to an instance connected to powerful tools.
- **Answer keys.** Correct answers are stored server-side and only returned to the model (`get_pending_question`),
  not to the end user. A model that chooses to leak them can still do so.
- **Data at rest.** A single SQLite file in `TUTOR_DATA_PATH`, unencrypted. Use disk encryption and back it up.
- **Container.** Runs as a non-root user; compose sets a read-only root filesystem, `no-new-privileges` and drops all capabilities.

## Out of scope

OAuth/OIDC is not implemented (see the roadmap). Denial-of-service against a publicly exposed instance without a
rate-limiting proxy is not considered a vulnerability.
