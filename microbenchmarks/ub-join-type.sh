#!/usr/bin/env bash

# Microbenchmark for the "Joining on Strings" section of the "Schema" page:
# self-join of the LDBC Comment table using identifiers of different types.
#
# Input: the LDBC Comment table, e.g., https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst
# extracted to ${DATA_DIR}/ldbc-sf${SF}-comments/
#
# Usage: SF=100 DATA_DIR=/path/to/data WORK_DIR=/path/to/work ./ub-join-type.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

SF="${SF:-100}"
INPUT="${DATA_DIR}/ldbc-sf${SF}-comments/part-*.csv.gz"
DB="ldbc_join.db"

echo "Running join type experiments on scale factor SF${SF}"
cd "${WORK_DIR}"

QUERY_ID="SELECT count(*) AS count FROM Comment c1 JOIN Comment c2 ON c1.ParentCommentId = c2.id;"
QUERY_UUID="SELECT count(*) AS count FROM Comment c1 JOIN Comment c2 ON c1.ParentCommentId_uuid = c2.id_uuid;"

load_typed() {
    ${DUCKDB} "${DB}" \
        -c ".read ${SCRIPT_DIR}/schema-without-pk.sql" \
        -c "COPY Comment FROM '${INPUT}' (HEADER true, DELIMITER '|');"
}

load_varchar() {
    ${DUCKDB} "${DB}" \
        -c "CREATE TABLE Comment AS FROM read_csv('${INPUT}', all_varchar = true, delim = '|', header = true);"
}

# Adds a random UUID to each comment and sets the ParentCommentId_uuid attribute accordingly
add_uuids() {
    local type="$1"
    ${DUCKDB} "${DB}" \
        -c "ALTER TABLE Comment ADD COLUMN id_uuid ${type};" \
        -c "ALTER TABLE Comment ADD COLUMN ParentCommentId_uuid ${type};" \
        -c "UPDATE Comment SET id_uuid = uuid();" \
        -c "UPDATE Comment
            SET ParentCommentId_uuid = ParentComment.id_uuid
            FROM Comment ParentComment
            WHERE ParentComment.id = Comment.ParentCommentId;"
}

run_variant() {
    local payload_type="$1"
    local schema_type="$2"
    local query="$3"
    local count
    count=$(${DUCKDB} -batch -noheader -csv "${DB}" -c "${query}")
    echo "${payload_type},${schema_type},$(file_size "${DB}"),${count},$(median_query_time "${DB}" "${query}")" \
        | tee -a join-type-results.csv
    rm -f "${DB}" "${DB}.wal"
}

echo "payload_type,schema_type,storage_size_bytes,count,query_time_s" > join-type-results.csv
rm -f "${DB}" "${DB}.wal"

load_typed
run_variant BIGINT BIGINT "${QUERY_ID}"

load_varchar
run_variant BIGINT VARCHAR "${QUERY_ID}"

load_typed
add_uuids UUID
run_variant UUID UUID "${QUERY_UUID}"

load_typed
add_uuids VARCHAR
run_variant UUID VARCHAR "${QUERY_UUID}"

${DUCKDB} -c "
    SELECT
        payload_type AS 'Join column payload type',
        schema_type AS 'Join column schema type',
        format_bytes(storage_size_bytes) AS 'Storage size',
        count AS 'Count',
        query_time_s || ' s' AS 'Query time'
    FROM 'join-type-results.csv';"
