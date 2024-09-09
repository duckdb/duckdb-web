---
layout: docu
redirect_from:
- docs/archive/1.0/sql/postgresl_compatibility
title: PostgreSQL Compatibility
---

DuckDB's SQL dialect closely follows the conventions of the PostgreSQL dialect.
The few exceptions to this are listed on this page.

## Floating-Point Arithmetic

DuckDB and PostgreSQL handle floating-point arithmetic differently for division by zero. Neither system confirm the [IEEE Standard for Floating-Point Arithmetic (IEEE 754)](https://en.wikipedia.org/wiki/IEEE_754).
On operations involving infinity values, DuckDB and PostgreSQL align with each other and conform to IEEE 754.
To show the differences, run the following SQL queries:

```sql
SELECT 1.0 / 0.0 AS x;
SELECT 0.0 / 0.0 AS x;
SELECT -1.0 / 0.0 AS x;
SELECT 'Infinity'::FLOAT / 'Infinity'::FLOAT AS x;
SELECT 1.0 / 'Infinity'::FLOAT AS x;
SELECT 'Infinity'::FLOAT - 'Infinity'::FLOAT AS x;
SELECT 'Infinity'::FLOAT - 1.0 AS x;
```

<div class="narrow_table monospace_table"></div>

| Expression              |   DuckDB | PostgreSQL |  IEEE 754 |
| :---------------------- | -------: | ---------: | --------: |
| 1.0 / 0.0               |     NULL |      error |  Infinity |
| 0.0 / 0.0               |     NULL |      error |       NaN |
| -1.0 / 0.0              |     NULL |      error | -Infinity |
| 'Infinity' / 'Infinity' |      NaN |        NaN |       NaN |
| 1.0 / 'Infinity'        |      0.0 |        0.0 |       0.0 |
| 'Infinity' - 'Infinity' |      NaN |        NaN |       NaN |
| 'Infinity' - 1.0        | Infinity |   Infinity |  Infinity |

## Division on Integers

When computing division on integers, PostgreSQL performs integer division, while DuckDB performs float division:

```sql
SELECT 1 / 2 AS x;
```

PostgreSQL returns:

```text
 x
---
 0
(1 row)
```

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

|    x |
| ---: |
|    1 |
|    2 |

## Case Sensitivity for Quoted Identifiers

PostgreSQL is case-insensitive. The way PostgreSQL achieves case insensitivity is by lowercasing unquoted identifiers within SQL, whereas quoting preserves case, e.g., the following command creates a table named `mytable` but tries to query for `MyTaBLe` because quotes preserve the case.

```sql
CREATE TABLE MyTaBLe(x INT);
SELECT * FROM "MyTaBLe";
```

```console
ERROR:  relation "MyTaBLe" does not exist
```

PostgreSQL does not only treat quoted identifiers as case-sensitive, PostgreSQL treats all identifiers as case-sensitive, e.g., this also does not work:

```sql
CREATE TABLE "PreservedCase"(x INT);
SELECT * FROM PreservedCase;
```

```console
ERROR:  relation "preservedcase" does not exist
```

Therefore, case-insensitivity in PostgreSQL only works if you never use quoted identifiers with different cases.

For DuckDB, this behavior was problematic when interfacing with other tools (e.g., Parquet, Pandas) that are case-sensitive by default - since all identifiers would be lowercased all the time.
Therefore, DuckDB achieves case insensitivity by making identifiers fully case insensitive throughout the system but [_preserving their case_]({% link docs/archive/1.0/sql/dialect/keywords_and_identifiers.md %}#rules-for-case-sensitivity). 

In DuckDB, the scripts above complete successfully:

```sql
CREATE TABLE MyTaBLe(x INT);
SELECT * FROM "MyTaBLe";
CREATE TABLE "PreservedCase"(x INT);
SELECT * FROM PreservedCase;
SELECT table_name FROM duckdb_tables();
```

<div class="narrow_table monospace_table"></div>

| table_name    |
| ------------- |
| MyTaBLe       |
| PreservedCase |

PostgreSQL's behavior of lowercasing identifiers is accessible using the [`preserve_identifier_case` option]({% link docs/archive/1.0/configuration/overview.md %}#local-configuration-options):

```sql
SET preserve_identifier_case = false;
CREATE TABLE MyTaBLe(x INT);
SELECT table_name FROM duckdb_tables();
```

<div class="narrow_table monospace_table"></div>

| table_name |
| ---------- |
| mytable    |

However, the case insensitive matching in the system for identifiers cannot be turned off.

## Scalar Subqueries

Subqueries in DuckDB are not required to return a single row. Take the following query for example:

```sql
SELECT (SELECT 1 UNION SELECT 2) AS b;
```

PostgreSQL returns an error:

```console
ERROR:  more than one row returned by a subquery used as an expression
```

DuckDB non-deterministically returns either `1` or `2`.