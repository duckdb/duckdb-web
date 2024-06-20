---
layout: docu
title: FROM & JOIN Clauses
railroad: query_syntax/from.js
blurb: The FROM clause can contain a single table, a combination of multiple tables that are joined together, or another SELECT query inside a subquery node.
---

The `FROM` clause specifies the *source* of the data on which the remainder of the query should operate. Logically, the `FROM` clause is where the query starts execution. The `FROM` clause can contain a single table, a combination of multiple tables that are joined together using `JOIN` clauses, or another `SELECT` query inside a subquery node. DuckDB also has an optional `FROM`-first syntax which enables you to also query without a `SELECT` statement.

## Examples

Select all columns from the table called `table_name`:

```sql
SELECT *
FROM table_name;
```

Select all columns from the table using the `FROM`-first syntax:

```sql
FROM table_name
SELECT *;
```

Select all columns using the `FROM`-first syntax and omitting the `SELECT` clause:

```sql
FROM table_name;
```

Select all columns from the table called `table_name` through an alias `tn`:

```sql
SELECT tn.*
FROM table_name tn;
```

Select all columns from the table `table_name` in the schema `schema_name`:

```sql
SELECT *
FROM schema_name.table_name;
```

Select the column `i` from the table function `range`, where the first column of the range function is renamed to `i`:

```sql
SELECT t.i
FROM range(100) AS t(i);
```

Select all columns from the CSV file called `test.csv`:

```sql
SELECT *
FROM 'test.csv';
```

Select all columns from a subquery:

```sql
SELECT *
FROM (SELECT * FROM table_name);
```

Select the entire row of the table as a struct:

```sql
SELECT t
FROM t;
```

Select the entire row of the subquery as a struct (i.e., a single column):

```sql
SELECT t
FROM (SELECT unnest(generate_series(41, 43)) AS x, 'hello' AS y) t;
```

Join two tables together:

```sql
SELECT *
FROM table_name
JOIN other_table ON (table_name.key = other_table.key);
```

Select a 10% sample from a table:

```sql
SELECT *
FROM table_name
TABLESAMPLE 10%;
```

Select a sample of 10 rows from a table:

```sql
SELECT *
FROM table_name
TABLESAMPLE 10 ROWS;
```

Use the `FROM`-first syntax with `WHERE` clause and aggregation:

```sql
FROM range(100) AS t(i)
SELECT sum(t.i)
WHERE i % 2 = 0;
```

## Joins

Joins are a fundamental relational operation used to connect two tables or relations horizontally.
The relations are referred to as the _left_ and _right_ sides of the join
based on how they are written in the join clause.
Each result row has the columns from both relations.

A join uses a rule to match pairs of rows from each relation.
Often this is a predicate, but there are other implied rules that may be specified.

### Outer Joins

Rows that do not have any matches can still be returned if an `OUTER` join is specified.
Outer joins can be one of:

* `LEFT` (All rows from the left relation appear at least once)
* `RIGHT` (All rows from the right relation appear at least once)
* `FULL` (All rows from both relations appear at least once)

A join that is not `OUTER` is `INNER` (only rows that get paired are returned).

When an unpaired row is returned, the attributes from the other table are set to `NULL`.

### Cross Product Joins (Cartesian Product)

The simplest type of join is a `CROSS JOIN`.
There are no conditions for this type of join,
and it just returns all the possible pairs.

Return all pairs of rows:

```sql
SELECT a.*, b.*
FROM a
CROSS JOIN b;
```

This is equivalent to omitting the `JOIN` clause:

```sql
SELECT a.*, b.*
FROM a, b;
```

### Conditional Joins

Most joins are specified by a predicate that connects
attributes from one side to attributes from the other side.
The conditions can be explicitly specified using an `ON` clause
with the join (clearer) or implied by the `WHERE` clause (old-fashioned).

We use the `l_regions` and the `l_nations` tables from the TPC-H schema:

```sql
CREATE TABLE l_regions (
    r_regionkey INTEGER NOT NULL PRIMARY KEY,
    r_name      CHAR(25) NOT NULL,
    r_comment   VARCHAR(152)
);

CREATE TABLE l_nations (
    n_nationkey INTEGER NOT NULL PRIMARY KEY,
    n_name      CHAR(25) NOT NULL,
    n_regionkey INTEGER NOT NULL,
    n_comment   VARCHAR(152),
    FOREIGN KEY (n_regionkey) REFERENCES l_regions(r_regionkey)
);
```

