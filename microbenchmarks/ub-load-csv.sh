#!/usr/bin/env bash

set -Eeuo pipefail

DUCKDB=/opt/homebrew/bin/duckdb
TIMEFORMAT='%3R'

echo "Load the table from compressed representation (.csv.gz)"
rm -rf *.db*
${DUCKDB}      ldbc_comment_csv_test.db -c ".read schema-without-pk.sql"
time ${DUCKDB} ldbc_comment_csv_test.db -c "COPY Comment FROM '~/ldbc-data/Comment-compressed/part-*.csv.gz' (HEADER true, DELIMITER '|');"
${DUCKDB}      ldbc_comment_csv_test.db -c "SELECT count(*) AS numComment FROM Comment;"

echo "Load the table from uncompressed representation (.csv)"
rm -rf *.db*
${DUCKDB}      ldbc_comment_csv_test.db -c ".read schema-without-pk.sql"
time ${DUCKDB} ldbc_comment_csv_test.db -c "COPY Comment FROM '~/ldbc-data/Comment-decompressed/part-*.csv' (HEADER true, DELIMITER '|');"
${DUCKDB}      ldbc_comment_csv_test.db -c "SELECT count(*) AS numComment FROM Comment;"
