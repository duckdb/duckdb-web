---
layout: post
title:  "Querying Postgres Tables Directly From DuckDB"
author: Hannes Mühleisen
excerpt_separator: <!--more-->
---


*TLDR: DuckDB can now directly query queries stored in PostgreSQL and speed up complex analytical queries without duplicating data.*

<!--more-->

<img src="/images/blog/elephant-duck.jpg"
     alt="DuckDB goes Postgres"
     width=200
 />


## Introduction
PostgreSQL is the world's most advanced open source database ([self-proclaimed](https://www.postgresql.org)). From its [interesting beginnings as an academic DBMS](https://dsf.berkeley.edu/papers/ERL-M90-34.pdf), it has evolved over the past 30 years into a fundamental workhorse of our digital environment. 

PostgreSQL is designed for traditional [transactional use cases, "OLTP"](https://en.wikipedia.org/wiki/Online_transaction_processing), where rows in tables are created, updated and removed concurrently, and it excels at this. But this design decision makes PostgreSQL far less suitable for [analytical use cases, "OLAP"](https://en.wikipedia.org/wiki/Online_analytical_processing), where large chunks of tables are read to create summaries of the stored data. Yet there are many use cases where both transactional and analytical use cases are important, for example when trying to gain the latest business intelligence insights into transactional data.

There have been [some attempts to build database management systems that do well on both workloads, "HTAP"](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing), but in general many design decisions between OLTP and OLAP systems are hard trade-offs, making this endeavour difficult. Accepting that [one size does not fit all after all](http://cs.brown.edu/~ugur/fits_all.pdf), systems are often separated, with the transactional application data living in a purpose-built system like PostgreSQL, and a copy of the data being stored in an entirely different DBMS. Using a purpose-built analytical system speeds up analytical queries by several orders of magnitude.

Unfortunately, maintaining a copy of the data for analytical purposes can be problematic: The copy will immediately be outdated as new transactions are processed, requiring a complex and non-trivial synchronization setup. Storing two copies of the database also will require twice the storage space. For example, OLTP systems like PostgreSQL traditionally use a row-based data representation, and OLAP systems tend to favor a chunked-columnar data representation. You can't have both without maintaining a copy of the data with all the issues that brings with it. Also, the SQL syntaxes between whatever OLAP system you're using and Postgres may differ quite significantly.

But the design space is not as black and white as it seems. For example, the OLAP performance in systems like DuckDB does not only come from a chunked-columnar on-disk data representation. Much of DuckDB's performance comes from its vectorized query processing engine that is custom-tuned for analytical queries. What if DuckDB was able to somehow *read data stored in PostgreSQL*? While it seems daunting, we have embarked on a quest to make just this possible. 

 To allow for fast and consistent analytical reads of Postgres databases, we designed and implemented the "Postgres Scanner". This scanner leverages the *binary transfer mode* of the Postgres client-server protocol (See the [Implementation Section](#Implementation) for more details.), allowing us to efficiently transform and use the data directly in DuckDB.
     
Among other things, DuckDB's design is different from conventional data management systems because DuckDB's query processing engine can run on nearly arbitrary data sources without needing to copy the data into its own storage format. For example, DuckDB can currently directly run queries on [Parquet files](https://duckdb.org/docs/data/parquet), [CSV files](https://duckdb.org/docs/data/csv), [SQLite files](https://github.com/duckdblabs/sqlite_scanner), [Pandas](https://duckdb.org/docs/guides/python/sql_on_pandas), [R](https://duckdb.org/docs/api/r#efficient-transfer) and [Julia](https://duckdb.org/docs/api/julia#scanning-dataframes) data frames as well as [Apache Arrow sources](https://duckdb.org/docs/guides/python/sql_on_arrow). This new extension adds the capability to directly query PostgreSQL tables from DuckDB. 


## Usage
The Postgres Scanner DuckDB extension source code [is available on GitHub](https://github.com/duckdblabs/postgresscanner), but it is directly installable through DuckDB's new binary extension installation mechanism. To install, just run the following SQL query once:
```SQL
INSTALL postgres_scanner;
```
Then, whenever you want to use the extension, you need to first load it:
```SQL
LOAD postgres_scanner;
```

To make a Postgres database accessible to DuckDB, use the `POSTGRES_ATTACH` command:
```SQL
CALL postgres_attach('dbname=myshinydb');
```
`postgres_attach` takes a single required string parameter, which is the [`libpq` connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING). For example you can pass `'dbname=myshinydb'` to select a different database name. In the simplest case, the parameter is just `''`. There are three additional named parameters to the function:
 * `source_schema` the name of a non-standard schema name in Postgres to get tables from. Default is `public`.
 * `overwrite` whether we should overwrite existing views in the target schema, default is `false`.
* `filter_pushdown` whether filter predicates that DuckDB derives from the query should be forwarded to Postgres, defaults to `false`. See below for a discussion of what this parameter controls.

The tables in the database are registered as views in DuckDB, you can list them with
```SQL
PRAGMA show_tables;
```
Then you can query those views normally using SQL. Again, no data is being copied, this is just a virtual view on the tables in your Postgres database. 

If you prefer to not attach all tables, but just query a single table, that is possible using the `POSTGRES_SCAN` and `POSTGRES_SCAN_PUSHDOWN` table-producing functions directly, e.g.

```SQL
SELECT * FROM postgres_scan('dbname=myshinydb', 'public', 'mytable');
SELECT * FROM postgres_scan_pushdown('dbname=myshinydb', 'public', 'mytable');

```

Both functions takes three unnamed string parameters, the `libpq` connection string (see above), a Postgres schema name and a table name. The schema name is often `public`. As the name suggest, the variant with "pushdown" in the name will perform selection pushdown as described below.

The Postgres scanner will only be able to read actual tables, views are not supported. However, you can of course recreate such views within DuckDB, the syntax should be exactly the same!

## Implementation
From an architectural perspective, the Postgres Scanner is implemented as a plug-in extension for DuckDB that provides a so-called table scan function (`postgres_scan`) in DuckDB. There are many such functions in DuckDB and in extensions, such as the Parquet and CSV readers, Arrow readers etc. 

The Postgres Scanner uses the standard `libpq` library, which it statically links in. Ironically, this makes the Postgres Scanner easier to install than the other Postgres clients. However, Postgres' normal client-server protocol is [quite slow](https://ir.cwi.nl/pub/26415/p852-muehleisen.pdf), so we spent quite some time optimizing this. As a note, DuckDB's [SQLite Scanner](https://github.com/duckdblabs/sqlite_scanner) does not face this issue, as SQLite is also an in-process database.

We actually implemented a prototype direct reader for Postgres' database files, but while performance was great, there is the issue that committed but not yet checkpointed data would not be stored in the heap files yet. In addition, if a checkpoint was currently running, our reader would frequently overtake the checkpointer, causing additional inconsistencies. We abandoned that approach since we want to be able to query an actively used Postgres database and believe that consistency is important. Another architectural option would have been to implement a DuckDB Foreign Data Wrapper (FDW) for Postgres similar to [duckdb_fdw](https://github.com/alitrack/duckdb_fdw) but while this could improve the protocol situation, deployment of a postgres extension is quite risky on production servers so we expect few people will be able to do so.

Instead, we use the rarely-used *binary transfer mode* of the Postgres client-server protocol. This format is quite similar to the on-disk representation of Postgres data files and avoids some of the otherwise expensive to-string and from-string conversions. For example, to read a normal `int32` from the protocol message, all we need to do is to swap byte order ([`ntohl`](https://linux.die.net/man/3/ntohl)).

The Postgres scanner connects to PostgreSQL and issues a query to read a particular table using the binary protocol. In the simplest case (see optimizations below), to read a table called `lineitem`, we internally run the query:

```SQL
COPY (SELECT * FROM lineitem) TO STDOUT (FORMAT binary);
```

This query will start reading the contents of `lineitem` and write them directly to the protocol stream in binary format.


### Parallelization
DuckDB supports automatic intra-query parallelization through pipeline parallelism, so we also want to parallelize scans on Postgres tables: Our scan operator opens multiple connections to Postgres, and reads subsets of the table from each. To efficiently split up reading the table, we use Postgres' rather obscure *TID Scan* (Tuple ID) operator, which allows a query to surgically read a specified range of tuple IDs from a table. The Tuple IDs have the form `(page, tuple)`. We parallelize our scan of a Postgres table based on database page ranges expressed in TIDs. Each scan task reads 1000 pages currently. For example, to read a table consisting of 2500 pages, we would start three scan tasks with TID ranges `[(0,0),(999,0)]`, `[(1000,0),(1999,0)]` and `[(2000,0),(UINT32_MAX,0)]`. Having an open bound for the last range is important because the number of pages (`relpages`) in a table in the `pg_class` table is merely an estimate. For a given page range (P_MIN, P_MAX), our query from above is thus extended to look like this:

```SQL
COPY (
   SELECT 
     * 
   FROM lineitem 
   WHERE 
     ctid BETWEEN '(P_MIN,0)'::tid AND '(P_MAX,0)'::tid
   ) TO STDOUT (FORMAT binary);
```
This way, we can efficiently scan the table in parallel while not relying on the schema in any way. Because page size is fixed in Postgres, this also has the added bonus of equalizing the effort to read a subset of the page independent of the number of columns in each row. 

"But wait!", you will say, according to the documentation the tuple ID is not stable and may be changed by operations such as `VACUUM ALL`. How can you use it for synchronizing parallel scans? This is true, and could be problematic, but we found a solution: 


### Transactional Synchronization
Of course a transactional database such as Postgres is expected to run transactions while we run our table scans for analytical purposes. Therefore we need to address concurrent changes to the table we are scanning in parallel. We solve this by first creating a new read-only transaction in DuckDB's bind phase, where query planning happens. We leave this transaction running until we are completely done reading the table. We use yet another little-known Postgres feature, `pg_export_snapshot()`, which allows us to get the current transaction context in one connection, and then import it into our parallel read connections using `SET TRANSACTION SNAPSHOT ...`. This way, all connections related to one single table scan will see the table state exactly as it appeared at the very beginning of our scan throughout the potentially lengthy read process.


### Projection and Selection Push-Down
DuckDB's query optimizer moves selections (filters on rows) and projections (removal of unused columns) as low as possible in the query plan (push down), and even instructs the lowermost scan operators to perform those operations if they support them. For the Postgres scanner, we have implemented both push down variants. Projections are rather straightforward - we can immediately instruct Postgres to only retrieve the columns the query is using. This of course also reduces the number of bytes that need to be transferred, which speeds up queries. For selections, we construct a SQL filter expression from the pushed down filters. For example, if we run a query like `SELECT l_returnflag, l_linestatus FROM lineitem WHERE l_shipdate < '1998-09-02'` through the Postgres scanner, it would run the following queries:

```SQL
COPY (
  SELECT 
    "l_returnflag",
    "l_linestatus" 
  FROM "public"."lineitem" 
  WHERE 
    ctid BETWEEN '(0,0)'::tid AND '(1000,0)'::tid AND 
    ("l_shipdate" < '1998-09-02' AND "l_shipdate" IS NOT NULL)
  ) TO STDOUT (FORMAT binary);
-- and so on
```

As you can see, the projection and selection pushdown has expanded the queries ran against Postgres accordingly. Using the selection push-down is optional. There may be cases where running a filter in Postgres is actually slower than transferring the data and running the filter in DuckDB, for example when filters are not very selective (many rows match).


## Performance
To investigate the performance of the Postgres Scanner, we ran the well-known TPC-H benchmark on DuckDB using its internal storage format, on Postgres also using its internal format and with DuckDB reading from Postgres using the new Postgres Scanner. We used DuckDB 0.5.1 and Postgres 14.5, all experiments were run on a MacBook Pro with an M1 Max CPU. The experiment script [is available](https://gist.github.com/hannes/d2f0914a8e0ed0fb235040b9981c58a7). We run "scale factor" 1 of TPCH, creating a dataset of roughly 1 GB with ca. 6 M rows in the biggest table, `lineitem`. Each of the 22 TPC-H benchmark queries was run 5 times, and we report the median run time in seconds. The time breakdown is given in the following table. 

|query | duckdb| duckdb/postgres| postgres|
|:-----|------:|---------------:|--------:|
|1     |   0.03|            0.74|     1.12|
|2     |   0.01|            0.20|     0.18|
|3     |   0.02|            0.55|     0.21|
|4     |   0.03|            0.52|     0.11|
|5     |   0.02|            0.70|     0.13|
|6     |   0.01|            0.24|     0.21|
|7     |   0.04|            0.56|     0.20|
|8     |   0.02|            0.74|     0.18|
|9     |   0.05|            1.34|     0.61|
|10    |   0.04|            0.41|     0.35|
|11    |   0.01|            0.15|     0.07|
|12    |   0.01|            0.27|     0.36|
|13    |   0.04|            0.18|     0.32|
|14    |   0.01|            0.19|     0.21|
|15    |   0.03|            0.36|     0.46|
|16    |   0.03|            0.09|     0.12|
|17    |   0.05|            0.75|  > 60.00|
|18    |   0.08|            0.97|     1.05|
|19    |   0.03|            0.32|     0.31|
|20    |   0.05|            0.37|  > 60.00|
|21    |   0.09|            1.53|     0.35|
|22    |   0.03|            0.15|     0.15|


Stock Postgres is not able to finish queries 17 and 20 within a one-minute timeout because of correlated subqueries containing a query on the lineitem table. For the other queries, we can see that DuckDB with the Postgres Scanner not only finished all queries, it also was faster than stock Postgres on roughly half of them, which is astonishing given that DuckDB has to read its input data from Postgres through the client/server protocol as described above. Of course, stock DuckDB is still 10x faster with its own storage, but as discussed at the very beginning of this post this requires the data to be imported there first. 

## Other Use Cases

The Postgres Scanner can also be used to combine live Postgres data with pre-cached data in creative ways. This is especially effective when dealing with an append only table, but could also be used if a modified date column is present. Consider the following SQL template:

```SQL
INSERT INTO my_table_duckdb_cache
SELECT * FROM postgres_scan('dbname=myshinydb', 'public', 'my_table') 
WHERE incrementing_id_column > (SELECT MAX(incrementing_id_column) FROM my_table_duckdb_cache);

SELECT * FROM my_table_duckdb_cache;
```

This provides faster query performance with fully up to date query results, at the cost of data duplication. It also avoids complex data replication technologies.

DuckDB has built-in support to write query results to Parquet files. The Postgres scanner provides a rather simple way to write Postgres tables to Parquet files, it can even directly write to S3 if desired. For example,
```SQL
COPY(SELECT * FROM postgres_scan('dbname=myshinydb', 'public', 'lineitem')) TO 'lineitem.parquet' (FORMAT PARQUET);
```


## Conclusion
DuckDB's new Postgres Scanner extension can read PostgreSQL's tables while PostgreSQL is running and compute the answers to complex OLAP SQL queries often faster than PostgreSQL itself can without the need to duplicate data. The Postgres Scanner is currently in preview and we are curious to hear what you think. 
If you find any issues with the Postgres Scanner, please [report them](https://github.com/duckdblabs/postgresscanner/issues). 


