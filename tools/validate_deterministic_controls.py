#!/usr/bin/env python3
"""Validate static deterministic-control invariants without live network calls."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_RUNNER = ROOT / "Local" / "greenops_local.py"
GEMINI_CONFIG = ROOT / "Local" / "gemini_config.py"
WORKFLOW = ROOT / ".github" / "workflows" / "carbon-aware-pipeline.yml"
POLICY = ROOT / "docs" / "deterministic-systems-check.md"


def _tool_names(source: str) -> set[str]:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "tools_list" for target in node.targets
        ):
            if not isinstance(node.value, ast.List):
                raise AssertionError("tools_list must be an explicit list")
            return {
                element.id
                for element in node.value.elts
                if isinstance(element, ast.Name)
            }
    raise AssertionError("tools_list assignment not found")


def validate() -> list[str]:
    local_source = LOCAL_RUNNER.read_text(encoding="utf-8")
    gemini_config_source = GEMINI_CONFIG.read_text(encoding="utf-8")
    workflow_source = WORKFLOW.read_text(encoding="utf-8")
    policy_source = POLICY.read_text(encoding="utf-8")
    tool_names = _tool_names(local_source)

    assertions = [
        ("get_carbon_gate_decision" in tool_names, "local AI tool list lacks deterministic gate readout"),
        ("deploy_task" not in tool_names, "local AI tool list exposes deployment execution"),
        ("GEMINI_API_KEY" in gemini_config_source, "local runner does not use secure Gemini key precedence"),
        ("curl --fail --silent --show-error" in workflow_source, "workflow does not fail closed on carbon API errors"),
        ("should_run=false" in workflow_source, "workflow does not initialize a fail-closed decision"),
        ("systems_check_attestation" in workflow_source, "workflow lacks systems-check override evidence"),
        ("deterministic-systems-check" in workflow_source, "workflow lacks invariant validation job"),
        ("does not authenticate the human" in policy_source, "policy overclaims free-text identity verification"),
    ]

    failures = [message for passed, message in assertions if not passed]
    if failures:
        raise AssertionError("; ".join(failures))
    return [message for _, message in assertions]


if __name__ == "__main__":
    validated = validate()
    print(f"Validated {len(validated)} deterministic-control invariants.")
