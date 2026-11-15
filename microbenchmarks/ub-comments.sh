#!/usr/bin/env bash

# Microbenchmarks for the "Using Timestamps" section of the "Schema" page and
# the "The Effect of Ordering" section of the "Indexing" page.
#
# Input: the creationDate column of the LDBC SF300 Comment table, available at
# https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet
#
# Usage: DATA_DIR=/path/to/data WORK_DIR=/path/to/work ./ub-comments.sh

set -Eeuo pipefail

source "$(dirname "$0")/common.sh"

INPUT="${DATA_DIR}/ldbc-sf300-comments-creationDate.parquet"
cd "${WORK_DIR}"
rm -f comment_*.db comment_*.db.wal

echo "Creating the databases"
${DUCKDB} comment_timestamp.db         -c "CREATE TABLE comment AS SELECT creationDate FROM '${INPUT}';"
${DUCKDB} comment_timestamp_ordered.db -c "CREATE TABLE comment AS SELECT creationDate FROM '${INPUT}' ORDER BY creationDate;"
${DUCKDB} comment_varchar.db           -c "CREATE TABLE comment AS SELECT creationDate::VARCHAR AS creationDate FROM '${INPUT}';"
${DUCKDB} comment_varchar_ordered.db   -c "CREATE TABLE comment AS SELECT creationDate::VARCHAR AS creationDate FROM '${INPUT}' ORDER BY creationDate;"

QUERY_TIMESTAMP="SELECT avg(extract('day' FROM creationDate)) FROM comment;"
QUERY_VARCHAR="SELECT avg(CAST(creationDate[9:10] AS INTEGER)) FROM comment;"

echo "configuration,storage_size_bytes,query_time_s" > comments-results.csv
for CONFIG in timestamp timestamp_ordered varchar varchar_ordered; do
    DB="comment_${CONFIG}.db"
    case "${CONFIG}" in
        timestamp*) QUERY="${QUERY_TIMESTAMP}" ;;
        varchar*)   QUERY="${QUERY_VARCHAR}" ;;
    esac
    echo "${CONFIG},$(file_size "${DB}"),$(median_query_time "${DB}" "${QUERY}")" | tee -a comments-results.csv
done

${DUCKDB} -c "
    SELECT
        configuration AS 'Configuration',
        format_bytes(storage_size_bytes) AS 'Storage size',
        query_time_s || ' s' AS 'Query time'
    FROM 'comments-results.csv';"
