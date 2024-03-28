---
layout: docu
title: Parquet Tips
---

Below is a collection of tips to help when dealing with Parquet files.

## Tips for Reading Parquet Files

### Use `union_by_name` When Loading Files with Different Schemas

The `union_by_name` option can be used to unify the schema of files that have different or missing columns. For files that do not have certain columns, `NULL` values are filled in.

```sql
SELECT *
FROM read_parquet('flights*.parquet', union_by_name = true);
```

## Tips for Writing Parquet Files

### Enabling `PER_THREAD_OUTPUT`

If the final number of Parquet files is not important, writing one file per thread can significantly improve performance.
Using a [glob pattern](../multiple_files/overview#glob-syntax) upon read or a [Hive partitioning](../partitioning/hive_partitioning) structure are good ways to transparently handle multiple files.

```sql
COPY
    (FROM generate_series(10_000_000))
    TO 'test.parquet'
    (FORMAT PARQUET, PER_THREAD_OUTPUT true);
```

### Selecting a `ROW_GROUP_SIZE`

The `ROW_GROUP_SIZE` parameter specifies the minimum number of rows in a Parquet row group, with a minimum value equal to DuckDB's vector size (currently 2048, but adjustable when compiling DuckDB), and a default of 122,880.
A Parquet row group is a partition of rows, consisting of a column chunk for each column in the dataset.

Compression algorithms are only applied per row group, so the larger the row group size, the more opportunities to compress the data.
DuckDB can read Parquet row groups in parallel even within the same file and uses predicate pushdown to only scan the row groups whose metadata ranges match the `WHERE` clause of the query.
However there is some overhead associated with reading the metadata in each group.
A good approach would be to ensure that within each file, the total number of row groups is at least as large as the number of CPU threads used to query that file.
More row groups beyond the thread count would improve the speed of highly selective queries, but slow down queries that must scan the whole file like aggregations.

```sql
-- write a query to a Parquet file with a different row_group_size
COPY
    (FROM generate_series(100_000))
    TO 'row-groups.parquet'
    (FORMAT PARQUET, ROW_GROUP_SIZE 100_000);
```

See the [Performance Guide on file formats](../../guides/performance/file_formats#parquet-file-sizes) for more tips.

### The `ROW_GROUPS_PER_FILE` Option

The `ROW_GROUPS_PER_FILE` parameter creates a new Parquet file if the current one has a specified number of row groups.

```sql
COPY
    (FROM generate_series(100_000))
    TO 'output-directory'
    (FORMAT PARQUET, ROW_GROUP_SIZE 20_000, ROW_GROUPS_PER_FILE 2);
```

> If multiple threads are active, the number of row groups in a file may slightly exceed the specified number of row groups to limit the amount of locking – similarly to the behaviour of [`FILE_SIZE_BYTES`](../../sql/statements/copy#copy--to-options).
> However, if `PER_THREAD_OUTPUT` is set, only one thread writes to each file, and it becomes accurate again.

See the [Performance Guide on file formats](../../guides/performance/file_formats#parquet-file-sizes) for more tips.
