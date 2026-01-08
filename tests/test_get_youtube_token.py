import subprocess
import sys


def test_helper_shows_help():
    # Running with --help should exit 0 and show usage
    proc = subprocess.run([sys.executable, "scripts/integrations/get_youtube_token.py", "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "Obtain a YouTube OAuth refresh token" in proc.stdout


def test_missing_google_libs_shows_instructions():
    # Simulate environment without google libraries by running the module
    # and expecting a non-zero exit code and an install hint
    proc = subprocess.run([sys.executable, "scripts/integrations/get_youtube_token.py", "--client-secrets", "./nonexistent.json"], capture_output=True, text=True)
    # If google-auth-oauthlib is not installed, the helper prints an install message or a file-not-found message
    assert proc.returncode in (2, 3)
    assert ("google-auth-oauthlib" in proc.stdout) or ("client secrets file not found" in proc.stdout)
