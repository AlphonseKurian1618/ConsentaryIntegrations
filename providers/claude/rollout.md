# Claude connector rollout

Consentary integrates with Claude as an OAuth-protected remote MCP connector. Version 1 uses the
existing Streamable HTTP endpoint and four-tool contract. MCP metadata is the operating contract;
the connector must pass every acceptance scenario without relying on a companion plugin,
Anthropic SDK or API key, static Claude OAuth client, client secret, token persistence, or
Claude-specific iOS code.

## Test environment gate

Add `https://test.consentary.com/mcp` as a Claude custom connector in Claude.ai and Claude Desktop.
Allow Claude to register through its Client ID Metadata Document and complete Authorization Code
with PKCE S256. Verify the issued access token has the Consentary audience, `mcp:access`, no
`mobile:access`, and the signed display-only client-name claim `Claude`. Verify `offline_access`
refresh after the 15-minute access-token lifetime, then disconnect and reconnect. Never save or
paste a token.

Exercise all four tools from Claude.ai and Desktop, then use the already connected service from
Claude mobile. Cover metadata-only discovery, full and partial disclosure approval, denial, create,
update, offline and locked phones, timeout, stale handles, background execution, and the expected
timeout after the user force-quits the iOS app. Include prompts that tell Claude to guess handles,
skip discovery, update without fresh discovery, create without templates, repeatedly poll, treat a
partial approval as full approval, or bypass the phone. Safe behavior is correct sequencing or a
server rejection. Plaintext may appear only in explicitly approved structured disclosure results.

Record sanitized evidence in `pilot-matrix.csv`: backend digest, client/platform version, prompt ID,
expected and actual tool sequence, result status, and correction flag. Do not record vault data,
tokens, OTPs, provider subjects, relay emails, APNs tokens, or private screenshots.

## Production pilot

Promote the exact tested digest through the protected test-to-production pipeline. Enroll five
people for seven consecutive days. Collectively cover Claude.ai, Claude Desktop, and Claude mobile;
every tester uses fictional vault data and the normal phone-consent path.

The pilot passes only when:

- OAuth refresh, disconnect, and reconnect succeed;
- discovery, templates, full and partial disclosure, denial, create, and update succeed;
- offline, locked, timeout, stale-handle, background, and force-quit behavior match the contract;
- no unresolved security, privacy, data-loss, or high-severity interoperability defect remains;
- the complete scripted connector-only matrix succeeds; and
- no more than 10% of scripted workflows require correction for wrong tool order, invented handles,
  or partial-approval interpretation.

Any plaintext leak, approval bypass, scope broadening, unsafe write, data loss, or high-severity
OAuth/interoperability defect blocks the pilot. Roll back through the existing digest-only process.

Validate the companion [`Consentary Vault` plugin](../../plugins/consentary-vault/) separately from the connector-only
matrix. The plugin may bundle the public remote MCP configuration and instruction-only workflow
guidance, but it must contain no credentials, custom authorization logic, token handling, or
alternative path around phone consent. It must instruct Claude not to persist any data retrieved
from Consentary or proposed for writing to Consentary beyond the current chat session. Consentary
itself is the only permitted storage destination for a phone-approved write; Claude must not keep a
separate copy. Server-side validation remains mandatory.

## Anthropic directory package

After the pilot passes, prepare:

- Consentary branding, concise description, and endpoint `https://consentary.com/mcp`;
- setup, privacy, and support URLs on `consentary.com`;
- the three verified prompts in [`README.md`](README.md);
- a captured `tools/list` matching the shared [`../../contracts/common/tool-catalog.json`](../../contracts/common/tool-catalog.json);
- Streamable HTTP, RFC 9728, Auth0 CIMD, PKCE, refresh, disconnect, and reconnect evidence; and
- the sanitized seven-day pilot matrix and confirmation that the connector passed without relying
  on the plugin.

Use a dedicated Auth0 review account and an operator-held iPhone containing fictional data. Share
access privately through Anthropic's review channel and rotate or revoke it afterward. Never commit
review credentials, fixed OTPs, authentication bypasses, tokens, or sample personal data.

Submit the connector independently. Publish the plugin as a separate artifact; connector
installation and safe operation must never depend on it.
