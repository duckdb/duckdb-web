#!/usr/bin/env bash

# Microbenchmark for the "The Effect of Primary Keys" section of the "Schema" page.
#
# Input: the LDBC Comment table, e.g., https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst
# extracted to ${DATA_DIR}/ldbc-sf${SF}-comments/
#
# Usage: SF=300 DATA_DIR=/path/to/data WORK_DIR=/path/to/work ./ub-pk.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

SF="${SF:-300}"
INPUT="${DATA_DIR}/ldbc-sf${SF}-comments/part-*.csv.gz"
DB="ldbc_comment_pk.db"
DUCKDB_PK="${DUCKDB} ${DB} -init ${SCRIPT_DIR}/ub-init.sql"
LOAD="COPY Comment FROM '${INPUT}' (HEADER true, DELIMITER '|');"
ITERATIONS="${ITERATIONS:-1}"

echo "Running microbenchmark for SF${SF}"

if ! ls ${INPUT} > /dev/null 2>&1; then
    echo "No input files found at ${INPUT}, exiting"
    exit 1
fi

cd "${WORK_DIR}"
echo "operation,iteration,time" > pk.csv

echo "Load the table without PK constraint (dry run to fill caches)"
rm -f "${DB}" "${DB}.wal"
${DUCKDB_PK} -f "${SCRIPT_DIR}/schema-without-pk.sql"
timed ${DUCKDB_PK} -c "${LOAD}" > /dev/null

for IDX in $(seq 1 "${ITERATIONS}"); do
    echo "Load the table without PK constraint"
    rm -f "${DB}" "${DB}.wal"
    ${DUCKDB_PK} -f "${SCRIPT_DIR}/schema-without-pk.sql"
    echo "load without pk,${IDX},$(timed ${DUCKDB_PK} -c "${LOAD}")" | tee -a pk.csv
    echo "Database size without PK: $(du -sh "${DB}" | cut -f1)"

    echo "Add PK constraint"
    echo "add primary key,${IDX},$(timed ${DUCKDB_PK} -c "ALTER TABLE Comment ADD PRIMARY KEY (id);")" | tee -a pk.csv

    echo "Load the table with PK constraint"
    rm -f "${DB}" "${DB}.wal"
    ${DUCKDB_PK} -f "${SCRIPT_DIR}/schema-with-pk.sql"
    echo "load with pk,${IDX},$(timed ${DUCKDB_PK} -c "${LOAD}")" | tee -a pk.csv
    echo "Database size with PK: $(du -sh "${DB}" | cut -f1)"
done

rm -f "${DB}" "${DB}.wal"
${DUCKDB} -f "${SCRIPT_DIR}/process-pk-results.sql"
