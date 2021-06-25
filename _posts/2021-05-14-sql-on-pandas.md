---

layout: post
title:  "Efficient SQL on Pandas with DuckDB"
author: Mark Raasveldt and Hannes Mühleisen
excerpt_separator: <!--more-->

---

_TLDR: DuckDB, a free and open source analytical data management system, can efficiently run SQL queries directly on Pandas DataFrames._

Recently, an article was published [advocating for using SQL for Data Analysis](https://hakibenita.com/sql-for-data-analysis). Here at team DuckDB, we are huge fans of [SQL](https://en.wikipedia.org/wiki/SQL). It is a versatile and flexible language that allows the user to efficiently perform a wide variety of data transformations, without having to care about how the data is physically represented or how to do these data transformations in the most optimal way.

<!--more-->

For Data Science in Python, however, the [Pandas](https://pandas.pydata.org) and [NumPy](https://numpy.org) libraries are irreplaceable. They serve as the standard for data exchange between the vast ecosystem of Data Science libraries in Python<sup>1</sup>. You can very effectively perform aggregations and data transformations in an external database system such as Postgres. However, you will need to convert that data back into NumPy or Pandas if you want to use it in libraries such as [scikit-learn](https://scikit-learn.org/stable/) or [TensorFlow](https://www.tensorflow.org).

[1] [Apache Arrow](https://arrow.apache.org) is gaining significant traction in this domain as well, and DuckDB also quacks Arrow.

#### SQL on Pandas
After your data has been converted into a Pandas DataFrame often additional data wrangling and analysis still need to be performed. SQL is a very powerful tool for performing these types of data transformations. Using DuckDB, it is possible to run SQL efficiently right on top of Pandas DataFrames.

As a short teaser, here is a code snippet that allows you to do exactly that: run arbitrary SQL queries directly on Pandas DataFrames using DuckDB.

```py
# to install: pip install duckdb
import pandas as pd
import duckdb

mydf = pd.DataFrame({'a' : [1, 2, 3]})
print(duckdb.query("SELECT SUM(a) FROM mydf").to_df())
```

In the rest of the article, we will go more in-depth into how this works and how fast it is.

# Data Integration & SQL on Pandas
One of the core goals of DuckDB is that accessing data in common formats should be easy. DuckDB is fully capable of running queries in parallel *directly* on top of a Pandas DataFrame (or on a Parquet/CSV file, or on an Arrow table, …). A separate (time-consuming) import step is not necessary.

DuckDB can also write query results directly to any of these formats. You can use DuckDB to process a Pandas DataFrame in parallel using SQL, and convert the result back to a Pandas DataFrame again, so you can then use the result in other Data Science libraries.

When you run a query in SQL, DuckDB will look for Python variables whose name matches the table names in your query and automatically start reading your Pandas DataFrames. Looking back at the previous example we can see this in action:


```py
import pandas as pd
import duckdb

mydf = pd.DataFrame({'a' : [1, 2, 3]})
print(duckdb.query("SELECT SUM(a) FROM mydf").to_df())
```

The SQL table name `mydf` is interpreted as the local Python variable `mydf` that happens to be a Pandas DataFrame, which DuckDB can read and query directly. The column names and types are also extracted automatically from the DataFrame.

Not only is this process painless, it is highly efficient. For many queries, you can use DuckDB to process data faster than Pandas, and with a much lower total memory usage, *without ever leaving the Pandas DataFrame binary format* ("Pandas-in, Pandas-out"). Unlike when using an external database system such as Postgres, the data transfer time of the input or the output is negligible (see Appendix A for details).

# SQL on Pandas Performance
To demonstrate the performance of DuckDB when executing SQL on Pandas DataFrames, we now present a number of benchmarks. The source code for the benchmarks is available for interactive use [in Google Colab](https://colab.research.google.com/drive/1eg_TJpPQr2tyYKWjISJlX8IEAi8Qln3U?usp=sharing). In these benchmarks, we operate *purely* on Pandas DataFrames. Both the DuckDB code and the Pandas code operates fully on a `Pandas-in, Pandas-out` basis.

#### Benchmark Setup and Data Set

We run the benchmark entirely from within the Google Colab environment. For our benchmark dataset, we use the [infamous TPC-H data set](http://www.tpc.org/tpch/). Specifically, we focus on the `lineitem` and `orders` tables as these are the largest tables in the benchmark. The total dataset size is around 1GB in uncompressed CSV format ("scale factor" 1).

As DuckDB is capable of using multiple processors (multi-threading), we include both a single-threaded variant and a variant with two threads. Note that while DuckDB can scale far beyond two threads, Google Colab only supports two.

#### Setup

First we need to install DuckDB. This is a simple one-liner.

```bash
pip install duckdb
```

To set up the dataset for processing we download two parquet files using `wget`. After that, we load the data into a Pandas DataFrame using the built-in Parquet reader of DuckDB. The system automatically infers that we are reading a parquet file by looking at the `.parquet` extension of the file.

```py
lineitem = duckdb.query(
    "SELECT * FROM 'lineitemsf1.snappy.parquet'"
).to_df()
orders = duckdb.query(
    "SELECT * FROM 'orders.parquet'"
).to_df()
```

#### Ungrouped Aggregates

For our first query, we will run a set of ungrouped aggregates over the Pandas DataFrame. Here is the SQL query:

```sql
SELECT SUM(l_extendedprice),
       MIN(l_extendedprice),
       MAX(l_extendedprice),
       AVG(l_extendedprice)
FROM lineitem
```

The Pandas code looks similar:

```py
lineitem.agg(
  Sum=('l_extendedprice', 'sum'),
  Min=('l_extendedprice', 'min'),
  Max=('l_extendedprice', 'max'),
  Avg=('l_extendedprice', 'mean')
)
```


|    Name     | Time (s) |
|:-------------|----------:|
| DuckDB (1 Thread) | 0.079    |
| DuckDB (2 Threads) | 0.048    |
| Pandas      | 0.070    |

This benchmark involves a very simple query, and Pandas performs very well here. These simple queries are where Pandas excels (ha), as it can directly call into the numpy routines that implement these aggregates, which are highly efficient. Nevertheless, we can see that DuckDB performs similar to to Pandas in the single-threaded scenario, and benefits from its multi-threading support when enabled.

## Grouped Aggregate
For our second query, we will run the same set of aggregates, but this time include a grouping condition. In SQL, we can do this by adding a GROUP BY clause to the query.

```sql
SELECT
      l_returnflag,
      l_linestatus,
      SUM(l_extendedprice),
      MIN(l_extendedprice),
      MAX(l_extendedprice),
      AVG(l_extendedprice)
FROM lineitem
GROUP BY
        l_returnflag,
        l_linestatus
```

In Pandas, we use the groupby function before we perform the aggregation.

```py
lineitem.groupby(
  ['l_returnflag', 'l_linestatus']
).agg(
  Sum=('l_extendedprice', 'sum'),
  Min=('l_extendedprice', 'min'),
  Max=('l_extendedprice', 'max'),
  Avg=('l_extendedprice', 'mean')
)
```

|    Name     | Time (s) |
|:-------------|----------:|
| DuckDB (1 Thread) | 0.43     |
| DuckDB (2 Threads)&nbsp; | 0.32     |
| Pandas      | 0.84     |

This query is already getting more complex, and while Pandas does a decent job, it is a factor two slower than the single-threaded version of DuckDB. DuckDB has a highly optimized aggregate hash-table implementation that will perform both the grouping and the computation of all the aggregates in a single pass over the data.

## Grouped Aggregate with a Filter

Now suppose that we don't want to perform an aggregate over all of the data, but instead only want to select a subset of the data to aggregate. We can do this by adding a filter clause that removes any tuples we are not interested in. In SQL, we can accomplish this through the `WHERE` clause.

```sql
SELECT l_returnflag,
      l_linestatus,
      SUM(l_extendedprice),
      MIN(l_extendedprice),
      MAX(l_extendedprice),
      AVG(l_extendedprice)
FROM lineitem
WHERE
   l_shipdate <= DATE '1998-09-02'
GROUP BY l_returnflag,
        l_linestatus

```

 In Pandas, we can create a filtered variant of the DataFrame by using the selection brackets.

```py
# filter out the rows
filtered_df = lineitem[
  lineitem['l_shipdate'] < "1998-09-02"]
# perform the aggregate
result = filtered_df.groupby(
  ['l_returnflag', 'l_linestatus']
).agg(
  Sum=('l_extendedprice', 'sum'),
  Min=('l_extendedprice', 'min'),
  Max=('l_extendedprice', 'max'),
  Avg=('l_extendedprice', 'mean')
)
```

In DuckDB, the query optimizer will combine the filter and aggregation into a single pass over the data, only reading relevant columns. In Pandas, however, we have no such luck. The filter as it is executed will actually subset the entire lineitem table, *including any columns we are not using!* As a result of this, the filter operation is much more time-consuming than it needs to be.

We can manually perform this optimization ("projection pushdown" in database literature). To do this, we first need to select only the columns that are relevant to our query and then subset the lineitem dataframe. We will end up with the following code snippet:

```py
# projection pushdown
pushed_down_df = lineitem[
  ['l_shipdate',
   'l_returnflag',
   'l_linestatus',
   'l_extendedprice']
]
# perform the filter
filtered_df = pushed_down_df[
  pushed_down_df['l_shipdate'] < "1998-09-02"]
# perform the aggregate
result = filtered_df.groupby(
  ['l_returnflag', 'l_linestatus']
).agg(
  Sum=('l_extendedprice', 'sum'),
  Min=('l_extendedprice', 'min'),
  Max=('l_extendedprice', 'max'),
  Avg=('l_extendedprice', 'mean')
)
```

|           Name             | Time (s) |
|:----------------------------|----------:|
| DuckDB (1 Thread)          | 0.60     |
| DuckDB (2 Threads)         | 0.42     |
| Pandas                     | 3.57     |
| Pandas (manual pushdown)&nbsp;&nbsp;   | 2.23     |

While the manual projection pushdown significantly speeds up the query in Pandas, there is still a significant time penalty for the filtered aggregate. To process a filter, Pandas will write a copy of the entire DataFrame (minus the filtered out rows) back into memory. This operation can be time consuming when the filter is not very selective.

Due to its holistic query optimizer and efficient query processor, DuckDB performs significantly better on this query.


## Joins
For the final query, we will join (`merge` in Pandas) the lineitem table with the orders table, and apply a filter that only selects orders which have the status we are interested in. This leads us to the following query in SQL:

```sql
SELECT l_returnflag,
       l_linestatus,
       sum(l_extendedprice),
       min(l_extendedprice),
       max(l_extendedprice),
       avg(l_extendedprice)
FROM lineitem lineitem
JOIN orders orders ON (l_orderkey=o_orderkey)
WHERE l_shipdate <= DATE '1998-09-02'
  AND o_orderstatus='O'
GROUP BY l_returnflag,
         l_linestatus
```

For Pandas, we have to add a `merge` step. In a basic approach, we merge lineitem and orders together, then apply the filters, and finally apply the grouping and aggregation. This will give us the following code snippet:

```py
# perform the join
merged = lineitem.merge(
  orders,
  left_on='l_orderkey',
  right_on='o_orderkey')
# filter out the rows
filtered_a = merged[
  merged['l_shipdate'] < "1998-09-02"]
filtered_b = filtered_a[
  filtered_a['o_orderstatus'] == "O"]
# perform the aggregate
result = filtered_b.groupby(
  ['l_returnflag', 'l_linestatus']
).agg(
  Sum=('l_extendedprice', 'sum'),
  Min=('l_extendedprice', 'min'),
  Max=('l_extendedprice', 'max'),
  Avg=('l_extendedprice', 'mean')
)
```

Now we have missed two performance opportunities:

* First, we are merging far too many columns, because we are merging columns that are not required for the remainder of the query (projection pushdown).
* Second, we are merging far too many rows. We can apply the filters prior to the merge to reduce the amount of data that we need to merge (filter pushdown).

Applying these two optimizations manually results in the following code snippet:

```py
# projection & filter on lineitem table
lineitem_projected = lineitem[
  ['l_shipdate',
   'l_orderkey',
   'l_linestatus',
   'l_returnflag',
   'l_extendedprice']
]
lineitem_filtered = lineitem_projected[
  lineitem_projected['l_shipdate'] < "1998-09-02"]
# projection and filter on order table
orders_projected = orders[
  ['o_orderkey',
   'o_orderstatus']
]
orders_filtered = orders_projected[
  orders_projected['o_orderstatus'] == 'O']
# perform the join
merged = lineitem_filtered.merge(
  orders_filtered,
  left_on='l_orderkey',
  right_on='o_orderkey')
# perform the aggregate
result = merged.groupby(
  ['l_returnflag', 'l_linestatus']
).agg(
  Sum=('l_extendedprice', 'sum'),
  Min=('l_extendedprice', 'min'),
  Max=('l_extendedprice', 'max'),
  Avg=('l_extendedprice', 'mean')
)
```

Both of these optimizations are automatically applied by DuckDB's query optimizer.


|           Name           | Time (s) |
|:--------------------------|----------:|
| DuckDB (1 Thread)        | 1.05     |
| DuckDB (2 Threads)       | 0.53     |
| Pandas                   | 15.2     |
| Pandas (manual pushdown)&nbsp;&nbsp; | 3.78     |

We see that the basic approach is extremely time consuming compared to the optimized version. This demonstrates the usefulness of the automatic query optimizer. Even after optimizing, the Pandas code is still significantly slower than DuckDB because it stores intermediate results in memory after the individual filters and joins.

#### Takeaway
Using DuckDB, you can take advantage of the powerful and expressive SQL language without having to worry about moving your data in - and out - of Pandas. DuckDB is extremely simple to install, and offers many advantages such as a query optimizer, automatic multi-threading and larger-than-memory computation. DuckDB uses the Postgres SQL parser, and offers many of the same SQL features as Postgres, including advanced features such as window functions, correlated subqueries, (recursive) common table expressions, nested types and sampling. If you are missing a feature, please [open an issue](https://github.com/duckdb/duckdb/issues).

# Appendix A: There and back again: Transferring data from Pandas to a SQL engine and back

Traditional SQL engines use the Client-Server paradigm, which means that a client program connects through a socket to a server. Queries are run on the server, and results are sent back down to the client afterwards. This is the same when using for example Postgres from Python. Unfortunately, this transfer [is a serious bottleneck](http://www.vldb.org/pvldb/vol10/p1022-muehleisen.pdf). In-process engines such as SQLite or DuckDB do not run into this problem.

To showcase how costly this data transfer over a socket is, we have run a benchmark involving Postgres, SQLite and DuckDB. The source code for the benchmark can be found [here](https://gist.github.com/hannesmuehleisen/a95a39a1eda63aeb0ca13fd82d1ba49c).

In this benchmark we copy a (fairly small) Pandas data frame consisting of 10M 4-Byte integers (40MB) from Python to the PostgreSQL, SQLite and DuckDB databases. Since the default Pandas `to_sql` was rather slow, we added a separate optimization in which we tell Pandas to write the data frame to a temporary CSV file, and then tell PostgreSQL to directly copy data from that file into a newly created table. This of course will only work if the database server is running on the same machine as Python.

|                    Name                     | Time (s) |
|:---------------------------------------------|----------:|
| Pandas to Postgres using to_sql             | 111.25   |
| Pandas to Postgres using temporary CSV file&nbsp;&nbsp; | 5.57     |
| Pandas to SQLite using to_sql               | 6.80     |
| Pandas to DuckDB                            | 0.03     |

While SQLite performs significantly better than Postgres here, it is still rather slow. That is because the `to_sql` function in Pandas runs a large number of `INSERT INTO` statements, which involves transforming all the individual values of the Pandas DataFrame into a row-wise representation of  Python objects which are then passed onto the system. DuckDB on the other hand directly reads the underlying array from Pandas, which makes this operation almost instant.

Transferring query results or tables back from the SQL system into Pandas is another potential bottleneck. Using the built-in `read_sql_query` is extremely slow, but even the more optimized CSV route still takes at least a second for this tiny data set. DuckDB, on the other hand, also performs this transformation almost instantaneously.

|                     Name                      | Time (s) |
|:-----------------------------------------------|----------:|
| PostgreSQL to Pandas using read_sql_query     | 7.08     |
| PostgreSQL to Pandas using temporary CSV file | 1.29     |
| SQLite to Pandas using read_sql_query         | 5.20     |
| DuckDB to Pandas                              | 0.04     |


# Appendix B: Comparison to PandaSQL

There is a package called [PandaSQL](https://pypi.org/project/pandasql/) that also provides the facilities of running SQL directly on top of Pandas. However, it is built using the to_sql and from_sql infrastructure that we have seen is extremely slow in Appendix A.

Nevertheless, for good measure we have run the first Ungrouped Aggregate query in PandaSQL to time it. When we first tried to run the query on the original dataset, however, we ran into an out-of-memory error that crashed our colab session. For that reason, we have decided to run the benchmark again for PandaSQL using a sample of 10% of the original data set size (600K rows). Here are the results:

|    Name     | Time (s)  |
|:-------------|-----------:|
| DuckDB (1 Thread) |   0.023   |
| DuckDB (2 Threads)&nbsp; |   0.014   |
| Pandas      |   0.017   |
| PandaSQL    |   24.43   |

We can see that PandaSQL (powered by SQLite) is around 1000X~ slower than either Pandas or DuckDB on this straightforward benchmark. The performance difference was so large we have opted not to run the other benchmarks for PandaSQL.

# Appendix C: Query on Parquet Directly
In the benchmarks above, we fully read the parquet files into Pandas. However, DuckDB also has the capability of directly running queries on top of Parquet files (in parallel!). In this appendix, we show the performance of this compared to loading the file into Python first.

For the benchmark, we will run two queries: the simplest query (the ungrouped aggregate) and the most complex query (the final join) and compare the cost of running this query directly on the Parquet file, compared to loading it into Pandas using the `read_parquet` function.

#### Setup
In DuckDB, we can create a view over the Parquet file using the following query. This allows us to run queries over the Parquet file as if it was a regular table. Note that we do not need to worry about projection pushdown at all: we can just do a `SELECT *` and DuckDB's optimizer will take care of only projecting the required columns at query time.

```sql
CREATE VIEW lineitem_parquet AS SELECT * FROM 'lineitemsf1.snappy.parquet';
CREATE VIEW orders_parquet AS SELECT * FROM 'orders.parquet';
```

#### Ungrouped Aggregate
After we have set up this view, we can run the same queries we ran before, but this time against the `lineitem_parquet` table.

```sql
SELECT SUM(l_extendedprice), MIN(l_extendedprice), MAX(l_extendedprice), AVG(l_extendedprice) FROM lineitem_parquet
```

For Pandas, we will first need to run `read_parquet` to load the data into Pandas. To do this, we use the Parquet reader powered by Apache Arrow. After that, we can run the query as we did before.

```py
lineitem_pandas_parquet = pd.read_parquet('lineitemsf1.snappy.parquet')
result = lineitem_pandas_parquet.agg(Sum=('l_extendedprice', 'sum'), Min=('l_extendedprice', 'min'), Max=('l_extendedprice', 'max'), Avg=('l_extendedprice', 'mean'))
```

However, we now again run into the problem where Pandas will read the Parquet file in its entirety. In order to circumvent this, we will need to perform projection pushdown manually again by providing the `read_parquet` method with the set of columns that we want to read.

The optimizer in DuckDB will figure this out by itself by looking at the query you are executing.

```py
lineitem_pandas_parquet = pd.read_parquet('lineitemsf1.snappy.parquet', columns=['l_extendedprice'])
result = lineitem_pandas_parquet.agg(Sum=('l_extendedprice', 'sum'), Min=('l_extendedprice', 'min'), Max=('l_extendedprice', 'max'), Avg=('l_extendedprice', 'mean'))
```

|    Name                       | Time (s) |
|:-------------------------------|----------:|
| DuckDB (1 Thread)             | 0.16     |
| DuckDB (2 Threads)            | 0.14     |
| Pandas                        | 7.87     |
| Pandas (manual pushdown)&nbsp;&nbsp;      | 0.17     |

We can see that the performance difference between doing the pushdown and not doing the pushdown is dramatic. When we perform the pushdown, Pandas has performance in the same ballpark as DuckDB. Without the pushdown, however, it is loading the entire file from disk, including the other 15 columns that are not required to answer the query.

## Joins
Now for the final query that we saw in the join section previously. To recap:

```sql
SELECT l_returnflag,
       l_linestatus,
       sum(l_extendedprice),
       min(l_extendedprice),
       max(l_extendedprice),
       avg(l_extendedprice)
FROM lineitem lineitem
JOIN orders orders ON (l_orderkey=o_orderkey)
WHERE l_shipdate <= DATE '1998-09-02'
  AND o_orderstatus='O'
GROUP BY l_returnflag,
         l_linestatus
```

For Pandas we again create two versions. A naive version, and a manually optimized version. The exact code used can be found [in Google Colab](https://colab.research.google.com/drive/1eg_TJpPQr2tyYKWjISJlX8IEAi8Qln3U?usp=sharing).

|    Name     | Time (s) |
|:-------------|----------:|
| DuckDB (1 Thread) | 1.04    |
| DuckDB (2 Threads) | 0.89    |
| Pandas      | 20.4    |
| Pandas (manual pushdown)&nbsp;&nbsp;      | 3.95    |

We see that for this more complex query the slight difference in performance between running over a Pandas DataFrame and a Parquet file vanishes, and the DuckDB timings become extremely similar to the timings we saw before. The added Parquet read again increases the necessity of manually performing optimizations on the Pandas code, which is not required at all when running SQL in DuckDB.
