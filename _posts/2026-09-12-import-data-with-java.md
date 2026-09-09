---
layout: post
title: "Importing 2.7 Million MongoDB Records into DuckDB from Java"
author: "Guest Author, Geertjan Wielenga, Alex Kasko"
excerpt: "When the analytics screen running on our main MongoDB database got too slow, we moved a year of data into DuckDB on the same server. Getting the data in was the hard part. This is the story of every method we tried, and why a table function written in pure Java is the one we shipped."
tags: ["using DuckDB"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

> This is a guest post. The author is a Java developer who maintains the analytics features of a vulnerability management application. The technical editing was done by Alex Kasko, maintainer of the DuckDB Java client.

## TL;DR

We store vulnerability data for our customers in MongoDB, and the analytics screen ran its aggregations straight against that collection. By about 2.7 million records it was too slow, and months of tuning queries and adding indexes had not fixed it. So we decided to copy one year of data into DuckDB on the same server and run the analytics there.

Getting the data in was the hard part. The obvious tool, the [MongoDB community extension]({% link community_extensions/extensions/mongo.md %}), was also the fastest thing I tried, but it is unreviewed native C++, and as a Java team with strict security audits and a fast DuckDB upgrade cadence we could not ship it. So the real question was whether I could match it from pure Java, with no native code. The Appender and exporting to files both fell short. What finally worked was a table function written in Java, following the [Table Functions in Java]({% post_url 2026-08-25-table-functions-in-java %}) post: it hit the same import time and the same 3.34 GB file as the extension, a parallel version beat it, and the whole import stayed a single SQL statement with nothing but Java in the build. This post walks through every attempt and why the table function won.

## Why We Looked at DuckDB

Our analytics screen ran aggregations over the vulnerability data: how many vulnerabilities are open or closed, the ten most affected business units over the last six months, and similar reports. There was also an export to Excel.

When the collection was small this was fine. As it grew, some queries took tens of seconds. We spent months on query optimization, restructuring and new indexes, and the numbers improved a lot, but a few scenarios were still stuck in the tens of seconds. The Excel export was the worst of it, two to three minutes for 50,000 records, and the response times were not consistent from one run to the next.

So we set two targets. Every query on the analytics screen should finish in one second or less, and an export of 50,000 records should complete in ten seconds. Anything slower would move to a background job.

There were constraints outside performance too. The company was cutting costs, so a new server was out of the question. Whatever we chose had to run next to MongoDB on the same machine, and it had to be free, open source and actively developed. DuckDB checked every box.

A note on the numbers before I start. I have rounded them so the setup is easy to reproduce. The collection holds about 2.7 million documents with roughly 50 fields each. Two of those fields hold long text, a description and a list of references, and for the customer whose data I tested with they run from 15,000 to 32,000 characters. An average record is about 8 KB and the largest are around 60 KB. My workstation has 4 cores, 32 GB of RAM and 38 GB of free SSD space. I gave DuckDB 4 threads and a 12 GB memory limit, and the JVM 4 GB of heap.

```sql
SET threads = 4;
SET memory_limit = '12GB';
```

## The MongoDB Community Extension

My first proof of concept used the [MongoDB community extension]({% link community_extensions/extensions/mongo.md %}). It takes minutes to set up, and the entire import is a single statement:

```sql
INSTALL mongo FROM community;
LOAD mongo;
ATTACH 'host=localhost port=27017' AS mongo_db (TYPE MONGO);

CREATE OR REPLACE TABLE vulnerability AS
    SELECT ⟨columns⟩
    FROM mongo_db.vulndb.vulnerability
    ORDER BY ⟨sort columns⟩; -- the columns the analytics screen filters and groups on
```

It consistently took 18 to 20 minutes to copy the 2.7 million documents, and the queries afterward were fast. Group and count queries came back in under 100 ms, and exporting 50,000 records took less than 5 seconds. Sorting the data during the import made query times better still. The one exception is queries that project the long text columns. Sorting a result that includes them is much slower even when they are not in the `ORDER BY` or the `WHERE` clause. I reported that in [duckdb/duckdb#24935](https://github.com/duckdb/duckdb/issues/24935).

### File Size and `storage_compatibility_version`

The first database file was about 19 GB. Sorting brought it down to 15 GB. Then I set the storage format to the latest version:

```sql
SET storage_compatibility_version = 'latest';
```

The same data now took 3.34 GB. At first I thought I had made a mistake and lost some records, but the data was all there. The default value is `v0.10.2`, which keeps the file readable by old DuckDB releases and does not use the newer compression. If you do not need to open the file with an old version of DuckDB, set this before you load anything. It is easy to miss, and for us it was the difference between 15 GB and 3.34 GB.

### Why I Didn't Ship It

The community extension is the simplest and fastest way I found to move data from MongoDB into DuckDB. I still did not use it, for three reasons.

Community extensions are not reviewed by the DuckDB team, and the documentation says so plainly: DuckLabs and the DuckDB Foundation do not vet the code within community extensions and cannot guarantee they are safe to use. Our internal security audits are strict and take anywhere from a day to several days per finding. So when I presented the proof of concept, the decision was to try everything else before running unreviewed native code inside the database process.

The extension is also built against a specific DuckDB version, and at the time there was no build for 1.5.5, the release we wanted. We are still moving fast and did not want our upgrade schedule tied to a third-party extension.

Finally, nobody on the team writes C++. All our projects are Java, so building the extension ourselves and keeping an internal fork was not something we seriously considered.

That left the extension as the benchmark to beat from Java: about 20 minutes to import, a 3.34 GB file, and sub-second queries.

## The Appender

The plan for the [Appender]({% link docs/current/clients/java/data_import.md %}#appender) was to load every row into a table first, then build the final sorted table with `CREATE TABLE AS SELECT`.

My first version used four threads reading from MongoDB into a queue that held 50,000 documents, and one thread draining that queue into an Appender. The readers filled the queue faster than the single Appender could empty it. Loading the unsorted table took 22 minutes, and I had not even started sorting.

The second version used four Appender threads, each with its own duplicated connection and transaction, fed by four queues. That needed a fair amount of coordination code. If one thread fails, the others have to stop, and at the end either all four transactions commit or all of them roll back.

```java
try (DuckDBConnection conn =
         (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:dest.duckdb")) {
    conn.setAutoCommit(false);
    try (DuckDBAppender appender = conn.createAppender("main", "vulnerability_raw")) {
        Document doc;
        while ((doc = queue.take()) != POISON_PILL) {
            appender.beginRow();
            appender.append(doc.getString("company_id"));
            appender.append(doc.getString("business_unit"));
            // ... the remaining columns
            appender.endRow();
        }
    }
    conn.commit();
}
```

The four-thread version took 18 minutes. That is four minutes saved for code that made my head hurt, and the sort still had to run afterward. The unsorted load alone already took about as long as the whole extension run, and adding the sort on top of that would put it over, so I stopped here.

## Exporting to NDJSON and CSV

The next idea was to keep JDBC out of the bulk of the work. I would write the documents to files from Java, then load the files with `read_json` or `read_csv`.

Writing four NDJSON files in parallel took 14 minutes and produced 24 GB. Replacing Mongo's `RawBsonDocument.toJson()` with [Apache Fory](https://fory.apache.org/) for serialization cut that to 9 minutes, and compressing the output with zstd saved about another minute. The import was the problem:

```sql
CREATE OR REPLACE TABLE vulnerability AS
    SELECT ⟨columns⟩
    FROM read_json('export/*.ndjson.zst')
    ORDER BY ⟨sort columns⟩;
```

This ran for more than 20 minutes and then failed because the disk filled up. The export files, the growing database file, and the temporary files DuckDB writes while sorting did not fit into the 38 GB I had. The partial database was already over 10 GB when the import died, well above the 3.34 GB the extension produced.

CSV was quicker to write, 8 minutes for 21 GB, and failed the same way during the import. Even ignoring the disk, the total would have been write time plus import time, and the write alone was already close to half of the extension's whole run. I dropped this approach.

## A Table Function in Java

After giving up on the Appender, and pretty much convinced I could not beat the extension, I did the thing I should have done at the start. I asked an AI assistant to read the MongoDB extension's source and tell me how it worked. The answer was that it is a table function. I searched for table functions properly for the first time and found the [Table Functions in Java]({% post_url 2026-08-25-table-functions-in-java %}) post, published a few days earlier.

I had actually seen table functions mentioned before, in a [benchmark of DuckDB from Java](https://sqg.dev/blog/java-duckdb-benchmark/), but the examples there looked complicated and I did not follow up. In hindsight that cost me several days. The post from the DuckDB team was easy to follow, and I had a single-threaded table function reading from MongoDB working quickly.

The function is registered with the `DuckDBFunctions.tableFunction()` builder and implemented as a `DuckDBTableFunction` with the three callbacks from that post: `bind` declares the result columns, `init` opens the MongoDB cursor, and `apply` fills one chunk of up to 2048 rows per call. Simplified:

```java
DuckDBFunctions.tableFunction()
    .withName("mongo_vulnerability")
    .withFunction(new VulnerabilityFunction())
    .register(connection);
```

```java
public class VulnerabilityFunction implements DuckDBTableFunction {

    static final List<String> COLUMNS = List.of("company_id", "business_unit", /* ... */);

    public BindData bind(DuckDBTableFunctionBindInfo info) {
        for (String name : COLUMNS) {
            info.addResultColumn(name, String.class);
        }
        return new BindData(mongoCollection());
    }

    public InitData init(DuckDBTableFunctionInitInfo info) {
        info.setMaxThreads(1);
        BindData bindData = info.getBindData();
        return new InitData(bindData.collection.find().cursor());
    }

    public long apply(DuckDBTableFunctionCallInfo info, DuckDBDataChunkWriter output) {
        MongoCursor<Document> cursor = info.getInitData().cursor;
        long row = 0;
        for (; row < output.capacity() && cursor.hasNext(); row++) {
            Document doc = cursor.next();
            for (int col = 0; col < COLUMNS.size(); col++) {
                String value = doc.getString(COLUMNS.get(col));
                if (value == null) {
                    output.vector(col).setNull(row);
                } else {
                    output.vector(col).setString(row, value);
                }
            }
        }
        return row; // 0 means no more data
    }
}
```

The non-string columns use `setInt`, `setLong`, `setTimestamp` and so on. The list-of-references field is joined into one comma-separated value here and split with `string_split` on the SQL side, because nested types are not supported in the vector API yet.

With that in place the import is one SQL statement again, and it reads exactly like the extension version:

```sql
CREATE OR REPLACE TABLE vulnerability AS
    SELECT ⟨columns⟩
    FROM mongo_vulnerability()
    ORDER BY ⟨sort columns⟩;
```

Fetching, loading and sorting all happened in that one query in 20 minutes, less than the single-threaded Appender needed for the unsorted load on its own. The database file was 3.34 GB, the same as the extension. The code was shorter than the multi-threaded Appender and had no transaction handling at all, since a single `CREATE TABLE AS` commits or rolls back on its own.

### Missing Fields and Uninitialized Vectors

The `setNull` branch above was not in my first version. MongoDB does not return a field that is missing from a document, so my first attempt walked the fields each document actually had and wrote those into the vectors. Documents that were missing a field left a slot behind that I never wrote.

The result was baffling. Sometimes the JVM died right after the first chunk, with no exception and no stack trace. Sometimes it failed with an out of memory error. Neither pointed anywhere near the real cause, and it took me a while to find it.

The reason is how a string is stored in a vector. Each entry holds a length, a short prefix and a pointer to the string data. An entry I never wrote contained whatever happened to be in that memory. On read, DuckDB either followed a garbage pointer and crashed, or read a garbage length and tried to allocate a huge string, which failed with out of memory. The fix is to write every slot of every vector in every chunk, and to call `setNull` when a document does not have the field.

At the time the Java API had no guard against this. It does now: output vectors passed to Java table function and scalar callbacks (and to the Appender) are zeroed between invocations, so a slot you forget to write can no longer crash the JVM. The change landed in [duckdb-java#864](https://github.com/duckdb/duckdb-java/pull/864) and was backported to the 1.5 branch in [duckdb-java#865](https://github.com/duckdb/duckdb-java/pull/865). You still want to call `setNull` for a missing field, otherwise it comes through as an empty string or a zero rather than `NULL`, but the silent crash is gone.

### Running It in Parallel

To use all four cores, `init` first runs a `$bucketAuto` aggregation that splits the collection into four `_id` ranges of roughly equal size, and `setMaxThreads(1)` becomes `setMaxThreads(4)`. The `initLocal` callback then opens one MongoDB cursor per thread, each over one range, and `apply` reads from the cursor of the thread it runs on. Four MongoDB queries run at once, and DuckDB merges the chunks.

```java
List<Document> buckets = collection.aggregate(List.of(
    new Document("$bucketAuto",
        new Document("groupBy", "$_id").append("buckets", 4))
)).into(new ArrayList<>());
```

With four threads the full import dropped from 20 minutes to 16, faster than the extension, with the same file size and the same query performance afterward.

## Summary

| Method                          | Time to sorted table  | Result                                 |
|---------------------------------|----------------------:|----------------------------------------|
| MongoDB community extension     | 18 to 20 min          | Not allowed by security policy         |
| Appender, 1 writer thread       | 22 min (unsorted)     | Too slow before sorting                |
| Appender, 4 writer threads      | 18 min (unsorted)     | Too slow, complex transaction handling |
| Export to NDJSON, `read_json`   | 9 min + failed import | Ran out of disk during sort            |
| Export to CSV, `read_csv`       | 8 min + failed import | Ran out of disk during sort            |
| Java table function, 1 thread   | 20 min                | Works, one statement, 3.34 GB file     |
| Java table function, 4 threads  | 16 min                | Final choice                           |

The parallel table function is what we settled on for the ingestion pipeline. A few things I took away from this:

* Set `storage_compatibility_version` to `latest` before loading data if you do not need to open the file with an old DuckDB version. For us it was the difference between 15 GB and 3.34 GB.
* Sorting during the import with `CREATE TABLE AS ... ORDER BY` costs time but pays off in query speed and compression. On a machine with little free disk, avoid intermediate files so the sort has room for its temporary data.
* If a table function can produce a row, fill every column of that row. A missing field has to become `NULL` explicitly.
* If the source can be read as a cursor from Java, a table function is the simplest way into DuckDB. It removed both the staging table and the export files, and it needed no native code.

Two things are still open. The sorting slowdown when long text columns are in the projection is being looked at by the DuckDB team. And nested types are not yet supported in the vector API. The comma-separated workaround is fine for a list of strings, but our other collections hold arrays of nested documents, which need list and struct support. That is planned, and I hope to help with it.
