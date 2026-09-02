# ChatGPT and Codex rollout

## Package gate

Register the test endpoint `https://test.consentary.com/mcp` in ChatGPT Developer mode, obtain its
real `plugin_asdk_app_...` connection ID, and build `.app.json` from that value. Validate both the
universal plugin and repository marketplace before testing. The production package must use the
production connection registration and must never embed tokens, credentials, client secrets, or a
test connection ID.

## Acceptance matrix

Exercise all four tools in ChatGPT and Codex with fictional vault data. Cover metadata-only
discovery, template discovery, full and partial disclosure approval, denial, create, update,
offline and locked phones, timeout, stale handles, background execution, and force-quit behavior.
Include adversarial prompts that encourage the assistant to guess handles, skip discovery, create
without templates, poll repeatedly, treat partial approval as full approval, or bypass the phone.

The gate passes only when:

- Authorization Code plus PKCE S256 succeeds without a client secret;
- the access token has `mcp:access`, never `mobile:access`, and refreshes through `offline_access`;
- the phone displays the signed registered name **ChatGPT**, without using it for authorization;
- direct connector workflows succeed without depending on the shared skill;
- packaged workflows follow the shared skill and never persist data retrieved from Consentary or
  proposed for writing to Consentary beyond the current chat session; and
- plaintext appears only in explicitly approved structured results, never summaries, receipts,
  logs, telemetry, plugin files, tests, or pilot evidence.

Record sanitized results in `pilot-matrix.csv`. Any plaintext leak, approval bypass, scope
broadening, unsafe write, data loss, or high-severity OAuth/interoperability defect blocks rollout.
Server-side validation and phone consent remain mandatory regardless of plugin behavior.
