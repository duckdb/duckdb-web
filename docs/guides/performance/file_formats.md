---
layout: docu
title: File Formats
redirect_from:
  - /docs/guides/performance/file-formats
---

## Handling Parquet Files

DuckDB has advanced support for Parquet files, which includes [directly querying Parquet files](/2021/06/25/querying-parquet).
When deciding on whether to query these files directly or to first load them to the database, you need to consider several factors.

### Reasons for Querying Parquet Files

**Availability of basic statistics:** Parquet files use a columnar storage format and contain basic statistics such as [zonemaps](indexing#zonemaps). Thanks to these features, DuckDB can leverage optimizations such as projection and filter pushdown on Parquet files. Therefore, workloads that combine projection, filtering, and aggregation tend to perform quite well when run on Parquet files.

**Storage considerations:** Loading the data from Parquet files will require approximately the same amount of space for the DuckDB database file. Therefore, if the available disk space is constrained, it is worth running the queries directly on Parquet files.

### Reasons against Querying Parquet Files

**Lack of advanced statistics:** The DuckDB database format has the [hyperloglog statistics](https://en.wikipedia.org/wiki/HyperLogLog) that Parquet files do not have. These improve the accuracy of cardinality estimates, and are especially important if the queries contain a large number of join operators.

**Tip.** If you find that DuckDB produces a suboptimal join order on Parquet files, try loading the Parquet files to DuckDB tables. The improved statistics likely help obtain a better join order.

**Repeated queries:** If you plan to run multiple queries on the same data set, it is worth loading the data into DuckDB. The queries will always be somewhat faster, which over time amortizes the initial load time.

**High decompression times:** Some Parquet files are compressed using heavyweight compression algorithms such as gzip. In these cases, querying the Parquet files will necessitate an expensive decompression time every time the file is accessed. Meanwhile, lightweight compression methods like snappy, lz4, zstd, are faster to decompress. You may use the [`parquet_metadata` function](../../data/parquet/metadata#parquet-metadata) to find out the compression algorithm used.

#### Microbenchmark: Running TPC-H on a DuckDB Database vs. Parquet

The queries on the [TPC-H benchmark](/docs/extensions/tpch) run approximately 1.1-5.0x slower on Parquet files than on a DuckDB database.

> Bestpractice If you have the storage space available, and have a join-heavy workload and/or plan to run many queries on the same dataset, load the Parquet files into the database first. The compression algorithm and the row group sizes in the Parquet files have a large effect on performance: study these using the [`parquet_metadata` function](../../data/parquet/metadata#parquet-metadata).

### The Effect of Row Group Sizes

DuckDB works best on Parquet files with row groups of 100K-1M rows each. The reason for this is that DuckDB can only [parallelize over row groups](how_to_tune_workloads#parallelism-multi-core-processing) – so if a Parquet file has a single giant row group it can only be processed by a single thread. You can use the [`parquet_metadata` function](../../data/parquet/metadata#parquet-metadata) to figure out how many row groups a Parquet file has. When writing Parquet files, use the [`row_group_size`](../../sql/statements/copy#parquet-options) option.

#### Microbenchmark: Running Aggregation Query at Different Row Group Sizes

We run a simple aggregation query over Parquet files using different row group sizes, selected between 960 and 1,966,080. The results are as follows.

<div class="narrow_table"></div>

| Row Group Size | Execution Time |
|----------------|----------------|
| 960            | 8.77s          |
| 1920           | 8.95s          |
| 3840           | 4.33s          |
| 7680           | 2.35s          |
| 15360          | 1.58s          |
| 30720          | 1.17s          |
| 61440          | 0.94s          |
| 122880         | 0.87s          |
| 245760         | 0.93s          |
| 491520         | 0.95s          |
| 983040         | 0.97s          |
| 1966080        | 0.88s          |

The results show that row group sizes <5,000 have a strongly detrimental effect, making runtimes more than 5-10x larger than ideally-sized row groups, while row group sizes between 5,000 and 20,000 are still 1.5-2.5x off from best performance. Above row group size of 100,000, the differences are small: the gap is about 10% between the best and the worst runtime.

### Parquet File Sizes

DuckDB can also parallelize across multiple Parquet files. It is advisable to have at least as many total row groups across all files as there are CPU threads. For example, with a machine having 10 threads, both 10 files with 1 row group or 1 file with 10 row groups will achieve full parallelism. It is also beneficial to keep the size of individual Parquet files moderate.

> Bestpractice The ideal range is between 100MB and 10GB per individual Parquet file.

### Hive Partitioning for Filter Pushdown

When querying many files with filter conditions, performance can be improved by using a [Hive-format folder structure](../../data/partitioning/hive_partitioning) to partition the data along the columns used in the filter condition. DuckDB will only need to read the folders and files that meet the filter criteria. This can be especially helpful when querying remote files.

### More Tips on Reading and Writing Parquet Files

For tips on reading and writing Parquet files, see the [Parquet Tips page](../../data/parquet/tips).

## Loading CSV Files

CSV files are often distributed in compressed format such as GZIP archives (`.csv.gz`). DuckDB can decompress these files on the fly. In fact, this is typically faster than decompressing the files first and loading them due to reduced IO.

<div class="narrow_table"></div>

| Schema | Load Time |
|---|---|
| Load from GZIP-compressed CSV files (`.csv.gz`) | 107.1s |
| Decompressing (using parallel `gunzip`) and loading from decompressed CSV files | 121.3s |

### Loading Many Small CSV Files

The [CSV reader](../../data/csv/overview) runs the [CSV sniffer](/2023/10/27/csv-sniffer) on all files. For many small files, this may cause an unnecessarily high overhead.
A potential optimization to speed this up is to turn the sniffer off. Assuming that all files have the same CSV dialect and colum names/types, get the sniffer options as follows:

```sql
.mode line
SELECT Prompt FROM sniff_csv('part-0001.csv');
```

```text
Prompt = FROM read_csv('file_path.csv', auto_detect=false, delim=',', quote='"', escape='"', new_line='\n', skip=0, header=true, columns={'hello': 'BIGINT', 'world': 'VARCHAR'});
```

Then, you can adjust `read_csv` command, by e.g. applying filename expansion (globbing), and run with the rest of the options detected by the sniffer:

```sql
FROM read_csv('part-*.csv', auto_detect=false, delim=',', quote='"', escape='"', new_line='\n', skip=0, header=true, columns={'hello': 'BIGINT', 'world': 'VARCHAR'});
```
