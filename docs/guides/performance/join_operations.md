---
layout: docu
title: Join Operations
---

## How to Force a Join Order

DuckDB has a cost-based query optimizer, which uses statistics in the base tables (stored in a DuckDB database or Parquet files) to estimate the cardinality of operations.

### Turn off the Join Order Optimizer

```sql
SET disabled_optimizers = 'join_order';
```

Then, DuckDB will perform the joins in the order specified in the query:

```sql
SELECT …
FROM …
JOIN … -- this join is performed first
JOIN … -- this join is performed second
```

Once the query in question has been executed, turn back the join optimizer with the following command:

```sql
SET disabled_optimizers = '';
```

### Create Temporary Tables

To force a particular join order, you can break up the query into multiple queries with each creating a temporary tables:

```sql
CREATE OR REPLACE TEMPORARY TABLE t1 AS
    …;

-- join on the result of the first query, t1
CREATE OR REPLACE TEMPORARY TABLE t2 AS
    SELECT * FROM t1 …;

-- compute the final result using t2
SELECT * FROM t1 …
```

To clean up, drop the interim tables:

```sql
DROP TABLE IF EXISTS t1;
DROP TABLE IF EXISTS t2;
```
