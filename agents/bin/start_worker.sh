#!/usr/bin/env bash
set -euo pipefail

# Quick start script for local worker (dev mode)
# Requires: python 3.11, virtualenv, env vars set (see docs/24-7-worker.md)

python -m agents.worker --run-once
# For continuous mode: python -m agents.worker
