---
layout: docu
title: Join Operations
---

## Forcing a Join Order

DuckDB has a cost-based query optimizer, which uses statistics in the base tables (stored in a DuckDB database or Parquet files) to estimate the cardinality of operations.
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
