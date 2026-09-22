---
layout: post
title: "Importing Data into DuckDB with Java - Practical Experience"
author: "John Nadar, Geertjan Wielenga, Alex Kasko"
excerpt: "When the analytics screen running on our main operational database got too slow, we moved a year of data into DuckDB on the same server. Getting the data in was the hard part. This is the story of every method we tried, and why a table function written in pure Java is the one we shipped."
tags: ["using DuckDB"]
thumb: "/images/blog/thumbs/mongodb.svg"
image: "/images/blog/thumbs/mongodb.png"
---

> Guest blog post by [John Nadar](https://github.com/jonadar98).

## The Analytics Screen Problem

At a company I work for we store vulnerabilities data for other companies as a collection of JSON documents in MongoDB. Our analytics screen was working fine at first but as our data volume increased - the response times start getting slow. For many months we did a lot of query optimization, restructuring, index additions, and saw significant improvement. But still the execution time for few scenarios was in 10s of seconds: for example, when returning the count of closed or open vulnerabilities or when getting top 10 vulnerable business units for last 6 months. The main issue was in our MS Excel export feature which was taking 2-3 minutes for 50k records; also the performance was not very consistent. So we needed to find an alternative.

The plan was to import our 1 year record in an alternative database and query on it. The requirements were to run all the queries in 1s or less and export 50k records in Excel format in 10s. Anything more than that will run in background.

Due to internal requirements the analytical database needs to run on the same server as MongoDB. It should be actively developed, should be free and open-source and should work well with limited resources - and DuckDB checked all the boxes.

## Sample Data Set and Code Snippets

To be able to share my performance measurement results I prepared an anonymised dataset that roughly corresponds to the data I was importing. The size of the dataset was reduced multiple times over the real one to allow running the experiments on it faster.

The dataset is available at this link: [vulnerability_sample.csv.zst](TODO: link on duckdb.org), it contains 485k records with 24 fields. Two notable fields in it are `VARCHAR` "description" and "references" that contain long strings, with corresponding median length of 5k and 2.5k characters and with many recods there being up to 32k characters. These long fields make many operations on this dataset quite expensive.

Also, along with DuckLabs editors, we prepared a number of code snippets to illustrate the data import in Java. These snippets are significantly simplified compared with actual code we run. Still their performance characteristics more or less matched the real ones. The code snippets are available in this GitHub repository [staticlibs/duckdb_java_data_import](https://github.com/staticlibs/duckdb_java_data_import).

## MongoDB Community Extension

I was looking at options to copy the data from MongoDB and found the [`mongo` community extension](https://duckdb.org/community_extensions/extensions/mongo). My first POC was created using that and it was very simple to setup and use, it looked like the following snippet:

```sql
INSTALL mongo FROM community;
ATTACH 'host=localhost port=27017 database=db1' AS m (TYPE MONGO);
CREATE OR REPLACE TABLE m.vuln1 AS FROM 'vulnerability_sample.csv.zst';
```

On the sample data this method took 55 seconds.

I was quickly able to get it up and running and import the data into DuckDB. I ran many of our analytical queries and it was very fast, sub 100ms for `GROUP BY` and `COUNT` queries and I was able to export 50k records in less than 5s. The only exceptions was when large text columns were projected those caused a degradation in performance, I have raised an [issue](https://github.com/duckdb/duckdb/issues/24935) for that.

Sorting the data gave further query performance improvement and combined with: `SET storage_compatibility_version = 'latest'` resulted into the database file size reduction.

Thus the `mongo` community extension may be the easiest, pain free and performant way to setup a MongoDB to DuckDB pipeline.

But we decided against using it because of no future-proof gurantees with community extensions. DuckDB is a fast moving project which is constantly improving and we did not want to be held back from updating to new DuckDB version just because an extension was not updated and can no longer be built.

The only real option with the community extension was to build it locally - effectively to maintain an internal fork of it. While that was a possibility, we decided against it. The burden of maintaining a C++ code base was a major factor. And besides that, we prefer our data ingestion pipeline to be written in Java, that is much easier for us to maintain, to be able to reuse parts of this pipeline to other internal data sources that we use from Java and that don't have ready-to-use DuckDB extensions for them.

Below I am describing 3 ingestion approaches I tried, using the `mongo` extension performance numbers as a reference point.

Besides these 3 there were other attemts that were aborted early. The notable one being the intermediate export from Mongo into NDJSON or CSV files and import of these files directly from DuckDB. That attempt, while looking promising at first, was aborted due to the lack of disk space for intermediate data copies.

## Standard JDBC Batch Inserts

The initial attempt on the data import with Java was done with using `INSERT` queries with standard JDBC `executeBatch` API.

For simplicity, in this and following examples the period of data to import is split in day-sized batches. With each batch fetched from Mongo separately. This approach is imperfect (the number of records per day may be quite different, a single query from Mongo may be more performant), but is very easy to implement in parallel form and was found to not skew the results too much. So for `executeBatch` a worker like this can be used:

```java
public class InsertWorker implements Runnable {
    Queue<LocalDate> queue; // concurrent queue distributed between worker threads
    MongoCollection<Document> collection; // Mongo query interface
    Connection connection; // DuckDB connection
    PreparedStatement ps; // DuckDB prepared statement

    @Override
    public void run() {
        this.ps = connection.prepareStatement("INSERT INTO staging VALUES(?, ?, ...)");
        for (;;) {
            LocalDate day = queue.poll();
            if (day == null) {// input queue exhausted
                break;
            }
            insertDayRecords(day, collection, ps);
        } 
        // error handling omitted
    }

    static void insertDayRecords(LocalDate day, MongoCollection<Document> collection, PreparedStatement ps) {
        MongoCursor<Document> docs = collection.find(Filters.and( // other filters omittted 
                Filters.gte("updated_date", day.atStartOfDay().toInstant(ZoneOffset.UTC)),
                Filters.lt("updated_date", day.plusDays(1).atStartOfDay().toInstant(ZoneOffset.UTC))
        )).iterator();
        int count = 0;
        while (docs.hasNext()) {
            Document doc = docs.next();
            ps.setString(1, doc.getObjectId("_id").toString());
            ps.setString(2, doc.getString("vendor"));
            // other 22 fields omitted
            ps.addBatch();
            count++;
        }
        if (count > 0) {
            ps.executeBatch();
        }
    }
}
```

Note, that it is not necessary to change anything about transactions handling, like disabling auto-commit, because we call `executeBatch` on all the records of the chosen day and this `executeBatch` call will start and commit the single transaction for us automatically.

Running 8 of such workers in parallel we import data into a table in a staging DuckDB database file. And then copy the staging table into the final database file adding `ORDER BY updated_date DESC` sorting, that was found to drastically improve the resulting database file size.

Overall time with this approach on the sample data was 3 min 37 seconds. With the last `CREATE TABLE ... AS FROM ... ORDER BY` taking about 30 seconds.

The 3.5x slower performance comparing with the `mongo` extension is largely caused by the lack of real "batch" insert support in DuckDB. The `executeBatch` is implemented on Java level. And while the statement is prepared only once per batch, the each entry in the batch is run in a separate database level `INSERT`, thus incurring per-row cost. To solve this the Appender was tried next.

## Java Appender Interface

DuckDB [Appender](https://duckdb.org/docs/current/data/appender) is exposed in Java with the `Connection#createAppender` method. The worker for Appender can be structured very similar to the batch insert worker above:

```java
public class AppendWorker implements Runnable {
    Queue<LocalDate> queue; // concurrent queue distributed between worker threads
    MongoCollection<Document> collection; // Mongo query interface
    Connection connection; // DuckDB connection
    DuckDBAppender appender; // Appender insatnce

    @Override
    public void run() {
        this.appender = connection.createAppender("staging_db", "main", "vuln1");
        for (;;) {
            LocalDate day = queue.poll();
            if (day == null) {// input queue exhausted
                break;
            }
            appendDayRecords(day, collection, appender);
        }
        // error handling omitted
    }

    static void appendDayRecords(LocalDate day, MongoCollection<Document> collection, DuckDBAppender appender) throws Exception {
        MongoCursor<Document> docs = collection.find(...).iterator();
        int count = 0;
        while (docs.hasNext()) {
            Document doc = docs.next();
            appender.beginRow();
            appender.append(doc.getObjectId("_id").toString());
            appender.append(doc.getString("vendor"));
            // other 22 fields omitted
            appender.endRow();
            count++;
        }
        if (count > 0) {
            appender.flush();
        }
    }
}
```

Unlike the `executeBatch`, the Appender in DuckDB is doing actual batching - a [Data Chunk](https://duckdb.org/docs/lts/clients/c/data_chunk) of 2048 rows is prepared in Java and then flushed to DuckDB at once.

Overall time with this approach on the sample data was 2 min 2 seconds. It is still 2x (or 1.5x if we exclude final CTAS with sorting) slower than the `mongo` extension. On real data this performance was not acceptable so I continued the experiments.

## COPY over a Java Table Function

After accepting defeat with the `Appender` and on the verge of giving up, thinking I cannot beat the mongo extension, I did what I should have done much earlier. I looked inside the `mongo` community extension code to find out what it is doing internally so I can redo it in Java. It appeared that the extension was using user-defined table functions. So I searched properly regarding table functions for the first time and found two following resources that appeared to be very helpful:

 - [Benchmarking DuckDB From Java: Fast INSERT, UPDATE, and DELETE](https://sqg.dev/blog/java-duckdb-benchmark/)
 - [DuckDB Table Functions in Java](https://duckdb.org/2026/08/25/table-functions-in-java)

Based on them the following parallel table function can be used with sample data:

```java
DuckDBFunctions.tableFunction()
            .withName("vuln_import")
            .withParameters(LocalDate.class, LocalDate.class)
            .withFunction(new ImportFunction())
            .register(conn);
stmt.execute("SET preserve_insertion_order = FALSE"); // necessary to allow parallel import
stmt.execute("CREATE TABLE staging.vuln1 AS FROM vuln_import('2026-02-13'::DATE, '2026-08-13'::DATE)");
```

Where the key parts of the `ImportFunction` are (see the full example in [duckdb_java_data_import](https://github.com/staticlibs/duckdb_java_data_import) repo):

```java
public class ImportFunction implements DuckDBTableFunction<BindData, GlobalData, LocalData> {

    @Override
    public BindData bind(DuckDBTableFunctionBindInfo info) {
        LocalDate from = info.getParameter(0).getLocalDate();
        LocalDate to = info.getParameter(1).getLocalDate();

        info.addResultColumn("_id", String.class);
        info.addResultColumn("vendor", String.class);
        // other 22 columns omitted
        return new BindData(from, to);
    }

    @Override
    public GlobalData init(DuckDBTableFunctionInitInfo info) {
        BindData bdata = info.getBindData();
        info.setMaxThreads(8);
        // open connection to Mongo, prepare days queue
        return new GlobalData(client, collection, queue);
    }

    @Override
    public long apply(DuckDBTableFunctionCallInfo info, DuckDBDataChunkWriter output) {
        GlobalData gdata = info.getInitData();
        LocalData ldata = info.getLocalInitData();

        while (ldata.cursor == null || !ldata.cursor.hasNext()) {
            LocalDate day = gdata.queue.poll();
            if (day == null) { // input queue exhausted
                return 0;
            }
            // fetch the day data from Mongo
            ldata.cursor = gdata.collection.find(...).iterator();
        }

        long row = 0;
        for (; ldata.cursor.hasNext() && row < output.capacity(); row++) {
            Document doc = ldata.cursor.next();
            output.vector(0).setString(row, doc.getObjectId("_id").toString());
            output.vector(1).setString(row, doc.getString("vendor"));
            // other 22 fields omitted
        }
        return row;
    }
}

```

We are using our table function as data source on which we are running the CTAS query. `apply` method is invoked by DuckDB repeateadly, each time it can write up to 2048 (`output.capacity()`) rows to the output. The source is considered to be exhausted, when there are no more "days" in the input queue and 0 records count is returned from `apply`.

To make the query over this function to run in parallel we need two bits:

 - `info.setMaxThreads(8)` in `globalInit`: tells DuckDB that function supports multiple parallel `apply` calls
 - `SET preserve_insertion_order = FALSE`: tells DuckDB that there is no need to preserve the order in which records (data chunks) are read from table function when inserting them into the newely created table. If this flag is not set to `FALSE` - DuckDB will only call the `apply` from a single thread to preserve the order. In our case we are doing sorting as a post-processing step after the import, so do not need to preserve the order.

With this approach the overall time on the sample data was 1 minute 27 seconds. That is still slower than the `mongo` extension, but if we exclude 30 seconds of sorting time (that is offloaded to Mongo in `mongo` extension approach) - the resulting time will be almost the same. Note, that we still can offload the sorting to Mongo if we give up the parallel processing and run the table function in a single thread mode.

On real data (where I did not use day-sized Mongo queries) the performance was close to the `mongo` extension. As a result we got a robust ingestion pipeline written in pure Java and learned how to use DuckDB with user-defined table functions in practice.
