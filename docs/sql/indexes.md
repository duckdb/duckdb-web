---
layout: docu
title: Indexes
railroad: statements/indexes.js
---

## Index Types

DuckDB has two built-in index types. Indexes can also be defined via [extensions]({% link docs/extensions/overview.md %}).

### Min-Max Index (Zonemap)

A [min-max index](https://en.wikipedia.org/wiki/Block_Range_Index) (also known as zonemap and block range index) is automatically created for columns of all [general-purpose data types]({% link docs/sql/data_types/overview.md %}).

### Adaptive Radix Tree (ART)

An [Adaptive Radix Tree (ART)](https://db.in.tum.de/~leis/papers/ART.pdf) is mainly used to ensure primary key constraints and to speed up point and very highly selective (i.e., < 0.1%) queries. ART indexes are automatically created for columns with a `UNIQUE` or `PRIMARY KEY` constraint and can be defined using `CREATE INDEX`.

> Warning ART indexes must currently be able to fit in-memory during index creation. Avoid creating ART indexes if the index does not fit in memory during index creation.

### Indexes Defined by Extensions

[Starting with version 1.1.0]({% post_url 2024-09-09-announcing-duckdb-110 %}#r-tree), DuckDB supports [R-trees for spatial indexing]({% link docs/extensions/spatial/r-tree_indexes.md %}) via the `spatial` extension.

## Persistence

Both min-max indexes and ART indexes are persisted on disk.

## `CREATE INDEX` and `DROP INDEX`

To create an index, use the [`CREATE INDEX` statement]({% link docs/sql/statements/create_index.md %}#create-index).
To drop an index, use the [`DROP INDEX` statement]({% link docs/sql/statements/create_index.md %}#drop-index).

## Limitations of ART Indexes

ART indexes create a secondary copy of the data in a second location – this complicates processing, particularly when combined with transactions. Certain limitations apply when it comes to modifying data that is also stored in secondary indexes.

> As expected, indexes have a strong effect on performance, slowing down loading and updates, but speeding up certain queries. Please consult the [Performance Guide]({% link docs/guides/performance/indexing.md %}) for details.

### Updates Become Deletes and Inserts

When an update statement is executed on a column that is present in an index, the statement is transformed into a *DELETE* of the original row followed by an *INSERT*.
This has certain performance implications, particularly for wide tables, as entire rows are rewritten instead of only the affected columns.
