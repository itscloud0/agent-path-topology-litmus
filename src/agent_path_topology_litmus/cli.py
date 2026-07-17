from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    FIXTURES,
    codex_prompt_input,
    create_and_validate,
    opencode_debug_skill,
    opencode_worktree_submodule,
    render_json,
    render_markdown,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-path-topology-litmus")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("fixtures", help="list fixture names")

    validate = subparsers.add_parser("validate", help="create and baseline-validate topology fixtures")
    validate.add_argument("--output", type=Path, required=True, help="directory for disposable fixtures")
    validate.add_argument("--format", choices=["json", "markdown"], default="json")

    run_adapter = subparsers.add_parser("run-adapter", help="run a local client diagnostic adapter")
    run_adapter.add_argument(
        "adapter",
        choices=["codex-prompt-input", "opencode-debug-skill", "opencode-worktree-submodule"],
    )
    run_adapter.add_argument("--output", type=Path, required=True, help="directory for disposable fixtures")
    run_adapter.add_argument("--format", choices=["json", "markdown"], default="json")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "fixtures":
        for fixture in FIXTURES:
            print(fixture)
        return 0

    if args.command == "validate":
        results = create_and_validate(args.output)
    elif args.command == "run-adapter":
        if args.adapter == "codex-prompt-input":
            results = [codex_prompt_input(args.output)]
        elif args.adapter == "opencode-worktree-submodule":
            results = [opencode_worktree_submodule(args.output)]
        else:
            results = [opencode_debug_skill(args.output)]
    else:
        parser.error(f"unknown command: {args.command}")

    if args.format == "markdown":
        print(render_markdown(results, args.output), end="")
    else:
        print(render_json(results, args.output))
    return 1 if any(result.status == "FAIL" for result in results) else 0
