---

layout: post
title:  "Querying Parquet with Precision using DuckDB"
author: Hannes Mühleisen and Mark Raasveldt
excerpt_separator: <!--more-->

---

_TLDR: DuckDB, a free and open source analytical data management system, can run SQL queries directly on Parquet files and automatically take advantage of the advanced features of the Parquet format._

Apache Parquet is the most common "Big Data" storage format for analytics. In Parquet files, data is stored in a columnar-compressed binary format. Each Parquet file stores a single table. The table is partitioned into row groups, which each contain a subset of the rows of the table. Within a row group, the table data is stored in a columnar fashion.

<!--more-->

<img src="/images/blog/parquet.svg" alt="Example parquet file shown visually. The parquet file (taxi.parquet) is divided into row-groups that each have two columns (pickup_at and dropoff_at)"
	title="Taxi Parquet File" class="parquet"/>

The Parquet format has a number of properties that make it suitable for analytical use cases:

1. The columnar representation means that individual columns can be (efficiently) read. No need to always read the entire file!
2. The file contains per-column statistics in every row group (min/max value, and the number of `NULL` values). These statistics allow the reader to skip row groups if they are not required.
3. The columnar compression significantly reduces the file size of the format, which in turn reduces the storage requirement of data sets. This can often turn Big Data into Medium Data.

#### DuckDB and Parquet
DuckDB's zero-dependency Parquet reader is able to directly execute SQL queries on Parquet files without any import or analysis step. Because of the natural columnar format of Parquet, this is very fast!

DuckDB will read the Parquet files in a streaming fashion, which means you can perform queries on large Parquet files that do not fit in your main memory.

DuckDB is able to automatically detect which columns and rows are required for any given query. This allows users to analyze much larger and more complex Parquet files without needing to perform manual optimizations or investing in more hardware.

And as an added bonus, DuckDB is able to do all of this using parallel processing and over multiple Parquet files at the same time using the glob syntax.

As a short teaser, here is a code snippet that allows you to directly run a SQL query on top of a Parquet file.

```py
# to install: pip install duckdb
# to download the parquet file:
# wget https://github.com/cwida/duckdb-data/releases/download/v1.0/taxi_2019_04.parquet
import duckdb

print(duckdb.query('''
SELECT COUNT(*)
FROM 'taxi_2019_04.parquet'
WHERE pickup_at BETWEEN '2019-04-15' AND '2019-04-20'
''').fetchall())
```

#### Automatic Filter & Projection Pushdown
Let us dive into the previous query to better understand the power of the Parquet format when combined with DuckDB's query optimizer.

```sql
SELECT COUNT(*)
FROM 'taxi_2019_04.parquet'
WHERE pickup_at BETWEEN '2019-04-15' AND '2019-04-20'
```

In this query, we read a single column from our Parquet file (`pickup_at`). Any other columns stored in the Parquet file can be entirely skipped, as we do not need them to answer our query.

<img src="/images/blog/parquet-filter-svg.svg" alt="Projection & filter pushdown into parquet file example."
	title="Filter Pushdown" class="parquet"/>

In addition, only rows that have a `pickup_at` between the 15th and the 20th of April 2019 influence the result of the query. Any rows that do not satisfy this predicate can be skipped.

We can use the statistics inside the Parquet file to great advantage here. Any row groups that have a max value of `pickup_at` lower than `2019-04-15`, or a min value higher than `2019-04-20`, can be skipped. In some cases, that allows us to skip reading entire files.

#### DuckDB versus Pandas
To illustrate how effective these automatic optimizations are, we will run a number of queries on top of Parquet files using both Pandas and DuckDB.

In these queries, we use a part of the infamous New York Taxi dataset stored as Parquet files, specifically data from April, May and June 2019. These files are ca. 360 MB in size together and contain around 21 million rows of 18 columns each. The three files are placed into the `taxi/` folder.

