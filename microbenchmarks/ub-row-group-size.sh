#!/usr/bin/env bash

# Microbenchmark for the "The Effect of Row Group Sizes" section of the "File Formats" page:
# runs an aggregation query on Parquet files written with different row group sizes.
#
# Input: the LDBC Comment table, e.g., https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst
# extracted to ${DATA_DIR}/ldbc-sf${SF}-comments/
# The Parquet files are written directly from the CSV files to avoid storing an intermediate database.
#
# Usage: SF=300 DATA_DIR=/path/to/data WORK_DIR=/path/to/work ./ub-row-group-size.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

SF="${SF:-300}"
INPUT="${DATA_DIR}/ldbc-sf${SF}-comments/part-*.csv.gz"
# The Parquet writer rounds the row group size up to a multiple of 2,048 (the vector size)
ROW_GROUP_SIZES="${ROW_GROUP_SIZES:-2048 4096 8192 16384 30720 61440 122880 245760 491520 983040 1966080}"
PARQUET_FILE="comment.parquet"
QUERY="SELECT avg(extract('day' FROM creationDate)) FROM '${PARQUET_FILE}';"

cd "${WORK_DIR}"

echo "row_group_size,num_row_groups,iteration,time" > row-group-size-comparison.csv
for ROW_GROUP_SIZE in ${ROW_GROUP_SIZES}; do
    rm -f "${PARQUET_FILE}"
    ${DUCKDB} -c "
        SET enable_progress_bar = false;
        SET preserve_insertion_order = false;
        COPY (FROM read_csv('${INPUT}', delim = '|', header = true))
            TO '${PARQUET_FILE}' (FORMAT parquet, ROW_GROUP_SIZE ${ROW_GROUP_SIZE});" > /dev/null

    NUM_ROW_GROUPS=$(${DUCKDB} -batch -noheader -csv -c "SELECT num_row_groups FROM parquet_file_metadata('${PARQUET_FILE}');")
    printf "Row group size %s (%s row groups): " "${ROW_GROUP_SIZE}" "${NUM_ROW_GROUPS}"

    # Each query runs in a new process, so the Parquet metadata is read from scratch every time
    for I in $(seq 1 "${RUNS}"); do
        TIME=$(timed ${DUCKDB} -c "SET enable_progress_bar = false;" -c "${QUERY}")
        echo "${ROW_GROUP_SIZE},${NUM_ROW_GROUPS},${I},${TIME}" >> row-group-size-comparison.csv
        printf "%s s " "${TIME}"
    done
    echo
done
rm -f "${PARQUET_FILE}"

${DUCKDB} -f "${SCRIPT_DIR}/process-row-group-size-results.sql"
