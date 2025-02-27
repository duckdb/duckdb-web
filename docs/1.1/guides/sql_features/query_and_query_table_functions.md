---
layout: docu
title: query and query_table Functions
---

The [`query`]({% link docs/1.1/sql/functions/utility.md %}#queryquery_string_literal)
and [`query_table`]({% link docs/1.1/sql/functions/utility.md %}#query_tabletbl_name)
functions take a string literal, and convert it into a `SELECT` subquery and a table reference, respectively.
Note that these functions only accept literal strings.
As such, they are not as powerful (or dangerous) as a generic `eval`.

These functions are conceptually simple, but enable powerful and more dynamic SQL. For example, they allow passing in a table name as a prepared statement parameter:

```sql
CREATE TABLE my_table(i INTEGER);
INSERT INTO my_table VALUES (42);

PREPARE select_from_table AS SELECT * FROM query_table($1);
EXECUTE select_from_table('my_table');
```

| i  |
|---:|
| 42 |

When combined with the [`COLUMNS` expression]({% link docs/1.1/sql/expressions/star.md %}#columns), we can write very generic SQL-only macros. For example, below is a custom version of `SUMMARIZE` that computes the `min` and `max` of every column in a table:

```sql
CREATE OR REPLACE MACRO my_summarize(table_name) AS TABLE
SELECT
    unnest([*COLUMNS('alias_.*')]) AS column_name,
    unnest([*COLUMNS('min_.*')]) AS min_value,
    unnest([*COLUMNS('max_.*')]) AS max_value
FROM (
    SELECT
        any_value(alias(COLUMNS(*))) AS "alias_\0",
        min(COLUMNS(*))::VARCHAR AS "min_\0",
        max(COLUMNS(*))::VARCHAR AS "max_\0"
    FROM query_table(table_name::VARCHAR)
);

SELECT *
FROM my_summarize('https://blobs.duckdb.org/data/ontime.parquet')
LIMIT 3;
```

| column_name | min_value | max_value |
|-------------|----------:|----------:|
| year        | 2017      | 2017      |
| quarter     | 1         | 3         |
| month       | 1         | 9         |