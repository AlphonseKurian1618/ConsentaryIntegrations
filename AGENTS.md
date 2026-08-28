# Repository rules

This repository contains provider-specific integration documentation, conformance contracts, and
sanitized test evidence. It does not implement the Consentary MCP server or iPhone app.

- Use fictional vault data in every test and pilot.
- Never commit credentials, OAuth tokens, refresh tokens, OTPs, provider subjects, relay email
  addresses, APNs tokens, review-account passwords, or screenshots containing private data.
- Never add an authentication bypass, fixed OTP, static provider client secret, or alternative path
  around phone consent.
- Treat MCP tool metadata and server-side validation as the operating contract. Provider guidance
  may explain that contract but may not weaken it.
- Keep provider-specific material under `providers/<provider>/` and `contracts/<provider>/`.
- Put cross-provider tool contracts under `contracts/common/` and reusable plugin assets under
  `plugins/`. Provider packages must reference those shared sources instead of copying prompts,
  MCP configuration, or tool metadata.
