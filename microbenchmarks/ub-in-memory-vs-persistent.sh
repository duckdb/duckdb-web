#!/usr/bin/env bash

# Microbenchmark for the "Persistent vs. In-Memory Tables" section of the
# "How to Tune Workloads" page: TPC-H Q1 on SF30 in three database setups.
#
# Usage: WORK_DIR=/path/to/work SF=30 ./ub-in-memory-vs-persistent.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

SF="${SF:-30}"

cd "${WORK_DIR}"

# Generate the data once, run Q1 several times, and report the median of the reported query times.
run_q1() {
    local label="$1"
    shift
    local args=(-c "SET enable_progress_bar = false;")
    if [ "${GENERATE}" == "true" ]; then
        args+=(-c "CALL dbgen(sf = ${SF});")
    fi
    # In-memory databases are only compressed when they are checkpointed
    if [ "${CHECKPOINT:-false}" == "true" ]; then
        args+=(-c "CHECKPOINT;")
    fi
    args+=(-c ".timer on")
    for _ in $(seq 1 "${RUNS}"); do
        args+=(-c "PRAGMA tpch(1);")
    done
    printf "%s: " "${label}"
    "$@" "${args[@]}" 2>&1 \
        | grep '^Run Time' \
        | awk '{print $5}' \
        | sort -n \
        | awk '{a[NR]=$1} END {print a[int((NR+1)/2)] " s (median of " NR " runs)"}'
}

GENERATE=true  run_q1 "In-memory DB (uncompressed)" ${DUCKDB} -csv
GENERATE=true CHECKPOINT=true run_q1 "In-memory DB (compressed)" ${DUCKDB} -csv -cmd "ATTACH ':memory:' AS db (COMPRESS); USE db;"

rm -f tpch-sf${SF}.db tpch-sf${SF}.db.wal
${DUCKDB} tpch-sf${SF}.db -c "CALL dbgen(sf = ${SF});" > /dev/null
GENERATE=false run_q1 "Persistent DB (compressed)"  ${DUCKDB} -csv tpch-sf${SF}.db
