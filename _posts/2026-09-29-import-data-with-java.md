---
layout: post
title: "Importing Data using Java Table Functions"
author: "Guest Author, Geertjan Wielenga, Alex Kasko"
excerpt: "When the analytics screen running on our main operational database got too slow, we moved a year of data into DuckDB on the same server. Getting the data in was the hard part. This is the story of every method we tried, and why a table function written in pure Java is the one we shipped."
tags: ["using DuckDB"]
thumb: "/images/blog/thumbs/mongodb.svg"
image: "/images/blog/thumbs/mongodb.png"
---

> Guest blog post by a DuckDB user.

## The Analytics Screen Problem

At the company where I work, we store vulnerability data for our clients as a collection of documents in MongoDB. Initially, our analytics screen performed well, but as our data volume increased, response times began to slow. For many months we did a lot of query optimization, restructuring, index additions, and saw significant improvement. However, execution times for certain scenarios remained in the tens of seconds, for example, when returning counts of closed/open vulnerabilities or when getting the top 10 most vulnerable business units for last six months. The main issue was in our MS Excel export feature which was taking 2-3 minutes for 50,000 records, and performance was often inconsistent. So we needed to find an alternative.

The plan was to import one year record into an alternative database and run analytical queries on it. The requirements were to run all the queries under one second or less and export 50,000 records in Excel format under ten seconds. Anything more than that would be handled in background.

Due to internal requirements, the analytical database had to run on the same server as MongoDB. It needed to be actively developed, free, open-source and capabale of working well with limited resources - and DuckDB checked all the boxes.

## Sample Data Set and Code Snippets

To share my performance measurement results, I have prepared an anonymized dataset that roughly corresponds to the data used in our production environment. The size of this dataset has been scaled down significantly from the original to allow for faster experimentation.

The dataset is available at this link: [vulnerability_sample.csv.zst](TODO: link on duckdb.org), it contains 485168 records with 24 fields. Two notable fields are the `VARCHAR` "description" and "references"which contain long strings with median lengths of 5,000 and 2,500 characters, respectively. Some records contain strings as large as 32,000 characters, making many operations on this dataset computationally expensive.

