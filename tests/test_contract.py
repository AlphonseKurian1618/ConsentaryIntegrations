from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IntegrationContractTests(unittest.TestCase):
    def test_repository_contracts_validate(self) -> None:
        path = ROOT / "scripts/validate.py"
        spec = importlib.util.spec_from_file_location("validate_integrations", path)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.validate()

    def test_claude_oauth_evidence_is_sanitized(self) -> None:
        text = (ROOT / "providers/claude/oauth.md").read_text(encoding="utf-8")
        self.assertIn("Unknown client", text)
        self.assertIn("third-party CIMD client", text)
        self.assertIn("Never save authorization codes", text)
        self.assertNotIn("client_secret=", text)
        self.assertNotIn("access_token=", text)

    def test_rollout_keeps_phone_consent_and_connector_only_gate(self) -> None:
        text = (ROOT / "providers/claude/rollout.md").read_text(encoding="utf-8")
        self.assertIn("without relying on a companion plugin", text)
        self.assertIn("no more than 10%", text)
        self.assertIn("fictional data", text)
        self.assertIn("Server-side validation remains mandatory", text)

    def test_shared_plugin_requires_session_only_vault_handling(self) -> None:
        text = (
            ROOT / "plugins/consentary-vault/skills/vault-workflows/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("only in the current conversation", text)
        self.assertIn("Do not store or copy vault-derived information", text)
        self.assertIn("assistant memory", text)
        self.assertIn("external services", text)
        self.assertIn("later conversations or", text)
        self.assertNotIn("current Claude session", text)

    def test_all_marketplaces_reference_the_same_plugin_source(self) -> None:
        import json

        claude = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        openai = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(claude["plugins"][0]["source"], "./plugins/consentary-vault")
        self.assertEqual(
            openai["plugins"][0]["source"]["path"], "./plugins/consentary-vault"
        )

    def test_vscode_and_generic_clients_share_portable_skill(self) -> None:
        import json

        contracts = []
        for provider in ("vscode", "generic-mcp"):
            contracts.append(
                json.loads(
                    (ROOT / f"contracts/{provider}/conformance.json").read_text(
                        encoding="utf-8"
                    )
                )
            )

        self.assertEqual(
            contracts[0]["distribution"]["skill"],
            contracts[1]["distribution"]["skill"],
        )
        self.assertFalse(contracts[0]["skillRequiredForAuthorization"])
        self.assertFalse(contracts[1]["skillRequiredForAuthorization"])

        plugin = ROOT / "plugins/consentary-vault"
        manifest = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "consentary-vault")
        self.assertEqual(
            manifest["$schema"],
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        )

        mcp = json.loads((plugin / "mcp.json").read_text(encoding="utf-8"))
        server = mcp["mcpServers"]["consentary"]
        self.assertEqual(server["type"], "streamable-http")
        self.assertEqual(server["url"], "https://consentary.com/mcp")
        self.assertNotIn("oauth", json.dumps(mcp).lower())
        self.assertNotIn("secret", json.dumps(mcp).lower())

        skill = (plugin / "skills/vault-workflows/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("VS Code and other skills-compatible agents", skill)
        for provider in ("vscode", "generic-mcp"):
            documentation = (ROOT / f"providers/{provider}/README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("skills/vault-workflows", documentation)

    def test_chatgpt_contract_never_broadens_phone_authority(self) -> None:
        text = (ROOT / "providers/chatgpt/oauth.md").read_text(encoding="utf-8")
        self.assertIn("https://chatgpt.com/oauth/client.json", text)
        self.assertIn("PKCE S256", text)
        self.assertIn("never request `mobile:access`", (ROOT / "providers/chatgpt/README.md").read_text(encoding="utf-8"))
        self.assertIn("label is never", text)
        self.assertNotIn("client_secret=", text)
        self.assertNotIn("access_token=", text)

    def test_auth0_action_is_display_only(self) -> None:
        text = (ROOT / "auth0/actions/set-client-name.js").read_text(encoding="utf-8")
        self.assertIn("api.accessToken.setCustomClaim", text)
        self.assertIn("https://consentary.com/client_name", text)
        self.assertNotIn("api.idToken", text)
        self.assertNotIn("addScope", text)
        self.assertNotIn("api.access.deny", text)
        readme = (ROOT / "auth0/README.md").read_text(encoding="utf-8")
        self.assertIn("**Claude** and **ChatGPT**", readme)
        self.assertIn("display-only checks", readme)

    def test_agent_directory_identity_and_disconnect_contract(self) -> None:
        import json

        catalog = json.loads(
            (ROOT / "contracts/common/agent-catalog.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            set(catalog["knownProviders"]),
            {"chatgpt", "claude", "vscode"},
        )
        self.assertEqual(
            catalog["genericClient"]["displayNameSource"],
            "signed_auth0_registered_client_name",
        )
        self.assertIn(
            "mcp_initialize_client_info",
            catalog["genericClient"]["ignoredIdentitySources"],
        )
        self.assertEqual(catalog["disconnect"]["order"][0], "block_at_consentary")
        auth0 = (ROOT / "auth0/README.md").read_text(encoding="utf-8")
        self.assertIn("read:grants", auth0)
        self.assertIn("delete:grants", auth0)
        self.assertIn("cleanup_pending", auth0)


if __name__ == "__main__":
    unittest.main()
