---
layout: docu
title: Profiling Queries
---

DuckDB supports profiling queries via the [`EXPLAIN`]({% link docs/preview/guides/meta/explain.md %}) and [`EXPLAIN ANALYZE`]({% link docs/preview/guides/meta/explain_analyze.md %}) statements.

## `EXPLAIN`

To see the query plan of a query without executing it, run:

```sql
EXPLAIN ⟨query⟩;
```

The output of `EXPLAIN` contains the estimated cardinalities for each operator.

### `EXPLAIN (SQL)`

> New As of DuckDB 2.0, `EXPLAIN (SQL)` renders the optimized logical plan back as an executable DuckDB SQL string instead of as a plan tree:
>
> ```sql
> EXPLAIN (SQL) SELECT 1 + 2 AS answer;
> ```
>
> | explain_key | explain_value                      |
> |-------------|------------------------------------|
> | sql         | SELECT CAST(3 AS INTEGER) AS answer |

Because the output is the *optimized* plan, it can differ substantially from the input query (for example through join reordering, constant folding, or subquery introduction). The generated query preserves the result column names, column order, and logical types, but the exact formatting and any generated aliases are not a stable interface. `EXPLAIN (SQL)` does not execute the query, supports only `SELECT`, `VALUES`, and `WITH` queries, and cannot be combined with `ANALYZE` or `FORMAT`.

## `EXPLAIN ANALYZE`

To profile a query, run:

```sql
EXPLAIN ANALYZE ⟨query⟩;
```

The `EXPLAIN ANALYZE` statement runs the query, and shows the actual cardinalities for each operator,
as well as the cumulative wall-clock time spent in each operator.
