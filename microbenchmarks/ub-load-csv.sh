#!/usr/bin/env bash

# Microbenchmark for the "Loading CSV Files" section of the "File Formats" page:
# loading compressed (.csv.gz) vs. decompressing and loading uncompressed (.csv) files.
#
# Input: the LDBC Comment table, e.g., https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst
# extracted to ${DATA_DIR}/ldbc-sf${SF}-comments/
# The decompressed files are written to ${WORK_DIR}, which needs approx. 3× the space of the compressed files.
#
# Usage: SF=100 DATA_DIR=/path/to/data WORK_DIR=/path/to/work ./ub-load-csv.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

SF="${SF:-100}"
INPUT_DIR="${DATA_DIR}/ldbc-sf${SF}-comments"
DECOMPRESSED_DIR="${WORK_DIR}/ldbc-sf${SF}-comments-decompressed"
DB="ldbc_comment_csv_test.db"

cd "${WORK_DIR}"

echo "Load the table from compressed files (.csv.gz)"
rm -f "${DB}" "${DB}.wal"
${DUCKDB} "${DB}" -c ".read ${SCRIPT_DIR}/schema-without-pk.sql"
LOAD_COMPRESSED=$(timed ${DUCKDB} "${DB}" -c "COPY Comment FROM '${INPUT_DIR}/part-*.csv.gz' (HEADER true, DELIMITER '|');")
${DUCKDB} "${DB}" -c "SELECT count(*) AS numComment FROM Comment;"

echo "Decompress the files in parallel (one gzip process per CPU thread)"
rm -rf "${DECOMPRESSED_DIR}"
mkdir "${DECOMPRESSED_DIR}"
NUM_THREADS=$(${DUCKDB} -batch -noheader -csv -c "SELECT current_setting('threads');")
export DECOMPRESSED_DIR
DECOMPRESS=$(timed bash -c "ls '${INPUT_DIR}'/part-*.csv.gz | xargs -P ${NUM_THREADS} -n 1 sh -c 'gzip -dc \"\$1\" > \"\${DECOMPRESSED_DIR}/\$(basename \"\$1\" .gz)\"' _")

echo "Load the table from uncompressed files (.csv)"
rm -f "${DB}" "${DB}.wal"
${DUCKDB} "${DB}" -c ".read ${SCRIPT_DIR}/schema-without-pk.sql"
LOAD_UNCOMPRESSED=$(timed ${DUCKDB} "${DB}" -c "COPY Comment FROM '${DECOMPRESSED_DIR}/part-*.csv' (HEADER true, DELIMITER '|');")
${DUCKDB} "${DB}" -c "SELECT count(*) AS numComment FROM Comment;"

echo "Size of compressed files:   $(du -sh "${INPUT_DIR}" | cut -f1)"
echo "Size of uncompressed files: $(du -sh "${DECOMPRESSED_DIR}" | cut -f1)"
rm -rf "${DECOMPRESSED_DIR}" "${DB}" "${DB}.wal"

echo "Load from compressed files:                  ${LOAD_COMPRESSED} s"
echo "Decompress:                                  ${DECOMPRESS} s"
echo "Load from uncompressed files:                ${LOAD_UNCOMPRESSED} s"
echo "Decompress and load from uncompressed files: $(echo "${DECOMPRESS} + ${LOAD_UNCOMPRESSED}" | bc) s"
