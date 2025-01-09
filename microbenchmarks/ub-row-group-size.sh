#!/usr/bin/env bash

set -Eeuo pipefail

DUCKDB=/opt/homebrew/bin/duckdb
TIMEFORMAT='%R'

rm -rf *.db

printf "loading the comments to DuckDB"
time ${DUCKDB} ldbc-comments.db -c "CREATE TABLE comment AS FROM 'Comment/part-*.csv.gz'";

echo "row_group_size,iteration,time" > row-group-size-comparison.csv
for ROW_GROUP_SIZE in 960 1920 3840 7680 15360 30720 61440 122880 245760 491520 983040 1966080; do
    rm -rf tmpdb.db
    rm -rf comment-sf300-parquet
    ${DUCKDB} ldbc-comments.db -c "SET preserve_insertion_order=false; EXPORT DATABASE 'comment-sf300-parquet' (FORMAT PARQUET, ROW_GROUP_SIZE ${ROW_GROUP_SIZE});" > /dev/null

    printf "Row group size ${ROW_GROUP_SIZE}: "
    for I in $(seq 1 5); do
        exec 3>&1 4>&2
        TIME=$(TIMEFORMAT="%R"; { time ${DUCKDB} tmpdb.db -c "SELECT avg(extract('day' FROM creationDate)) FROM 'comment-sf300-parquet/comment.parquet';" 1>&3 2>&4; } 2>&1)
        exec 3>&- 4>&-
        if [ $? == 0 ]; then
            echo "${ROW_GROUP_SIZE},${I},${TIME}" >> row-group-size-comparison.csv
        fi
    done
done

${DUCKDB} -c ".read process-row-group-size-results.sql"
