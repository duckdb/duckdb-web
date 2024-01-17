#!/usr/bin/env bash

set -Eeuo pipefail

echo "type,iteration,duration" > results.csv

rm -rf ldbc.duckdb*
python3 ub-join-type-1.py
du -hd0 ldbc.duckdb

rm -rf ldbc.duckdb*
python3 ub-join-type-2.py
du -hd0 ldbc.duckdb

rm -rf ldbc.duckdb*
python3 ub-join-type-3.py
du -hd0 ldbc.duckdb

python3 ub-join-type-analyze.py
