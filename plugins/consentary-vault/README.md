# Consentary Vault universal plugin

This is the canonical package installed by Claude, ChatGPT, Codex, Visual Studio Code, and
Agent-Plugins-compatible clients. It combines Consentary's OAuth-protected remote MCP connection
with the session-only `vault-workflows` skill.

For the fastest supported installation, start with the repository's
[user guide](../../README.md#choose-your-agent).

## Quick install

### Claude Code

```bash
claude plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations && claude plugin install consentary-vault@consentary-plugins
```

### Codex CLI

```bash
codex plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations && codex plugin add consentary-vault@consentary-plugins
```

### Visual Studio Code with GitHub Copilot CLI

```bash
copilot plugin install AlphonseKurian1618/ConsentaryIntegrations:plugins/consentary-vault
```

Restart the client or start a new chat after installation, complete browser sign-in, and keep the
linked iPhone online for value requests and proposed changes.

## Package contents

- `plugin.json` is the portable Agent Plugins 1.0 manifest.
- `mcp.json` declares the production Streamable HTTP MCP endpoint in portable format.
- `skills/vault-workflows/SKILL.md` is the canonical cross-provider workflow and privacy guidance.
- `.claude-plugin/plugin.json` provides Claude package metadata.
- `.codex-plugin/plugin.json` provides ChatGPT and Codex package metadata.
- `.mcp.json` configures the production MCP connection for supported OpenAI and Claude hosts.
- `.app.json` maps the production ChatGPT Developer-mode registration.

The portable MCP manifest intentionally contains no OAuth fields. Compatible clients discover OAuth
from `https://consentary.com/mcp`, store their own credentials, and open the interactive browser
flow. Never add credentials, access tokens, client secrets, or fixed authorization headers to this
package.

## Skills-only clients

Clients that support Agent Skills but not complete Agent Plugins can install only
[`skills/vault-workflows/`](skills/vault-workflows/) and configure the same remote MCP endpoint
separately. The skill is instruction-only: it contains no scripts, credentials, OAuth
implementation, approval logic, or alternative path around phone consent.

Do not copy the skill or MCP configuration into a provider directory. Update this shared source and
release a new package version so every host receives the same behavior.
