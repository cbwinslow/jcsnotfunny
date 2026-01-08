# Secrets & Credentials (how to provide access securely)

This document explains secure options for granting access to platform APIs (YouTube, X/Twitter, etc.) without sharing passwords and how to store credentials safely using Bitwarden or GitHub Secrets.

## Key recommendations ✅

- Prefer **invites or direct account roles** (e.g., YouTube Studio Permissions) when possible — no password sharing.
- For programmatic access, use **OAuth** flows and store the resulting tokens in a secrets manager (Bitwarden, GitHub Actions secrets, cloud secret manager).
- Use **least privilege**: request only the scopes you need and rotate credentials regularly.
- Do **not** commit any credentials to the repo. Add `.env` and any `client_secret.json` to `.gitignore`.

---

## Bitwarden (recommended)

- Create an organization and a collection (e.g. `jareds-not-funny`).
- Add items for each credential, e.g. `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, `X_API_KEY`, etc.
- Use the Bitwarden UI or the CLI (`bw`) to grant access, audit logs, and rotate keys.
- Use Bitwarden Send for one-time transfers or collection shares for ongoing use.

Example Bitwarden CLI commands (owner runs locally):

```bash
# login and export session (do NOT commit the session value)
bw login you@example.com
export BW_SESSION="$(bw login --raw)"

# add an item (example storing refresh token as secure note)
bw create item '{"type":1,"name":"YOUTUBE_REFRESH_TOKEN","notes":"REFRESH_TOKEN_HERE"}' --session "$BW_SESSION"

# or edit an existing item
bw edit item <ITEM_ID> --session "$BW_SESSION"
```

> Tip: Enable 2FA and require 2FA for org access.

---

## OAuth helper (scripts/integrations/get_youtube_token.py)

We provide a small helper that the owner runs locally to perform the OAuth consent flow and print the `REFRESH_TOKEN` value. The owner should then store that token in Bitwarden or a GitHub Secret.

Usage (owner runs locally):

```bash
python scripts/integrations/get_youtube_token.py --client-secrets ./client_secret.json
```

The helper prints a command-line snippet you can copy to store the token in Bitwarden or as a GitHub secret.

---

## GitHub Actions secrets

Add secrets to the repository settings for CI use (Settings → Secrets → Actions):

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`
- `GITHUB_TOKEN` (already provided by GitHub Actions, but consider a dedicated token for operations)

When possible, prefer short-lived tokens and OIDC where supported.

### Quick: set a GitHub Action secret with `gh`

If you have the GitHub CLI configured and want to set a repository secret from a local value:

```bash
# from a local environment variable
echo -n "$YOUTUBE_REFRESH_TOKEN" | gh secret set YT_REFRESH_TOKEN -b -

# or from a file
cat ./refresh_token.txt | gh secret set YT_REFRESH_TOKEN -b -
```

Be sure to limit the token scope and rotate it periodically.

---

## Minimal policies

- Rotate keys every 90 days or after a personnel change.
- Revoke unused tokens immediately.
- Keep a record of where each token is used and which systems are allowed to access it.

---

## Troubleshooting notes

- If the owner cannot run the helper, they can still provide the token directly via Bitwarden Send.
- If using a service account or cloud-based approach, follow the cloud provider's best practices for key rotation and access control.

---

## Next actions for this repo

- Add a `.env.example` (done) and a short local-run instructions snippet in this repo's README.
- Add CI checks that prevent committing `.env` or `client_secret.json`.
