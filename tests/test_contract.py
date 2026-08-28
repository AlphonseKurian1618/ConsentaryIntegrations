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

    def test_rollout_keeps_phone_consent_and_no_skill_gate(self) -> None:
        text = (ROOT / "providers/claude/rollout.md").read_text(encoding="utf-8")
        self.assertIn("without a Claude Skill", text)
        self.assertIn("no more than 10%", text)
        self.assertIn("fictional data", text)
        self.assertIn("Server-side validation remains mandatory", text)

    def test_auth0_action_is_display_only(self) -> None:
        text = (ROOT / "auth0/actions/set-client-name.js").read_text(encoding="utf-8")
        self.assertIn("api.accessToken.setCustomClaim", text)
        self.assertIn("https://consentary.com/client_name", text)
        self.assertNotIn("api.idToken", text)
        self.assertNotIn("addScope", text)
        self.assertNotIn("api.access.deny", text)


if __name__ == "__main__":
    unittest.main()
