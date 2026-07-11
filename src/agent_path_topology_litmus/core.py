from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable


FIXTURES = [
    "symlinked-skills-dir",
    "relative-symlink-resolution",
    "submodule-instruction-scope",
    "worktree-submodule-state",
    "ignore-rules-over-submodules",
    "symlink-write-safety",
]


@dataclass
class Result:
    name: str
    status: str
    evidence: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def run_command(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    merged_env["PWD"] = str(cwd.resolve())
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=merged_env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run_command(["git", "init", "-q"], path)
    run_command(["git", "config", "user.email", "litmus@example.invalid"], path)
    run_command(["git", "config", "user.name", "Path Topology Litmus"], path)


def commit_all(path: Path, message: str) -> None:
    run_command(["git", "add", "-A"], path)
    run_command(["git", "commit", "-q", "-m", message], path)


def reset_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def create_and_validate(output: Path) -> list[Result]:
    reset_output(output)
    validators: list[Callable[[Path], Result]] = [
        symlinked_skills_dir,
        relative_symlink_resolution,
        submodule_instruction_scope,
        worktree_submodule_state,
        ignore_rules_over_submodules,
        symlink_write_safety,
    ]
    return [validator(output) for validator in validators]


def symlinked_skills_dir(output: Path) -> Result:
    repo = output / "symlinked-skills-dir"
    shared = output / "shared-skills"
    write(shared / "skills" / "topology-sentinel" / "SKILL.md", "---\nname: topology-sentinel\ndescription: Use when validating symlink skill discovery.\n---\n\n# Topology Sentinel\n")
    write(repo / "README.md", "fixture\n")
    (repo / ".agents").mkdir(parents=True)
    os.symlink(shared / "skills", repo / ".agents" / "skills")
    expected = repo / ".agents" / "skills" / "topology-sentinel" / "SKILL.md"
    return Result(
        "symlinked-skills-dir",
        "PASS" if expected.exists() else "FAIL",
        {
            "literal_path": str(expected),
            "literal_path_exists": expected.exists(),
            "resolved_target": str(expected.resolve()) if expected.exists() else None,
            "expected_behavior": "agent skill discovery descends through directory symlink",
        },
    )


def relative_symlink_resolution(output: Path) -> Result:
    repo = output / "relative-symlink-resolution"
    write(repo / ".agents" / "skills" / "rel-sentinel" / "SKILL.md", "# Relative Sentinel\n")
    (repo / ".codex").mkdir(parents=True)
    os.symlink("../.agents/skills", repo / ".codex" / "skills")
    link = repo / ".codex" / "skills"
    posix_target = (link.parent / os.readlink(link)).resolve()
    cwd_wrong_target = (repo / "nested" / "session-cwd" / os.readlink(link)).resolve()
    expected = link / "rel-sentinel" / "SKILL.md"
    return Result(
        "relative-symlink-resolution",
        "PASS" if expected.exists() and posix_target.exists() and not cwd_wrong_target.exists() else "FAIL",
        {
            "readlink": os.readlink(link),
            "posix_target": str(posix_target),
            "cwd_relative_target_example": str(cwd_wrong_target),
            "skill_visible": expected.exists(),
            "expected_behavior": "relative symlink target resolves from symlink directory, not process cwd",
        },
    )


def submodule_instruction_scope(output: Path) -> Result:
    super_repo = output / "submodule-instruction-scope" / "superproject"
    sub_repo = output / "submodule-instruction-scope" / "submodule-src"
    init_repo(sub_repo)
    write(sub_repo / "AGENTS.md", "SUBMODULE_RULE=1\n")
    write(sub_repo / "src.py", "print('sub')\n")
    commit_all(sub_repo, "init submodule")

    init_repo(super_repo)
    write(super_repo / "AGENTS.md", "SUPERPROJECT_RULE=1\n")
    commit_all(super_repo, "init superproject")
    add = run_command(
        ["git", "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(sub_repo), "vendor/sub"],
        super_repo,
    )
    if add.returncode != 0:
        return Result("submodule-instruction-scope", "FAIL", {"git_submodule_add_stderr": add.stderr.strip()})
    commit_all(super_repo, "add submodule")

    sub_path = super_repo / "vendor" / "sub"
    show_toplevel = run_command(["git", "rev-parse", "--show-toplevel"], sub_path)
    show_super = run_command(["git", "rev-parse", "--show-superproject-working-tree"], sub_path)
    superproject_match = Path(show_super.stdout.strip()).resolve() == super_repo.resolve()
    return Result(
        "submodule-instruction-scope",
        "PASS" if superproject_match else "FAIL",
        {
            "submodule_path": str(sub_path),
            "submodule_toplevel": show_toplevel.stdout.strip(),
            "superproject_working_tree": show_super.stdout.strip(),
            "submodule_agents_exists": (sub_path / "AGENTS.md").exists(),
            "superproject_agents_exists": (super_repo / "AGENTS.md").exists(),
            "expected_behavior": "diagnose when submodule-root walks hide superproject instructions",
        },
    )


def worktree_submodule_state(output: Path) -> Result:
    repo = output / "worktree-submodule-state" / "main"
    module = output / "worktree-submodule-state" / "submodule-src"
    worktree = output / "worktree-submodule-state" / "worktree-copy"
    init_repo(module)
    write(module / "mod.txt", "mod\n")
    commit_all(module, "init module")
    init_repo(repo)
    write(repo / "README.md", "main\n")
    commit_all(repo, "init main")
    add = run_command(
        ["git", "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(module), "deps/mod"],
        repo,
    )
    if add.returncode != 0:
        return Result("worktree-submodule-state", "FAIL", {"git_submodule_add_stderr": add.stderr.strip()})
    commit_all(repo, "add module")
    created = run_command(["git", "worktree", "add", "-q", str(worktree), "-b", "validation-worktree"], repo)
    content = worktree / "deps" / "mod" / "mod.txt"
    return Result(
        "worktree-submodule-state",
        "PASS" if created.returncode == 0 and not content.exists() else "FAIL",
        {
            "worktree_created": created.returncode == 0,
            "submodule_content_present": content.exists(),
            "expected_behavior": "diagnose uninitialized submodule content in fresh worktrees",
        },
    )


def ignore_rules_over_submodules(output: Path) -> Result:
    repo = output / "ignore-rules-over-submodules" / "main"
    vendor = output / "ignore-rules-over-submodules" / "vendor-src"
    init_repo(vendor)
    write(vendor / "secret.txt", "DO_NOT_READ\n")
    commit_all(vendor, "init vendor")
    init_repo(repo)
    write(repo / ".rooignore", "vendor/lib/\n")
    commit_all(repo, "init ignore root")
    add = run_command(
        ["git", "-c", "protocol.file.allow=always", "submodule", "add", "-q", str(vendor), "vendor/lib"],
        repo,
    )
    if add.returncode != 0:
        return Result("ignore-rules-over-submodules", "FAIL", {"git_submodule_add_stderr": add.stderr.strip()})
    commit_all(repo, "add vendor")
    pattern_present = (repo / ".rooignore").read_text(encoding="utf-8").strip() == "vendor/lib/"
    return Result(
        "ignore-rules-over-submodules",
        "PASS" if pattern_present else "FAIL",
        {
            "rooignore_pattern_present": pattern_present,
            "ignored_path": "vendor/lib/secret.txt",
            "expected_behavior": "agent file listing, reads, and indexing honor ignore rules for submodule paths",
        },
    )


def symlink_write_safety(output: Path) -> Result:
    repo = output / "symlink-write-safety" / "repo"
    outside = output / "symlink-write-safety" / "outside-config"
    write(outside / "settings.json", '{"safe": true}\n')
    write(repo / "docs" / "demo.md", "visible docs\n")
    os.symlink(outside / "settings.json", repo / "docs" / "clip.md")
    link = repo / "docs" / "clip.md"
    target = link.resolve()
    return Result(
        "symlink-write-safety",
        "PASS" if link.is_symlink() and not str(target).startswith(str(repo.resolve())) else "FAIL",
        {
            "literal_path": str(link),
            "resolved_target": str(target),
            "target_inside_repo": str(target).startswith(str(repo.resolve())),
            "expected_behavior": "agent write prompts canonicalize symlink targets before approval",
        },
    )


def codex_prompt_input(output: Path) -> Result:
    if shutil.which("codex") is None:
        return Result("codex-prompt-input", "SKIP", {"reason": "codex not found on PATH"})
    sub_path = output / "submodule-instruction-scope" / "superproject" / "vendor" / "sub"
    if not sub_path.exists():
        create_and_validate(output)
    codex_home = output / ".litmus-codex-home"
    codex_home.mkdir(parents=True, exist_ok=True)
    proc = run_command(
        ["codex", "debug", "prompt-input", "Report visible rules."],
        sub_path,
        env={"CODEX_HOME": str(codex_home)},
    )
    text = proc.stdout
    json_valid = True
    try:
        json.loads(text)
    except json.JSONDecodeError:
        json_valid = False
    submodule_visible = "SUBMODULE_RULE=1" in text
    superproject_visible = "SUPERPROJECT_RULE=1" in text
    return Result(
        "codex-prompt-input",
        "PASS" if proc.returncode == 0 and json_valid and submodule_visible and superproject_visible else "FAIL",
        {
            "command": "codex debug prompt-input",
            "isolated_codex_home": str(codex_home),
            "returncode": proc.returncode,
            "json_valid": json_valid,
            "submodule_rule_visible": submodule_visible,
            "superproject_rule_visible": superproject_visible,
            "stderr": proc.stderr.strip()[:1000],
            "expected_behavior": "when run inside a submodule, report whether superproject instructions remain visible",
        },
    )


def parse_skill_names(stdout: str) -> tuple[bool, list[str]]:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return False, []
    if not isinstance(payload, list):
        return False, []
    names = [item.get("name") for item in payload if isinstance(item, dict) and isinstance(item.get("name"), str)]
    return True, sorted(names)


def write_skill(path: Path, name: str) -> None:
    write(
        path / name / "SKILL.md",
        (
            "---\n"
            f"name: {name}\n"
            f"description: Use when validating opencode project skill discovery for {name}.\n"
            "---\n\n"
            f"# {name}\n"
        ),
    )


def run_opencode_skill_variant(repo: Path, variant: str, token: str, skill_path: Path) -> dict[str, object]:
    isolated_home = repo / ".litmus-home"
    (isolated_home / ".config" / "opencode").mkdir(parents=True, exist_ok=True)
    env = {
        "HOME": str(isolated_home),
        "XDG_CONFIG_HOME": str(isolated_home / ".config"),
        "OPENCODE_DISABLE_EXTERNAL_SKILLS": "true",
        "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS": "true",
    }
    proc = run_command(["opencode", "debug", "skill", "--pure"], repo, env=env)
    json_valid, names = parse_skill_names(proc.stdout)
    visible_by_text = token in proc.stdout
    return {
        "variant": variant,
        "cwd": str(repo),
        "skill_path": str(skill_path),
        "skill_path_exists": skill_path.exists(),
        "skill_path_is_symlink": skill_path.is_symlink(),
        "skill_path_resolved": str(skill_path.resolve()) if skill_path.exists() else None,
        "command": "opencode debug skill --pure",
        "env": env,
        "returncode": proc.returncode,
        "stdout_json_valid": json_valid,
        "stdout_parse_note": None if json_valid else "debug output was not a complete JSON list; visibility is checked by substring",
        "visible": token in names or visible_by_text,
        "visible_by_text": visible_by_text,
        "matching_names": [name for name in names if "topology-" in name],
        "skill_count": len(names) if json_valid else None,
        "stdout_bytes": len(proc.stdout),
        "stdout_contains_builtin_skill": "customize-opencode" in proc.stdout,
        "stderr": proc.stderr.strip()[:1000],
    }


def opencode_debug_skill(output: Path) -> Result:
    if shutil.which("opencode") is None:
        return Result("opencode-debug-skill", "SKIP", {"reason": "opencode not found on PATH"})

    root = output / "opencode-debug-skill"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)

    version_proc = run_command(["opencode", "--version"], root)
    variants: list[dict[str, object]] = []

    default_real = root / "default-real-opencode-skills"
    init_repo(default_real)
    default_real_path = default_real / ".opencode" / "skills"
    write_skill(default_real_path, "topology-default-real")
    commit_all(default_real, "init default real project skill fixture")
    variants.append(run_opencode_skill_variant(default_real, "default-real-opencode-skills", "topology-default-real", default_real_path))

    configured_real = root / "configured-real-claude-skills"
    init_repo(configured_real)
    configured_real_path = configured_real / ".claude" / "skills"
    write_skill(configured_real_path, "topology-config-real")
    write(
        configured_real / "opencode.json",
        '{\n  "$schema": "https://opencode.ai/config.json",\n  "skills": { "paths": [".claude/skills"] }\n}\n',
    )
    commit_all(configured_real, "init configured real project skill fixture")
    variants.append(run_opencode_skill_variant(configured_real, "configured-real-claude-skills", "topology-config-real", configured_real_path))

    configured_symlink = root / "configured-symlink-claude-skills"
    init_repo(configured_symlink)
    write_skill(configured_symlink / "shared" / "skills", "topology-config-symlink")
    (configured_symlink / ".claude").mkdir(parents=True, exist_ok=True)
    os.symlink("../shared/skills", configured_symlink / ".claude" / "skills")
    configured_symlink_path = configured_symlink / ".claude" / "skills"
    write(
        configured_symlink / "opencode.json",
        '{\n  "$schema": "https://opencode.ai/config.json",\n  "skills": { "paths": [".claude/skills"] }\n}\n',
    )
    commit_all(configured_symlink, "init configured symlink project skill fixture")
    variants.append(
        run_opencode_skill_variant(
            configured_symlink,
            "configured-symlink-claude-skills",
            "topology-config-symlink",
            configured_symlink_path,
        )
    )

    all_visible = all(bool(variant["visible"]) for variant in variants)
    default_visible = bool(variants[0]["visible"])
    symlink_visible = bool(variants[-1]["visible"])
    if all_visible:
        failure_class = None
    elif not default_visible:
        failure_class = "project_skill_discovery_not_visible_in_debug_skill"
    elif not symlink_visible:
        failure_class = "symlinked_project_skill_not_visible_in_debug_skill"
    else:
        failure_class = "configured_project_skill_path_not_visible_in_debug_skill"

    return Result(
        "opencode-debug-skill",
        "PASS" if all_visible else "FAIL",
        {
            "opencode_version": version_proc.stdout.strip(),
            "failure_class": failure_class,
            "variants": variants,
            "expected_behavior": "opencode debug skill surfaces project skills from default, configured, and symlinked skill paths",
        },
    )


def results_payload(results: list[Result], output: Path) -> dict[str, object]:
    return {
        "output": str(output),
        "summary": {
            "pass": sum(result.status == "PASS" for result in results),
            "fail": sum(result.status == "FAIL" for result in results),
            "skip": sum(result.status == "SKIP" for result in results),
        },
        "results": [result.to_dict() for result in results],
    }


def render_json(results: list[Result], output: Path) -> str:
    return json.dumps(results_payload(results, output), indent=2, sort_keys=True)


def render_evidence_value(value: object) -> list[str]:
    if isinstance(value, (dict, list)):
        return ["", "```json", json.dumps(value, indent=2, sort_keys=True), "```"]
    return [f"`{value}`"]


def render_markdown(results: list[Result], output: Path) -> str:
    payload = results_payload(results, output)
    lines = [
        "# Agent Path Topology Litmus Report",
        "",
        f"Output: `{payload['output']}`",
        "",
        f"Summary: {payload['summary']['pass']} PASS, {payload['summary']['fail']} FAIL, {payload['summary']['skip']} SKIP",
        "",
    ]
    for result in results:
        lines.extend([f"## {result.name}", "", f"Status: `{result.status}`", ""])
        for key, value in result.evidence.items():
            rendered = render_evidence_value(value)
            if len(rendered) == 1:
                lines.append(f"- `{key}`: {rendered[0]}")
            else:
                lines.append(f"- `{key}`:")
                lines.extend(rendered)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
