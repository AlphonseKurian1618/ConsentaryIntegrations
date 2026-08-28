# Consentary integrations

Provider-specific integration assets for Consentary's OAuth-protected remote MCP service. This
repository contains connector setup, provider conformance contracts, sanitized interoperability
evidence, pilot plans, reusable plugin assets, and directory-submission material.

Provider files never contain credentials or create a second authorization path. The phone remains
the final authority for disclosure and writes.

## Providers

| Provider | Entry point | Status |
|---|---|---|
| Anthropic Claude | [`providers/claude/`](providers/claude/) | Production CIMD registration fixed; connector acceptance and plugin validation pending |
| OpenAI ChatGPT and Codex | [`providers/chatgpt/`](providers/chatgpt/) | Production ChatGPT plugin registered; interactive OAuth and acceptance pending |
| Visual Studio Code | [`providers/vscode/`](providers/vscode/) | Portable Agent Plugin and shared skill added; end-to-end acceptance pending |
| Other remote MCP clients | [`providers/generic-mcp/`](providers/generic-mcp/) | Portable Agent Plugin/Skill plus registered-client naming with explicit unverified-brand labeling |

## Universal plugin

[`plugins/consentary-vault/`](plugins/consentary-vault/) is the only source for the Consentary MCP
configuration and vault-workflow instructions. Claude, ChatGPT, Codex, VS Code, and generic Agent
Plugins/Skills package metadata all point to that directory, so a workflow or privacy instruction
is changed once and received by every supported plugin host on its next package release.

The repository exposes both a Claude marketplace and an OpenAI/Codex marketplace. The remote
connector remains independently safe: MCP metadata and server-side validation are canonical, while
the plugin adds reusable session-only handling and workflow guidance.

The same directory also implements the portable Agent Plugins 1.0 layout with root `plugin.json`,
`mcp.json`, and `skills/`. Skills-only clients can install the `vault-workflows` directory while
configuring the remote MCP endpoint separately; no maintained copy of the skill is permitted.

```text
/plugin marketplace add <this-repository>
/plugin install consentary-vault@consentary-plugins

codex plugin marketplace add <this-repository>
codex plugin add consentary-vault@consentary-plugins
```

The production ChatGPT Developer-mode registration is recorded in `.app.json` using the real
`plugin_asdk_app_...` connection ID. See [`providers/chatgpt/README.md`](providers/chatgpt/README.md)
for the remaining OAuth and acceptance gates; never replace it with a placeholder or a test ID.

## Validate

The checks use only the Python standard library:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```
