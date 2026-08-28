#!/usr/bin/env python3
"""Validate integration contracts without network access or third-party packages."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "contracts/claude/tool-catalog.json"
EXPECTED_TOOLS = {
    "list_available_properties": (
        "List available vault properties",
        {"readOnlyHint": True, "openWorldHint": False},
    ),
    "list_templates": (
        "List vault templates",
        {"readOnlyHint": True, "openWorldHint": False},
    ),
    "request_properties": (
        "Request vault properties",
        {"readOnlyHint": True, "openWorldHint": False},
    ),
    "add_properties": (
        "Propose vault changes",
        {
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    ),
}
PILOT_HEADER = [
    "date",
    "environment",
    "backend_digest",
    "client",
    "client_version",
    "platform",
    "prompt_id",
    "expected_sequence",
    "actual_sequence",
    "result_status",
    "user_correction",
    "notes",
]


def validate() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    assert catalog["descriptionLimitBytes"] == 2048
    assert catalog["skillRequired"] is False
    assert set(catalog["tools"]) == set(EXPECTED_TOOLS)
    for name, (title, annotations) in EXPECTED_TOOLS.items():
        assert catalog["tools"][name] == {"title": title, "annotations": annotations}

    invariants = set(catalog["workflowInvariants"])
    assert invariants == {
        "discover before requesting or updating",
        "inspect templates before creation",
        "copy handles and metadata exactly",
        "never poll",
        "refresh discovery after writes",
    }

    required = [
        ROOT / "README.md",
        ROOT / "providers/README.md",
        ROOT / "providers/claude/README.md",
        ROOT / "providers/claude/oauth.md",
        ROOT / "providers/claude/rollout.md",
    ]
    for path in required:
        text = path.read_text(encoding="utf-8")
        assert text.strip(), f"{path.relative_to(ROOT)} is empty"

    with (ROOT / "providers/claude/pilot-matrix.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        assert next(csv.reader(stream)) == PILOT_HEADER


if __name__ == "__main__":
    validate()
    print("Consentary integration contracts are valid")

