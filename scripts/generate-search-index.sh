#!/usr/bin/env bash

set -euo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

duckdb-web-venv/bin/python scripts/generate_search.py
