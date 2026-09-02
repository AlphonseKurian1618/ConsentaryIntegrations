# Consentary for ChatGPT and Codex

Consentary connects ChatGPT and Codex to the same OAuth-protected remote MCP endpoint:
`https://consentary.com/mcp`.

The **full plugin** includes the MCP connection and Consentary's session-only `vault-workflows`
skill. A **connector-only** setup reaches the same protected MCP server but does not install the
skill.

## ChatGPT Desktop — full plugin

Install [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) if needed, then add the Consentary
marketplace:

```bash
codex plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations
```

Restart ChatGPT Desktop, open **Plugins**, select **Consentary Plugins** under your personal
marketplaces, and install **Consentary Vault**. Start a new chat after installation and complete
browser sign-in when prompted.

## ChatGPT web — connector-only fallback

The repository plugin is not currently listed in ChatGPT's public plugin directory. To add only the
remote connection:

1. Open **Settings → Security and login** and enable **Developer mode**.
2. Open [ChatGPT Plugins](https://chatgpt.com/plugins) and select the plus button.
3. Name the connection **Consentary**, choose a public remote MCP connection, and enter
   `https://consentary.com/mcp`.
4. Review the discovered tools and complete browser sign-in.
5. Start a new chat and add Consentary from the tools menu.

This path does not install `vault-workflows`. Phone consent and server-side validation still apply.

## Codex CLI — full plugin

Install the marketplace and plugin with one command:

```bash
codex plugin marketplace add AlphonseKurian1618/ConsentaryIntegrations && codex plugin add consentary-vault@consentary-plugins
```

Start a new Codex session after installation and complete browser sign-in when prompted.

## Verify the connection

Confirm that the client discovers:

- `list_available_properties`
- `list_templates`
- `request_properties`
- `add_properties`

Do not enter a client secret or paste an access token, authorization header, or private key. The
client must discover OAuth from the endpoint and open Consentary's browser sign-in flow. It may
request `mcp:access offline_access`; it must never request `mobile:access`.

## Example prompts

- **Metadata only:** “Show what kinds of information are available in my Consentary vault. Do not
  request values.”
- **Selective disclosure:** “Discover my available contact fields, then ask my phone to share only
  the email address I select.”
- **Phone-approved change:** “Inspect Consentary templates, then propose saving a fictional vehicle
  for review on my phone.”

Every value request and proposed write returns to the linked iPhone for approval. The full plugin
also instructs the agent not to retain retrieved or write-bound data beyond the current chat
session. These instructions do not change the provider's account-level conversation-retention
settings.

## Troubleshooting

- **Consentary is not in Plugins:** confirm the marketplace command succeeded, restart ChatGPT
  Desktop, and look under the personal **Consentary Plugins** source.
- **Developer mode is unavailable:** account or workspace policy may block custom connections; ask
  the workspace administrator.
- **The tools are missing:** start a new chat and enable Consentary in the tools menu.
- **OAuth fails:** disconnect Consentary and reconnect it. Do not create a client secret.
- **No phone notification appears:** open Consentary, confirm the iPhone is online and linked, check
  notifications, and make one new request.

## Maintainer notes

The universal package at
[`../../plugins/consentary-vault/`](../../plugins/consentary-vault/) is the canonical source for the
OpenAI/Codex manifest, registered app mapping, MCP configuration, and workflow skill. Do not fork or
copy those files here.

Production registration was completed on 2026-08-28 using ChatGPT's per-plugin CIMD client, PKCE
S256, `mcp:access offline_access`, and no shared client secret. The real production connection ID is
stored in the shared plugin's `.app.json`. Interactive acceptance remains tracked in
[`rollout.md`](rollout.md).

See [`oauth.md`](oauth.md) for the OAuth boundary and the
[official OpenAI plugin guide](https://learn.chatgpt.com/docs/plugins) for current host behavior.
