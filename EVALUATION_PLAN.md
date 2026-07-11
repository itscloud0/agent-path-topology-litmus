# EVALUATION_PLAN: agent-path-topology-litmus

## Baseline

Compare agent diagnostics against manual Git and filesystem checks:

- `readlink`
- `realpath`
- `find -L`
- Python `Path.resolve()`
- `git rev-parse --show-toplevel`
- `git rev-parse --show-superproject-working-tree`
- `git submodule status`
- `git worktree list`

## Required Validation Before Publication

- At least three unrelated real-world cases modeled:
  - symlinked skill/config discovery
  - submodule/superproject instruction scope
  - symlink-write target safety
- At least two ecosystems validated:
  - Codex CLI diagnostic adapter
  - opencode diagnostic adapter
  - optional later: Claude Code, Copilot, Roo Code, or Gemini if stable non-UI diagnostics exist
- Reproducible benchmark or validation report:
  - fixture creation result
  - baseline expected topology
  - adapter observed topology
  - pass/fail or observed-status result
  - client version and command
- Documented failures and limitations.
- No live model calls required for CI.
- No fixture reads secrets or mutates outside its output directory.

## Success Criteria

- Fixture generation passes on macOS and Linux.
- Baseline validation passes 6/6 topology cases.
- Codex diagnostic adapter produces a stable report for submodule instruction scope.
- opencode diagnostic adapter produces a stable report for symlinked skill discovery.
- Markdown reports are compact enough to paste into upstream issues.
- False positives are documented for cases where client behavior is intentionally scoped differently.

## Kill Criteria

- The useful work is only an `agent-instruction-litmus` fixture extension.
- Stable adapter paths are unavailable without brittle UI automation or live paid model calls.
- Existing sync tools add equivalent behavior verification and reports.
- Native client diagnostics cover the same cross-topology evidence in a reusable way.
- Security-sensitive fixtures cannot be modeled without dangerous writes or secret exposure.

