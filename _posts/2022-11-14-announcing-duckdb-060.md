---
layout: post
title:  "Announcing DuckDB 0.6.0"
author: Mark Raasveldt
excerpt_separator: <!--more-->
---

<img src="/images/blog/white-headed-duck.jpeg"
     alt="Image of white-headed duck"
     width=200px
     />

The DuckDB team is happy to announce the latest DuckDB version (0.6.0) has been released. This release of DuckDB is named "Oxyura" after the [White-headed duck (Oxyura leucocephala)](https://en.wikipedia.org/wiki/White-headed_duck) which is an endangered species native to Eurasia.

To install the new version, please visit the [installation guide](https://duckdb.org/docs/installation/index). The full release notes can be found [here](https://github.com/duckdb/duckdb/releases/tag/v0.6.0).

<!--more-->

#### What's in 0.6.0
The new release contains many improvements to the storage system, general performance improvements, memory management improvements and new features. Below is a summary of the most impactful changes, together with the linked PRs that implement the features.

#### Storage Improvements
As we are working towards stabilizing the storage format and moving towards version 1.0, we have been actively working on improving our storage format, including many [compression improvements](https://duckdb.org/2022/10/28/lightweight-compression.html). 

**Optimistic writing to disk.** In previous DuckDB versions, the data of a single transaction was first loaded into memory, and would only be written to disk on a commit. While this works fine when data is loaded in batches that fit in memory, it does not work well when loading a lot of data in a single transaction, such as when ingesting one very large file into the system.

This version introduces [optimistic writing to disk](https://github.com/duckdb/duckdb/pull/4996). When loading large data sets in a single transaction, data is compressed and streamed to the database file, even before the `COMMIT` has occurred. When the transaction is committed, the data will already have been written to disk, and no further writing has to happen. On a rollback, any optimistically written data is reclaimed by the system. 

**Parallel data loading**. In addition to optimistically writing data to disk, this release includes support for parallel data loading into individual tables. This greatly improves performance of data loading on machines that have multiple cores (i.e. all modern machines).

Below is a benchmark comparing loading time of 150 million rows of the Taxi dataset from a Parquet file on an M1 Max with 10 cores:

| Version | Load Time |
|---------|-----------|
| v0.5.1  | 91.4s     |
| v0.6.0  | 17.2s     |

DuckDB supports two modes - the [`order-preserving`](https://github.com/duckdb/duckdb/pull/5082) and the [`non-order-preserving`](https://github.com/duckdb/duckdb/pull/5033) parallel data load.

The order-preserving load preserves the insertion order so that e.g. the first line in your CSV file is the first line in the DuckDB table. The non-order-preserving load does not offer such guarantees - and instead might re-order the data on load. By default the order-preserving load is used, which involves some extra book-keeping. The preservation of insertion order can be disabled using the `SET preserve_insertion_order=false` statement.

#### Compression Improvements

**FSST**. The [Fast Static Symbol Table](https://github.com/duckdb/duckdb/pull/4366) compression algorithm is introduced in this version. This state-of-the-art compression algorithm compresses data *inside* strings using a dictionary, while maintaining support for efficient scans and random look-ups. This greatly increases the compression ratio of strings that have many unique values but with common elements, such as e-mail addresses or URLs.

The compression ratio improvements of the TPC-H SF1 dataset are shown below:

|    Compression    | Size  |
|-------------------|-------|
| Uncompressed      | 761MB |
| Dictionary        | 510MB |
| FSST + Dictionary | 251MB |

**Chimp**. The [Chimp compression algorithm](https://github.com/duckdb/duckdb/pull/4878) is included, which is the state-of-the-art in lightweight floating point compression. Chimp is an improved version of Gorillas, that achieves both a better compression ratio as well as faster decompression speed.

**Patas**. [Patas](https://github.com/duckdb/duckdb/pull/5044) is a novel floating point compression method that iterates upon the Chimp algorithm by optimizing for a single case in the Chimp algorithm. While Patas generally has a slightly lower compression ratio than Chimp, it has significantly faster decompression speed, almost matching uncompressed data in read speed.

The compression ratio of a dataset containing temperatures of cities stored as double (8-byte floating point numbers) is shown below:

|    Compression    | Size  |
|-------------------|------:|
| Uncompressed      | 25.4MB |
| Chimp        | 9.7MB |
| Patas | 10.2MB |

#### Performance Improvements
DuckDB aims to have very high performance for a wide variety of workloads. As such, we are always working to improve performance for various workloads. This release is no different.


**Parallel CSV Loading (Experimental)**. In this release we are launching [a new experimental parallel CSV reader](https://github.com/duckdb/duckdb/pull/5194). This greatly improves the ingestion speed of large CSV files into the system. While we have done our best to make the parallel CSV reader robust - CSV parsing is a minefield as there is such a wide variety of different files out there - so we have marked the reader as experimental for now.

The parallel CSV reader can be enabled by setting the `experimental_parallel_csv` flag to true. We aim to make the parallel CSV reader the default reader in future DuckDB versions.

```sql
SET experimental_parallel_csv=true;
```

Below is the load time of a 720MB CSV file containing the `lineitem` table from the `TPC-H` benchmark, 

|     Variant     | Load Time |
|-----------------|-----------|
| Single Threaded | 3.5s      |
| Parallel        | 0.6s      |

**Parallel CREATE INDEX & Index Memory Management Improvements**. Index creation is also sped up significantly in this release, as [the `CREATE INDEX` statement can now be executed fully in parallel](https://github.com/duckdb/duckdb/pull/4655). In addition, the number of memory allocations done by the ART is greatly reduced through [inlining of small structures](https://github.com/duckdb/duckdb/pull/5292) which both reduces memory size and further improves performance.

The timings of creating an index on a single column with 16 million values is shown below.

| Version | Create Index Time |
|---------|-----------|
| v0.5.1  | 5.92s     |
| v0.6.0  | 1.38s     |

**Parallel COUNT(DISTINCT)**. Aggregates containing `DISTINCT` aggregates, most commonly used for exact distinct count computation (e.g. `COUNT(DISTINCT col)`) previously had to be executed in single-threaded mode. Starting with v0.6.0, [DuckDB can execute these queries in parallel](https://github.com/duckdb/duckdb/pull/5146), leading to large speed-ups.

#### SQL Syntax Improvements
SQL is the primary way of interfacing with DuckDB - and DuckDB [tries to have an easy to use SQL dialect](https://duckdb.org/2022/05/04/friendlier-sql.html). This release contains further improvements to the SQL dialect.

**UNION Type**. This release introduces the [UNION type](https://github.com/duckdb/duckdb/pull/4966), which allows sum types to be stored and queried in DuckDB. For example:

```sql
CREATE TABLE messages(u UNION(num INT, error VARCHAR));
INSERT INTO messages VALUES (42);
INSERT INTO messages VALUES ('oh my globs');
```
```
SELECT * FROM messages;
┌─────────────┐
│      u      │
├─────────────┤
│ 42          │
│ oh my globs │
└─────────────┘
```

Sum types are strongly typed - but they allow a single value in a table to be represented as one of various types. The [union page](https://duckdb.org/docs/sql/data_types/union) in the documentation contains more information on how to use this new composite type.

**FROM-first**. Starting with this release, DuckDB supports starting queries with the [FROM clause](https://github.com/duckdb/duckdb/pull/5076) instead of the `SELECT` clause. In fact, the `SELECT` clause is fully optional now, and defaults to `SELECT *`. That means the following queries are now valid in DuckDB:

```sql
-- SELECT clause is optional, SELECT * is implied (if not included)
FROM tbl;

-- first 5 rows of the table
FROM tbl LIMIT 5;

-- SELECT can be used after the FROM
FROM tbl SELECT l_orderkey;

-- insert all data from tbl1 into tbl2
INSERT INTO tbl2 FROM tbl1;
```

**COLUMNS Expression**. This release adds support for [the `COLUMNS` expression](https://github.com/duckdb/duckdb/pull/5120), inspired by [the Clickhouse syntax](https://clickhouse.com/docs/en/sql-reference/statements/select/#columns-expression). The `COLUMNS` expression allows you to execute expressions or functions on multiple columns without having to duplicate the full expression.

```sql
CREATE TABLE obs(id INT, val1 INT, val2 INT);
INSERT INTO obs VALUES (1, 10, 100), (2, 20, NULL), (3, NULL, 300);
SELECT MIN(COLUMNS(*)), COUNT(*) from obs;
```
```
┌─────────────┬───────────────┬───────────────┬──────────────┐
│ min(obs.id) │ min(obs.val1) │ min(obs.val2) │ count_star() │
├─────────────┼───────────────┼───────────────┼──────────────┤
│ 1           │ 10            │ 100           │ 3            │
└─────────────┴───────────────┴───────────────┴──────────────┘
```

The `COLUMNS` expression supports all star expressions, including [the `EXCLUDE` and `REPLACE` syntax](https://duckdb.org/docs/sql/query_syntax/select). In addition, the `COLUMNS` expression can take a regular expression as parameter:

```sql
SELECT COLUMNS('val[0-9]+') from obs;
```
```
┌──────┬──────┐
│ val1 │ val2 │
├──────┼──────┤
│ 10   │ 100  │
│ 20   │ NULL │
│ NULL │ 300  │
└──────┴──────┘
```

**List comprehension support**. List comprehension is an elegant and powerful way of defining operations on lists. DuckDB now also supports [list comprehension](https://github.com/duckdb/duckdb/pull/4926) as part of its SQL dialect. For example, the query below now works:

```sql
SELECT [x + 1 for x in [1, 2, 3]] AS l;
```
```
┌───────────┐
│     l     │
├───────────┤
│ [2, 3, 4] │
└───────────┘
```

Nested types and structures are very efficiently implemented in DuckDB, and are now also more elegant to work with.

#### Memory Management Improvements

When working with large data sets, memory management is always a potential pain point. By using a streaming execution engine and buffer manager, DuckDB supports many operations on larger than memory data sets. DuckDB also aims to support queries where *intermediate* results do not fit into memory by using disk-spilling techniques, and has support for an [efficient out-of-core sort](https://duckdb.org/2021/08/27/external-sorting.html), [out-of-core window functions](https://duckdb.org/2021/10/13/windowing.html) and [an out-of-core hash join](https://github.com/duckdb/duckdb/pull/4189).

This release further improves on that by greatly optimizing the [out-of-core hash join](https://github.com/duckdb/duckdb/pull/4970), resulting in a much more graceful degradation in performance as the data exceeds the memory limit.

| Memory limit (GB) | Old time (s) | New time (s) |
|:-|:-|:-|
|10|1.97|1.96|
|9|1.97|1.97|
|8|2.23|2.22|
|7|2.23|2.44|
|6|2.27|2.39|
|5|2.27|2.32|
|4|2.81|2.45|
|3|5.60|3.20|
|2|7.69|3.28|
|1|17.73|4.35|

**jemalloc**. In addition, this release bundles the [jemalloc allocator](https://github.com/duckdb/duckdb/pull/4971) with the Linux version of DuckDB by default, which fixes an outstanding issue where the standard `GLIBC` allocator would not return blocks to the operating system, unnecessarily leading to out-of-memory errors on the Linux version. Note that this problem does not occur on MacOS or Windows, and as such we continue using the standard allocators there (at least for now).

#### Shell Improvements
DuckDB has a command-line interface that is adapted from SQLite's command line interface, and therefore supports an extremely similar interface to SQLite. All of the tables in this blog post have been generated using the `.mode markdown` in the CLI.

The DuckDB shell also offers several improvements over the SQLite shell, such as syntax highlighting, and this release includes a few new goodies.

**DuckBox Rendering**. This release includes a [new `.mode duckbox` rendering](https://github.com/duckdb/duckdb/pull/5140) that is used by default. This box rendering adapts to the size of the shell, and leaves out columns and rows to provide a better overview of a result. It very quickly renders large result sets by leaving out rows in the middle. That way, typing `SELECT * FROM tbl` in the shell no longer blows it up. In fact, this can now be used to quickly get a good feel of a dataset instead.

The number of rows that are rendered can be changed by using the `.maxrows X` setting, and you can switch back to the old rendering using the `.mode box` command.

```
D SELECT * FROM '~/Data/nyctaxi/nyc-taxi/2014/04/data.parquet';
┌───────────┬─────────────────────┬─────────────────────┬───┬────────────┬──────────────┬──────────────┐
│ vendor_id │      pickup_at      │     dropoff_at      │ … │ tip_amount │ tolls_amount │ total_amount │
│  varchar  │      timestamp      │      timestamp      │   │   float    │    float     │    float     │
├───────────┼─────────────────────┼─────────────────────┼───┼────────────┼──────────────┼──────────────┤
│ CMT       │ 2014-04-08 08:59:39 │ 2014-04-08 09:28:57 │ … │        3.7 │          0.0 │         22.2 │
│ CMT       │ 2014-04-08 14:59:22 │ 2014-04-08 15:04:52 │ … │        1.3 │          0.0 │          7.8 │
│ CMT       │ 2014-04-08 08:45:28 │ 2014-04-08 08:50:41 │ … │        1.2 │          0.0 │          7.2 │
│ CMT       │ 2014-04-08 08:00:20 │ 2014-04-08 08:11:31 │ … │        1.7 │          0.0 │         10.2 │
│ CMT       │ 2014-04-08 08:38:36 │ 2014-04-08 08:44:37 │ … │        1.2 │          0.0 │          7.2 │
│ CMT       │ 2014-04-08 07:52:53 │ 2014-04-08 07:59:12 │ … │        1.3 │          0.0 │          7.8 │
│ CMT       │ 2014-04-08 16:08:16 │ 2014-04-08 16:12:38 │ … │        1.4 │          0.0 │          8.4 │
│ CMT       │ 2014-04-08 12:04:09 │ 2014-04-08 12:14:30 │ … │        1.7 │          0.0 │         10.2 │
│ CMT       │ 2014-04-08 16:18:38 │ 2014-04-08 16:37:04 │ … │        2.5 │          0.0 │         17.5 │
│ CMT       │ 2014-04-08 15:28:00 │ 2014-04-08 15:34:44 │ … │        1.4 │          0.0 │          8.4 │
│  ·        │          ·          │          ·          │ · │         ·  │           ·  │           ·  │
│  ·        │          ·          │          ·          │ · │         ·  │           ·  │           ·  │
│  ·        │          ·          │          ·          │ · │         ·  │           ·  │           ·  │
│ CMT       │ 2014-04-25 00:09:34 │ 2014-04-25 00:14:52 │ … │        2.5 │          0.0 │         10.0 │
│ CMT       │ 2014-04-25 01:59:39 │ 2014-04-25 02:16:07 │ … │        3.5 │          0.0 │         21.0 │
│ CMT       │ 2014-04-24 23:02:08 │ 2014-04-24 23:47:10 │ … │        8.8 │          0.0 │         52.8 │
│ CMT       │ 2014-04-25 01:27:11 │ 2014-04-25 01:56:53 │ … │        4.6 │          0.0 │         27.6 │
│ CMT       │ 2014-04-25 00:15:46 │ 2014-04-25 00:25:37 │ … │        1.0 │          0.0 │         11.5 │
│ CMT       │ 2014-04-25 00:17:53 │ 2014-04-25 00:22:52 │ … │        1.3 │          0.0 │          7.8 │
│ CMT       │ 2014-04-25 03:13:19 │ 2014-04-25 03:21:50 │ … │        2.1 │          0.0 │         12.6 │
│ CMT       │ 2014-04-24 23:53:03 │ 2014-04-25 00:16:01 │ … │       2.85 │          0.0 │        31.35 │
│ CMT       │ 2014-04-25 00:26:08 │ 2014-04-25 00:31:25 │ … │        1.4 │          0.0 │          8.4 │
│ CMT       │ 2014-04-24 23:21:39 │ 2014-04-24 23:33:57 │ … │        1.0 │          0.0 │         11.5 │
├───────────┴─────────────────────┴─────────────────────┴───┴────────────┴──────────────┴──────────────┤
│ 14618759 rows (20 shown)                                                        18 columns (6 shown) │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


**Context-Aware Auto-Complete**. The shell now also ships with [context-aware auto-complete](https://github.com/duckdb/duckdb/pull/4921). Auto-complete is triggered by pressing the tab character. The shell auto-completes four different groups: (1) keywords, (2) table names + table functions, (3) column names + scalar functions, and (4) file names. The shell looks at the position in the SQL statement to determine which of these auto-completions to trigger. For example:

```sql
S -> SELECT

SELECT s -> student_id

SELECT student_id F -> FROM


SELECT student_id FROM g -> grades

SELECT student_id FROM 'd -> data/

SELECT student_id FROM 'data/ -> data/grades.csv
```

**Progress Bars**. DuckDB has [supported progress bars in queries for a while now](https://github.com/duckdb/duckdb/pull/1432), but they have always been opt-in. In this release we have [prettied up the progress bar](https://github.com/duckdb/duckdb/pull/5187) and enabled it by default in the shell. The progress bar will pop up when a query is run that takes more than 2 seconds, and display an estimated time-to-completion for the query.

```
D copy lineitem to 'lineitem-big.parquet';
 32% ▕███████████████████▏                                        ▏ 
```

In the future we aim to enable the progress bar by default in other clients. For now, this can be done manually by running the following SQL queries:

```sql
PRAGMA enable_progress_bar;
PRAGMA enable_print_progress_bar;
```
