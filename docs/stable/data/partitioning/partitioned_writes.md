---
layout: docu
redirect_from:
- /docs/data/partitioning/partitioned_writes
title: Partitioned Writes
---

## Examples

Write a table to a Hive partitioned dataset of Parquet files:

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month));
```

Write a table to a Hive partitioned dataset of CSV files, allowing overwrites:

```sql
COPY orders TO 'orders'
(FORMAT csv, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE);
```

Write a table to a Hive partitioned dataset of GZIP-compressed CSV files, setting explicit data files' extension:

```sql
COPY orders TO 'orders'
(FORMAT csv, PARTITION_BY (year, month), COMPRESSION gzip, FILE_EXTENSION 'csv.gz');
```

## Partitioned Writes

When the `PARTITION_BY` clause is specified for the [`COPY` statement]({% link docs/stable/sql/statements/copy.md %}), the files are written in a [Hive partitioned]({% link docs/stable/data/partitioning/hive_partitioning.md %}) folder hierarchy. The target is the name of the root directory (in the example above: `orders`). The files are written in-order in the file hierarchy. Currently, one file is written per thread to each directory.

```text
orders
├── year=2021
│    ├── month=1
│    │   ├── data_1.parquet
│    │   └── data_2.parquet
│    └── month=2
│        └── data_1.parquet
└── year=2022
     ├── month=11
     │   ├── data_1.parquet
     │   └── data_2.parquet
     └── month=12
         └── data_1.parquet
```

The values of the partitions are automatically extracted from the data. Note that it can be very expensive to write a larger number of partitions as many files will be created. The ideal partition count depends on how large your dataset is.

To limit the maximum number of files the system can keep open before flushing to disk when writing using `PARTITION_BY`, use the `partitioned_write_max_open_files` configuration option (default: 100):

```batch
SET partitioned_write_max_open_files = 10;
```

> Bestpractice Writing data into many small partitions is expensive. It is generally recommended to have at least `100 MB` of data per partition.

### Filename Pattern

By default, files will be named `data_0.parquet` or `data_0.csv`. With the flag `FILENAME_PATTERN` a pattern with `{i}` or `{uuid}` can be defined to create specific filenames:

* `{i}` will be replaced by an index.
* `{uuid}` will be replaced by a 128 bits long UUID.

Write a table to a Hive partitioned dataset of .parquet files, with an index in the filename:

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN 'orders_{i}');
```

Write a table to a Hive partitioned dataset of .parquet files, with unique filenames:

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN 'file_{uuid}');
```

### Overwriting

By default the partitioned write will not allow overwriting existing directories.
On a local file system, the `OVERWRITE` and `OVERWRITE_OR_IGNORE` options remove the existing directories.
On remote file systems, overwriting is not supported.

### Appending

To append to an existing Hive partitioned directory structure, use the `APPEND` option:

```sql
COPY orders TO 'orders'
(FORMAT parquet, PARTITION_BY (year, month), APPEND);
```

Using the `APPEND` option results in a behavior similar the `OVERWRITE_OR_IGNORE, FILENAME_PATTERN '{uuid}'` options,
but DuckDB performs an extra check for whether the file already exists and then regenerates the UUID in the rare event that it does (to avoid clashes).

### Handling Slashes in Columns

To handle slashes in column names, use Percent-Encoding implemented by the [`url_encode` function]({% link docs/stable/sql/functions/text.md %}#url_encodestring).
