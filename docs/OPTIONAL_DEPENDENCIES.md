# Optional Dependencies for Advanced Tooling

Some tools in this repository have optional dependencies that enable real, high-quality behavior. These are optional so CI and dev environments can remain lightweight.

Recommended optional packages:
- yt-dlp (video downloads via Python API or binary)
  - Install: `pip install yt-dlp`
- whisperx (high-quality transcription pipeline)
  - Install: `pip install whisperx`
- Pillow (thumbnail image rendering)
  - Install: `pip install pillow`

Install all recommended optional dependencies:

```bash
pip install yt-dlp whisperx pillow
```

Notes
- The tool functions check for the presence of these packages and gracefully fall back to placeholders when they are not available.
- If you want to run full integration tests that use these packages, install them in your virtualenv.

Integration matrix & CI
- The repository includes a nightly GitHub Actions workflow "Integration Matrix" that attempts to install optional deps and runs the full test suite across multiple Python versions.
- If the integration workflow detects validation errors or failing tests, it will fail the job and surface the logs.
- You can trigger the integration workflow manually via the GitHub Actions UI (workflow: "Integration Matrix").
