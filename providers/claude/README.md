# Consentary for Claude

Consentary connects Claude to `https://consentary.com/mcp` and sends every value disclosure or
proposed vault change to your linked iPhone for approval.

The **full plugin** includes the remote MCP connection and Consentary's session-only
`vault-workflows` skill. A **connector-only** setup reaches the MCP server without the skill.

## Claude Code — one command

Install and sign in to a current version of Claude Code, then run:

```bash
claude plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations && claude plugin install consentary-vault@consentary-plugins
```

Restart Claude Code, run `/mcp`, select Consentary, and complete browser sign-in.

## Claude web or Desktop — no terminal

1. Open **Customize → Plugins**.
2. Under **Personal plugins**, select **+ → Add marketplace → Add from a repository**.
3. Enter `AlphonseKurian1618/ConsentaryIntegrations` or the full repository URL.
4. Install **Consentary Vault**.
5. Start a new chat and complete browser sign-in when prompted.

Plugin availability can depend on the Claude plan and workspace policy.

## Connector-only fallback

If Personal plugins are unavailable, open **Customize → Connectors → Add custom connector** and
enter `https://consentary.com/mcp`. Do not enter a client ID or secret. Complete browser sign-in,
start a new chat, and enable the Consentary tools.

This fallback does not install `vault-workflows`. Organization-managed Claude accounts may require
an Owner to add the connector first.

## Verify the connection

Confirm that Claude discovers:

- `list_available_properties`
- `list_templates`
- `request_properties`
- `add_properties`

The connection may request `mcp:access offline_access`; it must never request `mobile:access`.

Then try:

> Show what kinds of information are available in my Consentary vault. Do not request any values.

Metadata discovery does not reveal plaintext values. Every value request and proposed write still
requires the normal iPhone consent flow.

## Example prompts

- **Selective disclosure:** “Discover my available contact fields, then ask my phone to share only
  the email address I select for this application.”
- **Phone-approved change:** “Inspect Consentary's templates, then propose a fictional vehicle item
  for my phone to review.”

The full plugin instructs Claude not to retain data retrieved from Consentary or proposed for a
Consentary write beyond the current chat session. These instructions do not change Claude's
account-level conversation-retention settings.

## Troubleshooting

- **The plugin command is missing:** update Claude Code and restart it.
- **The marketplace is missing:** rerun the marketplace command, then restart Claude Code or Claude
  Desktop.
- **Linking fails before login:** record only the OAuth error code and sanitized URL parameters.
  Never paste a token or authorization code.
- **No notification appears:** open Consentary, verify notifications and phone linking, and make one
  new request. Do not repeatedly call the tool.
- **The request times out:** open and reconnect the iPhone, then start a new request. A force-quit
  iOS app is not background-launched by a notification.
- **A handle is stale:** run discovery again and use the newly returned opaque handle.
- **OAuth stops refreshing:** disconnect the connector and reconnect it; do not create a client
  secret.
- **Tools are missing on mobile:** finish linking on web or Desktop, open a new mobile conversation,
  and enable the connected tools.

The public user guide is also available at
[consentary.com/connectors/claude](https://consentary.com/connectors/claude).

## Maintainer notes

The distributable [`Consentary Vault` plugin](../../plugins/consentary-vault/) is the canonical
source for Claude, ChatGPT, Codex, VS Code, and compatible agents. Provider-specific copies are
prohibited. MCP metadata and server-side validation remain authoritative whether or not the host
loads the skill.

See [`oauth.md`](oauth.md) for the OAuth boundary, [`rollout.md`](rollout.md) for the release gate,
and [Anthropic's plugin installation guide](https://code.claude.com/docs/en/discover-plugins) for
current host instructions.
