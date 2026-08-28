# Consentary for ChatGPT and Codex

Consentary is exposed through the same OAuth-protected remote MCP endpoint used by every provider:
`https://consentary.com/mcp`. The universal package at
[`../../plugins/consentary-vault/`](../../plugins/consentary-vault/) owns the shared MCP
configuration and workflow skill. Do not fork or copy those files for ChatGPT.

## ChatGPT development setup

1. In ChatGPT, enable Developer mode and register `https://consentary.com/mcp` as a remote MCP
   connection.
2. Complete Authorization Code authentication with PKCE S256. Request only `mcp:access` and
   `offline_access`; never request `mobile:access` and never provide a client secret.
3. Copy the generated technical connection ID, which must start with `plugin_asdk_app_`.
4. Add `plugins/consentary-vault/.app.json` containing that real ID and add
   `"apps": "./.app.json"` to the Codex plugin manifest. Never invent a placeholder ID.
5. Validate the package, then install it from the repository marketplace in a fresh ChatGPT/Codex
   conversation.

Production registration completed on 2026-08-28 using ChatGPT's per-plugin CIMD client, PKCE S256,
`mcp:access offline_access`, and no shared client secret. The real production connection ID is
stored in the shared plugin's `.app.json`. Interactive authorization, tool discovery, refresh,
disconnect/reconnect, and the acceptance matrix remain pending.

## Example prompts

- **Metadata only:** “Show what kinds of information are available in my Consentary vault. Do not
  request values.”
- **Selective disclosure:** “Discover my available contact fields, then ask my phone to share only
  the email address I select.”
- **Phone-approved change:** “Inspect Consentary templates, then propose saving a fictional vehicle
  for review on my phone.”

The MCP server descriptions are sufficient for safe connector operation. The shared skill repeats
the workflow and session-only privacy rules for packaged distribution, but server-side validation
and phone consent remain mandatory whether or not a host invokes the skill.

See [`oauth.md`](oauth.md) for the OAuth boundary and [`rollout.md`](rollout.md) for acceptance.
