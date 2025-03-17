---
layout: post
title: "Vertical Stacking as the Relational Model Intended: UNION ALL BY NAME"
author: "Alex Monahan"
thumb: "/images/blog/thumbs/union-all-by-name.svg"
image: "/images/blog/thumbs/union-all-by-name.png"
excerpt: "DuckDB allows vertical stacking of datasets by column name rather than position. This allows DuckDB to read files with schemas that evolve over time and finally aligns SQL with Codd's relational model."
tags: ["using DuckDB"]
---

## Overview

Ever heard of SQL's `CORRESPONDING` keyword?
Yeah, me neither!
Well, it has been in the [SQL standard since at least 1992](https://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt), and almost nobody implemented it!
`CORRESPONDING` was an attempt to fix a flaw in SQL – but it failed.
It's time for SQL to get back to the relational model's roots when stacking data.
Let's wind the clocks back to 1969...

You just picked up your own [Ford Mustang Boss 302](https://en.wikipedia.org/wiki/Boss_302_Mustang), drifting around the corner at every street to make it to the library to read the latest [research report out of IBM by Edgar Codd](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf).
(Do we need a Neflix special about databases?)
Reading that report, wearing plenty of plaid, you gain a critical insight: data should be treated as unordered sets!
(Technically [multisets](https://en.wikipedia.org/wiki/Multiset) – duplicates are everywhere...)
Rows should be treated as unordered and so should columns.
The relational model is _the way_.
Any language built atop the relational model should absolutely follow those core principles.

A few years later, you learn about SQL, and it looks like a pretty cool idea.
Declarative, relational – none of this maintaining order business.
You don't want to be tied down by an ordering, after all.
What if you change your mind about how to query your data?
Sets are the best way to think about these things.

More time passes, and then, you have the need to stack some data in SQL.
Should be easy enough – I can just take two tables and stack them, and the corresponding attributes will map together.
No need to worry about ordering, and certainly no need to make sure that the relations are exactly the same width.

Wait.
This can't be right.

I have to get the order of my columns exactly right?
And I have to have the exact same number of columns in both relations?
Did these SQL folks forget about Codd??

Fast forward just a couple of decades, and DuckDB is making stacking in SQL totally groovy again.

## Making Vertical Stacking Groovy Again

In addition to the traditional [`UNION`]({% link docs/stable/sql/query_syntax/setops.md %}#union) and [`UNION ALL`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-bag-semantics) operators, DuckDB adds both [`UNION BY NAME` and `UNION ALL BY NAME`]({% link docs/stable/sql/query_syntax/setops.md %}#union-all-by-name).
These will vertically stack multiple relations (e.g., `SELECT` statements) by matching on the names of columns independent of their order.
As an example, we provide columns `a` and `b` out of order, and even introduce the entirely new column `c` and stacking will still succeed:

```sql
SELECT
    42 AS a,
    'woot' AS b

UNION ALL BY NAME

SELECT
    'woot2' AS b,
    9001 AS a,
    'more wooting' AS c;
```

|  a   |   b   |      c       |
|-----:|-------|--------------|
| 42   | woot  | NULL         |
| 9001 | woot2 | more wooting |

> Any column that is not present in all relations is filled in with `NULL` in the places where it is missing.

This capability unlocks a variety of useful patterns that can add flexibility and save time.
Some examples include:

* Stacking datasets that have different column orders
* Adding new columns to an analysis, but only for a portion of the rows
* Combining completely unrelated datasets into a single resultset
    * This can be useful if your IDE, BI tool, or API can only return a single resultset at a time, but you need to view multiple datasets

> DuckDB has had this capability since August of 2022, but the performance and scalability of this feature has recently been greatly improved!
See the end of the post for some micro-benchmarks.

### `UNION` vs. `UNION ALL`

If only using the keyword `UNION`, duplicates are removed when stacking.
With `UNION ALL`, duplicates are permitted and the stacking occurs without additional processing.

Unfortunately we have Codd to thank for this confusing bit!
If only `UNION ALL` were the default...
Typically, `UNION ALL` (and its new counterpart `UNION ALL BY NAME`!) are the desired behavior as they faithfully reproduce the input relations, just stacked together.
This is higher performance as well, since the deduplication that occurs with `UNION` can be quite time intensive with large datasets.
And finally, `UNION ALL` [preserves the original row order]({% link docs/stable/sql/dialect/order_preservation.md %}).

### Reading Multiple Files

This column matching functionality becomes particularly useful when querying data from multiple files with different schemas.
DuckDB provides a `union_by_name` boolean parameter in the table functions used to pull external flat files:

* [`read_csv`]({% link docs/stable/data/csv/overview.md %}#parameters)
* [`read_json`]({% link docs/stable/data/json/loading_json.md %}#parameters)
* [`read_parquet`]({% link docs/stable/data/parquet/overview.md %}#parameters)

To read multiple files, DuckDB can use glob patterns within the file path parameter (or a list of files, or a list of glob patterns!).
If those files could have different schemas, adding `union_by_name=True` will allow them to be read and stacked!
Any columns that do not appear in a particular file will be filled with `NULL` values.
For example:

```sql
COPY (SELECT 'Star' AS col1) TO 'star.parquet';
COPY (SELECT 'Wars' AS col2) TO 'wars.parquet';

FROM read_parquet(
    ['star.parquet', 'wars.parquet'],
    union_by_name = true);
```

| col1 | col2 |
|------|------|
| Star | NULL |
| NULL | Wars |

> If your files have different schemas and you did not expect it, DuckDB's friendly error messages will suggest the `union_by_name` parameter!
> There is no need for memorization:
>
> `If you are trying to read files with different schemas, try setting union_by_name=True`

### Data Lakes

It is very common to have schema changes over time in data lakes, so this unlocks many additional uses for DuckDB in those environments.
The secondary effect of this feature is that you may now feel free to change your data lake schemas freely!
Now it is painless to add more attributes to your data lake over time – DuckDB will be ready to handle the analysis!

> DuckDB's extensions to read lakehouse table formats like [Delta]({% link docs/stable/extensions/delta.md %}) and [Iceberg]({% link docs/stable/extensions/iceberg/overview.md %}) handle schema evolution within the formats' own metadata, so `union_by_name` is not needed.

## Inserting Data by Name

Another use case for vertically stacking data is when inserting into an existing table.
The DuckDB syntax of [`INSERT INTO ⟨my_table⟩ BY NAME`{:.language-sql .highlight}]({% link docs/stable/sql/statements/insert.md %}#insert-into--by-name) offers the same flexibility of referring to columns by name rather than by position.
This allows you to provide the data to insert with any column order and even including only a subset of columns.
For example:

```sql
CREATE TABLE year_info (year INTEGER, status VARCHAR);

INSERT INTO year_info BY NAME 
    SELECT 
        'The planet made it through' AS status,
        2024 AS year;

INSERT INTO year_info BY NAME 
    SELECT 
        2025 AS year;

FROM year_info;
```

| year |           status           |
|-----:|----------------------------|
| 2024 | The planet made it through |
| 2025 | NULL                       |

The pre-existing alternative approach was to provide an additional clause that specified the list of columns to be added in the same order as the dataset.
However, this requires the ordering and number of columns to be known up front rather than determined dynamically.
In many cases it also requires specifying columns in two locations: the `INSERT` statement and the `SELECT` statement producing the data.
Ignoring the sage advice of [“Don't Repeat Yourself”](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) has led to more than a few unintended consequences in my own code...
It is always nicer to have a single location to edit rather than having to keep things in sync!

## The Inspirations for `UNION ALL BY NAME`

Other systems and communities have tackled the challenges of stacking messy data for many years.
DuckDB takes inspiration from them and brings their improvements back into SQL!

The most direct inspiration is the [Pandas `concat` function](https://pandas.pydata.org/docs/reference/api/pandas.concat.html).
It was [added in January of 2012](https://github.com/pandas-dev/pandas/commit/35f3322ac5599c83e29fe0d61a606a7f6845b9fa), and from the very beginning it supported the addition of new columns.
Pandas is incredibly widely used and is a significant contributor to the popularity of Python today.
Bringing this capability to SQL can broaden its impact beyond Python and into the other languages that DuckDB supports (Java, Node.js, Go, Rust, etc.).
Databases should learn from dataframes!

PySpark added the function `unionByName` in 2018 and added the abilty to handle the addition of new columns in version 3.1 in March of 2021.
This is another option for Pythonistas, but carries with it the requirement for a Spark cluster and its overhead.

SQL's `UNION` clause had the `CORRESPONDING` keyword since 1992 (!) at the latest, but critically it lacks the ability to handle new or missing columns.
As a result, it is useless for handling schema evolution.

It is our hope that we inspire other SQL engines to become “friendlier” and allow for this flexibility!

## Improved Performance in DuckDB 1.1

DuckDB has supported `UNION ALL BY NAME` since 2022, but [version 1.1]({% post_url 2024-09-09-announcing-duckdb-110 %}) brought some significant scalability and performance improvements.
This feature used to be an “if you have to” approach, but can now be used more broadly!

The first change [reduced memory usage when reading multiple files over the network using `union_by_name`](https://github.com/duckdb/duckdb/pull/12730).
This provides scalability benefits when querying from cloud object storage like S3, especially when the files are large relative to available memory.

The second change was to [parallelize reads across files when using `union_by_name`](https://github.com/duckdb/duckdb/pull/12957).
This expectedly provides a dramatic performance improvement (~6× in the microbenchmark in the PR).

### Micro-Benchmark

This micro-benchmark is a reproduction of the work done by [Daniel Beach](https://dataengineeringcentral.substack.com/about) ([@DataEngDude](https://x.com/dataenggdude)) in [this post](https://dataengineeringcentral.substack.com/p/duckdb-vs-polars-thunderdome).
Thanks to Daniel for his permission to reuse his benchmark for this post!

The benchmark requires reading 16 GB of CSV files stored on S3 that have changing schemas on a cloud instance with 4 GB of memory.
The intent behind it is to process large datasets on small commodity hardware (which is a use case where we want to see DuckDB be helpful!).
The original post uses Linode, but for this post we selected the most similar AWS instance having the same amount of memory ([`c5d.large`](https://instances.vantage.sh/aws/ec2/c5d.large)).

We use two quarters' of CSV files from the [Backblaze dataset](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data#downloadingTheRawTestData) ([2023 Q2](https://blobs.duckdb.org/data/backblaze-data-2023-Q2.zip) and [2023 Q3](https://blobs.duckdb.org/data/backblaze-data-2023-Q3.zip)), which are placed in an S3 bucket.

I modified the query [from here](https://dataengineeringcentral.substack.com/i/141997113/duckdb-reading-gb-from-s-on-a-gb-machine) very slightly to remove the `ignore_errors = true` option.
The benchmark continued to use Python, but I'm just showing the SQL here for better syntax highlighting:

```sql
CREATE OR REPLACE VIEW metrics AS 
    SELECT 
        date,
        sum(failure) AS failures
    FROM read_csv_auto('⟨s3_path⟩/*.csv', union_by_name = true)
    GROUP BY date;

COPY metrics TO '⟨s3_path⟩/results/results.csv';
```

When using a 4 GB instance and an older version of DuckDB (1.0.0), I am able to replicate the out of memory errors that Daniel encountered.
If I upgrade to DuckDB 1.1.3, the queries run successfully! However, they required about 5.8 minutes to complete.

As I dug more deeply into the dataset, I discovered that the columns selected in the benchmark query are present in each file.
In prior versions of DuckDB, just having files with different sets of columns would require the `union_by_name = True` flag, even if the inconsistent or new columns were not used in the query.
However, between the original post and version 1.1.3, DuckDB added the capability to do projection pushdown into CSV files!
This means that only the columns used in the query are actually read from the CSV, not all columns.
As a result, we can actually remove the `union_by_name = true` for the benchmark query and run successfully.
This requires less overhead (since we do not need to invest time checking if all schemas match – we can rely on the first schema that is read).
The simplified query runs in only 4 minutes, but it fails to exercise the capability we discussed – handling schema evolution!

To exercise the `BY NAME` capability, we add a column to the SQL query that is present only in some of the files.

```sql
CREATE OR REPLACE VIEW metrics AS 
    SELECT 
        date,
        count(DISTINCT datacenter) AS datacenters,
        sum(failure) AS failures
    FROM read_csv_auto('⟨s3_path⟩/*.csv', union_by_name = true)
    GROUP BY date;

COPY metrics TO '⟨s3_path⟩/results/results.csv';
```

This query runs in approximately the same amount of time as the original (5.6 minutes), so it is a good proxy for the original while showcasing how DuckDB handles schema evolution!

I then made a few tweaks to improve the performance.
The first change is to skip the creation of a view and complete the operations all in one step.
The reason this improves performance is that DuckDB will try to ensure that a view is correctly defined by binding it when it is created.
Normally, this has negligible overhead (views are a great abstraction!), however when reading from cloud object storage and using `UNION ALL BY NAME`, this triggers a check of the schema of each file, which can take time.
In this case, around 2 minutes!
The updated SQL statement looks like this:

```sql
COPY (
    SELECT 
        date, 
        count(DISTINCT datacenter) AS datacenters,
        sum(failure) AS failures
    FROM read_csv_auto('⟨s3_path⟩/*.csv', union_by_name = true)
    GROUP BY date
) TO '⟨s3_path⟩/results/results.csv';
```

Performance improves to about 4.1 minutes with this change and also reduces the test down to a single query.

We can quantify the overhead of the flexibility that `UNION ALL BY NAME` provides if we keep the improved subquery syntax, but once again remove the `datacenter` column and the `union_by_name` flag.

```sql
COPY (
    SELECT 
        date, 
        sum(failure) AS failures
    FROM read_csv_auto('⟨s3_path⟩/*.csv')
    GROUP BY date
) TO '⟨s3_path⟩/results/results.csv';
```

This query runs in 3.7 minutes, so the overhead of handling schema evolution is only about 10%!
That is a small price to pay for flexibilty and ease of use.

However, we can improve performance further still.
The next change was to increase the number of threads that DuckDB uses.
By default, DuckDB will use a single thread per core.
However, this is a very I/O intensive query (due to the network hops reading from then writing to S3) and less of a CPU intensive one.
DuckDB uses synchronous I/O, so with the default thread count, if a thread is doing I/O, that CPU core is idle.
As a result, using more threads might be more likely to fully utilize network resources, which is the bottleneck in this test.
Here I just made an educated guess that this would help, but monitoring CPU utilization is a better approach.

With 4 threads, instead of the default of 2, performance improves to 3 minutes!

Adding more threads did not meaningfully improve performance any further.
Additional threads do use more memory, but with the improvements in 1.1, this is no longer a significant issue (I tested up to 16 threads with only 2.2 GB of memory used).

The table below summarizes the results achieved on a [`c5d.large`](https://instances.vantage.sh/aws/ec2/c5d.large) instance, which has 2 vCPUs and 4 GB RAM. We report the total runtime and the maximum memory usage for each query.

|           Query syntax            |    `UNION` type     | Threads | Runtime | Memory  |
|:----------------------------------|---------------------|--------:|--------:|--------:|
| create view, copy                 | `BY NAME`           | 2       | 5.8 min | 0.47 GB |
| create view, copy                 | `BY POSITION`       | 2       | 4.0 min | 0.47 GB |
| create view, copy, new column     | `BY NAME`           | 2       | 5.6 min | 0.47 GB |
| copy subquery, new column         | `BY NAME`           | 2       | 4.1 min | 0.47 GB |
| copy subquery                     | `BY POSITION`       | 2       | 3.7 min | 0.49 GB |
| copy subquery, new column         | `BY NAME`           | 4       | 3.0 min | 0.77 GB |

## Closing Thoughts

When stacking data, DuckDB brings the spirit of the relational model back to SQL!
After all, stacking data should not require column orders to match...
The `BY NAME` keywords can simplify common operations like combining relations with different orders or sets of columns, inserting the results of a query into a table, or querying a data lake with a changing schema.
As of DuckDB version 1.1, this is now a performant and scalable approach!

Happy analyzing!
