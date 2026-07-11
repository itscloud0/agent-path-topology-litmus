# PRODUCT_SPEC: agent-path-topology-litmus

## User Persona

Coding-agent client authors, extension authors, security engineers, and power users who keep shared agent instructions, skills, commands, or dependencies behind symlinks, submodules, and worktrees.

## Job To Be Done

Before trusting a coding agent on a real repository, verify in 5-30 minutes whether it correctly and safely sees the same repository topology that Git and the filesystem expose.

## Painful Problem

Agent configuration is increasingly path-scoped. Real projects use symlinked `AGENTS.md`/`CLAUDE.md`, skill directories, git submodules, git worktrees, monorepo multi-root workspaces, and ignore files. Current failures are hard to classify:

- the agent did not follow a directory symlink
- the agent resolved a relative symlink from the wrong cwd
- a submodule boundary hid superproject instructions
- a worktree had empty submodule content
- ignore rules were not enforced over submodule paths
- a write path looked safe but resolved through a symlink outside the repo

Users currently debug this with `readlink`, `realpath`, `find -L`, `git rev-parse`, screenshots, and client-specific issue threads. That proves filesystem facts, but not agent behavior.

## Proposed Better Workflow

Run a local fixture suite:

```bash
agent-path-topology-litmus validate --output /tmp/topology-fixtures
agent-path-topology-litmus run-adapter codex-prompt-input --output /tmp/topology-fixtures
agent-path-topology-litmus run-adapter opencode-debug-skill --output /tmp/topology-fixtures
```

The tool creates disposable repositories, records Git/filesystem invariants, then runs stable client diagnostics where available. Reports explain:

- which topology case was exercised
- which path should have applied
- the literal path and canonical target
- whether the client loaded, ignored, hid, or misresolved the path
- enough evidence to attach to an upstream issue without exposing real repo data

## Core v0.1 Feature Set

- Local Python CLI only.
- Deterministic fixture generation under a user-provided output directory.
- Baseline fixture validation for six topology cases.
- Local Codex CLI diagnostic adapter using `codex debug prompt-input` for submodule instruction scope.
- Local opencode diagnostic adapter using `opencode debug skill` for symlinked skill discovery.
- JSON and Markdown output.
- No live model calls, exploit payloads, secret reads, network calls, or mutation outside the fixture directory.

## Non-Goals

- No new agent rule syncer.
- No `AGENTS.md` or `CLAUDE.md` content linter.
- No prompt-writing helper.
- No policy gateway.
- No broad agent leaderboard.
- No package scanner, MCP scanner, or secret scanner.
- No claim that a passed fixture proves future safety.
- No publication if the useful scope collapses into only new fixtures for `agent-instruction-litmus`.

## Existing Tools And Why This Is Different

- AgentSync and similar sync tools propagate agent config, often with symlinks. They do not prove how each agent resolves those symlinks, submodules, worktrees, or write targets.
- Ruler-style rule systems copy or distribute rules and skills to supported agents. They reduce config drift, but they do not run behavior fixtures against installed clients.
- Native diagnostics such as Codex `debug prompt-input` and opencode `debug skill` are useful per-client probes. They do not provide a cross-client fixture corpus or comparable upstream-ready report.
- `agent-instruction-litmus` tests whether agents follow instruction files. This project stays narrower and lower-level: path topology discovery and safety before instruction-following semantics.

## Why Upstream Contribution Is Insufficient

Individual defects belong upstream in Codex, Claude Code, opencode, Roo Code, Copilot, Cursor, and other clients. The repeated failure class spans clients and path types, so a shared harmless fixture corpus is still useful: it turns anecdotal issue reports into comparable reproduction artifacts.

The standalone gate remains valid only while the project stays focused on topology behavior. If it becomes a generic instruction-file fixture extension, route that work to OWNED for `agent-instruction-litmus` instead.

## Value Gate

Status: `PASS`.

- Target user: coding-agent client authors, extension authors, security engineers, and power users.
- Job: verify agent filesystem topology behavior before trusting real repo work.
- External pain evidence: Codex, Claude Code, Roo Code, Copilot, opencode, and symlink-RCE reports cited in `DEMAND_EVIDENCE.md`.
- Alternative insufficiency: sync tools propagate config but do not prove behavior; native diagnostics are per-client; existing instruction fixtures do not cover topology safety.
- First 5-30 minute outcome: create fixtures, run baseline validation, and run at least one local diagnostic that reports observed topology behavior.

## Publish Criteria

- At least three unrelated real-world cases modeled.
- At least two agent ecosystems validated through stable diagnostics or guarded adapters.
- Meaningful baseline against manual Git/filesystem checks and available native diagnostics.
- Reproducible validation results committed.
- CI tests fixture generation and report rendering without live models.
- README, package metadata, limitations, examples, and comparison sections make the practical value clear without hype.

