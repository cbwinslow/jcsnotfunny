"""Small helper to run the OAuth installed app flow and print a refresh token.

This helper is meant to be run by the account owner locally:

    python scripts/integrations/get_youtube_token.py --client-secrets ./client_secret.json

It will open a browser, perform the consent flow, and print a shell-friendly line you can copy into Bitwarden or `gh secret set`.

This script is intentionally simple and does not attempt to log into Bitwarden or GitHub for you.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

HELPER_TEXT = """
After completing the flow, you will see a line like:

    REFRESH_TOKEN=ya29.a0AfH6SM...\n

Store it safely, for example with Bitwarden CLI (owner local):

  export BW_SESSION="$(bw login --raw)"
  echo -n "REFRESH_TOKEN_VALUE" | bw create item '{"type":1,"name":"YOUTUBE_REFRESH_TOKEN","notes":"REPLACE_ME"}' --session "$BW_SESSION"

Or use GitHub CLI to set a repository secret:

  echo -n "REFRESH_TOKEN_VALUE" | gh secret set YT_REFRESH_TOKEN -b -

"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Obtain a YouTube OAuth refresh token using an installed app flow.")
    parser.add_argument("--client-secrets", required=True, help="Path to Google client_secret.json file")
    parser.add_argument("--scopes", nargs="*", default=SCOPES, help="OAuth scopes (optional)")
    parser.add_argument("--print-bw-example", action="store_true", help="Print an example Bitwarden command to store the token")
    args = parser.parse_args(argv)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except Exception as e:  # pragma: no cover - import guard
        print("google-auth-oauthlib is required to run this helper.")
        print("Install with: pip install google-auth-oauthlib")
        print("If you cannot install it, run the OAuth flow manually following docs/SECRETS.md")
        return 2

    client_secrets_path = Path(args.client_secrets)
    if not client_secrets_path.exists():
        print(f"client secrets file not found: {client_secrets_path}")
        return 3

    print("Starting OAuth flow in your browser. If a browser does not open, follow the printed URL.")
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_path), args.scopes)
    creds = flow.run_local_server(port=0)

    refresh_token = getattr(creds, "refresh_token", None)
    if not refresh_token:
        print("No refresh token was returned. If you previously authorized the app, you may need to remove the authorization and try again (ensure access_type='offline').")
        return 4

    print("\nCopy this line into Bitwarden or your environment (DO NOT COMMIT):\n")
    print(f"REFRESH_TOKEN={refresh_token}\n")

    if args.print_bw_example:
        print(HELPER_TEXT)

    # if bw cli is available, show a suggestion (do not execute anything)
    if shutil.which("bw"):
        print("\nDetected Bitwarden CLI (bw) on PATH. Example to store the token (owner runs locally):")
        print("  export BW_SESSION=\"$(bw login --raw)\"")
        print("  echo -n \"REFRESH_TOKEN_VALUE\" | bw create item '{\"type\":1,\"name\":\"YOUTUBE_REFRESH_TOKEN\",\"notes\":\"REFRESH_TOKEN_HERE\"}' --session \"$BW_SESSION\"")

    # helpful GitHub CLI snippet if available
    if shutil.which("gh"):
        print("\nDetected GitHub CLI (gh) on PATH. To set a repo secret:")
        print("  echo -n \"REFRESH_TOKEN_VALUE\" | gh secret set YT_REFRESH_TOKEN -b -")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
