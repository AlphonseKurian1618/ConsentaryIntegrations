# ChatGPT OAuth compatibility

## Required boundary

- MCP resource: `https://consentary.com/mcp`
- Authorization server: `https://auth.consentary.com/`
- Flow: Authorization Code with PKCE S256
- Scopes: `mcp:access offline_access`
- Stable ChatGPT client metadata document: `https://chatgpt.com/oauth/client.json`
- Stable redirect URI when issuer identification is supported:
  `https://chatgpt.com/connector_platform_oauth_redirect`
- Fallback redirect form: `https://chatgpt.com/connector/oauth/{callback_id}`
- Production plugin client metadata: `https://chatgpt.com/oauth/lDHHA7lBl98a/client.json`
- Production plugin redirect URI: `https://chatgpt.com/connector/oauth/lDHHA7lBl98a`
- Token endpoint authentication: `private_key_jwt` for the production plugin CIMD client; no shared
  client secret

ChatGPT is a third-party public client. Prefer validated client metadata and Auth0 CIMD/DCR; do not
create a Consentary-owned ChatGPT client, static client secret, callback wildcard, token store, or
`mobile:access` grant. Auth0 may copy the registered client name into the signed display-only
`https://consentary.com/client_name` claim so the phone can show **ChatGPT**. That label is never
authorization input.

Before interactive testing, validate the published ChatGPT client metadata and let Auth0 import the
per-plugin CIMD client. Review the exact callback, grants, application type, private-key JWT token
authentication, and only the `mcp:access` API permission. The stable ChatGPT metadata document is a
compatibility reference; the production Developer-mode plugin currently uses its generated
per-plugin metadata document and callback.

Acceptance must verify login, consent, callback, 15-minute access-token refresh through
`offline_access`, disconnect, and reconnect. Record only sanitized status, metadata digests,
grants, scopes, and pass/fail results. Never save authorization codes, access or refresh tokens,
subjects, cookies, credentials, or vault values.

## Primary references

- [OpenAI plugin authentication](https://developers.openai.com/plugins/build/auth)
- [OpenAI: Connect from ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt)
- [Auth0: Register Applications with CIMD](https://auth0.com/docs/get-started/auth0-overview/create-applications/register-applications-with-cimd)
