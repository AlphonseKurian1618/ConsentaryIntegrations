# Claude OAuth compatibility

## Required boundary

- MCP resource: `https://consentary.com/mcp`
- Authorization server: `https://auth.consentary.com/`
- Flow: Authorization Code with PKCE S256
- Scopes: `mcp:access offline_access`
- Current redirect URI: `https://claude.ai/api/mcp/auth_callback`
- Anticipated future redirect URI: `https://claude.com/api/mcp/auth_callback`, to be accepted only
  after Claude publishes it through validated client metadata
- Claude client metadata document: `https://claude.ai/oauth/mcp-oauth-client-metadata`
- Token endpoint authentication: `none`

Claude remains a third-party public client. Do not create a first-party Claude application, static
client secret, Anthropic API key, callback wildcard, token store, or `mobile:access` grant. A signed
client-name claim may display **Claude** on the phone, but it is never authorization input.

## Production observation — 2026-08-27

Sanitized live checks showed:

1. Auth0 discovery advertised an OIDC registration endpoint and Client ID Metadata Document (CIMD)
   support.
2. Claude's metadata document identified **Claude**, the `claude.ai` callback, authorization-code
   and refresh grants, PKCE S256, and token endpoint authentication `none`.
3. Auth0 rejected the authorization request with `invalid_request` and `Unknown client` for
   `https://claude.ai/oauth/mcp-oauth-client-metadata`.

This means capability discovery is enabled, but the external CIMD client is not registered in the
Auth0 tenant. Advertising CIMD support does not itself create the third-party client.

## Auth0 correction — completed 2026-08-27

In the Auth0 Dashboard, keep **Client ID Metadata Document Registration** and **Resource Parameter
Compatibility** enabled. Register Claude's metadata URL as a third-party CIMD client, authorize only
the Consentary MCP API's `mcp:access` permission, and promote only the login connections intended for
third-party clients. This is CIMD registration, not a static Consentary-owned Claude client.

Claude's CIMD was validated and registered in the production tenant. The imported mapping retained
the exact `claude.ai` callback, Authorization Code and Refresh Token grants, native application type,
token endpoint authentication `none`, and strict third-party ownership. Production API access shows
one of two user-delegated permissions: `mcp:access` selected and `mobile:access` unselected. Only
Apple and Google are available as domain-level connections; passwordless email is not promoted.
No client secret was created or read.

Repeating the previously failing production authorization request resolved the external client and
reached branded Consentary Universal Login instead of returning `Unknown client`. Interactive login,
consent, callback, refresh, disconnect, and reconnect remain connector acceptance steps rather than
tenant-registration blockers.

Do not add the anticipated `claude.com` callback manually or as a wildcard. When Claude publishes
new validated client metadata, register that metadata document or use **Refresh Application** and
review its mapped callback before saving.

After registration, repeat the authorization request and verify:

- Auth0 resolves the external metadata URL instead of returning `Unknown client`;
- the redirect URI is an exact value from the signed/validated client metadata;
- the authorization request uses PKCE S256;
- the access token has the Consentary audience and only `mcp:access`;
- `offline_access` produces refresh behavior after the 15-minute access-token lifetime;
- the signed display claim says `Claude`, but changing it cannot change authorization;
- disconnect invalidates the local connector session and reconnect succeeds without a secret.

Record only the date, environment, sanitized error code, metadata digest, grants, scopes, and
pass/fail result. Never save authorization codes, tokens, subjects, cookies, credentials, or vault
values.

## Primary references

- [Auth0: Register Applications with CIMD](https://auth0.com/docs/get-started/auth0-overview/create-applications/register-applications-with-cimd)
- [Auth0: Dynamic Client Registration](https://auth0.com/docs/get-started/applications/dynamic-client-registration)
- [Auth0: Configure Third-Party Applications](https://auth0.com/docs/get-started/applications/third-party-applications/configure-third-party-applications)
