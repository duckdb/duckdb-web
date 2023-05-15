---
layout: docu
title: Partitioned Writes
---

### Examples

```sql
-- write a table to a hive partitioned data set of parquet files
COPY orders TO 'orders' (FORMAT PARQUET, PARTITION_BY (year, month));
-- write a table to a hive partitioned data set of CSV files, allowing overwrites
COPY orders TO 'orders' (FORMAT CSV, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE 1);
```

### Partitioned Writes
When the `partition_by` clause is specified for the `COPY` statement, the files are written in a [hive partitioned](hive_partitioning) folder hierarchy. The target is the name of the root directory (in the example above: `orders`). The files are written in-order in the file hierarchy. Currently, one file is written per thread to each directory.

```
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

> Writing data into many small partitions is expensive. It is generally recommended to have at least  `100MB` of data per partition. 


#### Overwriting

By default the partitioned write will not allow overwriting existing directories. Use the `OVERWRITE_OR_IGNORE` option to allow overwriting an existing directory.

#### Filename pattern

By default files will be named `data_0.parquet` or `data_1.csv`. With the flag `FILENAME_PATTERN` a pattern with `{i}` or `{uuid}` can be defined to create specific filenames:
* `{i}` will be replaced by an index
* `{uuid}` will be replaced by a 128 bits long UUID

```sql
-- write a table to a hive partitioned data set of .parquet files, with an index in the filename
COPY orders TO 'orders' (FORMAT PARQUET, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN "orders_{i}");
-- write a table to a hive partitioned data set of .parquet files, with unique filenames
COPY orders TO 'orders' (FORMAT PARQUET, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE, FILENAME_PATTERN "file_{uuid}");
```
