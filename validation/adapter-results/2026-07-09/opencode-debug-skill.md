# Agent Path Topology Litmus Report

Output: `/tmp/agent-path-topology-litmus-opencode-20260709-md2`

Summary: 0 PASS, 1 FAIL, 0 SKIP

## opencode-debug-skill

Status: `FAIL`

- `opencode_version`: `1.16.2`
- `failure_class`: `project_skill_discovery_not_visible_in_debug_skill`
- `variants`:

```json
[
  {
    "command": "opencode debug skill --pure",
    "cwd": "/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/default-real-opencode-skills",
    "env": {
      "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS": "1",
      "OPENCODE_DISABLE_EXTERNAL_SKILLS": "1"
    },
    "matching_names": [],
    "returncode": 0,
    "skill_count": null,
    "skill_path": "/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/default-real-opencode-skills/.opencode/skills",
    "skill_path_exists": true,
    "skill_path_is_symlink": false,
    "skill_path_resolved": "/private/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/default-real-opencode-skills/.opencode/skills",
    "stderr": "",
    "stdout_bytes": 65220,
    "stdout_contains_builtin_skill": true,
    "stdout_json_valid": false,
    "stdout_parse_note": "debug output was not a complete JSON list; visibility is checked by substring",
    "variant": "default-real-opencode-skills",
    "visible": false,
    "visible_by_text": false
  },
  {
    "command": "opencode debug skill --pure",
    "cwd": "/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/configured-real-claude-skills",
    "env": {
      "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS": "1",
      "OPENCODE_DISABLE_EXTERNAL_SKILLS": "1"
    },
    "matching_names": [],
    "returncode": 0,
    "skill_count": null,
    "skill_path": "/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/configured-real-claude-skills/.claude/skills",
    "skill_path_exists": true,
    "skill_path_is_symlink": false,
    "skill_path_resolved": "/private/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/configured-real-claude-skills/.claude/skills",
    "stderr": "",
    "stdout_bytes": 65317,
    "stdout_contains_builtin_skill": true,
    "stdout_json_valid": false,
    "stdout_parse_note": "debug output was not a complete JSON list; visibility is checked by substring",
    "variant": "configured-real-claude-skills",
    "visible": false,
    "visible_by_text": false
  },
  {
    "command": "opencode debug skill --pure",
    "cwd": "/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/configured-symlink-claude-skills",
    "env": {
      "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS": "1",
      "OPENCODE_DISABLE_EXTERNAL_SKILLS": "1"
    },
    "matching_names": [],
    "returncode": 0,
    "skill_count": null,
    "skill_path": "/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/configured-symlink-claude-skills/.claude/skills",
    "skill_path_exists": true,
    "skill_path_is_symlink": true,
    "skill_path_resolved": "/private/tmp/agent-path-topology-litmus-opencode-20260709-md2/opencode-debug-skill/configured-symlink-claude-skills/shared/skills",
    "stderr": "",
    "stdout_bytes": 65365,
    "stdout_contains_builtin_skill": true,
    "stdout_json_valid": false,
    "stdout_parse_note": "debug output was not a complete JSON list; visibility is checked by substring",
    "variant": "configured-symlink-claude-skills",
    "visible": false,
    "visible_by_text": false
  }
]
```
- `expected_behavior`: `opencode debug skill surfaces project skills from default, configured, and symlinked skill paths`
