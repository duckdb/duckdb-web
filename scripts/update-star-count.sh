#!/usr/bin/env bash

set -euo pipefail

STAR_COUNT=$(gh api repos/duckdb/duckdb | jq ".stargazers_count")
STAR_COUNT_FORMATTED=$(python3 -c 'import sys; import math; print(f"{math.floor(int(sys.argv[1]) / 100 + 0.5) / 10:.1f}k", end="")' ${STAR_COUNT})
sed -i "s/^star_count:.*/star_count: '${STAR_COUNT_FORMATTED}'/" _config.yml
