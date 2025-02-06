---
layout: docu
redirect_from:
- docs/archive/1.1/sql/postgresl_compatibility
title: PostgreSQL Compatibility
---

DuckDB's SQL dialect closely follows the conventions of the PostgreSQL dialect.
The few exceptions to this are listed on this page.

## Floating-Point Arithmetic

DuckDB and PostgreSQL handle floating-point arithmetic differently for division by zero. DuckDB conforms to the [IEEE Standard for Floating-Point Arithmetic (IEEE 754)](https://en.wikipedia.org/wiki/IEEE_754) for both division by zero and operations involving infinity values. PostgreSQL returns an error for division by zero but aligns with IEEE 754 for handling infinity values. To show the differences, run the following SQL queries:

```sql
SELECT 1.0 / 0.0 AS x;
SELECT 0.0 / 0.0 AS x;
SELECT -1.0 / 0.0 AS x;
SELECT 'Infinity'::FLOAT / 'Infinity'::FLOAT AS x;
SELECT 1.0 / 'Infinity'::FLOAT AS x;
SELECT 'Infinity'::FLOAT - 'Infinity'::FLOAT AS x;
SELECT 'Infinity'::FLOAT - 1.0 AS x;
```

<div class="monospace_table"></div>

| Expression              | PostgreSQL |    DuckDB |  IEEE 754 |
|:------------------------|-----------:|----------:|----------:|
| 1.0 / 0.0               |      error |  Infinity |  Infinity |
| 0.0 / 0.0               |      error |       NaN |       NaN |
| -1.0 / 0.0              |      error | -Infinity | -Infinity |
| 'Infinity' / 'Infinity' |        NaN |       NaN |       NaN |
| 1.0 / 'Infinity'        |        0.0 |       0.0 |       0.0 |
| 'Infinity' - 'Infinity' |        NaN |       NaN |       NaN |
| 'Infinity' - 1.0        |   Infinity |  Infinity |  Infinity |

## Division on Integers

When computing division on integers, PostgreSQL performs integer division, while DuckDB performs float division:

```sql
SELECT 1 / 2 AS x;
```

PostgreSQL returns:

|    x |
| ---: |
|    0 |

DuckDB returns:

|    x |
| ---: |
|  0.5 |

To perform integer division in DuckDB, use the `//` operator:

```sql
SELECT 1 // 2 AS x;
```

|    x |
| ---: |
|    0 |

## `UNION` of Boolean and Integer Values

The following query fails in PostgreSQL but successfully completes in DuckDB:

```sql
SELECT true AS x
UNION
SELECT 2;
```

PostgreSQL returns an error:

```console
ERROR:  UNION types boolean and integer cannot be matched
```

DuckDB performs an enforced cast, therefore, it completes the query and returns the following:

|   x|
|---:|
|   1|
|   2|

## Case Sensitivity for Quoted Identifiers

PostgreSQL is case-insensitive. The way PostgreSQL achieves case insensitivity is by lowercasing unquoted identifiers within SQL, whereas quoting preserves case, e.g., the following command creates a table named `mytable` but tries to query for `MyTaBLe` because quotes preserve the case.

```sql
CREATE TABLE MyTaBLe(x INTEGER);
SELECT * FROM "MyTaBLe";
```

```console
ERROR:  relation "MyTaBLe" does not exist
```

PostgreSQL does not only treat quoted identifiers as case-sensitive, PostgreSQL treats all identifiers as case-sensitive, e.g., this also does not work:

```sql
CREATE TABLE "PreservedCase"(x INTEGER);
SELECT * FROM PreservedCase;
```

```console
ERROR:  relation "preservedcase" does not exist
```

Therefore, case-insensitivity in PostgreSQL only works if you never use quoted identifiers with different cases.

For DuckDB, this behavior was problematic when interfacing with other tools (e.g., Parquet, Pandas) that are case-sensitive by default - since all identifiers would be lowercased all the time.
Therefore, DuckDB achieves case insensitivity by making identifiers fully case insensitive throughout the system but [_preserving their case_]({% link docs/archive/1.1/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity).

In DuckDB, the scripts above complete successfully:

```sql
CREATE TABLE MyTaBLe(x INTEGER);
SELECT * FROM "MyTaBLe";
CREATE TABLE "PreservedCase"(x INTEGER);
SELECT * FROM PreservedCase;
SELECT table_name FROM duckdb_tables();
```

<div class="monospace_table"></div>

|  table_name   |
|---------------|
| MyTaBLe       |
| PreservedCase |

PostgreSQL's behavior of lowercasing identifiers is accessible using the [`preserve_identifier_case` option]({% link docs/archive/1.1/configuration/overview.md %}#local-configuration-options):

```sql
SET preserve_identifier_case = false;
CREATE TABLE MyTaBLe(x INTEGER);
SELECT table_name FROM duckdb_tables();
```

<div class="monospace_table"></div>

| table_name |
|------------|
| mytable    |

However, the case insensitive matching in the system for identifiers cannot be turned off.

## Using Double Equality Sign for Comparison

DuckDB supports both `=` and `==` for quality comparison, while Postgres only supports `=`.

```sql
SELECT 1 == 1 AS t;
```

DuckDB returns:

<div class="monospace_table"></div>

|  t   |
|-----:|
| true |

Postgres returns:

```console
postgres=# SELECT 1 == 1 AS t;
ERROR:  operator does not exist: integer == integer
LINE 1: SELECT 1 == 1 AS t;
```

Note that the use of `==` is not encouraged due to its limited portability.

## Vacuuming tables

In PostgreSQL, the `VACUUM` statement garbage collects tables and analyzes tables.
In DuckDB, the [`VACUUM` statement]({% link docs/archive/1.1/sql/statements/vacuum.md %}) is only used to rebuild statistics.
For instruction on reclaiming space, refer to the [“Reclaiming space” page]({% link docs/archive/1.1/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).

## Functions

### `regexp_extract` Function

Unlike PostgreSQL's `regexp_substr` function, DuckDB's `regexp_extract` returns empty strings instead of `NULL`s when there is no match. 

### `to_date` Function

DuckDB does not support the [`to_date` PostgreSQL date formatting function](https://www.postgresql.org/docs/17/functions-formatting.html).
Instead, please use the [`strptime` function]({% link docs/archive/1.1/sql/functions/dateformat.md %}#strptime-examples).

### `current_date` / `current_time` / `current_timestamp`

DuckDB's `current_date` and `current_time` pseudo-columns return the current date (as `DATE`) and time (as `TIME`) in UTC, whereas PostgreSQL returns the current date (as `DATE`) in the configured local timezone and time as `TIMETZ`. For the current time in the configured timezone, still as regular `TIME`, DuckDB offers the function `current_localtime()`.

Both DuckDB and PostgreSQL return `current_timestamp` as `TIMESTAMPTZ`. DuckDB additionally offers `current_localtimestamp()`, which returns the time in the configured timezone as `TIMESTAMP`.

DuckDB does not currently offer `current_localdate()`; though this can be computed via `current_timestamp::DATE` or `current_localtimestamp()::DATE`.

> See the [DuckDB blog entry on time zones]({% post_url 2022-01-06-time-zones %}) for more information on timestamps and timezones and DuckDB's handling thereof.

## Resolution of Type Names in the Schema

For [`CREATE TABLE` statements]({% link docs/archive/1.1/sql/statements/create_table.md %}), DuckDB attempts to resolve type names in the schema where a table is created. For example:

```sql
CREATE SCHEMA myschema;
CREATE TYPE myschema.mytype AS ENUM ('as', 'df');
CREATE TABLE myschema.mytable (v mytype);
```

PostgreSQL returns an error on the last statement:

```console
ERROR:  type "mytype" does not exist
LINE 1: CREATE TABLE myschema.mytable (v mytype);
```

DuckDB runs the statement and creates the table successfully, confirmed by the following query:

```sql
DESCRIBE myschema.mytable;
```

<div class="monospace_table"></div>

| column_name |   column_type    | null | key  | default | extra |
|-------------|------------------|------|------|---------|-------|
| v           | ENUM('as', 'df') | YES  | NULL | NULL    | NULL  |