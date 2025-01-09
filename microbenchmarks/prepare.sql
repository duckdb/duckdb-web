CREATE TABLE comment AS FROM 'Comment/part-*.csv.gz';

CREATE TABLE ldbc_comment_datetime AS SELECT creationDate FROM comment;
CREATE TABLE ldbc_comment_datetime_ordered AS SELECT creationDate FROM ldbc_comment_datetime ORDER BY creationDate;
CREATE TABLE ldbc_comment_datetime_varchar AS SELECT creationDate::VARCHAR AS creationDate FROM ldbc_comment_datetime;
CREATE TABLE ldbc_comment_datetime_varchar_ordered AS SELECT creationDate::VARCHAR AS creationDate FROM ldbc_comment_datetime_ordered;

COPY ldbc_comment_datetime_ordered TO 'ldbc_comment_datetime_ordered.parquet';
COPY ldbc_comment_datetime TO 'ldbc_comment_datetime.parquet';
COPY ldbc_comment_datetime_varchar_ordered TO 'ldbc_comment_datetime_varchar_ordered.parquet';
COPY ldbc_comment_datetime_varchar TO 'ldbc_comment_datetime_varchar.parquet';
