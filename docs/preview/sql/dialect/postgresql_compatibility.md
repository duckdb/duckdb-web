---
layout: docu
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
| :---------------------- | ---------: | --------: | --------: |
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

PostgreSQL returns `0`, while DuckDB returns `0.5`.

To perform integer division in DuckDB, use the `//` operator:

```sql
SELECT 1 // 2 AS x;
```

This returns `0`.

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

|    x |
| ---: |
|    1 |
|    2 |

## Implicit Casting on Equality Checks

DuckDB performs implicit casting on equality checks, e.g., converting strings to numeric and boolean values.
Therefore, there are several instances, where PostgreSQL throws an error while DuckDB successfully computes the result:

<div class="monospace_table"></div>

| Expression    | PostgreSQL | DuckDB |
| :------------ | ---------- | ------ |
| '1.1' = 1     | error      | true   |
| '1.1' = 1.1   | true       | true   |
| 1 = 1.1       | false      | false  |
| true = 'true' | true       | true   |
| true = 1      | error      | true   |
| 'true' = 1    | error      | error  |

## Case Sensitivity for Quoted Identifiers

PostgreSQL is case-insensitive. The way PostgreSQL achieves case insensitivity is by lowercasing unquoted identifiers within SQL, whereas quoting preserves case, e.g., the following command creates a table named `mytable` but tries to query for `MyTaBLe` because quotes preserve the case.

```sql
CREATE TABLE MyTaBLe (x INTEGER);
SELECT * FROM "MyTaBLe";
```

```console
ERROR:  relation "MyTaBLe" does not exist
```

PostgreSQL does not only treat quoted identifiers as case-sensitive; it treats all identifiers as case-sensitive, e.g., this also does not work:

```sql
CREATE TABLE "PreservedCase" (x INTEGER);
SELECT * FROM PreservedCase;
```

```console
ERROR:  relation "preservedcase" does not exist
```

Therefore, case-insensitivity in PostgreSQL only works if you never use quoted identifiers with different cases.

For DuckDB, this behavior was problematic when interfacing with other tools (e.g., Parquet, Pandas) that are case-sensitive by default – since all identifiers would be lowercased all the time.
Therefore, DuckDB achieves case insensitivity by making identifiers fully case insensitive throughout the system but [_preserving their case_]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity).

In DuckDB, the scripts above complete successfully:

```sql
CREATE TABLE MyTaBLe (x INTEGER);
SELECT * FROM "MyTaBLe";
CREATE TABLE "PreservedCase" (x INTEGER);
SELECT * FROM PreservedCase;
SELECT tbl FROM duckdb_tables();
```

<div class="monospace_table"></div>

| tbl    |
| ------------- |
| MyTaBLe       |
| PreservedCase |

PostgreSQL's behavior of lowercasing identifiers is accessible using the [`preserve_identifier_case` option]({% link docs/preview/configuration/overview.md %}#local-configuration-options):

```sql
SET preserve_identifier_case = false;
CREATE TABLE MyTaBLe (x INTEGER);
SELECT tbl FROM duckdb_tables();
```

<div class="monospace_table"></div>

| tbl |
| ---------- |
| mytable    |

However, the case insensitive matching in the system for identifiers cannot be turned off.

## Using Double Equality Sign for Comparison

DuckDB supports both `=` and `==` for equality comparison, while PostgreSQL only supports `=`.

```sql
SELECT 1 == 1 AS t;
```

DuckDB returns `true`, while PostgreSQL returns:

```console
postgres=# SELECT 1 == 1 AS t;
ERROR:  operator does not exist: integer == integer
LINE 1: SELECT 1 == 1 AS t;
```

Note that the use of `==` is not encouraged due to its limited portability.

## Vacuuming Tables

In PostgreSQL, the `VACUUM` statement garbage collects tables and analyzes tables.
In DuckDB, the [`VACUUM` statement]({% link docs/preview/sql/statements/vacuum.md %}) is only used to rebuild statistics.
For instruction on reclaiming space, refer to the [“Reclaiming space” page]({% link docs/preview/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).

## Strings

Since version 1.3.0, DuckDB escapes characters such as `'` in strings serialized in nested data structures.
PostgreSQL does not do this.

For an example, run:

```sql
SELECT ARRAY[''''];
```

PostgreSQL returns:

```text
{'}
```

DuckDB returns:

```text
['\'']
```

## Functions

### `regexp_extract` Function

Unlike PostgreSQL's `regexp_substr` function, DuckDB's `regexp_extract` returns empty strings instead of `NULL`s when there is no match.

### `to_date` Function

DuckDB does not support the [`to_date` PostgreSQL date formatting function](https://www.postgresql.org/docs/17/functions-formatting.html).
Instead, please use the [`strptime` function]({% link docs/preview/sql/functions/dateformat.md %}#strptime-examples).

### `date_part` Function

Most parts extracted by the [`date_part` function]({% link docs/preview/sql/functions/datepart.md %}) are returned as integers. Since there are no infinite integer values in DuckDB, `NULL`s are returned for infinite timestamps.

## Resolution of Type Names in the Schema

For [`CREATE TABLE` statements]({% link docs/preview/sql/statements/create_table.md %}), DuckDB attempts to resolve type names in the schema where a table is created. For example:

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

| column_name | column_type      | null | key  | default | extra |
| ----------- | ---------------- | ---- | ---- | ------- | ----- |
| v           | ENUM('as', 'df') | YES  | NULL | NULL    | NULL  |

## Exploiting Functional Dependencies for `GROUP BY`

PostgreSQL can exploit functional dependencies, such as `i -> j` in the following query:

```sql
CREATE TABLE tbl (i INTEGER, j INTEGER, PRIMARY KEY (i));
SELECT j
FROM tbl
GROUP BY i;
```

PostgreSQL runs the query.

DuckDB fails:

```console
Binder Error:
column "j" must appear in the GROUP BY clause or must be part of an aggregate function.
Either add it to the GROUP BY list, or use "ANY_VALUE(j)" if the exact value of "j" is not important.
```

To work around this, add the other attributes or use the [`GROUP BY ALL` clause](https://duckdb.org/docs/sql/query_syntax/groupby#group-by-all).

## Behavior of Regular Expression Match Operators

PostgreSQL supports the [POSIX regular expression matching operators]({% link docs/preview/sql/functions/pattern_matching.md %}) `~` (case-sensitive partial regex matching) and `~*` (case-insensitive partial regex matching) as well as their negated variants, `!~` and `!~*`, respectively.

In DuckDB, `~` is equivalent to [`regexp_full_match`]({% link docs/preview/sql/functions/text.md %}#regexp_full_matchstring-regex) and `!~` is equivalent to `NOT regexp_full_match`.
The operators `~*` and `!~*` are not supported.

The table below shows that the correspondence between these functions in PostgreSQL and DuckDB is almost non-existent.
Avoid using the POSIX regular expression matching operators in DuckDB.

<div class="monospace_table"></div>

<!-- markdownlint-disable MD056 -->

| Expression          | PostgreSQL | DuckDB |
| :------------------ | ---------- | ------ |
| `'aaa' ~ '(a|b)'`   | true       | false  |
| `'AAA' ~* '(a|b)'`  | true       | error  |
| `'aaa' !~ '(a|b)'`  | false      | true   |
| `'AAA' !~* '(a|b)'` | false      | error  |

<!-- markdownlint-enable MD056 -->
