# Provider layout

Each provider gets one directory containing only provider-specific material:

```text
providers/<provider>/
  README.md       setup, supported surfaces, and workflows
  oauth.md        provider OAuth behavior and sanitized compatibility evidence
  rollout.md      acceptance, pilot, and release gates
  pilot-matrix.csv
```

Provider-neutral tool expectations belong in `contracts/common/`; provider OAuth and packaging
expectations belong in `contracts/<provider>/`. Reusable plugin assets live in
`plugins/consentary-vault/` and must not be copied into a provider directory.

A provider integration must use the public MCP and OAuth contracts; it must not require backend
forks, provider-specific vault code, static secrets, token persistence, or an approval bypass.

The shared agent directory contract is `contracts/common/agent-catalog.json`. Known providers are
identified only by reviewed OAuth client IDs. Generic client labels come from Auth0's signed
registered-client claim and are never treated as verified brand identity.
