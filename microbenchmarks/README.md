# Microbenchmarks

This directory contains microbenchmarks used for the [Performance Guide](https://duckdb.org/docs/guides/performance/overview).
For details, see the [Benchmarks page](https://duckdb.org/docs/guides/performance/benchmarks).

## Scripts

| Script | Performance Guide section | Dataset |
|---|---|---|
| `ub-comments.sh` | Schema: Using Timestamps; Indexing: The Effect of Ordering | [LDBC SF300 Comment `creationDate` column](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) |
| `ub-join-type.sh` | Schema: Joining on Strings | [LDBC SF100 Comment table](https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst) |
| `ub-pk.sh` | Schema: The Effect of Primary Keys | [LDBC SF300 Comment table](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) |
| `ub-row-group-size.sh` | File Formats: The Effect of Row Group Sizes | [LDBC SF300 Comment table](https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst) |
| `ub-load-csv.sh` | File Formats: Loading CSV Files | [LDBC SF100 Comment table](https://blobs.duckdb.org/data/ldbc-sf100-comments.tar.zst) |
| `ub-tpch-parquet.sh` | File Formats: Running TPC-H on a DuckDB Database vs. Parquet | TPC-H SF30 (generated) |
| `ub-in-memory-vs-persistent.sh` | How to Tune Workloads: Persistent vs. In-Memory Tables | TPC-H SF30 (generated) |

The `.tar.zst` archives can be extracted on the fly:

```bash
curl -s https://blobs.duckdb.org/data/ldbc-sf300-comments.tar.zst | zstd -dc | tar -x -C ⟨data_dir⟩
```

## Running the Scripts

The scripts are configured using the following environment variables (see `common.sh`):

* `DUCKDB`: path to the DuckDB CLI binary (default: `duckdb`)
* `DATA_DIR`: directory containing the input datasets, e.g., the `ldbc-sf300-comments` directory (default: current directory)
* `WORK_DIR`: directory where the database files and the results are created (default: current directory)
* `SF`: scale factor (the default depends on the script)
* `RUNS`: number of times each query is executed, the median is reported (default: 5)

For example:

```bash
DUCKDB=/path/to/duckdb DATA_DIR=~/ldbc-data WORK_DIR=/tmp/ub SF=300 ./ub-pk.sh
```

The SF300 benchmarks require approx. 60 GB of free disk space in addition to the input data.
