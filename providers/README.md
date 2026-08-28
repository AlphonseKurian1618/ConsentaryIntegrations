# Provider layout

Each provider gets one directory containing only provider-specific material:

```text
providers/<provider>/
  README.md       setup, supported surfaces, and workflows
  oauth.md        provider OAuth behavior and sanitized compatibility evidence
  rollout.md      acceptance, pilot, and release gates
  pilot-matrix.csv
```

Machine-readable expectations belong in `contracts/<provider>/`. A provider integration must use
the public MCP and OAuth contracts; it must not require backend forks, provider-specific vault code,
static secrets, token persistence, or an approval bypass.