Return the regions for the nations:

```sql
SELECT n.*, r.*
FROM l_nations n
JOIN l_regions r ON (n_regionkey = r_regionkey);
```

If the column names are the same and are required to be equal,
then the simpler `USING` syntax can be used:

```sql
CREATE TABLE l_regions (regionkey INTEGER NOT NULL PRIMARY KEY,
                        name      CHAR(25) NOT NULL,
                        comment   VARCHAR(152));

CREATE TABLE l_nations (nationkey INTEGER NOT NULL PRIMARY KEY,
                        name      CHAR(25) NOT NULL,
                        regionkey INTEGER NOT NULL,
                        comment   VARCHAR(152),
                        FOREIGN KEY (regionkey) REFERENCES l_regions(regionkey));
```

Return the regions for the nations:

```sql
SELECT n.*, r.*
FROM l_nations n
JOIN l_regions r USING (regionkey);
```

The expressions do not have to be equalities – any predicate can be used:

Return the pairs of jobs where one ran longer but cost less:

```sql
SELECT s1.t_id, s2.t_id
FROM west s1, west s2
WHERE s1.time > s2.time
  AND s1.cost < s2.cost;
```

### Natural Joins

Natural joins join two tables based on attributes that share the same name. For example:

```sql
CREATE TABLE city_airport ("city" VARCHAR, "IATA" VARCHAR);
CREATE TABLE airport_names ("IATA" VARCHAR, "airport name" VARCHAR);
INSERT INTO city_airport VALUES ('Amsterdam', 'AMS'), ('Rotterdam', 'RTM');
INSERT INTO airport_names VALUES ('AMS', 'Amsterdam Airport Schiphol'), ('RTM', 'Rotterdam The Hague Airport');
```

