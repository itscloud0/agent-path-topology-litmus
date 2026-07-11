# agent-path-topology-litmus v0.1.0

Initial release candidate for reproducible coding-agent path-topology testing.

## Included

- Six harmless fixtures covering symlinked skills, relative symlinks, git submodule instruction scope, git worktree/submodule state, ignore rules over submodules, and symlink-write targets.
- JSON and Markdown baseline reports.
- Non-live Codex CLI and opencode diagnostic adapters isolated from user-global configuration.
- Reproducible validation results with documented client failures and limitations.
- Ubuntu and macOS CI for Python 3.10-3.12.

## Known Limits

- Client results are version- and platform-specific.
- Claude Code, Copilot, Roo Code, Cursor, and Gemini do not have adapters yet.
- The tool reports topology behavior; it is not a rule syncer, security scanner, or proof of future client safety.
