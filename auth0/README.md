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

Deployment status on 2026-08-27: the Node 22 Action version is created and deployed in the
production Auth0 tenant. It still must be attached to the **Post Login** flow and the flow applied
before the claim is emitted. Treat phone display-name verification as pending until a freshly issued
Claude access token produces the requester label **Claude**.
