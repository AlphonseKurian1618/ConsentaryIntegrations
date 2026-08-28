/**
 * Copy Auth0's registered application name into a signed display-only access-token claim.
 * Authorization remains entirely server-side; this claim must never select scopes or grant access.
 */
exports.onExecutePostLogin = async (event, api) => {
  const rawName = event.client && event.client.name;
  if (typeof rawName !== "string") {
    return;
  }

  const displayName = rawName.trim().replace(/\s+/g, " ").slice(0, 80);
  if (displayName) {
    api.accessToken.setCustomClaim(
      "https://consentary.com/client_name",
      displayName,
    );
  }
};

