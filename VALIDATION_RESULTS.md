# VALIDATION_RESULTS

## 2026-07-07 Targeted Validation

Lifecycle mode: `SPEC` -> `BUILD`.

Local fixture feasibility: `PASS`.

- Disposable validator created six harmless topology cases under `.automation/tmp/flagship-path-topology-validation/`.
- Baseline run passed 6/6 cases:
  - `symlinked-skills-dir`
  - `relative-symlink-resolution`
  - `submodule-instruction-scope`
  - `worktree-submodule-state`
  - `ignore-rules-over-submodules`
  - `symlink-write-safety`

Native diagnostic validation:

- Codex CLI 0.133.0 `debug prompt-input` from the generated submodule included `SUBMODULE_RULE=1` and did not include `SUPERPROJECT_RULE=1`. This validates a stable, no-model diagnostic path and reproduces the hidden-superproject-instruction failure shape.
- Codex CLI 0.133.0 `debug prompt-input` with temporary `CODEX_HOME` included a symlinked skill named `topology-sentinel`.
- opencode 1.16.2 `debug skill --pure` is callable without a model, but the packaged adapter reports `FAIL` in the generated fixture: `topology_sentinel_visible=false`. A direct shell probe in a git-root fixture did see `topology-sentinel`, so this is a validation target before publication rather than a release-ready adapter.

## 2026-07-09 Adapter Stability Validation

Lifecycle mode: `VALIDATE` -> `POLISH`.

Baseline fixture validation: `PASS`.

- `PYTHONPATH=src python3 -m agent_path_topology_litmus validate --output /tmp/agent-path-topology-litmus-baseline --format json` passed with 6/6 baseline fixtures.
- `PYTHONPATH=src python3 -m unittest discover -s tests` passed with 4 tests.
- `PYTHONPATH=src python3 -m compileall -q src tests` passed.

Native diagnostic validation:

- Codex CLI 0.133.0 `debug prompt-input` remains stable and non-live. It returned valid JSON, included `SUBMODULE_RULE=1`, and did not include `SUPERPROJECT_RULE=1`, so the adapter produces a useful upstream-ready `FAIL` report for hidden superproject instructions.
- opencode 1.16.2 `debug skill --pure` remains stable and non-live, but targeted isolation changed the failure classification. Default real `.opencode/skills`, configured real `.claude/skills`, and configured symlinked `.claude/skills` variants all returned exit code 0 while omitting the custom `topology-*` project skill. The debug output includes the built-in skill body and is not a complete JSON list at this size, so the adapter records substring visibility plus stdout metadata. The current observed class is `project_skill_discovery_not_visible_in_debug_skill`, not a symlink-only failure.

Publication impact:

- Adapter stability: `PASS` for command execution and compact result capture.
- opencode behavior scope: `UNKNOWN` for publication value because the diagnostic currently proves broader project-skill invisibility in `debug skill`, not isolated symlink traversal.
- CI path: `PASS` for adding Linux/macOS Python matrix coverage; remote CI has not run because no repository has been published.
- Private/public publication: `UNKNOWN`; do not publish until the opencode diagnostic is either isolated to topology behavior or explicitly documented as a known broader client limitation.

Decision:

- Value gate: `PASS`.
- Standalone gap: `PASS` for topology behavior fixtures and diagnostic reports.
- Upstream-insufficiency: `PASS` because individual bugs belong upstream, but the cross-client fixture corpus is still useful and not covered by sync tools or native per-client diagnostics.
- Publication gates: `UNKNOWN`; no repository was created or published.

## 2026-07-11 Isolated Adapter Validation

Lifecycle mode: `VALIDATE` -> `BENCHMARK` -> `POLISH`.

Harness correction:

- The earlier opencode `FAIL` was a harness false negative. Boolean environment flags were passed as `1`, user-global skills remained loaded, and the large JSON response hit the configured output limit before the fixture skill appeared.
- The adapter now uses `true` boolean values and an isolated `HOME`/`XDG_CONFIG_HOME`. It neither reads nor changes the user's opencode configuration.
- The Codex adapter now uses an isolated `CODEX_HOME`; this prevents unrelated user configuration errors from changing the diagnostic result.
- The isolation behavior is covered by unit tests.

Objective results:

- Baseline: `PASS`, 6/6 harmless topology fixtures.
- opencode 1.16.2: `PASS`, 3/3 variants. Default `.opencode/skills`, configured real `.claude/skills`, and configured symlinked `.claude/skills` each produced valid JSON containing the expected project skill.
- Codex CLI 0.133.0 diagnostic execution: `PASS`; return code 0 and valid JSON.
- Codex submodule/superproject behavior: observed `FAIL`; `SUBMODULE_RULE=1` was visible and `SUPERPROJECT_RULE=1` was not visible.
- Official opencode 1.16.2 source confirms `debug skill` serializes all discovered skills and the loader scans project/configured skill paths with symlink following:
  - https://github.com/anomalyco/opencode/blob/v1.16.2/packages/opencode/src/cli/cmd/debug/skill.ts
  - https://github.com/anomalyco/opencode/blob/v1.16.2/packages/opencode/src/skill/index.ts

Publication impact:

- Two-ecosystem diagnostic gate: `PASS`.
- Reproducibility: `PASS`; adapters are isolated from user-global configuration and require no live model calls.
- Documented failures: `PASS`; the Codex behavior failure is retained as evidence, while the earlier opencode harness failure is explicitly corrected.
- Publication remains gated on final safety, packaging, discoverability, and remote CI verification.
