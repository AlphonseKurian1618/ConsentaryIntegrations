#!/usr/bin/env python3
"""Validate integration contracts without network access or third-party packages."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "contracts/common/tool-catalog.json"
AGENT_CATALOG = ROOT / "contracts/common/agent-catalog.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
OPENAI_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
PLUGIN = ROOT / "plugins/consentary-vault"
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
    assert catalog["pluginRequired"] is False
    assert catalog["securitySchemes"] == [
        {"type": "oauth2", "scopes": ["mcp:access"]}
    ]
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
        ROOT / "auth0/README.md",
        ROOT / "auth0/actions/set-client-name.js",
        ROOT / "providers/README.md",
        ROOT / "providers/claude/README.md",
        ROOT / "providers/claude/oauth.md",
        ROOT / "providers/claude/rollout.md",
        ROOT / "providers/chatgpt/README.md",
        ROOT / "providers/chatgpt/oauth.md",
        ROOT / "providers/chatgpt/rollout.md",
        ROOT / "providers/vscode/README.md",
        ROOT / "providers/generic-mcp/README.md",
        ROOT / "plugins/consentary-vault/README.md",
        ROOT / "plugins/consentary-vault/plugin.json",
        ROOT / "plugins/consentary-vault/mcp.json",
        ROOT / "plugins/consentary-vault/skills/vault-workflows/SKILL.md",
    ]
    for path in required:
        text = path.read_text(encoding="utf-8")
        assert text.strip(), f"{path.relative_to(ROOT)} is empty"

    claude_marketplace = json.loads(CLAUDE_MARKETPLACE.read_text(encoding="utf-8"))
    assert claude_marketplace["name"] == "consentary-plugins"
    assert claude_marketplace["plugins"][0]["name"] == "consentary-vault"
    assert claude_marketplace["plugins"][0]["source"] == "./plugins/consentary-vault"

    openai_marketplace = json.loads(OPENAI_MARKETPLACE.read_text(encoding="utf-8"))
    assert openai_marketplace["name"] == "consentary-plugins"
    openai_entry = openai_marketplace["plugins"][0]
    assert openai_entry == {
        "name": "consentary-vault",
        "source": {"source": "local", "path": "./plugins/consentary-vault"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Productivity",
    }

    claude_manifest = json.loads(
        (PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    assert claude_manifest["name"] == "consentary-vault"

    openai_manifest = json.loads(
        (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    assert openai_manifest["name"] == "consentary-vault"
    assert openai_manifest["skills"] == "./skills"
    assert openai_manifest["mcpServers"] == "./.mcp.json"
    app_manifest = PLUGIN / ".app.json"
    if app_manifest.exists():
        apps = json.loads(app_manifest.read_text(encoding="utf-8"))["apps"]
        assert apps
        assert all(
            isinstance(app["id"], str) and app["id"].startswith("plugin_asdk_app_")
            for app in apps.values()
        )
        assert openai_manifest["apps"] == "./.app.json"
    else:
        assert "apps" not in openai_manifest

    mcp = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
    server = mcp["mcpServers"]["consentary"]
    assert server == {
        "type": "http",
        "url": "https://consentary.com/mcp",
        "oauth": {"scopes": "mcp:access offline_access"},
    }

    portable_manifest = json.loads(
        (PLUGIN / "plugin.json").read_text(encoding="utf-8")
    )
    assert portable_manifest["$schema"] == (
        "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    )
    assert portable_manifest["name"] == "consentary-vault"
    assert portable_manifest["version"] == "1.0.0"

    portable_mcp = json.loads((PLUGIN / "mcp.json").read_text(encoding="utf-8"))
    assert portable_mcp["$schema"] == (
        "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    )
    portable_server = portable_mcp["mcpServers"]["consentary"]
    assert portable_server == {
        "type": "streamable-http",
        "url": server["url"],
    }
    portable_mcp_text = json.dumps(portable_mcp).lower()
    for forbidden in ("oauth", "secret", "token", "authorization", "header"):
        assert forbidden not in portable_mcp_text

    skill = (PLUGIN / "skills/vault-workflows/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert skill.startswith("---\nname: vault-workflows\n")
    assert "VS Code and other skills-compatible agents" in skill
    assert "This skill does not contain credentials, perform OAuth" in skill
    for privacy_rule in (
        "only in the current conversation",
        "Do not store or copy vault-derived information",
        "assistant memory",
        "plugin data",
        "external services",
        "summaries intended for later conversations or",
    ):
        assert privacy_rule in skill

    action = (ROOT / "auth0/actions/set-client-name.js").read_text(encoding="utf-8")
    assert "api.accessToken.setCustomClaim" in action
    assert '"https://consentary.com/client_name"' in action
    assert "api.idToken" not in action
    assert "addScope" not in action
    assert "removeScope" not in action
    assert "api.access.deny" not in action

    expected_token_auth = {
        "claude": "none",
        "chatgpt": "private_key_jwt",
        "vscode": "none",
    }
    for provider in ("claude", "chatgpt"):
        with (ROOT / f"providers/{provider}/pilot-matrix.csv").open(
            encoding="utf-8", newline=""
        ) as stream:
            assert next(csv.reader(stream)) == PILOT_HEADER

    for provider in ("claude", "chatgpt", "vscode"):
        conformance = json.loads(
            (ROOT / f"contracts/{provider}/conformance.json").read_text(encoding="utf-8")
        )
        assert conformance["toolCatalog"] == "../common/tool-catalog.json"
        assert conformance["mcpEndpoint"] == "https://consentary.com/mcp"
        assert conformance["scopes"] == ["mcp:access", "offline_access"]
        assert conformance["pkceMethods"] == ["S256"]
        assert conformance["tokenEndpointAuthMethod"] == expected_token_auth[provider]

    agents = json.loads(AGENT_CATALOG.read_text(encoding="utf-8"))
    assert set(agents["knownProviders"]) == {"chatgpt", "claude", "vscode"}
    assert all(
        item["identityAssurance"] == "known_provider"
        for item in agents["knownProviders"].values()
    )
    assert agents["genericClient"]["displayNameSource"] == (
        "signed_auth0_registered_client_name"
    )
    assert agents["genericClient"]["ignoredIdentitySources"] == [
        "mcp_initialize_client_info"
    ]
    assert agents["disconnect"]["order"][0] == "block_at_consentary"

    generic = json.loads(
        (ROOT / "contracts/generic-mcp/conformance.json").read_text(encoding="utf-8")
    )
    assert generic["clientSecretRequestedFromUser"] is False
    assert generic["brandIdentityVerified"] is False

    expected_distribution = {
        "agentPluginManifest": "../../plugins/consentary-vault/plugin.json",
        "portableMcpConfig": "../../plugins/consentary-vault/mcp.json",
        "skill": "../../plugins/consentary-vault/skills/vault-workflows/SKILL.md",
    }
    for provider in ("vscode", "generic-mcp"):
        contract_path = ROOT / f"contracts/{provider}/conformance.json"
        conformance = json.loads(contract_path.read_text(encoding="utf-8"))
        assert conformance["distribution"] == expected_distribution
        assert conformance["skillRequiredForAuthorization"] is False
        for relative_path in conformance["distribution"].values():
            assert (contract_path.parent / relative_path).resolve().is_file()


if __name__ == "__main__":
    validate()
    print("Consentary integration contracts are valid")
