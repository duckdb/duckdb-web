#!/usr/bin/env bash
set -euo pipefail

if [ "${1-}" = "" ]
then
    echo >&2 "usage: $0 duckdb_dir"
    exit 1
fi

DUCKDB=$1;
echo "Generating docs using duckdb source in $DUCKDB"

python3 ./scripts/generate_config_docs.py $DUCKDB/build/debug/duckdb
# python3 ./scripts/generate_descriptions.py $DUCKDB
python3 ./scripts/generate_docs.py $DUCKDB
python3 ./scripts/generate_python_docs.py
node ./scripts/generate_nodejs_docs.js $DUCKDB

# generate search index last, once all the docs are generated
python3 ./scripts/generate_search.py
