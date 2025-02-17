#!/usr/bin/env bash

set -Eeuo pipefail

DUCKDB=/opt/homebrew/bin/duckdb
TIMEFORMAT='%3R'

echo "operation,iteration,time" > pk.csv

for I in `seq 1 5`; do

    echo "Load the table without PK constraint (dry run to fill caches)"
    rm -rf *.db*
    ${DUCKDB} ldbc_comment_pk.db -c ".read schema-without-pk.sql"

    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} ldbc_comment_pk.db -c "COPY Comment FROM 'Comment/part-*.csv.gz' (HEADER true, DELIMITER '|');" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-

    # ---

    echo "Load the table without PK constraint (actual run)"
    rm -rf *.db*
    ${DUCKDB} ldbc_comment_pk.db -c ".read schema-without-pk.sql"

    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} ldbc_comment_pk.db -c "COPY Comment FROM 'Comment/part-*.csv.gz' (HEADER true, DELIMITER '|');" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-
    if [ $? == 0 ]; then
        echo "load without pk,${I},${TIME}" >> pk.csv
    fi

    echo "Add PK constraint"
    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} ldbc_comment_pk.db -c "ALTER TABLE Comment ADD PRIMARY KEY(id);" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-
    if [ $? == 0 ]; then
        echo "add primary key,${I},${TIME}" >> pk.csv
    fi

    # ---

    echo "Load the table with PK constraint"
    rm -rf *.db*
    ${DUCKDB} ldbc_comment_pk.db -c ".read schema-with-pk.sql"

    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} ldbc_comment_pk.db -c "COPY Comment FROM 'Comment/part-*.csv.gz' (HEADER true, DELIMITER '|');" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-
    if [ $? == 0 ]; then
        echo "load with pk,${I},${TIME}" >> pk.csv
    fi
done

${DUCKDB} -c ".read process-pk-results.sql"
