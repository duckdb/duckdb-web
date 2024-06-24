---
layout: docu
title: Partitioned Writes
---

## Examples

Write a table to a Hive partitioned data set of Parquet files:

```sql
COPY orders TO 'orders' (FORMAT PARQUET, PARTITION_BY (year, month));
```

Write a table to a Hive partitioned data set of CSV files, allowing overwrites:

```sql
COPY orders TO 'orders' (FORMAT CSV, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE);
```

## Partitioned Writes

When the `partition_by` clause is specified for the [`COPY` statement]({% link docs/sql/statements/copy.md %}), the files are written in a [Hive partitioned]({% link docs/data/partitioning/hive_partitioning.md %}) folder hierarchy. The target is the name of the root directory (in the example above: `orders`). The files are written in-order in the file hierarchy. Currently, one file is written per thread to each directory.

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

The values of the partitions are automatically extracted from the data. Note that it can be very expensive to write many partitions as many files will be created. The ideal partition count depends on how large your data set is.

> Bestpractice Writing data into many small partitions is expensive. It is generally recommended to have at least `100MB` of data per partition.

### Overwriting

By default the partitioned write will not allow overwriting existing directories. Use the `OVERWRITE_OR_IGNORE` option to allow overwriting an existing directory.

### Filename Pattern

By default, files will be named `data_0.parquet` or `data_0.csv`. With the flag `FILENAME_PATTERN` a pattern with `{i}` or `{uuid}` can be defined to create specific filenames:

* `{i}` will be replaced by an index
* `{uuid}` will be replaced by a 128 bits long UUID

Write a table to a Hive partitioned data set of .parquet files, with an index in the filename:

```sql
COPY orders TO 'orders'
    (FORMAT PARQUET, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN "orders_{i}");
```

Write a table to a Hive partitioned data set of .parquet files, with unique filenames:

```sql
COPY orders TO 'orders'
    (FORMAT PARQUET, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN "file_{uuid}");
```
