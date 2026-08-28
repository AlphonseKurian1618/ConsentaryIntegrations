# Consentary for Claude

Consentary is exposed to Claude as an OAuth-protected remote MCP connector at
`https://consentary.com/mcp`. The connector is installed in Claude.ai or Claude Desktop and is then
available on Claude mobile after the same account is linked and its tools are enabled.

Version 1 uses the existing four-tool MCP contract. It requires no Anthropic SDK, Anthropic API
key, static Claude OAuth client, client secret, token persistence, or Claude-specific iOS code.
MCP metadata and server-side validation are the canonical operating contract.

## Supported workflow

1. Add `https://consentary.com/mcp` as a custom connector without entering a client ID or secret.
2. Complete Authorization Code authentication with PKCE S256 and approve `mcp:access` plus
   `offline_access`. Never grant `mobile:access` to the connector.
3. Enable the Consentary tools in the conversation.
4. Discover current property handles before requesting or updating values. Inspect templates before
   creating items or fields. Copy all handles and metadata exactly.
5. Make one disclosure or write request and wait for the phone decision. Never poll or attempt to
   bypass the phone. Refresh discovery after a write.

The public, no-tracking user guide is
[`https://consentary.com/connectors/claude`](https://consentary.com/connectors/claude).

## Example prompts

- **Metadata only:** “List the kinds of information available in my Consentary vault. Do not
  request any values.”
- **Selective disclosure:** “Discover my available contact fields, then ask my phone to share only
  the email address I select for this application.”
- **Phone-approved change:** “Inspect Consentary's templates, then propose a fictional vehicle item
  for my phone to review.”

## Troubleshooting

- **Linking fails before login:** capture only the OAuth error code and sanitized URL parameters;
  compare them with [`oauth.md`](oauth.md). Never paste a token or authorization code.
- **No notification:** verify notifications and phone linking, then use inbox recovery. Do not
  repeatedly call the tool.
- **Timeout:** unlock or reconnect the phone and start a new request. A force-quit iOS app is not
  background-launched by notification.
- **Stale handle:** run discovery again and use the newly returned opaque handle.
- **OAuth stops refreshing:** disconnect the connector and reconnect it; do not create a client
  secret.
- **Tools are missing on mobile:** finish linking on web or Desktop, open a new mobile conversation,
  and enable the connected tools.

See [`rollout.md`](rollout.md) for the release gate. The connector can run independently, while the
distributable [`Consentary Vault` plugin](../../plugins/consentary-vault/) bundles the shared remote
MCP connection and workflow guidance for broad installation. The same instruction source is used
for Claude, ChatGPT, and Codex; provider-specific copies are prohibited.
