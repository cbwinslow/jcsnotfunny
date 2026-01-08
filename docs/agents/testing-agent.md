# Troubleshooting and Testing Agent

## Overview
Runs validation checks, diagnostics, and targeted test suites to isolate issues.

## Capabilities
- Config validation (JSON/TOML)
- Credential audit (offline or live)
- System diagnostics snapshot (disk, network, streams)
- Log scanning for errors/warnings
- Optional pytest execution

## CLI Usage
```bash
python -m scripts.cli troubleshooting --config config.json --config config.toml
python -m scripts.cli troubleshooting --run-pytest --pytest-args tests/test_diagnostics.py
python -m scripts.cli troubleshooting --credential-mode live --diagnostics-live
```

## Notes
- Live checks require network access and valid credentials.
- Use `--run-pytest` sparingly on production systems.
