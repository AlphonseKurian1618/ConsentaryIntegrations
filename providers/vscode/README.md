# Consentary for Visual Studio Code

The Consentary Agent Plugin gives GitHub Copilot in Visual Studio Code the remote MCP connection and
the session-only `vault-workflows` skill in one package.

## Install with GitHub Copilot CLI

Install and sign in to [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli),
then run one command:

```bash
copilot plugin install AlphonseKurian1618/ConsentaryIntegrations:plugins/consentary-vault
```

Reload Visual Studio Code. It automatically discovers plugins installed by Copilot CLI.

## Install without a terminal

1. Open the Command Palette.
2. Run **Chat: Install Plugin From Source**.
3. Enter `https://github.com/AlphonseKurian1618/ConsentaryIntegrations`.
4. Select `consentary-vault` and approve the source when prompted.
5. Reload Visual Studio Code.

## Finish connecting

1. Complete browser sign-in when the Consentary MCP server starts.
2. Run **Chat: Configure Skills** and confirm `vault-workflows` is enabled.
3. Run **MCP: List Servers** and confirm `consentary` is running.
4. Open Consentary on the linked iPhone and verify **Visual Studio Code** appears under
   **Connected**.

Never paste a client secret, access token, authorization header, or private key. Visual Studio Code
must discover OAuth from `https://consentary.com/mcp` and open the sign-in flow.

## MCP-only fallback

If the installed Visual Studio Code version does not support Agent Plugins, add only the remote MCP
server:

```bash
code --add-mcp '{"name":"consentary","type":"http","url":"https://consentary.com/mcp"}'
```

This fallback does not install the `vault-workflows` skill. If Agent Skills are supported, install
[`../../plugins/consentary-vault/skills/vault-workflows/`](../../plugins/consentary-vault/skills/vault-workflows/)
in the client's documented skills directory.

Every value request and proposed write still requires normal iPhone consent, including with the
connector-only fallback.

## Troubleshooting

- **`copilot plugin` is unavailable:** update Copilot CLI and confirm it is signed in.
- **The plugin is installed but missing in Visual Studio Code:** reload the window and confirm
  `chat.plugins.enabled` is enabled.
- **The skill is missing:** run **Chat: Configure Skills** and enable `vault-workflows`.
- **The MCP server is stopped:** run **MCP: List Servers**, select `consentary`, and restart it.
- **OAuth fails:** disconnect Consentary and reconnect it. Do not create a client secret.
- **A managed workspace blocks installation:** ask the administrator to allow the plugin source and
  the Consentary MCP endpoint.

## Maintainer notes

Visual Studio Code is a known Consentary agent identified by its registered Auth0 OAuth client ID.
It connects through `https://consentary.com/mcp`, requests `mcp:access offline_access`, and uses PKCE
S256. No client secret, copied token, local proxy, or alternate mobile scope is part of setup.

The portable package at
[`../../plugins/consentary-vault/`](../../plugins/consentary-vault/) is the canonical source. Do not
copy the skill or MCP configuration into this provider directory.

See the [Visual Studio Code Agent Plugins guide](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
and [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
for current host behavior.
