# Auth0 integration configuration

This directory contains reviewable source for Auth0 configuration that supports third-party MCP
clients. The Auth0 Dashboard remains the deployment surface; never export tenant secrets or tokens
into this repository.

`actions/set-client-name.js` adds the Auth0-registered application name to the signed access-token
claim `https://consentary.com/client_name`. Consentary uses that claim only as a short requester label
on the phone. The backend independently enforces issuer, audience, signature, expiry, authorized
party, and `mcp:access`, and ignores this label for first-party clients.

The Action must never add scopes, make authorization decisions, copy user profile fields, call a
remote service, or set an ID-token claim.

Deployment status on 2026-08-28: the Node 22 Action version is deployed and attached to the
production Auth0 tenant's **Post Login** flow between authentication and token issuance. Auth0
reports the flow as live. The Action applies to every application using that tenant-wide trigger,
so freshly issued third-party MCP tokens receive their Auth0-registered application name as the
display-only requester label. Reconnect each provider before verification so cached access and
refresh tokens are replaced, then confirm the phone shows **Claude** and **ChatGPT**, plus the
registered name of any other MCP agent. These remain display-only checks. The backend continues to
authorize with signed token identity, audience, and scope rather than the label.

Third-party login policy on 2026-08-28: only the Apple and Google social connections are promoted
to the Auth0 domain level. Passwordless email is not promoted, so Claude, ChatGPT, and other strict
third-party MCP clients cannot offer it. Provider clients remain limited to the Consentary MCP
API's `mcp:access`; `mobile:access` is not granted.

## Agent disconnect control plane

Create a dedicated confidential machine-to-machine application for the Consentary backend and
authorize only the Auth0 Management API permissions needed to read and delete user grants
(`read:grants` and `delete:grants`). Store its secret in Azure Key Vault as
`auth0-management-client-secret`; never put it in Helm values, GitHub variables, the iPhone app,
or a provider package. The public management client ID is supplied as
`AUTH0_MANAGEMENT_CLIENT_ID`.

On confirmed disconnect the backend first writes a strongly consistent block for the connection,
then deletes matching user/client/API-audience grants and verifies that none remain. A provider
failure leaves the connection in `cleanup_pending`: MCP traffic remains blocked and a later retry
continues cleanup. A disconnected client becomes active again only after cleanup and a genuinely
fresh OAuth authorization. Refreshing an old token is not a reconnect path.

ChatGPT, Claude, and Visual Studio Code are mapped by exact reviewed OAuth client IDs. Every other
OAuth client gets its own record keyed by client ID. Its visible name may come only from the signed
registered-client claim emitted by `set-client-name.js`; MCP `clientInfo` is never an identity
source.