To join the tables on their shared [`IATA`](https://en.wikipedia.org/wiki/IATA_airport_code) attributes, run:

```sql
SELECT *
FROM city_airport
NATURAL JOIN airport_names;
```

This produces the following result:

|   city    | ICAO |        airport name         |
|-----------|------|-----------------------------|
| Amsterdam | AMS  | Amsterdam Airport Schiphol  |
| Rotterdam | RTM  | Rotterdam The Hague Airport |

### Semi and Anti Joins

Semi joins return rows from the left table that have at least one match in the right table. Anti joins return rows from the left table that have _no_ matches in the right table. When using a semi or anti join the result will never have more rows than the left hand side table. Semi and anti joins provide the same logic as [`(NOT) IN`]({% link docs/sql/expressions/in.md %}) statements.

Return a list of cars that have a valid region:

```sql
SELECT cars.name, cars.manufacturer
FROM cars
SEMI JOIN region
       ON cars.region = region.id;
```

Return a list of cars with no recorded safety data:

```sql
SELECT cars.name, cars.manufacturer
FROM cars
ANTI JOIN safety_data
       ON cars.safety_report_id = safety_data.report_id;
```

### Lateral Joins

The `LATERAL` keyword allows subqueries in the `FROM` clause to refer to previous subqueries. This feature is also known as a _lateral join_.

```sql
SELECT *
FROM range(3) t(i), LATERAL (SELECT i + 1) t2(j);
```

| i | j |
|--:|--:|
| 0 | 1 |
| 2 | 3 |
| 1 | 2 |

Lateral joins are a generalization of correlated subqueries, as they can return multiple values per input value rather than only a single value.

```sql
SELECT *
FROM
    generate_series(0, 1) t(i),
    LATERAL (SELECT i + 10 UNION ALL SELECT i + 100) t2(j);
```

| i |  j  |
|--:|----:|
| 0 | 10  |
| 1 | 11  |
| 0 | 100 |
| 1 | 101 |

It may be helpful to think about `LATERAL` as a loop where we iterate through the rows of the first subquery and use it as input to the second (`LATERAL`) subquery.
In the examples above, we iterate through table `t` and refer to its column `i` from the definition of table `t2`. The rows of `t2` form column `j` in the result.

It is possible to refer to multiple attributes from the `LATERAL` subquery. Using the table from the first example:

```sql
CREATE TABLE t1 AS
    SELECT *
    FROM range(3) t(i), LATERAL (SELECT i + 1) t2(j);

SELECT *
    FROM t1, LATERAL (SELECT i + j) t2(k)
    ORDER BY ALL;
```

| i | j | k |
|--:|--:|--:|
| 0 | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | 5 |

> DuckDB detects when `LATERAL` joins should be used, making the use of the `LATERAL` keyword optional.

### Positional Joins

When working with data frames or other embedded tables of the same size,
the rows may have a natural correspondence based on their physical order.
In scripting languages, this is easily expressed using a loop:

```cpp
for (i = 0; i < n; i++) {
    f(t1.a[i], t2.b[i]);
}
```

It is difficult to express this in standard SQL because
relational tables are not ordered, but imported tables such as [data frames]({% link docs/api/python/data_ingestion.md %}#pandas-dataframes-–-object-columns)
or disk files (like [CSVs]({% link docs/data/csv/overview.md %}) or [Parquet files]({% link docs/data/parquet/overview.md %})) do have a natural ordering.

Connecting them using this ordering is called a _positional join:_

```sql
CREATE TABLE t1 (x INTEGER);
CREATE TABLE t2 (s VARCHAR);

INSERT INTO t1 VALUES (1), (2), (3);
INSERT INTO t2 VALUES ('a'), ('b');

SELECT *
FROM t1
POSITIONAL JOIN t2;
```

| x |  s   |
|--:|------|
| 1 | a    |
| 2 | b    |
| 3 | NULL |

Positional joins are always `FULL OUTER` joins, i.e., missing values (the last values in the shorter column) are set to `NULL`.

### As-Of Joins

A common operation when working with temporal or similarly-ordered data
is to find the nearest (first) event in a reference table (such as prices).
This is called an _as-of join:_

Attach prices to stock trades:

```sql
SELECT t.*, p.price
FROM trades t
ASOF JOIN prices p
       ON t.symbol = p.symbol AND t.when >= p.when;
```

The `ASOF` join requires at least one inequality condition on the ordering field.
The inequality can be any inequality condition (`>=`, `>`, `<=`, `<`)
on any data type, but the most common form is `>=` on a temporal type.
Any other conditions must be equalities (or `NOT DISTINCT`).
This means that the left/right order of the tables is significant.

`ASOF` joins each left side row with at most one right side row.
It can be specified as an `OUTER` join to find unpaired rows
(e.g., trades without prices or prices which have no trades.)

Attach prices or NULLs to stock trades:

```sql
SELECT *
FROM trades t
ASOF LEFT JOIN prices p
            ON t.symbol = p.symbol
           AND t.when >= p.when;
```

`ASOF` joins can also specify join conditions on matching column names with the `USING` syntax,
but the *last* attribute in the list must be the inequality,
which will be greater than or equal to (`>=`):

```sql
SELECT *
FROM trades t
ASOF JOIN prices p USING (symbol, "when");
```

Returns symbol, trades.when, price (but NOT prices.when):

If you combine `USING` with a `SELECT *` like this,
the query will return the left side (probe) column values for the matches,
not the right side (build) column values.
To get the `prices` times in the example, you will need to list the columns explicitly:

```sql
SELECT t.symbol, t.when AS trade_when, p.when AS price_when, price
FROM trades t
ASOF LEFT JOIN prices p USING (symbol, "when");
```

## `FROM`-First Syntax

DuckDB's SQL supports the `FROM`-first syntax, i.e., it allows putting the `FROM` clause before the `SELECT` clause or completely omitting the `SELECT` clause. We use the following example to demonstrate it:

```sql
CREATE TABLE tbl AS
    SELECT *
    FROM (VALUES ('a'), ('b')) t1(s), range(1, 3) t2(i);
```

### `FROM`-First Syntax with a `SELECT` Clause

The following statement demonstrates the use of the `FROM`-first syntax:

```sql
FROM tbl
SELECT i, s;
```

This is equivalent to:

```sql
SELECT i, s
FROM tbl;
```

| i | s |
|--:|---|
| 1 | a |
| 2 | a |
| 1 | b |
| 2 | b |

### `FROM`-First Syntax without a `SELECT` Clause

The following statement demonstrates the use of the optional `SELECT` clause:

```sql
FROM tbl;
```

This is equivalent to:

```sql
SELECT *
FROM tbl;
```

| s | i |
|---|--:|
| a | 1 |
| a | 2 |
| b | 1 |
| b | 2 |

## Syntax

<div id="rrdiagram"></div>
