---
layout: docu
title: FROM & JOIN Clauses
selected: Documentation/SQL/Query Syntax/From
expanded: SQL
railroad: query_syntax/from.js
blurb: The FROM clause can contain a single table, a combination of multiple tables that are joined together, or another SELECT query inside a subquery node.
---
The `FROM` clause specifies the *source* of the data on which the remainder of the query should operate. Logically, the `FROM` clause is where the query starts execution. The `FROM` clause can contain a single table, a combination of multiple tables that are joined together using `JOIN` clauses, or another `SELECT` query inside a subquery node. DuckDB also has an optional `FROM`-first syntax which enables you to also query without a `SELECT` statement.

### Examples

```sql
--  select all columns from the table called "table_name"
FROM table_name;
-- select all columns from the table called "table_name"
SELECT * FROM table_name;
-- select all columns from the table called "table_name" in the schema "schema_name
SELECT * FROM schema_name.table_name;
-- select the column "i" from the table function "range", where the first column of the range function is renamed to "i"
SELECT t.i FROM range(100) AS t(i);
-- select all columns from the CSV file called "test.csv"
SELECT * FROM 'test.csv';
-- select all columns from a subquery
SELECT * FROM (SELECT * FROM table_name);
-- join two tables together
SELECT * FROM table_name JOIN other_table ON (table_name.key = other_table.key);
-- select a 10% sample from a table
SELECT * FROM table_name TABLESAMPLE 10%;
-- select a sample of 10 rows from a table
SELECT * FROM table_name TABLESAMPLE 10 ROWS;
```
### Joins

Joins are a fundamental relational operation used to connect two tables or relations horizontally.
The relations are referred to as the _left_ and _right_ sides of the join
based on how they are written in the join clause.
Each result row has the columns from both relations.

A join uses a rule to match pairs of rows from each relation.
Often this is a predicate, but there are other implied rules that may be specified.

#### Outer Joins

Rows that do not have any matches can still be returned if an `OUTER` join is specified.
Outer joins can be one of:

* `LEFT` (All rows from the left relation appear at least once)
* `RIGHT` (All rows from the right relation appear at least once)
* `FULL` (All rows from both relations appear at least once)

A join that is not `OUTER` is `INNER` (only rows that get paired are returned).

When an unpaired row is returned, the attributes from the other table are set to `NULL`.

#### Cross Product Joins

The simplest type of join is a `CROSS JOIN`. 
There are no conditions for this type of join, 
and it just returns all the possible pairs.

```sql
-- return all pairs of rows
SELECT a.*, b.* FROM a CROSS JOIN b
```

#### Conditional Joins

Most joins are specified by a predicate that connects 
attributes from one side to attributes from the other side.
The conditions can be explicitly specified using an `ON` clause
with the join (clearer) or implied by the `WHERE` clause (old-fashioned).

```sql
-- return the regions for the nations
SELECT n.*, r.*
FROM l_nations n, JOIN l_regions r ON (n_regionkey = r_regionkey)
```

If the column names are the same and are required to be equal,
then the simpler `USING` syntax can be used:

```sql
-- return the regions for the nations
SELECT n.*, r.*
FROM l_nations n, JOIN l_regions r USING (regionkey)
```

The expressions to not have to be equalities - any predicate can be used:

```sql
-- return the pairs of jobs where one ran longer but cost less
SELECT s1.t_id, s2.t_id 
FROM west s1, west s2
WHERE s1.time > s2.time 
  AND s1.cost < s2.cost;
```

#### Positional Joins

When working with data frames or other embedded tables of the same size, 
the rows may have a natural correspondence based on their physical order.
In scripting languages, this is easily expressed using a loop:

```cpp
for (i=0;i<n;i++) 
    f(t1.a[i], t2.b[i])
```

It is difficult to express this in standard SQL because 
relational tables are not ordered, but imported tables (like data frames)
or disk files (like CSVs or Parquet files) do have a natural ordering.

Connecting them using this ordering is called a _positional join_:

```sql
-- treat two data frames as a single table
SELECT df1.*, df2.*
FROM df1 POSITIONAL JOIN df2
```

Positional joins are always `FULL OUTER` joins.

#### As-Of Joins

A common operation when working with temporal or similarly-ordered data
is to find the nearest (first) event in a reference table (such as prices).
This is called an _as-of join_:

```sql
-- attach prices to stock trades
SELECT t.*, p.price
FROM trades t ASOF JOIN prices p 
  ON t.symbol = p.symbol AND t.when >= p.when

-- same query with USING, but the last attribute must be the inequality
SELECT t.*, p.price
FROM trades t ASOF JOIN prices p USING (symbol, when)
```

The `ASOF` join requires at least one inequality condition on the ordering field,
and the left table must be side that is greater in that inequality.
Any other conditions must be equalities (or `NOT DISTINCT`).
This means that the left/right order of the tables is significant.

`ASOF` joins only pair each left side row with at most one right side row.
It can be specified as an `OUTER` join to find unpaired rows 
(e.g., trades without prices or prices which have no trades.)

```sql
-- attach prices or NULLs to stock trades
SELECT *
FROM trades t ASOF LEFT JOIN prices p 
  ON t.symbol = p.symbol AND t.when >= p.when
```

If you use the `USING` syntax with a `SELECT *`, the query will return the left side (probe) column
values for the matches, not the right side (build) column values:

```sql
SELECT *
FROM trades t ASOF LEFT JOIN prices p 
  ON t.symbol = p.symbol AND t.when >= p.when
-- Returns symbol, trades.when, price
```

To get the `prices` time, you will need to list the columns explicitly. 

### Syntax
<div id="rrdiagram"></div>
