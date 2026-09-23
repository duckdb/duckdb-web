---
layout: docu
title: Join Operations
---

## How to Force a Join Order

DuckDB has a cost-based query optimizer, which uses statistics in the base tables (stored in a DuckDB database or Parquet files) to estimate the cardinality of operations.

### Turn off the Join Order Optimizer

To turn off the join order optimizer, set the following [`PRAGMA`s]({% link docs/preview/configuration/pragmas.md %}):

```sql
SET disabled_optimizers = 'join_order,build_side_probe_side';
```

This disables both the join order optimizer and left/right swapping for joins.
This way, DuckDB builds a left-deep join tree following the order of `JOIN` clauses.

```sql
SELECT ...
FROM ...
JOIN ...  -- this join is performed first
JOIN ...; -- this join is performed second
```

Once the query in question has been executed, turn back the optimizers with the following command:

```sql
SET disabled_optimizers = '';
```

### Create Temporary Tables

To force a particular join order, you can break up the query into multiple queries, with each creating a temporary table:

```sql
CREATE OR REPLACE TEMPORARY TABLE t1 AS
    ...;

-- join on the result of the first query, t1
CREATE OR REPLACE TEMPORARY TABLE t2 AS
    SELECT * FROM t1 ...;

-- compute the final result using t2
SELECT * FROM t1 ...
```

To clean up, drop the interim tables:

```sql
DROP TABLE IF EXISTS t1;
DROP TABLE IF EXISTS t2;
```

## Configuring the Join Order Optimizer

DuckDB's join order optimizer computes the optimal join order exactly using a dynamic programming algorithm. As the number of tables in a join grows, exact enumeration becomes expensive, so for large joins the optimizer switches to an approximate (greedy) algorithm. The `approximate_join_order_threshold` [setting]({% link docs/preview/configuration/overview.md %}) controls when this happens: joins with at least this many tables are ordered approximately, while joins with fewer tables are ordered exactly. The default value is 12.

For example, to use the exact algorithm for joins of up to 15 tables, run:

```sql
SET approximate_join_order_threshold = 16;
```

Raising the threshold can lead to better join orders for queries with many joins at the cost of longer optimization times. Lowering it reduces optimization time for large joins.

> Even below the threshold, the optimizer falls back to the approximate algorithm if exact enumeration exceeds its internal budget.
