#!/usr/bin/env bash

set -Eeuo pipefail

echo Checking whether the benchmark kit and the tools are installed
which hyperfine
which duckdb
which grep
which pcregrep

wget https://blobs.duckdb.org/nl-railway/services-2023.csv.gz
gunzip -k services-2023.csv.gz

# DuckDB with csv.gz
DUCKDB_COMMAND1=$(
cat << 'EOF'
  duckdb -c "SELECT count(*) FROM 'services-2023.csv.gz' WHERE \"Service:Type\" = 'Intercity';"
EOF
)
hyperfine "$DUCKDB_COMMAND1"

# pcregrep with csv.gz
hyperfine "gzcat services-2023.csv.gz | pcregrep '^[^,]*,[^,]*,Intercity,' | wc -l"

# grep with csv.gz
hyperfine "gzcat services-2023.csv.gz | grep '^[^,]*,[^,]*,Intercity,' | wc -l"

# DuckDB with csv
DUCKDB_COMMAND2=$(
cat << 'EOF'
  duckdb -c "SELECT count(*) FROM 'services-2023.csv' WHERE \"Service:Type\" = 'Intercity';"
EOF
)
hyperfine "$DUCKDB_COMMAND2"

# pcregrep with csv
hyperfine "pcregrep '^[^,]*,[^,]*,Intercity,' services-2023.csv | wc -l"

# grep with csv
hyperfine "grep '^[^,]*,[^,]*,Intercity,' services-2023.csv | wc -l"