The examples are available [here as an interactive notebook over at Google Colab](https://colab.research.google.com/drive/1e1beWqYOcFidKl2IxHtxT5s9i_6KYuNY). The timings reported here are from this environment for reproducibility.

#### Reading Multiple Parquet Files
First we look at some rows in the dataset. There are three Parquet files in the `taxi/` folder. [DuckDB supports the globbing syntax](https://duckdb.org/docs/data/parquet), which allows it to query all three files simultaneously.

```py
con.execute("""
   SELECT *
   FROM 'taxi/*.parquet'
   LIMIT 5""").df()
```

|      pickup_at      |     dropoff_at      | passenger_count | trip_distance | rate_code_id |
|---------------------|---------------------|-----------------|---------------|--------------|
| 2019-04-01 00:04:09 | 2019-04-01 00:06:35 | 1               | 0.5           | 1            |
| 2019-04-01 00:22:45 | 2019-04-01 00:25:43 | 1               | 0.7           | 1            |
| 2019-04-01 00:39:48 | 2019-04-01 01:19:39 | 1               | 10.9          | 1            |
| 2019-04-01 00:35:32 | 2019-04-01 00:37:11 | 1               | 0.2           | 1            |
| 2019-04-01 00:44:05 | 2019-04-01 00:57:58 | 1               | 4.8           | 1            |

Despite the query selecting all columns from three (rather large) Parquet files, the query completes instantly. This is because DuckDB processes the Parquet file in a streaming fashion, and will stop reading the Parquet file after the first few rows are read as that is all required to satisfy the query.

If we try to do the same in Pandas, we realize it is not so straightforward, as Pandas cannot read multiple Parquet files in one call. We will first have to use `pandas.concat` to concatenate the three Parquet files together:

```py
import pandas
import glob
df = pandas.concat(
	[pandas.read_parquet(file)
	 for file
	 in glob.glob('taxi/*.parquet')])
print(df.head(5))
```

Below are the timings for both of these queries.

| System | Time (s) |
|:--------|---------:|
| DuckDB | 0.015    |
| Pandas | 12.300    |

Pandas takes significantly longer to complete this query. That is because Pandas not only needs to read each of the three Parquet files in their entirety, it has to concatenate these three separate Pandas DataFrames together.

#### Concatenate Into a Single File
We can address the concatenation issue by creating a single big Parquet file from the three smaller parts. We can use the `pyarrow` library for this, which has support for reading multiple Parquet files and streaming them into a single large file. Note that the `pyarrow` parquet reader is the very same parquet reader that is used by Pandas internally.

```py
import pyarrow.parquet as pq

# concatenate all three parquet files
pq.write_table(pq.ParquetDataset('taxi/').read(), 'alltaxi.parquet', row_group_size=100000)
```

Note that [DuckDB also has support for writing Parquet files](https://duckdb.org/docs/data/parquet#writing-to-parquet-files) using the COPY statement.

#### Querying the Large File
Now let us repeat the previous experiment, but using the single file instead.

```py
# DuckDB
con.execute("""
   SELECT *
   FROM 'alltaxi.parquet'
   LIMIT 5""").df()

# Pandas
pandas.read_parquet('alltaxi.parquet')
      .head(5)
```

| System | Time (s) |
|:--------|---------:|
| DuckDB | 0.02    |
| Pandas | 7.50     |

We can see that Pandas performs better than before, as the concatenation is avoided. However, the entire file still needs to be read into memory, which takes both a significant amount of time and memory.

For DuckDB it does not really matter how many Parquet files need to be read in a query.

#### Counting Rows
Now suppose we want to figure out how many rows are in our data set. We can do that using the following code:

```py
# DuckDB
con.execute("""
   SELECT COUNT(*)
   FROM 'alltaxi.parquet'
""").df()

# Pandas
len(pandas.read_parquet('alltaxi.parquet'))
```

| System | Time (s) |
|:--------|---------:|
| DuckDB | 0.015   |
| Pandas | 7.500     |

DuckDB completes the query very quickly, as it automatically recognizes  what needs to be read from the Parquet file and minimizes the required reads. Pandas has to read the entire file again, which causes it to take  the same amount of time as the previous query.

For this query, we can improve Pandas' time through manual optimization. In order to get a count, we only need a single column from the file. By manually specifying a single column to be read in the `read_parquet` command, we can get the same result but much faster.

```py
len(pandas.read_parquet('alltaxi.parquet', columns=['vendor_id']))
```

|       System       | Time (s) |
|:--------------------|---------:|
| DuckDB             | 0.015   |
| Pandas             | 7.500     |
| Pandas (optimized) | 1.200     |

While this is much faster, this still takes more than a second as the entire `vendor_id` column has to be read into memory as a Pandas column only to count the number of rows.

#### Filtering Rows
It is common to use some sort of filtering predicate to only look at the interesting parts of a data set. For example, imagine we want to know how many taxi rides occur after the 30th of June 2019. We can do that using the following query in DuckDB:

```py
con.execute("""
   SELECT COUNT(*)
   FROM 'alltaxi.parquet'
   WHERE pickup_at > '2019-06-30'
""").df()
```

The query completes in `45ms` and yields the following result:

| count  |
|--------|
| 167022 |

In Pandas, we can perform the same operation using a naive approach.

```py
# pandas naive
len(pandas.read_parquet('alltaxi.parquet')
          .query("pickup_at > '2019-06-30'"))
```

This again reads the entire file into memory, however, causing this query to take `7.5s`. With the manual projection pushdown we can bring this down to `0.9s`. Still significantly higher than DuckDB.

```py
# pandas projection pushdown
len(pandas.read_parquet('alltaxi.parquet', columns=['pickup_at'])
          .query("pickup_at > '2019-06-30'"))
```

The `pyarrow` parquet reader also allows us to perform filter pushdown into the scan, however. Once we add this we end up with a much more competitive `70ms` to complete the query.

```py
len(pandas.read_parquet('alltaxi.parquet', columns=['pickup_at'], filters=[('pickup_at', '>', '2019-06-30')]))
```

|                System                 | Time (s) |
|:---------------------------------------|---------:|
| DuckDB                                | 0.05   |
| Pandas                                | 7.50     |
| Pandas (projection pushdown)          | 0.90     |
| Pandas (projection & filter pushdown) | 0.07    |

This shows that the results here are not due to DuckDB's parquet reader being faster than the `pyarrow` Parquet reader. The reason that DuckDB performs better on these queries is because its optimizers automatically extract all required columns and filters from the SQL query, which then get automatically utilized in the Parquet reader with no manual effort required.

Interestingly, both the `pyarrow` Parquet reader and DuckDB are significantly faster than performing this operation natively in Pandas on a materialized DataFrame.

```py
# read the entire parquet file into Pandas
df = pandas.read_parquet('alltaxi.parquet')
# run the query natively in Pandas
# note: we only time this part
print(len(df[['pickup_at']].query("pickup_at > '2019-06-30'")))
```

|                System                 | Time (s) |
|:---------------------------------------|---------:|
| DuckDB                                | 0.05    |
| Pandas                                | 7.50     |
| Pandas (projection pushdown)          | 0.90     |
| Pandas (projection & filter pushdown) | 0.07    |
| Pandas (native)                       | 0.26    |

#### Aggregates
Finally lets look at a more complex aggregation. Say we want to compute the number of rides per passenger. With DuckDB and SQL, it looks like this:

```py
con.execute("""
    SELECT passenger_count, COUNT(*)
    FROM 'alltaxi.parquet'
    GROUP BY passenger_count""").df()
```

The query completes in `220ms` and yields the following result:

| passenger_count |  count   |
|:-----------------|----------:|
| 0               | 408742   |
| 1               | 15356631 |
| 2               | 3332927  |
| 3               | 944833   |
| 4               | 439066   |
| 5               | 910516   |
| 6               | 546467   |
| 7               | 106      |
| 8               | 72       |
| 9               | 64       |

For the SQL-averse and as a teaser for a future blog post, DuckDB also has a "Relational API" that allows for a more Python-esque declaration of queries. Here's the equivalent to the above SQL query, that provides the exact same result and performance:

```py
con.from_parquet('alltaxi.parquet')
   .aggregate('passenger_count, count(*)')
   .df()
```

Now as a comparison, let's run the same query in Pandas in the same way we did previously.

```py
# naive
pandas.read_parquet('alltaxi.parquet')
      .groupby('passenger_count')
      .agg({'passenger_count' : 'count'})

# projection pushdown
pandas.read_parquet('alltaxi.parquet', columns=['passenger_count'])
      .groupby('passenger_count')
      .agg({'passenger_count' : 'count'})

# native (parquet file pre-loaded into memory)
df.groupby('passenger_count')
  .agg({'passenger_count' : 'count'})
```

|            System            | Time (s) |
|:------------------------------|---------:|
| DuckDB                       | 0.22    |
| Pandas                       | 7.50     |
| Pandas (projection pushdown) | 0.58    |
| Pandas (native)              | 0.51    |

We can see that DuckDB is faster than Pandas in all three scenarios, without needing to perform any manual optimizations and without needing to load the Parquet file into memory in its entirety.

#### Conclusion

DuckDB can efficiently run queries directly on top of Parquet files without requiring an initial loading phase. The system will automatically take advantage of all of Parquet's advanced features to speed up query execution.

DuckDB is a free and open source database management system (MIT licensed). It aims to be the SQLite for Analytics, and provides a fast and efficient database system with zero external dependencies. It is available not just for Python, but also for C/C++, R, Java, and more.
