#!/usr/bin/env bash

set -Eeuo pipefail

rm -rf ldbc.duckdb*
python3 ub-string-joins-1.py
du -hd0 ldbc.duckdb

rm -rf ldbc.duckdb*
python3 ub-string-joins-2.py
du -hd0 ldbc.duckdb

rm -rf ldbc.duckdb*
python3 ub-string-joins-3.py
du -hd0 ldbc.duckdb