Additionally, along with DuckLabs editors, I have prepared several code snippets to illustrate data import in Java. While these snippets are significantly simplified compared to the code we run, their performance characteristics more or less matched the real ones. The code snippets are available in this GitHub repository [staticlibs/duckdb_java_data_import](https://github.com/staticlibs/duckdb_java_data_import).

## MongoDB Community Extension

While exploring options to copy the data from MongoDB, I discovered the [`mongo` community extension](https://duckdb.org/community_extensions/extensions/mongo). My first proof-of-concept was created using this extension, and it was very simple to setup and use, the implementation looked like this:

```sql
INSTALL mongo FROM community;
ATTACH 'host=localhost port=27017 database=db1' AS m (TYPE MONGO);
CREATE OR REPLACE TABLE m.vuln1 AS FROM 'vulnerability_sample.csv.zst';
```

Using the sample dataset, this query took 55 seconds.

I was quickly able to get it up and running and import the data into DuckDB. I ran many of our analytical queries and it was very fast, under 100ms for `GROUP BY` and `COUNT` queries and I was able to export 50,000 records in less than 5 seconds. The only exception was when projecting large text columns, which caused a performance degradation; I have raised an [issue](https://github.com/duckdb/duckdb/issues/24935) about that.

Sorting the data provided further query performance improvements, and using `SET storage_compatibility_version = 'latest'` resulted in a significant reduction in the database file size.

Ultimately, the `mongo` community extension appears to be the easiest, most painless, and performant ways to set up a MongoDB-to-DuckDB pipeline.

However, we decided against using it due to the lack of "future-proof" guarantees associated with community extensions. DuckDB is a fast- moving project which is constantly improving, and we did not want to be held back from updating to new DuckDB version simply because an extension was not updated and can no longer be built.

The only real option for using the community extension would have been to build it locally - effectively maintaining an internal fork of it. While possible, we decided against this for two reasons. First, the burden of maintaining a C++ codebase was a major concern. Second, we prefer our data ingestion pipelines to be written in Java, that is much easier for us to maintain, and to be able to reuse parts of this pipeline across other internal data sources that we use from Java and that do not have ready-to-use DuckDB extensions.

Below, I describe the three ingestion approaches I tested, using the `mongo` extension's performance numbers as a baseline.

Besides these three, there were other attempts that were abandoned early. The notable one being the intermediate export from MongoDB into NDJSON/CSV/Parquet files and then importing those files directly from DuckDB. While promising at first, this approach was aborted due to the lack of disk space for the intermediate data copies.

## Standard JDBC Batch Inserts

The initial attempt at importing data with Java utilized `INSERT` queries via the standard JDBC `executeBatch` API.

For simplicity, in this and subsequent examples, the data import period is divided into day-sized batches. With each batch fetched from MongoDB separately. This approach is imperfect (the number of records per day may be quite different, a single query from Mongo may be more performant), but is very easy to implement in parallel form and was found to not skew the results too much. Consequently, the following worker can be used to run `executeBatch`:

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

Note, that it is not necessary to change anything about transactions handling, like disabling auto-commit, because calling `executeBatch` on all records for a given day automatically handles the start and commit/rollback of a single transaction.

By running eight of these workers in parallel, we import data into a staging DuckDB database file. We then copy the staging table into the final database file using an `ORDER BY updated_date DESC` clause, because sorting was found to drastically improve the resulting database file size.

> Sorting the data in a post-processing step allowed us to easily run the import in parallel. However this requires an intermediate copy of the data, and the sorting step itself is relatively expensive due to large `VARCHAR` fields.

With this approach, the total execution time on the sample data was 3 minutes and 37 seconds, with the final `CREATE TABLE... AS... ORDER BY` operation taking approximately 30 seconds.

The performance being 3.5x slower compared to the `mongo` extension is largely due to the lack of native "batch" insert support in DuckDB. The `executeBatch` is implemented on Java level. And while the statement is prepared only once per batch, the each entry in the batch is run in a separate database-level `INSERT`, thereby incurring a per-row overhead.

## Java Appender Interface

The next attemp was to use the [Appender](https://duckdb.org/docs/current/clients/java/data_import#appender) interface, that is exposed in Java with the `Connection#createAppender` method. The worker for Appender can be structured very similar to the batch insert worker above:

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

Unlike `executeBatch`, the DuckDB Appender performs true batching: a [Data Chunk](https://duckdb.org/docs/lts/clients/c/data_chunk) of 2,048 rows is prepared in Java and then flushed to DuckDB in a single operation.

With this approach, the total execution time on the sample data was 2 minutes and 2 seconds. This remains 2x slower than the `mongo` extension (or 1.5x if the final CTAS with sorting is excluded). On real data this performance was not acceptable so I continued the experiments.

## COPY over a Java Table Function

After accepting defeat with the `Appender` and on the verge of giving up, thinking I cannot beat the `mongo` extension, I did what I should have done much earlier. I looked inside the `mongo` community extension code to find out what it is doing internally so I can do the same in Java. It appeared that the extension was using user-defined table functions. So I searched properly regarding table functions for the first time and found two following resources that appeared to be very helpful:

 - [Benchmarking DuckDB From Java: Fast INSERT, UPDATE, and DELETE](https://sqg.dev/blog/java-duckdb-benchmark/)
 - [DuckDB Table Functions in Java](https://duckdb.org/2026/08/25/table-functions-in-java)

Based on them the following parallel table function can be used with the sample dataset:

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

In this implementation, we use our table function as the data source for the `CREATE TABLE` query. The `apply` method is invoked by DuckDB repeateadly, each time it can write up to 2048 (`output.capacity()`) rows to the output.  The source is considered exhausted once the input queue is empty and the `apply` method returns a record count of zero.

To make the query over this function to run in parallel we need two bits:

 - `info.setMaxThreads(8)` in `globalInit`: tells DuckDB that function supports multiple concurrent `apply` calls
 - `SET preserve_insertion_order = FALSE`: tells DuckDB that it is not necessary to maintain the original order of records as they are read from the table function during insertion. If this flag is not set to FALSE, DuckDB will restrict apply calls to a single thread to preserve order. Since we perform sorting as a post-processing step after the import, preserving the insertion order is unnecessary.

With this approach, the total execution time on the sample data was 1 minute and 27 seconds. While it does not achieve the `mongo` extension time (it is not an apples-to-apples comparison due to day-sized queries and post-procesing sorting) - it incurs the least overhead among all Java approaches I tried.

On real data, due to storage space restrictions, I ended up with a non-parallel version of the table function, where `ORDER BY` was run in the same `CREATE TABLE` query without intermediate copies. It allowed me to achieve the import times on-par with the `mongo` extension. And as a result we got a robust ingestion pipeline written in pure Java that can be adapted for other data sources.
