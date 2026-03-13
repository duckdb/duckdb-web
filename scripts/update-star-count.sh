#!/usr/bin/env bash

set -euo pipefail

STAR_COUNT=$(gh api repos/duckdb/duckdb | jq ".stargazers_count")
STAR_COUNT_FORMATTED=$(python3 -c 'import sys; print(f"{int(sys.argv[1]) / 1000:.1f}k", end="")' ${STAR_COUNT})
sed -i "s/^star_count:.*/star_count: '${STAR_COUNT_FORMATTED}'/" _config.yml
