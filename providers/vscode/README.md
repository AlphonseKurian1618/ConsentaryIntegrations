# Visual Studio Code

Visual Studio Code is a known Consentary agent identified by its exact registered Auth0 OAuth
client ID. It connects to the production remote HTTP MCP endpoint at
`https://consentary.com/mcp`, requests `mcp:access offline_access`, and uses PKCE S256. No client
secret, copied access token, local proxy, or alternate mobile scope is part of setup.

## Recommended setup: Agent Plugin

Install `plugins/consentary-vault/` as an Agent Plugin. The package combines the portable
`plugin.json`, remote `mcp.json`, and the canonical `skills/vault-workflows/SKILL.md` instructions.
For local development, clone this repository and add the absolute plugin directory to VS Code's
`chat.pluginLocations` setting. When published to a plugin marketplace, install the same package
from that marketplace instead.

1. Install or enable the Consentary Vault Agent Plugin.
2. Complete Consentary OAuth when VS Code starts the remote MCP connection.
3. Enable the Consentary tools for the chat session.
4. Run **Chat: Configure Skills** and confirm `vault-workflows` is available.
5. Return to the Consentary iPhone app and verify Visual Studio Code under **Connected**.

## Skill-only fallback

If the installed VS Code version supports Agent Skills but not Agent Plugins, copy or symlink
`plugins/consentary-vault/skills/vault-workflows/` to
`~/.copilot/skills/vault-workflows/`, then add `https://consentary.com/mcp` as a remote OAuth MCP
server. Do not copy the skill text into another maintained file; the plugin directory remains the
canonical source.

Every value request and proposed write still requires the normal iPhone consent flow.
