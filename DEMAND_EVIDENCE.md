# DEMAND_EVIDENCE: agent-path-topology-litmus

## Public Pain Signals

- Codex issue #8943 reports symlinked skill directories not loading because Codex did not follow symlinks. Source: https://github.com/openai/codex/issues/8943
- Codex issue #9898 reports relative symlinks being resolved from the current working directory instead of from the symlink's own directory. Source: https://github.com/openai/codex/issues/9898
- Codex issue #30789 reports `AGENTS.md` discovery stopping at a git submodule root, hiding the superproject's `AGENTS.md`. Source: https://github.com/openai/codex/issues/30789
- Claude Code issue #27156 reports `claude -w` inside a git submodule creating a worktree for the parent repository instead of the submodule. Source: https://github.com/anthropics/claude-code/issues/27156
- Claude Code issue #17293 reports marketplace installation not initializing git submodules, leaving empty plugin directories. Source: https://github.com/anthropics/claude-code/issues/17293
- Claude Code issue #45601 reports the VS Code extension `@` file picker missing initialized git submodule directories. Source: https://github.com/anthropics/claude-code/issues/45601
- Claude Code issue #66559 reports documented `CLAUDE.md` symlink support conflicting with write/update tools that refuse to edit a symlinked `CLAUDE.md`. Source: https://github.com/anthropics/claude-code/issues/66559
- Claude Code issue #54904 reports background full checkout failing when worktree mode is enabled for a repository with submodules. Source: https://github.com/anthropics/claude-code/issues/54904
- Roo Code issue #11797 reports `.rooignore` not being enforced for indexing, file reads, or environment listing in workspaces containing git submodules or nested third-party directories. Source: https://github.com/RooCodeInc/Roo-Code/issues/11797
- GitHub Community discussion #155450 reports Copilot instructions at a monorepo root being unavailable when only selected packages are opened as a multi-root workspace. Source: https://github.com/orgs/community/discussions/155450
- opencode issue #18848 reports project-level skills not discovered when `.claude/skills` is a symlink inside a git worktree sandbox, even though filesystem globbing finds them. Source: https://github.com/anomalyco/opencode/issues/18848
- Adversa's SymJack research reports symlink-based coding-agent approval bypass across multiple coding agents. Source: https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/

## Alternatives Reviewed

- Manual Git and filesystem checks: `readlink`, `realpath`, `find -L`, `git rev-parse --show-toplevel`, `git rev-parse --show-superproject-working-tree`, `git submodule update --init --recursive`.
- AgentSync syncs agent configs and MCP server definitions across tools using symbolic links. Source: https://github.com/dallay/agentsync
- AgentSync documentation positions symbolic links as a way to keep one source of truth across tools. Source: https://dallay.github.io/agentsync/
- Ruler propagates rules and experimental skills to supported AI agents. Source: https://github.com/intellectronica/ruler
- Public workflow posts recommend symlinked shared `AGENTS.md`, `CLAUDE.md`, skills, and Copilot instruction files. Example source: https://www.ssw.com.au/rules/symlink-agents-to-claude
- Codex exposes `codex debug prompt-input`, which can inspect model-visible prompt inputs without a live model call.
- opencode exposes `opencode debug skill`, which can list available skills without a live model call.
- `agent-instruction-litmus` already tests instruction-file adherence, but its released scope does not cover topology discovery, submodule/worktree state, ignore enforcement over submodules, or symlink-write target safety.

## Targeted Validation On 2026-07-07

Local harmless fixture feasibility: `PASS`.

- `symlinked-skills-dir`: created a symlinked skill directory and verified the expected `SKILL.md` resolves through the symlink.
- `relative-symlink-resolution`: created a relative symlink and verified POSIX resolution from the symlink directory differs from cwd-relative resolution.
- `submodule-instruction-scope`: created a superproject plus submodule and verified both submodule and superproject `AGENTS.md` files exist while Git reports the submodule top-level separately.
- `worktree-submodule-state`: created a git worktree where submodule content is empty until initialized, reproducing a meaningful diagnostic state.
- `ignore-rules-over-submodules`: created a `.rooignore`-style pattern over a submodule path.
- `symlink-write-safety`: created a repo-visible symlink resolving outside the repo.

Native diagnostic validation: `PASS` for adapter feasibility, with observed client failures recorded.

- Codex CLI 0.133.0 `debug prompt-input` ran from the generated submodule fixture without a model call. It included `SUBMODULE_RULE=1` and did not include `SUPERPROJECT_RULE=1`, matching the hidden-superproject-instruction failure shape.
- Codex CLI 0.133.0 `debug prompt-input` with a temporary `CODEX_HOME` saw a valid symlinked skill under `CODEX_HOME/skills`.
- opencode 1.16.2 `debug skill --pure` can be run locally without a model call. The packaged adapter currently reports `FAIL` for a symlinked `.claude/skills` project path under the generated fixture: `topology_sentinel_visible=false`. A direct shell probe in a git-root fixture saw the same skill, so the next validation should isolate opencode project-root/subprocess behavior before publication.

## Gate Status

- Repeated public pain: `PASS`.
- Independent sources: `PASS`.
- Current workaround and existing-tool review: `PASS`.
- Clear standalone gap: `PASS`, limited to topology behavior fixtures and diagnostic reports.
- Reason upstream contribution is insufficient: `PASS`, because the failures span multiple clients and a shared fixture corpus can produce comparable evidence while individual fixes still belong upstream.
- Credible distribution path: `PASS`, through affected issue threads, coding-agent reliability users, agent-config/dotfiles users, and security researchers. No adoption is claimed.
- Measurable success criteria: `PASS`.
- Kill criteria: `PASS`. Kill if the scope collapses into only instruction-file adherence fixtures, requires brittle UI automation, duplicates sync tools, or cannot validate at least two ecosystems without live paid model calls.
