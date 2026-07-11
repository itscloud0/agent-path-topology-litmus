from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from agent_path_topology_litmus.cli import main
from agent_path_topology_litmus.core import (
    codex_prompt_input,
    create_and_validate,
    render_json,
    render_markdown,
    run_opencode_skill_variant,
)


class TopologyLitmusTests(unittest.TestCase):
    def test_create_and_validate_all_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            results = create_and_validate(Path(tmp))
            self.assertEqual(len(results), 6)
            self.assertTrue(all(result.status == "PASS" for result in results))

    def test_json_report_is_parseable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            results = create_and_validate(output)
            payload = json.loads(render_json(results, output))
            self.assertEqual(payload["summary"]["pass"], 6)
            self.assertEqual(payload["summary"]["fail"], 0)

    def test_markdown_report_names_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            results = create_and_validate(output)
            report = render_markdown(results, output)
            self.assertIn("symlinked-skills-dir", report)
            self.assertIn("symlink-write-safety", report)

    def test_fixtures_command(self) -> None:
        self.assertEqual(main(["fixtures"]), 0)

    def test_opencode_variant_isolates_user_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_path = repo / ".opencode" / "skills"
            payload = '[{"name":"topology-test"}]\n'
            with patch(
                "agent_path_topology_litmus.core.run_command",
                return_value=CompletedProcess(["opencode"], 0, payload, ""),
            ) as run:
                result = run_opencode_skill_variant(repo, "test", "topology-test", skill_path)

            env = run.call_args.kwargs["env"]
            self.assertEqual(env["HOME"], str(repo / ".litmus-home"))
            self.assertEqual(env["XDG_CONFIG_HOME"], str(repo / ".litmus-home" / ".config"))
            self.assertEqual(env["OPENCODE_DISABLE_EXTERNAL_SKILLS"], "true")
            self.assertTrue(result["visible"])

    def test_codex_adapter_isolates_user_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            sub_path = output / "submodule-instruction-scope" / "superproject" / "vendor" / "sub"
            sub_path.mkdir(parents=True)
            payload = json.dumps({"rules": "SUBMODULE_RULE=1 SUPERPROJECT_RULE=1"})
            with patch("agent_path_topology_litmus.core.shutil.which", return_value="/usr/bin/codex"), patch(
                "agent_path_topology_litmus.core.run_command",
                return_value=CompletedProcess(["codex"], 0, payload, ""),
            ) as run:
                result = codex_prompt_input(output)

            self.assertEqual(run.call_args.kwargs["env"], {"CODEX_HOME": str(output / ".litmus-codex-home")})
            self.assertEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
