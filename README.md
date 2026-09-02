# Consentary agent integrations

Give AI the information it needs without giving up the final say. Consentary lets compatible agents
discover what is available, then sends every value request and proposed change to your linked iPhone
for approval.

The production remote MCP endpoint is `https://consentary.com/mcp`.

**Get Consentary for iPhone:** [Join the beta on TestFlight](https://testflight.apple.com/join/dby4h3Vz).

## Before you install

You need:

- the Consentary TestFlight beta installed on a linked iPhone with notifications enabled;
- a current version of your AI client with plugins or remote HTTP MCP enabled; and
- permission to add plugins or MCP servers if your device or workspace is managed.

Consentary uses browser-based OAuth. Never paste a client secret, access token, authorization
header, or private key into a client configuration.

### Full plugin or connector only?

- **Full plugin** installs the remote MCP connection and Consentary's `vault-workflows` skill. The
  skill adds the session-only handling rules and the safest read/write sequence.
- **Connector only** installs the remote MCP connection without the skill. Phone consent and
  server-side validation still apply, but the additional agent instructions are not bundled.

Prefer the full plugin whenever your client supports it.

## Choose your agent

| Agent | Recommended setup | What it installs |
|---|---|---|
| [ChatGPT](#chatgpt) | Personal marketplace in ChatGPT Desktop | Full plugin |
| [Claude](#claude) | Personal marketplace or Claude Code command | Full plugin |
| [Visual Studio Code](#visual-studio-code) | Copilot CLI command or **Chat: Install Plugin From Source** | Full plugin |
| [Codex CLI](#codex-cli) | Marketplace and plugin command | Full plugin |
| [Other MCP clients](#other-mcp-clients) | Agent Plugin when supported; otherwise remote MCP | Full plugin or connector only |

## ChatGPT

### ChatGPT Desktop — full plugin

Install [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) if it is not already available, then
add this repository as a marketplace:

```bash
codex plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations
```

Restart ChatGPT Desktop, open **Plugins**, select **Consentary Plugins** under your personal
marketplaces, and install **Consentary Vault**. Start a new chat after installation.

### ChatGPT web — connector-only fallback

The repository plugin is not currently listed in ChatGPT's public plugin directory. To connect the
MCP server directly:

1. Open **Settings → Security and login** and enable **Developer mode**.
2. Open [ChatGPT Plugins](https://chatgpt.com/plugins), select the plus button, and create a
   connection named **Consentary**.
3. Choose a public remote MCP connection and enter `https://consentary.com/mcp`.
4. Review the four discovered tools, complete browser sign-in, and add Consentary from the tools
   menu in a new chat.

This fallback is connector only: it does not install the `vault-workflows` skill.

See the [ChatGPT guide](providers/chatgpt/) for details and safe example prompts.

## Claude

### Claude Code — one command

```bash
claude plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations && claude plugin install consentary-vault@consentary-plugins
```

Restart Claude Code, run `/mcp`, choose Consentary, and complete browser sign-in.

### Claude web or Desktop — no terminal

1. Open **Customize → Plugins**.
2. Under **Personal plugins**, select **+ → Add marketplace → Add from a repository**.
3. Enter `AlphonseKurian1618/ConsentaryIntegrations`.
4. Install **Consentary Vault**, then start a new chat and sign in when prompted.

See the [Claude guide](providers/claude/) for connector-only setup and troubleshooting.

## Visual Studio Code

With [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
installed, run:

```bash
copilot plugin install AlphonseKurian1618/ConsentaryIntegrations:plugins/consentary-vault
```

Reload Visual Studio Code. The installed plugin is discovered automatically. Complete browser
sign-in when Consentary starts, then use **Chat: Configure Skills** to confirm `vault-workflows` and
**MCP: List Servers** to confirm `consentary`.

Without a terminal, run **Chat: Install Plugin From Source**, enter
`https://github.com/AlphonseKurian1618/ConsentaryIntegrations`, and select `consentary-vault`.

If Agent Plugins are unavailable, the [Visual Studio Code guide](providers/vscode/) includes an
MCP-only fallback. That fallback does not install the skill.

## Codex CLI

Install the marketplace and full plugin with one copy-and-paste command:

```bash
codex plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations && codex plugin add consentary-vault@consentary-plugins
```

Start a new Codex session after installation and complete browser sign-in when prompted.

## Other MCP clients

There is no universal install command because clients choose how they install Agent Plugins and
where they store MCP configuration.

If the client supports [Agent Plugins 1.0](https://agent-plugins.org/specification), install or load
the [`plugins/consentary-vault/`](plugins/consentary-vault/) directory using its source or directory
installer. This is the full plugin.

For an MCP-only client, add a remote server with these values:

| Setting | Value |
|---|---|
| Name | `consentary` |
| Transport | `Streamable HTTP` |
| URL | `https://consentary.com/mcp` |

Clients that accept the portable Agent Plugins MCP format can use:

```json
{
  "mcpServers": {
    "consentary": {
      "type": "streamable-http",
      "url": "https://consentary.com/mcp"
    }
  }
}
```

Do not add manual OAuth URLs, static headers, secrets, or tokens. The client must discover OAuth
from the endpoint and open the browser sign-in flow. If the client supports Agent Skills but not
Agent Plugins, install
[`plugins/consentary-vault/skills/vault-workflows/`](plugins/consentary-vault/skills/vault-workflows/)
in its documented skills directory.

See the [generic MCP guide](providers/generic-mcp/) for compatibility details.

## Finish connecting

1. Restart the client or start a new chat so the installed plugin can load.
2. Enable the Consentary tools if the client asks which tools are available to the chat.
3. Complete Consentary sign-in in the browser. Do not copy credentials back into the client.
4. Keep the linked iPhone online. Metadata discovery does not reveal values; every value disclosure
   and proposed vault change returns to the phone for approval.
5. Confirm that the client shows these four tools:
   - `list_available_properties`
   - `list_templates`
   - `request_properties`
   - `add_properties`

Try this safe first prompt:

> Show what kinds of information are available in my Consentary vault. Do not request any values.

## Privacy behavior

The full plugin instructs agents to use data retrieved from Consentary, and data proposed for a
Consentary write, only in the current chat session. An approved write may persist in Consentary;
the agent must not keep a separate copy. These instructions do not change an AI provider's own
account-level conversation-retention settings.

## Troubleshooting

- **The plugin command is missing:** update the client and restart it. Agent Plugin support requires
  a current Claude Code, Codex CLI, GitHub Copilot CLI, or Visual Studio Code release.
- **Installation is blocked:** ask the workspace administrator to allow personal plugins and the
  Consentary MCP endpoint.
- **The skill or tools are missing:** restart the client, start a new chat, and verify both the
  installed plugin and MCP server are enabled.
- **Browser sign-in fails:** remove or disconnect Consentary in the client, then reconnect. Do not
  create a client secret or paste a token.
- **The phone request does not arrive:** open Consentary, confirm the phone is online and linked,
  check notifications, then make one new request. Do not repeatedly poll.

For help, visit [Consentary Support](https://consentary.com/support).

## Maintainers

This repository contains provider-specific documentation, conformance contracts, sanitized test
evidence, and the canonical distributable plugin. It does not implement the Consentary MCP server
or iPhone app.

[`plugins/consentary-vault/`](plugins/consentary-vault/) is the only maintained source for the MCP
configuration and `vault-workflows` skill. Provider directories must link to it rather than copying
plugin configuration or instructions.

| Provider | Status and acceptance material |
|---|---|
| Claude | [`providers/claude/`](providers/claude/) |
| ChatGPT and Codex | [`providers/chatgpt/`](providers/chatgpt/) |
| Visual Studio Code | [`providers/vscode/`](providers/vscode/) |
| Generic MCP | [`providers/generic-mcp/`](providers/generic-mcp/) |

Run the dependency-free contract checks with:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Official installation references: [OpenAI plugins](https://learn.chatgpt.com/docs/plugins),
[Claude plugins](https://code.claude.com/docs/en/discover-plugins),
[Visual Studio Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins),
[GitHub Copilot CLI plugins](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference),
and [Agent Plugins 1.0](https://agent-plugins.org/specification).
