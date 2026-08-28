# Generic remote MCP clients

Compatible remote HTTP MCP clients connect at `https://consentary.com/mcp` through OAuth. Users
must never be asked for an OAuth client secret or access token.

## Install the workflow skill

Prefer the complete `plugins/consentary-vault/` Agent Plugin when the client implements the Agent
Plugins 1.0 standard. Its portable `plugin.json` loads the canonical
`skills/vault-workflows/SKILL.md`, and its `mcp.json` connects the remote Consentary server.

For a client that supports Agent Skills but not Agent Plugins:

1. Install the `plugins/consentary-vault/skills/vault-workflows/` directory in the client's Agent
   Skills search path.
2. Configure `https://consentary.com/mcp` as a Streamable HTTP MCP server.
3. Complete OAuth through the client and enable the Consentary tools.
4. Confirm the client discovers `vault-workflows` before using vault tools.

The skill is instruction-only and shared by every supported package. It never contains scripts,
credentials, tokens, authorization logic, or an alternative path around phone consent. Clients
that implement neither Agent Plugins nor Agent Skills can still use the MCP connector safely;
server validation and MCP metadata remain mandatory and canonical.

Consentary can show a specific client name when Auth0 includes the registered application name in
the signed `https://consentary.com/client_name` access-token claim. That label is
**OAuth-registered, not brand-verified**. Consentary ignores the self-reported MCP
`initialize.clientInfo` name for identity, grouping, authorization, and disconnect behavior.

Each unrecognized OAuth client ID gets a separate connection record, even when two registrations
use the same display name. Disconnect blocks that exact connection before deleting and verifying
its Auth0 grants. Reconnection requires a fresh OAuth flow.
