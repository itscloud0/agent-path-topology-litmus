# Benchmark Results

Run date: 2026-07-11.

Environment:

- macOS arm64
- Python 3.12
- Git local file fixtures
- Codex CLI 0.133.0
- opencode 1.16.2
- no live model calls

## Baseline Matrix

Command:

```bash
PYTHONPATH=src python3 -m agent_path_topology_litmus validate --output /tmp/agent-path-topology-litmus-baseline --format json
```

Result: 6/6 `PASS`.

| Fixture | Result |
| --- | --- |
| symlinked-skills-dir | PASS |
| relative-symlink-resolution | PASS |
| submodule-instruction-scope | PASS |
| worktree-submodule-state | PASS |
| ignore-rules-over-submodules | PASS |
| symlink-write-safety | PASS |

## Client Diagnostic Matrix

| Client diagnostic | Case | Observed result |
| --- | --- | --- |
| opencode 1.16.2 `debug skill --pure` | default real `.opencode/skills` | PASS; expected skill visible |
| opencode 1.16.2 `debug skill --pure` | configured real `.claude/skills` | PASS; expected skill visible |
| opencode 1.16.2 `debug skill --pure` | configured symlinked `.claude/skills` | PASS; expected skill visible |
| Codex CLI 0.133.0 `debug prompt-input` | submodule rule visibility | PASS; submodule rule visible |
| Codex CLI 0.133.0 `debug prompt-input` | superproject rule visibility from submodule | FAIL; superproject rule hidden |
| opencode 1.16.2 `debug file list deps --pure` | fresh worktree/submodule state | PASS; empty submodule directory visible, uninitialized content absent |

## Meaningful Baseline

The fixture runner replaces six separate manual setups using `readlink`, `realpath`, `git rev-parse`, `git submodule`, and `git worktree` with one reproducible command. Native client diagnostics are then run against those known-good fixture states. A client `FAIL` therefore identifies observed behavior relative to a passing filesystem/Git baseline; it does not imply the fixture itself failed.

## Known Limits

- Results are version- and platform-specific.
- CI verifies fixture generation and report rendering without requiring client binaries.
- Only Codex CLI and opencode have non-live adapters in this release candidate.
- The worktree/submodule adapter checks opencode's file-list observation against Git state; it does not execute a model or prove tool behavior inside the submodule.
- The suite does not execute writes through the outside-repository symlink; it reports the canonical target for safe review.
