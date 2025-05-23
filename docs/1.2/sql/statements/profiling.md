---
layout: docu
title: Profiling Queries
---

DuckDB supports profiling queries via the `EXPLAIN` and `EXPLAIN ANALYZE` statements.

## `EXPLAIN`

To see the query plan of a query without executing it, run:

```sql
EXPLAIN ⟨query⟩;
```

The output of `EXPLAIN` contains the estimated cardinalities for each operator.

## `EXPLAIN ANALYZE`

To profile a query, run:

```sql
EXPLAIN ANALYZE ⟨query⟩;
```

The `EXPLAIN ANALYZE` statement runs the query, and shows the actual cardinalities for each operator,
as well as the cumulative wall-clock time spent in each operator.