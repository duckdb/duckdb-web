---
layout: post
title: "CSV Files: Dethroning Parquet as the Ultimate Storage File Format — or Not?"
author: "Pedro Holanda"
thumb: "/images/blog/thumbs/csv-vs-parquet.svg"
image: "/images/blog/thumbs/csv-vs-parquet.png"
excerpt: "Data analytics primarily uses two types of storage format files: human-readable text files like CSV and performance-driven binary files like Parquet. This blog post compares these two formats in an ultimate showdown of performance and flexibility, where there can be only one winner."
tags: ["benchmark"]
---

## File Formats

### CSV Files

Data is most [commonly stored](https://www.vldb.org/pvldb/vol17/p3694-saxena.pdf) in human-readable file formats, like JSON or CSV files. These file formats are easy to operate on, since anyone with a text editor can simply open, alter, and understand them.

For many years, CSV files have had a bad reputation for being slow and cumbersome to work with. In practice, if you want to operate on a CSV file using your favorite database system, you must follow this recipe:

1. Manually discover its schema by opening the file in a text editor.
2. Create a table with the given schema.
3. Manually figure out the dialect of the file (e.g., which character is used for a quote?)
4. Load the file into the table using a `COPY` statement and with the dialect set.
5. Start querying it.

Not only is this process tedious, but parallelizing a CSV file reader is [far from trivial](https://www.microsoft.com/en-us/research/uploads/prod/2019/04/chunker-sigmod19.pdf). This means most systems either process it single-threaded or use a two-pass approach.

Additionally, [CSV files are wild](https://youtu.be/YrqSp8m7fmk?si=v5rmFWGJtpiU5_PX&t=624): although [RFC-4180](https://www.ietf.org/rfc/rfc4180.txt) exists as a CSV standard, it is [commonly ignored](https://aic.ai.wu.ac.at/~polleres/publications/mitl-etal-2016OBD.pdf). Systems must therefore be sufficiently robust to handle these files as if they come straight from the wild west.

Last but not least, CSV files are wasteful: data is always laid out as strings. For example, numeric values like `1000000000` take 10 bytes instead of 4 bytes if stored as an `int32`. Additionally, since the data layout is row-wise, opportunities to apply [lightweight columnar compression]({% post_url 2022-10-28-lightweight-compression %}) are lost.

### Parquet Files

Due to these shortcomings, performance-driven file formats like Parquet have gained significant popularity in recent years. Parquet files cannot be opened by general text editors, cannot be easily edited, and have a rigid schema. However, they store data in columns, apply various compression techniques, partition the data into row groups, maintain statistics about these row groups, and define their schema directly in the file.

These features make Parquet a monolith of a file format — highly inflexible but efficient and fast. It is easy to read data from a Parquet file since the schema is well-defined. Parallelizing a scanner is straightforward, as each thread can independently process a row group. Filter pushdown is also simple to implement, as each row group contains statistical metadata, and the file sizes are very small.

The conclusion should be simple: if you have small files and need flexibility, CSV files are fine. However, for data analysis, one should pivot to Parquet files, right? Well, this pivot may not be a hard requirement anymore – read on to find out why!

## Reading CSV Files in DuckDB

For the past few releases, DuckDB has doubled down on delivering not only an easy-to-use CSV scanner but also an extremely performant one. This scanner features its own custom [CSV sniffer]({% post_url 2023-10-27-csv-sniffer %}), parallelization algorithm, buffer manager, casting mechanisms, and state machine-based parser.

For usability, the previous paradigm of manual schema discovery and table creation has been changed. Instead, DuckDB now utilizes a CSV Sniffer, similar to those found in dataframe libraries like Pandas.
This allows for querying CSV files as easily as:

```sql
FROM 'path/to/file.csv';
```

Or tables to be created from CSV files, without any prior schema definition with:

```sql
CREATE TABLE t AS FROM 'path/to/file.csv';
```

Furthermore, the reader became one of the fastest CSV readers in analytical systems, as can be seen by the load times of the [latest iteration](https://github.com/ClickHouse/ClickBench/commit/0aba4247ce227b3058d22846ca39826d27262fe0) of [ClickBench](https://benchmark.clickhouse.com/#eyJzeXN0ZW0iOnsiQWxsb3lEQiI6ZmFsc2UsIkFsbG95REIgKHR1bmVkKSI6ZmFsc2UsIkF0aGVuYSAocGFydGl0aW9uZWQpIjpmYWxzZSwiQXRoZW5hIChzaW5nbGUpIjpmYWxzZSwiQXVyb3JhIGZvciBNeVNRTCI6ZmFsc2UsIkF1cm9yYSBmb3IgUG9zdGdyZVNRTCI6ZmFsc2UsIkJ5Q29uaXR5IjpmYWxzZSwiQnl0ZUhvdXNlIjpmYWxzZSwiY2hEQiAoRGF0YUZyYW1lKSI6ZmFsc2UsImNoREIgKFBhcnF1ZXQsIHBhcnRpdGlvbmVkKSI6ZmFsc2UsImNoREIiOmZhbHNlLCJDaXR1cyI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQgKGF3cykiOmZhbHNlLCJDbGlja0hvdXNlIENsb3VkIChhenVyZSkiOmZhbHNlLCJDbGlja0hvdXNlIENsb3VkIChnY3ApIjpmYWxzZSwiQ2xpY2tIb3VzZSAoZGF0YSBsYWtlLCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJDbGlja0hvdXNlIChkYXRhIGxha2UsIHNpbmdsZSkiOmZhbHNlLCJDbGlja0hvdXNlIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJDbGlja0hvdXNlIChQYXJxdWV0LCBzaW5nbGUpIjpmYWxzZSwiQ2xpY2tIb3VzZSAod2ViKSI6ZmFsc2UsIkNsaWNrSG91c2UiOnRydWUsIkNsaWNrSG91c2UgKHR1bmVkKSI6dHJ1ZSwiQ2xpY2tIb3VzZSAodHVuZWQsIG1lbW9yeSkiOnRydWUsIkNsb3VkYmVycnkiOmZhbHNlLCJDcmF0ZURCIjpmYWxzZSwiQ3J1bmNoeSBCcmlkZ2UgZm9yIEFuYWx5dGljcyAoUGFycXVldCkiOmZhbHNlLCJEYXRhYmVuZCI6dHJ1ZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRGF0YUZ1c2lvbiAoUGFycXVldCwgc2luZ2xlKSI6ZmFsc2UsIkFwYWNoZSBEb3JpcyI6ZmFsc2UsIkRyaWxsIjpmYWxzZSwiRHJ1aWQiOmZhbHNlLCJEdWNrREIgKERhdGFGcmFtZSkiOmZhbHNlLCJEdWNrREIgKG1lbW9yeSkiOnRydWUsIkR1Y2tEQiAoUGFycXVldCwgcGFydGl0aW9uZWQpIjpmYWxzZSwiRHVja0RCIjpmYWxzZSwiRWxhc3RpY3NlYXJjaCI6ZmFsc2UsIkVsYXN0aWNzZWFyY2ggKHR1bmVkKSI6ZmFsc2UsIkdsYXJlREIiOmZhbHNlLCJHcmVlbnBsdW0iOmZhbHNlLCJIZWF2eUFJIjpmYWxzZSwiSHlkcmEiOmZhbHNlLCJJbmZvYnJpZ2h0IjpmYWxzZSwiS2luZXRpY2EiOmZhbHNlLCJNYXJpYURCIENvbHVtblN0b3JlIjpmYWxzZSwiTWFyaWFEQiI6ZmFsc2UsIk1vbmV0REIiOmZhbHNlLCJNb25nb0RCIjpmYWxzZSwiTW90aGVyRHVjayI6ZmFsc2UsIk15U1FMIChNeUlTQU0pIjpmYWxzZSwiTXlTUUwiOmZhbHNlLCJPY3RvU1FMIjpmYWxzZSwiT3hsYSI6ZmFsc2UsIlBhbmRhcyAoRGF0YUZyYW1lKSI6ZmFsc2UsIlBhcmFkZURCIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJQYXJhZGVEQiAoUGFycXVldCwgc2luZ2xlKSI6ZmFsc2UsInBnX2R1Y2tkYiAoTW90aGVyRHVjayBlbmFibGVkKSI6ZmFsc2UsInBnX2R1Y2tkYiI6ZmFsc2UsIlBpbm90IjpmYWxzZSwiUG9sYXJzIChEYXRhRnJhbWUpIjpmYWxzZSwiUG9sYXJzIChQYXJxdWV0KSI6ZmFsc2UsIlBvc3RncmVTUUwgKHR1bmVkKSI6ZmFsc2UsIlBvc3RncmVTUUwiOmZhbHNlLCJRdWVzdERCIjp0cnVlLCJSZWRzaGlmdCI6ZmFsc2UsIlNlbGVjdERCIjpmYWxzZSwiU2luZ2xlU3RvcmUiOmZhbHNlLCJTbm93Zmxha2UiOmZhbHNlLCJTcGFyayI6ZmFsc2UsIlNRTGl0ZSI6ZmFsc2UsIlN0YXJSb2NrcyI6ZmFsc2UsIlRhYmxlc3BhY2UiOmZhbHNlLCJUZW1ibyBPTEFQIChjb2x1bW5hcikiOmZhbHNlLCJUaW1lc2NhbGUgQ2xvdWQiOmZhbHNlLCJUaW1lc2NhbGVEQiAobm8gY29sdW1uc3RvcmUpIjpmYWxzZSwiVGltZXNjYWxlREIiOmZhbHNlLCJUaW55YmlyZCAoRnJlZSBUcmlhbCkiOmZhbHNlLCJVbWJyYSI6dHJ1ZX0sInR5cGUiOnsiQyI6dHJ1ZSwiY29sdW1uLW9yaWVudGVkIjp0cnVlLCJQb3N0Z3JlU1FMIGNvbXBhdGlibGUiOnRydWUsIm1hbmFnZWQiOnRydWUsImdjcCI6dHJ1ZSwic3RhdGVsZXNzIjp0cnVlLCJKYXZhIjp0cnVlLCJDKysiOnRydWUsIk15U1FMIGNvbXBhdGlibGUiOnRydWUsInJvdy1vcmllbnRlZCI6dHJ1ZSwiQ2xpY2tIb3VzZSBkZXJpdmF0aXZlIjp0cnVlLCJlbWJlZGRlZCI6dHJ1ZSwic2VydmVybGVzcyI6dHJ1ZSwiZGF0YWZyYW1lIjp0cnVlLCJhd3MiOnRydWUsImF6dXJlIjp0cnVlLCJhbmFseXRpY2FsIjp0cnVlLCJSdXN0Ijp0cnVlLCJzZWFyY2giOnRydWUsImRvY3VtZW50Ijp0cnVlLCJHbyI6dHJ1ZSwic29tZXdoYXQgUG9zdGdyZVNRTCBjb21wYXRpYmxlIjp0cnVlLCJEYXRhRnJhbWUiOnRydWUsInBhcnF1ZXQiOnRydWUsInRpbWUtc2VyaWVzIjp0cnVlfSwibWFjaGluZSI6eyIxNiB2Q1BVIDEyOEdCIjpmYWxzZSwiOCB2Q1BVIDY0R0IiOmZhbHNlLCJzZXJ2ZXJsZXNzIjpmYWxzZSwiMTZhY3UiOmZhbHNlLCJjNmEuNHhsYXJnZSwgNTAwZ2IgZ3AyIjpmYWxzZSwiTCI6ZmFsc2UsIk0iOmZhbHNlLCJTIjpmYWxzZSwiWFMiOmZhbHNlLCJjNmEubWV0YWwsIDUwMGdiIGdwMiI6dHJ1ZSwiMTkyR0IiOmZhbHNlLCIyNEdCIjpmYWxzZSwiMzYwR0IiOmZhbHNlLCI0OEdCIjpmYWxzZSwiNzIwR0IiOmZhbHNlLCI5NkdCIjpmYWxzZSwiZGV2IjpmYWxzZSwiNzA4R0IiOmZhbHNlLCJjNW4uNHhsYXJnZSwgNTAwZ2IgZ3AyIjpmYWxzZSwiQW5hbHl0aWNzLTI1NkdCICg2NCB2Q29yZXMsIDI1NiBHQikiOmZhbHNlLCJjNS40eGxhcmdlLCA1MDBnYiBncDIiOmZhbHNlLCJjNmEuNHhsYXJnZSwgMTUwMGdiIGdwMiI6ZmFsc2UsImNsb3VkIjpmYWxzZSwiZGMyLjh4bGFyZ2UiOmZhbHNlLCJyYTMuMTZ4bGFyZ2UiOmZhbHNlLCJyYTMuNHhsYXJnZSI6ZmFsc2UsInJhMy54bHBsdXMiOmZhbHNlLCJTMiI6ZmFsc2UsIlMyNCI6ZmFsc2UsIjJYTCI6ZmFsc2UsIjNYTCI6ZmFsc2UsIjRYTCI6ZmFsc2UsIlhMIjpmYWxzZSwiTDEgLSAxNkNQVSAzMkdCIjpmYWxzZSwiYzZhLjR4bGFyZ2UsIDUwMGdiIGdwMyI6ZmFsc2UsIjE2IHZDUFUgNjRHQiI6ZmFsc2UsIjQgdkNQVSAxNkdCIjpmYWxzZSwiOCB2Q1BVIDMyR0IiOmZhbHNlfSwiY2x1c3Rlcl9zaXplIjp7IjEiOnRydWUsIjIiOmZhbHNlLCI0IjpmYWxzZSwiOCI6ZmFsc2UsIjE2IjpmYWxzZSwiMzIiOmZhbHNlLCI2NCI6ZmFsc2UsIjEyOCI6ZmFsc2UsInNlcnZlcmxlc3MiOmZhbHNlLCJ1bmRlZmluZWQiOmZhbHNlfSwibWV0cmljIjoibG9hZCIsInF1ZXJpZXMiOlt0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlXX0=). In this benchmark, the data is loaded from an [82 GB uncompressed CSV file](https://datasets.clickhouse.com/hits_compatible/hits.csv.gz) into a database table.

<div align="center">
    <img src="/images/blog/csv-vs-parquet-clickbench.png"
    alt="Image showing the ClickBench result 2024-12-05"
    width="800px"
    /></div>
<div align="center">ClickBench CSV loading times (2024-12-05)</div>

## Comparing CSV and Parquet

With the large boost boost in usability and performance for the CSV reader, one might ask: what is the actual difference in performance when loading a CSV file compared to a Parquet file into a table? Additionally, how do these formats differ when running queries directly on them?

To find out, we will run a few examples using both CSV and Parquet files containing TPC-H data to shed light on their differences. All scripts used to generate the benchmarks of this blogpost can be found in a [repository](https://github.com/pdet/csv_vs_parquet).

### Usability

In terms of usability, scanning CSV files and Parquet files can differ significantly.

In simple cases, where all options are correctly detected by DuckDB, running queries on either CSV or Parquet files can be done directly.

```sql
FROM 'path/to/file.csv';
FROM 'path/to/file.parquet';
```

Things can differ drastically for wild, rule-breaking [Arthur Morgan](https://reddead.fandom.com/wiki/Arthur_Morgan)-like CSV files. This is evident from the number of parameters that can be set for each scanner. The [Parquet]({% link docs/data/parquet/overview.md %}) scanner has a total of six parameters that can alter how the file is read. For the majority of cases, the user will never need to manually adjust any of them.

The CSV reader, on the other hand, depends on the sniffer being able to automatically detect many different configuration options. For example: What is the delimiter? How many rows should it skip from the top of the file? Are there any comments? And so on. This results in over [30 configuration options]({% link docs/data/csv/overview.md %}) that the user might have to manually adjust to properly parse their CSV file. Again, this number of options is necessary due to the lack of a widely adopted standard. However, in most scenarios, users can rely on the sniffer or, at most, change one or two options.

The CSV reader also has an extensive error-handling system and will always provide suggestions for options to review if something goes wrong.

To give you an example of how the DuckDB error-reporting system works, consider the following CSV file:

```csv
name;age
Clint Eastwood;94
Samuel L. Jackson
```

In this file, the third line is missing the value for the `age` column.

```console
Invalid Input Error: CSV Error on Line: 3
Original Line: Samuel L. Jackson
Expected Number of Columns: 2 Found: 1
Possible fixes:
* Enable null padding (null_padding=true) to replace missing values with NULL
* Enable ignore errors (ignore_errors=true) to skip this row

  file = western_actors.csv
  delimiter = , (Auto-Detected)
  quote = " (Auto-Detected)
  escape = " (Auto-Detected)
  new_line = \n (Auto-Detected)
  header = false (Auto-Detected)
  skip_rows = 0 (Auto-Detected)
  comment = \0 (Auto-Detected)
  date_format =  (Auto-Detected)
  timestamp_format =  (Auto-Detected)
  null_padding = 0
  sample_size = 20480
  ignore_errors = false
  all_varchar = 0
```

DuckDB provides detailed information about any errors encountered. It highlights the line of the CSV file where the issue occurred, presents the original line, and suggests possible fixes for the error, such as ignoring the problematic line or filling missing values with `NULL`. It also displays the full configuration used to scan the file and indicates whether the options were auto-detected or manually set.

The bottom line here is that, even with the advancements in CSV usage, the strictness of Parquet files make them much easier to operate on.

Of course, if you need to open your file in a text editor or Excel, you will need to have your data in CSV format. Note that Parquet files do have some visualizers, like [TAD](https://www.tadviewer.com/).

### Performance

There are primarily two ways to operate on files using DuckDB:

1. The user creates a DuckDB table from the file and uses the table in future queries. This is a loading process, commonly used if you want to store your data as DuckDB tables or if you will run many queries on them. Also, note that these are the only possible scenarios for most database systems (e.g., Oracle, SQL Server, PostgreSQL, SQLite, ...).

2. One might run a query directly on the file scanner without creating a table. This is useful for scenarios where the user has limitations on memory and disk space, or if queries on these files are only executed once. Note that this scenario is typically not supported by database systems but is common for dataframe libraries (e.g., Pandas).

To fairly compare the scanners, we provide the table schemas upfront, ensuring that the scanners produce the exact same data types. We also set `preserve_insertion_order = false`, as this can impact the parallelization of both scanners, and set `max_temp_directory_size = '0GB'` to ensure no data is spilled to disk, with all experiments running fully in memory.

We use the default writers for both CSV files and Parquet (with the default Snappy compression), and also run a variation of Parquet with `CODEC 'zstd', COMPRESSION_LEVEL 1`, as this can speed up querying/loading times.

For all experiments, we use an Apple M1 Max, with 64 GB RAM. We use TPC-H scale factor 20 and report the median times from 5 runs.

#### Creating Tables

For creating the table, we focus on the `lineitem` table.

After defining the schema, both files can be loaded with a simple `COPY` statement, with no additional parameters set. Note that even with the schema defined, the CSV sniffer will still be executed to determine the dialect (e.g., quote character, delimiter character, etc.) and match types and names.

|      Name      | Time (s) | Size (GB) |
|----------------|---------:|----------:|
| CSV            |    11.76 |     15.95 |
| Parquet Snappy |     5.21 |      3.78 |
| Parquet ZSTD   |     5.52 |      3.22 |

We can see that the Parquet files are definitely smaller. About 5× smaller than the CSV file, but the performance difference is not drastic.

The CSV scanner is only about 2× slower than the Parquet scanner. It's also important to note that some of the cost associated with these operations (~1-2 seconds) is related to the insertion into the DuckDB table, not the scanner itself.

However, it is still important to consider this in the comparison. In practice, the raw CSV scanner is about 3× slower than the Parquet scanner, which is a considerable difference but much smaller than one might initially think.

#### Directly Querying Files

We will run two different TPC-H queries on our files.

**Query 01.** First, we run TPC-H Q01. This query operates solely on the `Lineitem` table, performing an aggregation and grouping with a filter. It filters on one column and projects 7 out of the 16 columns from `Lineitem`.

Therefore, this query will stress the filter pushdown, which is [supported by the Parquet reader]({% link docs/data/parquet/overview.md %}#partial-reading) but not the CSV reader, and the projection pushdown, which is supported by both.

```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum(l_quantity) AS sum_qty,
    sum(l_extendedprice) AS sum_base_price,
    sum(l_extendedprice * (1 - l_discount)) AS sum_disc_price,
    sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,
    avg(l_quantity) AS avg_qty,
    avg(l_extendedprice) AS avg_price,
    avg(l_discount) AS avg_disc,
    count(*) AS count_order
FROM
    lineitem
WHERE
    l_shipdate <= CAST('1996-09-02' AS date)
GROUP BY
    l_returnflag,
    l_linestatus
ORDER BY
    l_returnflag,
    l_linestatus;
```

|      Name      | Time (s) |
|----------------|---------:|
| CSV            |     6.72 |
| Parquet Snappy |     0.88 |
| Parquet ZSTD   |     0.95 |

We can see that running this query directly on our file presents a much larger performance gap of approximately 7x compared to simply loading the data into the table. In the Parquet file, we can directly skip row groups that do not match our filter `l_shipdate <= CAST('1996-09-02' AS date)`. Note that this filter, eliminates approximately 30% of the data. Not only that, but we can also skip individual rows that do not match the filter. Additionally, since the Parquet format is column-oriented, we can completely skip any computation on columns that are not projected.

Unfortunately, the CSV reader does not benefit from these filters. Since it lacks partitions, it can't efficiently skip parts of the data. Theoretically, a CSV scanner could skip the computation of rows that do not match a filter, but this is not currently implemented.

Furthermore, the CSV projection skips much of the computation on a column (e.g., it does not cast or copy the value), but it still must parse the value to be able to skip it.

**Query 21.** Query 21 is a query that not only heavily depends on filter and projection pushdown but also relies significantly on join ordering based on statistics to achieve good performance. In this query, four different files are used and joined together.

```sql
SELECT
    s_name,
    count(*) AS numwait
FROM
    supplier,
    lineitem l1,
    orders,
    nation
WHERE
    s_suppkey = l1.l_suppkey
    AND o_orderkey = l1.l_orderkey
    AND o_orderstatus = 'F'
    AND l1.l_receiptdate > l1.l_commitdate
    AND EXISTS (
        SELECT
            *
        FROM
            lineitem l2
        WHERE
            l2.l_orderkey = l1.l_orderkey
            AND l2.l_suppkey <> l1.l_suppkey)
    AND NOT EXISTS (
        SELECT
            *
        FROM
            lineitem l3
        WHERE
            l3.l_orderkey = l1.l_orderkey
            AND l3.l_suppkey <> l1.l_suppkey
            AND l3.l_receiptdate > l3.l_commitdate)
    AND s_nationkey = n_nationkey
    AND n_name = 'SAUDI ARABIA'
GROUP BY
    s_name
ORDER BY
    numwait DESC,
    s_name
LIMIT 100;
```

|      Name      | Time (s) |
|----------------|---------:|
| CSV            |    19.95 |
| Parquet Snappy |     2.08 |
| Parquet ZSTD   |     2.12 |

We can see that this query now has a performance difference of approximately 10×. We observe an effect similar to Query 01, but now we also incur the additional cost of performing join ordering with no statistical information for the CSV file.

## Conclusion

There is no doubt that the performance of CSV file scanning has drastically increased over the years. If we were to take a guess at the performance difference in table creation a few years ago, the answer would probably have been at least one order of magnitude.

This is excellent, as it allows data to be exported from legacy systems that do not support performance-driven file formats.

But oh boy, don't let super-convenient and fast CSV readers fool you. Your data is still best kept in self-describing, column-binary compressed formats like Parquet — or the DuckDB file format, of course! They are much smaller and more consistent. Additionally, running queries directly on Parquet files is much more beneficial due to efficient projection/filter pushdown and available statistics.

One thing to note is that there exists an extensive body of work on [indexing CSV files](https://stratos.seas.harvard.edu/sites/scholar.harvard.edu/files/stratos/files/nodb-cacm.pdf) (i.e., building statistics in a way) to speed up future queries and enable filter pushdown. However, DuckDB does not perform these operations yet.

Bottom line: Parquet is still the undisputed champion for most scenarios, but we will continue working on closing this gap wherever possible.
