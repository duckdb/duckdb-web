---
layout: docu
railroad: statements/vacuum.js
redirect_from:
  - /docs/sql/statements/vacuum
title: VACUUM Statement
---

The `VACUUM` statement only has basic support in DuckDB and is mostly provided for PostgreSQL-compatibility.

Some variants of it, such as when calling for a given column, recompute the distinct statistics (the number of distinct entities) if they have become stale due to updates.

> Warning The behavior of `VACUUM` is not consistent with PostgreSQL semantics and it is likely going to change in the future.

## Examples

No-op:

```sql
VACUUM;
```

No-op:

```sql
VACUUM ANALYZE;
```

Calling `VACUUM` on a given table-column pair rebuilds statistics for the table and column:

```sql
VACUUM my_table(my_column);
```

Rebuild statistics for the table and column:

```sql
VACUUM ANALYZE my_table(my_column);
```

The following operation is not supported:

```sql
VACUUM FULL;
```

```console
Not implemented Error:
Full vacuum option
```

## Reclaiming Space

The `VACUUM` statement does not reclaim space.
For instructions on reclaiming space, refer to the [“Reclaiming space” page]({% link docs/stable/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).

## Syntax

<div id="rrdiagram1"></div>
