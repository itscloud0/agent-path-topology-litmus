from __future__ import annotations

import re
import unittest
from pathlib import Path


class WorkflowTests(unittest.TestCase):
    def test_readme_exposes_exact_release_assets(self) -> None:
        readme = (Path(__file__).parents[1] / "README.md").read_text()
        asset_urls = (
            "https://github.com/itscloud0/agent-path-topology-litmus/releases/download/"
            "v0.2.1/agent_path_topology_litmus-0.2.1-py3-none-any.whl",
            "https://github.com/itscloud0/agent-path-topology-litmus/releases/download/"
            "v0.2.1/agent_path_topology_litmus-0.2.1.tar.gz",
        )

        for asset_url in asset_urls:
            self.assertEqual(readme.count(asset_url), 1)
        self.assertIn("prebuilt public `v0.2.1` wheel", readme)
        self.assertIn("matching source distribution", readme)

    def test_public_release_asset_smoke_uses_documented_wheel(self) -> None:
        root = Path(__file__).parents[1]
        workflow = (root / ".github" / "workflows" / "ci.yml").read_text()
        readme = (root / "README.md").read_text()
        wheel_url = (
            "https://github.com/itscloud0/agent-path-topology-litmus/releases/download/"
            "v0.2.1/agent_path_topology_litmus-0.2.1-py3-none-any.whl"
        )
        asset_job = workflow.split("  public-release-assets:", 1)[1]

        self.assertIn(wheel_url, readme)
        self.assertEqual(asset_job.count(wheel_url), 1)
        self.assertNotIn("actions/checkout@", asset_job)
        self.assertIn("agent-path-topology-litmus validate", asset_job)

    def test_external_actions_use_reviewed_full_commit_pins(self) -> None:
        workflow = Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml"
        refs = re.findall(r"^\s*- uses: (actions/[^\s]+)", workflow.read_text(), re.MULTILINE)

        self.assertEqual(
            refs,
            [
                "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
                "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
                "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
                "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
            ],
        )
        self.assertTrue(all(re.fullmatch(r"actions/[^@]+@[0-9a-f]{40}", ref) for ref in refs))


if __name__ == "__main__":
    unittest.main()
