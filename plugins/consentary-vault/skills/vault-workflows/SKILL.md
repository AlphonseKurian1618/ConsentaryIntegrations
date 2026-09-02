---
name: vault-workflows
description: Use Consentary vault tools safely for metadata discovery, phone-approved selective disclosure, phone-approved vault changes, and session-only handling of retrieved and write-bound data. Apply in VS Code and other skills-compatible agents whenever a task reads from or writes to Consentary, including when the user does not invoke this skill explicitly.
---

# Consentary vault workflows

Consentary is the authority for vault data. The user's linked phone is the final authority for every
disclosure and change. Server-side validation remains mandatory.

## Client compatibility

Use the MCP tools exposed by the `consentary` server. A client may prefix or namespace the tool
names, but the final tool-name segment and workflow are the same. If the Consentary tools are not
available, stop and tell the user to install or enable the Consentary plugin/MCP connection and
complete OAuth. This skill does not contain credentials, perform OAuth, or provide a second path to
the vault.

## Session-only data handling

Treat all Consentary-handled information as ephemeral and confidential:

- **Retrieved information** includes every value or piece of data returned by Consentary, including
  plaintext values, property handles, item identifiers, field metadata, approval results, and tool
  responses.
- **Write-bound information** includes every value supplied, inferred, drafted, transformed, or
  proposed for writing to Consentary, whether the write is awaiting review, approved, denied, or
  cancelled.

- Use Consentary-handled information only in the current chat session and only to complete the
  user's immediate request. Never retain it beyond the current chat session.
- Do not store or copy Consentary-handled information into files, project content, assistant memory,
  plugin data, notes, logs, caches, environment variables, shell history, clipboards, databases,
  external services, messages outside this chat, tickets, telemetry, training examples, tests, or
  fixtures.
- Do not invoke any tool whose purpose or effect is to persist, upload, transmit, or relay
  Consentary-handled information, except the Consentary tool calls required for the user's current
  phone-approved workflow.
- Do not include Consentary-handled information in summaries intended for later conversations or
  handoffs.
- Keep plaintext out of the response unless the user's current request requires the specifically
  approved value. Reveal the minimum approved data needed and do not repeat it unnecessarily.
- For a write, the only permitted persistence is the copy stored by Consentary through the normal
  `add_properties` workflow after phone approval. Do not keep a separate copy before or after the
  write, and do not treat a denied or cancelled proposal as permission to retain it.
- If the user asks to save, remember, export, log, upload, or send Consentary-handled information
  outside the current chat session, refuse that persistence step and explain that this plugin
  requires session-only handling.
- When the request is complete, do not take any action to retain Consentary-handled information or
  make it available to a later chat session.

These instructions constrain actions taken by the assistant and this plugin. They do not change the
hosting product's account-level conversation retention policy; users must configure that policy
separately where applicable.

## Required workflow

1. Use `list_available_properties` before requesting or updating existing vault properties.
2. Use `list_templates` before creating an item or field.
3. Copy opaque handles and returned metadata exactly. Never invent or infer them.
4. Submit only the minimum disclosure or change the user requested.
5. Wait for the phone decision. Never poll, retry repeatedly, or attempt to bypass phone consent.
6. Treat partial approval as approval only for the fields explicitly returned as approved.
7. Refresh discovery after a successful write before using vault state again.

Never request `mobile:access`, introduce credentials or static secrets, weaken server validation,
or create an alternative authorization path. If a safe workflow cannot proceed, stop and explain
what the user must resolve on the phone or in the Consentary connection.
