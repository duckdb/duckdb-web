#!/usr/bin/env bash

set -Eeuo pipefail

DUCKDB="/opt/homebrew/bin/duckdb ldbc_comment_pk.db -init ub-init.sql"
TIMEFORMAT="%3R"

echo "Running microbenchmark for SF${SF}"

if [ ! -d "ldbc-sf${SF}-comments" ]; then
    echo "'ldbc-sf${SF}-comments' directory does not exist, exiting"
    exit 1
fi

echo "operation,iteration,time" > pk.csv

for IDX in `seq 1 1`; do

    echo "Load the table without PK constraint (dry run to fill caches)"
    rm -rf *.db*
    ${DUCKDB} -f schema-without-pk.sql

    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} -c "COPY Comment FROM 'ldbc-sf${SF}-comments/part-*.csv.gz' (HEADER true, DELIMITER '|');" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-

    # ---

    echo "Load the table without PK constraint (actual run)"
    rm -rf *.db*
    ${DUCKDB} -f schema-without-pk.sql

    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} -c "COPY Comment FROM 'ldbc-sf${SF}-comments/part-*.csv.gz' (HEADER true, DELIMITER '|');" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-
    if [ $? == 0 ]; then
        echo "load without pk,${IDX},${TIME}" >> pk.csv
    fi

    echo "Add PK constraint"
    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} -c "ALTER TABLE Comment ADD PRIMARY KEY(id);" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-
    if [ $? == 0 ]; then
        echo "add primary key,${IDX},${TIME}" >> pk.csv
    fi

    # ---

    echo "Load the table with PK constraint"
    rm -rf *.db*
    ${DUCKDB} -f schema-with-pk.sql

    exec 3>&1 4>&2
    TIME=$( { time ${DUCKDB} -c "COPY Comment FROM 'ldbc-sf${SF}-comments/part-*.csv.gz' (HEADER true, DELIMITER '|');" 1>&3 2>&4; } 2>&1)
    exec 3>&- 4>&-
    if [ $? == 0 ]; then
        echo "load with pk,${IDX},${TIME}" >> pk.csv
    fi
done

${DUCKDB} -f process-pk-results.sql
