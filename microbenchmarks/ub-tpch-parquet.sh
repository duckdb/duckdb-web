#!/usr/bin/env bash

# Microbenchmark for the "Running TPC-H on a DuckDB Database vs. Parquet" section of the
# "File Formats" page: runs the 22 TPC-H queries on a DuckDB database and on Parquet files.
#
# Usage: WORK_DIR=/path/to/work SF=30 ./ub-tpch-parquet.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

SF="${SF:-30}"
TABLES="customer lineitem nation orders part partsupp region supplier"

cd "${WORK_DIR}"

DB="tpch-sf${SF}.db"
PARQUET_DIR="tpch-sf${SF}-parquet"

if [ ! -f "${DB}" ]; then
    echo "Generating ${DB}"
    ${DUCKDB} "${DB}" -c "CALL dbgen(sf = ${SF});" > /dev/null
fi

echo "Exporting to ${PARQUET_DIR} (using the default Parquet settings)"
rm -rf "${PARQUET_DIR}"
mkdir "${PARQUET_DIR}"
for T in ${TABLES}; do
    ${DUCKDB} "${DB}" -c "COPY ${T} TO '${PARQUET_DIR}/${T}.parquet';" > /dev/null
done

# The views over the Parquet files are created in an in-memory database
VIEWS=""
for T in ${TABLES}; do
    VIEWS="${VIEWS} CREATE VIEW ${T} AS FROM '${PARQUET_DIR}/${T}.parquet';"
done

# Prints the median of the query times reported by the CLI's timer
median_time() {
    grep '^Run Time' | awk '{print $5}' | sort -n | awk '{a[NR]=$1} END {print a[int((NR+1)/2)]}'
}

echo "query,duckdb,parquet" > tpch-parquet-results.csv
for Q in $(seq 1 22); do
    ARGS=(-c "SET enable_progress_bar = false;" -c ".timer on")
    for _ in $(seq 1 "${RUNS}"); do
        ARGS+=(-c "PRAGMA tpch(${Q});")
    done
    T_DUCKDB=$(${DUCKDB} -csv "${DB}" -readonly "${ARGS[@]}" 2>&1 | median_time)
    T_PARQUET=$(${DUCKDB} -csv -cmd "${VIEWS}" "${ARGS[@]}" 2>&1 | median_time)
    echo "${Q},${T_DUCKDB},${T_PARQUET}" | tee -a tpch-parquet-results.csv
done

${DUCKDB} -c "
    SELECT
        min(parquet / duckdb).round(2) AS min_slowdown,
        median(parquet / duckdb).round(2) AS median_slowdown,
        max(parquet / duckdb).round(2) AS max_slowdown,
        (sum(parquet) / sum(duckdb)).round(2) AS total_slowdown
    FROM 'tpch-parquet-results.csv';"
