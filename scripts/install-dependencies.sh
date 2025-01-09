#!/usr/bin/env bash

set -euo pipefail

# navigate to the repository root
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )/.."

python3 -m venv duckdb-web-venv
duckdb-web-venv/bin/pip install -r requirements.txt
