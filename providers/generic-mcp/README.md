# Consentary for other MCP clients

Compatible clients connect to Consentary through the OAuth-protected Streamable HTTP endpoint at
`https://consentary.com/mcp`.

There is no universal Agent Plugin install command. Each client decides how it loads plugin
directories and where it stores MCP configuration.

## Agent Plugins 1.0 — recommended

If the client supports [Agent Plugins 1.0](https://agent-plugins.org/specification), use its source
or directory installer to load
[`../../plugins/consentary-vault/`](../../plugins/consentary-vault/).

This full plugin includes:

- portable `plugin.json` package metadata;
- the remote `mcp.json` connection; and
- the canonical session-only `skills/vault-workflows/SKILL.md` instructions.

## MCP-only setup

If the client supports remote MCP but not Agent Plugins, add a server with:

| Setting | Value |
|---|---|
| Name | `consentary` |
| Transport | `Streamable HTTP` |
| URL | `https://consentary.com/mcp` |

For clients that accept the portable Agent Plugins MCP shape:

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

Do not add a client secret, access token, manual OAuth URL, or static authorization header. The
client must follow the endpoint's OAuth discovery challenge and open browser sign-in.

This path is connector only. Server-side validation and phone consent remain active, but the
session-only skill is not installed.

## Skill-only addition

If the client supports Agent Skills but not complete Agent Plugins, install
[`../../plugins/consentary-vault/skills/vault-workflows/`](../../plugins/consentary-vault/skills/vault-workflows/)
in the client's documented skills directory after configuring the MCP server. Do not copy the skill
text into a second maintained file.

## Verify the connection

After browser sign-in, confirm the client discovers:

- `list_available_properties`
- `list_templates`
- `request_properties`
- `add_properties`

Then try:

> Show what kinds of information are available in my Consentary vault. Do not request any values.

Every value disclosure and proposed vault change must return to the linked iPhone for approval.

## Compatibility requirements

The client must support:

- remote MCP over Streamable HTTP;
- OAuth protected-resource and authorization-server metadata discovery;
- Authorization Code with PKCE S256; and
- the `mcp:access` scope without requesting `mobile:access`.

The client must not require the user to supply a client secret or raw access token. A client that
cannot complete OAuth discovery is not compatible.

## Connection identity

Consentary can show a client name when Auth0 includes the registered application name in the signed
`https://consentary.com/client_name` access-token claim. The label is **OAuth-registered, not
brand-verified**. Consentary ignores self-reported MCP `initialize.clientInfo` names for identity,
grouping, authorization, and disconnect behavior.

Each unrecognized OAuth client ID gets a separate connection record. Disconnect blocks that exact
connection before its Auth0 grants are removed and verified. Reconnection requires a fresh OAuth
flow.

See the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
and [Agent Plugins 1.0 specification](https://agent-plugins.org/specification) for portable client
requirements.
