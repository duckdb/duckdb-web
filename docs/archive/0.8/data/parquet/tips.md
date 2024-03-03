---
layout: docu
title: Parquet Tips
---

Below is a collection of tips to help when dealing with Parquet files.

### Tips for reading Parquet files

#### Use `union_by_name` when loading files with different schemas

The `union_by_name` option can be used to unify the schema of files that have different or missing columns. For files that do not have certain columns, `NULL` values are filled in.  

```sql
SELECT * FROM read_parquet('flights*.parquet', union_by_name=True);
```

### Tips for writing Parquet files

#### Enabling `per_thread_output`
If the final number of parquet files is not important, writing one file per thread can significantly improve performance.
Using a [glob pattern](../multiple_files/overview#glob-syntax) upon read or a [hive partitioning](../partitioning/hive_partitioning) structure are good ways to transparently handle multiple files.

```sql
COPY (FROM generate_series(10000000)) TO 'test.parquet' (FORMAT PARQUET, PER_THREAD_OUTPUT TRUE);
```

#### Selecting a `row_group_size`

The `ROW_GROUP_SIZE` parameter specifies the minimum number of rows in a parquet row group, with a minimum value equal to DuckDB's vector size (currently 2048, but adjustable when compiling DuckDB), and a default of 122880.
A parquet row group is a partition of rows, consisting of a column chunk for each column in the dataset.

Compression algorithms are only applied per row group, so the larger the row group size, the more opportunities to compress the data.
DuckDB can read parquet row groups in parallel even within the same file and uses predicate pushdown to only scan the row groups whose metadata ranges match the `WHERE` clause of the query.
However there is some overhead associated with reading the metadata in each group.
A good approach would be to ensure that within each file, the total number of row groups is at least as large as the number of CPU threads used to query that file.
More row groups beyond the thread count would improve the speed of highly selective queries, but slow down queries that must scan the whole file like aggregations.

```sql
-- write a query to a parquet file with a different row_group_size
COPY (FROM generate_series(100000)) TO 'row-groups.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE 100000);
```
