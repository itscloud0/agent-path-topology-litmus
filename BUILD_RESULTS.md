# BUILD_RESULTS

## 2026-07-07 Initial Local Build

Built:

- Python CLI package under `src/agent_path_topology_litmus`.
- `fixtures` command.
- `validate --output ... --format json|markdown` command.
- `run-adapter codex-prompt-input` diagnostic command.
- `run-adapter opencode-debug-skill` diagnostic command.
- Unit tests for fixture generation and report rendering.

Verification is recorded in the FLAGSHIP run log for this automation run.

Initial verification:

- Unit tests: `PYTHONPATH=src python3 -m unittest discover -s tests` passed, 4 tests.
- Compile check: `PYTHONPATH=src python3 -m compileall -q src tests` passed.
- Fixture list smoke: `PYTHONPATH=src python3 -m agent_path_topology_litmus fixtures` passed.
- Baseline fixture validation: `PYTHONPATH=src python3 -m agent_path_topology_litmus validate --output /tmp/agent-path-topology-litmus-validation --format json` passed with 6 `PASS`.
- Codex diagnostic adapter: ran and returned `FAIL` because `SUPERPROJECT_RULE=1` was not visible from inside the submodule.
- opencode diagnostic adapter: ran and returned `FAIL` because `topology-sentinel` was not visible from the Python-spawned generated fixture.

## 2026-07-09 Adapter Matrix And CI Prep

Built:

- Expanded the opencode diagnostic from one symlinked `.claude/skills` fixture to a compact project-skill visibility matrix:
  - default real `.opencode/skills`
  - configured real `.claude/skills`
  - configured symlinked `.claude/skills`
- Added compact opencode evidence fields so reports keep command status, JSON validity, skill count, matching skill names, and symlink resolution without storing full skill bodies.
- Added GitHub Actions CI for Ubuntu and macOS across Python 3.10, 3.11, and 3.12.

Verification is recorded in `VALIDATION_RESULTS.md`.

## 2026-07-11 Reproducibility Hardening

Built:

- Isolated opencode diagnostics from user `HOME` and `XDG_CONFIG_HOME` state.
- Corrected opencode boolean environment flags from `1` to `true`.
- Isolated Codex diagnostics with a disposable `CODEX_HOME`.
- Added regression tests for both adapter isolation boundaries.

Verification:

- Unit tests passed with 6 tests.
- Python compile check passed.
- Baseline validation passed 6/6.
- opencode project-skill matrix passed 3/3.
- Codex diagnostic returned valid JSON and reproduced the hidden-superproject-rule behavior.
