# agent-path-topology-litmus v0.2.1

Fixes the runtime package version and documents checkout-free installation from the tagged GitHub release.

## Included

- Runtime `__version__` now matches the packaged `0.2.1` release.
- Tagged `pip`, isolated `uv tool`, and one-off `uvx` installation paths.

# agent-path-topology-litmus v0.2.0

Adds a reproducible fresh-worktree/submodule client diagnostic.

## Included

- Six harmless fixtures covering symlinked skills, relative symlinks, git submodule instruction scope, git worktree/submodule state, ignore rules over submodules, and symlink-write targets.
- JSON and Markdown baseline reports.
- Non-live Codex CLI and opencode diagnostic adapters isolated from user-global configuration.
- Non-live `opencode debug file list` validation that compares client file visibility with `git worktree list` and `git submodule status`.
- Reproducible validation results with documented client failures and limitations.
- Ubuntu and macOS CI for Python 3.10-3.12.

## Known Limits

- Client results are version- and platform-specific.
- Claude Code, Copilot, Roo Code, Cursor, and Gemini do not have adapters yet.
- The tool reports topology behavior; it is not a rule syncer, security scanner, or proof of future client safety.
