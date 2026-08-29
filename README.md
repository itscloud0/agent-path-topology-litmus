# agent-path-topology-litmus

`agent-path-topology-litmus` is a local fixture runner for coding-agent client authors, extension authors, security engineers, and power users debugging how agents handle symlinks, relative symlinks, git submodules, git worktrees, ignore rules, and symlink-write safety. It answers, in a few minutes, whether an agent sees the same repository topology that Git and the filesystem expose before you trust it on a real codebase.

The first build is intentionally small. It creates harmless disposable fixture repositories, validates the expected topology with local Git/filesystem checks, and can run local diagnostics for Codex CLI and opencode when those CLIs are installed. It does not execute agent-written code or read secrets.

## Install

Python 3.10 or newer is required. To install the public `v0.2.1` release without cloning the repository:

```bash
python3 -m pip install "git+https://github.com/itscloud0/agent-path-topology-litmus.git@v0.2.1"
```

For an isolated command-line install with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install "git+https://github.com/itscloud0/agent-path-topology-litmus.git@v0.2.1"
```

For a one-off fixture listing without a persistent install:

```bash
uvx --from "git+https://github.com/itscloud0/agent-path-topology-litmus.git@v0.2.1" \
  agent-path-topology-litmus fixtures
```

For local development from a checkout:

```bash
python3 -m pip install -e .
```

## Quickstart

List fixtures:

```bash
python -m agent_path_topology_litmus fixtures
```

Create and validate all fixtures:

```bash
python -m agent_path_topology_litmus validate --output /tmp/agent-path-topology-litmus --format markdown
```

Run a local Codex diagnostic against the submodule instruction fixture:

```bash
python -m agent_path_topology_litmus run-adapter codex-prompt-input --output /tmp/agent-path-topology-litmus
```

Run a local opencode diagnostic for project skill visibility:

```bash
python -m agent_path_topology_litmus run-adapter opencode-debug-skill --output /tmp/agent-path-topology-litmus
```

Run a local opencode diagnostic for fresh worktree/submodule visibility:

```bash
python -m agent_path_topology_litmus run-adapter opencode-worktree-submodule --output /tmp/agent-path-topology-litmus
```

## Validation Snapshot

- Baseline topology fixtures: 6/6 passed on macOS with Python 3.14.6, local Git, and filesystem checks.
- opencode 1.16.2: default, configured real, and configured symlinked project skills were all visible through `opencode debug skill --pure`.
- opencode 1.16.2: the fresh worktree/submodule adapter saw the empty `deps/mod` directory and no `deps/mod/mod.txt` content through `opencode debug file list deps --pure`.
- Codex CLI 0.150.1: `codex debug prompt-input` ran successfully inside a submodule, saw the submodule rule, and did not see the superproject rule. This is reported as an observed client failure, not a fixture failure.

See `BENCHMARK_RESULTS.md` for commands and `VALIDATION_RESULTS.md` for limitations.

## Fixtures

- `symlinked-skills-dir`: verifies that a symlinked skill/config directory resolves to the intended target.
- `relative-symlink-resolution`: catches clients that resolve relative symlinks from process cwd instead of the symlink directory.
- `submodule-instruction-scope`: shows whether a submodule hides superproject instruction files.
- `worktree-submodule-state`: exposes the empty-submodule state common in fresh git worktrees.
- `ignore-rules-over-submodules`: models agent-specific ignore rules over submodule paths.
- `symlink-write-safety`: checks whether a visible repo path resolves outside the repo before writes are approved.

## Limits

- Baseline validation proves only that the fixtures are well formed.
- Adapter results are client-version-specific and may differ across Codex, opencode, Claude Code, Copilot, Roo, Cursor, Gemini, and future releases.
- Codex and opencode diagnostics are local, non-model paths. The opencode adapters report project-skill visibility and fresh worktree/submodule file-list behavior; they do not prove model or tool behavior inside a submodule.
- Live model adapters are intentionally not included yet.
- The tool is not a rule syncer, config generator, prompt package, or static linter.
- No fixture reads `.env`, private keys, shell history, or unrelated project files.

## Compared With Sync Tools And Manual Checks

AgentSync, Ruler, and copy-based rule workflows distribute agent configuration. They do not verify how an installed coding agent resolves symlinks, submodule roots, worktree state, ignore rules, or write targets. Manual `readlink`, `realpath`, and `git rev-parse` checks establish the filesystem baseline; this tool packages those checks into repeatable fixtures and adds client-specific diagnostic evidence.

Individual client defects still belong upstream. This project produces compact reproduction evidence; it does not replace Codex, opencode, Claude Code, Copilot, Roo Code, Cursor, or Gemini issue trackers.
