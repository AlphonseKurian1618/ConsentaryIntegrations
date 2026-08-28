# Consentary integrations

Provider-specific integration assets for Consentary's OAuth-protected remote MCP service. This
repository owns connector setup, provider conformance, sanitized interoperability evidence, pilot
plans, and directory-submission material. It is deliberately separate from the backend and iOS
repositories so another provider can be added without coupling its lifecycle to the vault runtime.

## Ownership boundary

| Repository | Owns |
|---|---|
| `ConsentaryIntegrations` | Provider setup, compatibility contracts, test matrices, pilots, troubleshooting, and directory artifacts |
| `soffortmcp` | MCP tools, OAuth enforcement, phone-approval orchestration, public connector pages, and server-side validation |
| `AIVaultApp` | Local vault, phone consent UX, device authentication, and encrypted result delivery |

Provider files never contain credentials or create a second authorization path. The phone remains
the final authority for disclosure and writes.

## Providers

| Provider | Entry point | Status |
|---|---|---|
| Anthropic Claude | [`providers/claude/`](providers/claude/) | Production CIMD registration fixed; interactive connector acceptance pending |

## Validate

The checks use only the Python standard library:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```
