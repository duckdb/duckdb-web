---
layout: docu
railroad: statements/vacuum.js
redirect_from:
- /docs/sql/statements/vacuum
- /docs/stable/sql/statements/vacuum
- /docs/current/sql/statements/vacuum
- /docs/lts/sql/statements/vacuum
- /docs/preview/sql/statements/vacuum
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
VACUUM ANALYZE my_table(my_column);
```

The following operation is not supported:

```sql
VACUUM FULL;
```

```console
Not implemented Error:
FULL is not yet implemented
```

## Vacuum with Indexes

> New Starting with DuckDB 2.0, checkpoint vacuuming also compacts tables with ART indexes.

When a checkpoint vacuums (compacts) row groups, the row IDs of the moved rows change. On databases using [storage version]({% link docs/2.0/internals/storage.md %}) 2.0.0 or later, DuckDB incrementally remaps the affected ART index entries to the new row IDs, so tables with ART indexes (including those created by `PRIMARY KEY` and `UNIQUE` constraints) are vacuumed by default and no full index rebuild is required.

On databases using an older storage version, the row IDs cannot be remapped, so tables with indexes are skipped by checkpoint vacuuming. For such databases, the deprecated `vacuum_rebuild_indexes` setting provides a fallback: it specifies a maximum table row count up to which the indexes are rebuilt after vacuuming (the default, `0`, disables the fallback). It can only be set before the database is started or per database as an `ATTACH` option.

## Reclaiming Space

The `VACUUM` statement does not reclaim space.
For instructions on reclaiming space, refer to the [“Reclaiming space” page]({% link docs/2.0/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).

## Syntax

<div id="rrdiagram1"></div>
