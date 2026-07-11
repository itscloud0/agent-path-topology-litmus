# Security

## Scope

Fixtures are created only under the user-provided output directory. The suite does not read secrets, execute agent-written code, call live models, or intentionally write through symlinks that resolve outside the fixture repository.

Diagnostic adapters invoke installed local client binaries. They use disposable client homes so user-global configuration does not affect results.

## Reporting

Do not include secrets, private repository contents, or exploit payloads in a public report. Report suspected vulnerabilities privately to the affected client maintainer before opening a public issue when coordinated disclosure is appropriate.

This project does not accept confidential vulnerability reports for Codex, opencode, Claude Code, Copilot, Roo Code, Cursor, Gemini, or other third-party clients; use each vendor's security channel.
