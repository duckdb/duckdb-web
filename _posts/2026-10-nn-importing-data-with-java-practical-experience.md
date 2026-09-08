---
layout: post
title: "Importing Data with Java - Practical Experience"
author: "Guest Writer, Geertjan Wielenga, Alex Kasko"
excerpt: "When analytics running on a main operational database starts struggling - DuckDB can help! This article describes a journey to the fast data import with Java."
tags: []
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

> Guest blog post by [Guest Author](https://TODO) ([Company Inc.](https://TODO/)).

At Company Inc. we store vulnerabilities data for other companies as a collection of JSON documents in MongoDB. Our analytics screen was working fine at first but as our data volume increased - the response times start getting slow. For many months we did a lot of query optimization, restructuring, index additions, and saw significant improvement. But still the execution time for few scenarios was in 10s of seconds: for example, when returning the count of closed or open vulnerabilities or when getting top 10 vulnerable business units for last 6 months. The main issue was in our MS Excel export feature which was taking 2-3 minutes for 50k records; also the performance was not very consistent. So we needed to find an alternative.

The plan was to import our 1 year record in an alternative database and query on it. The requirements were to run all the queries in 1s or less and export 50k records in Excel format in 10s. Anything more than that will run in background.

We were having budget cuts so we cannot ask for another server for this new database - it needs to run on the same server as MongoDB. It should be actively developed, should be free and open-source and should work well with limited resources - and DuckDB checked all the boxes.

## MongoDB Community Extension

I was looking at options to migrate our data from MongoDB and found the [mongo community extension](https://duckdb.org/community_extensions/extensions/mongo). My first POC was created using that and it is very simple to setup and use. The main export query looked like this:

```sql
CREATE TABLE local_duckdb_table_on_disk AS FROM remote_mongo_collection WHERE date1 > [...] AND date1 < [...] ORDER BY col1
```

It consistently took 18-20 mins to copy ~2.7 million records. I was quickly able to get it up and running and import the data into DuckDB. I ran many of our analytical queries and it was very fast, sub 100ms for `GROUP BY` and `COUNT` queries and I was able to export 50k records in less than 5s. The only exceptions was when large text columns were projected those caused a degradation in performance, I have raised an [issue](https://github.com/duckdb/duckdb/issues/24935) for that.

Sorting the data gave further query performance improvement and combined with `storage_compatibility_version : latest` resulted into the database file size reduction.

Thus the community extension my be the best, pain free and performant way to setup a MongoDB to DuckDB pipeline.

But we decided against using it because of the no safety gurantee of community extension. DuckDB is a fast moving project which was constantly improving and we are still in the analysis and POC phase so we did not want to be held back from updating to new DuckDB version just because an extension is not yet built for that yet, which was the case with mongo extension which is not yet available for 1.5.5.

"DuckLabs and the DuckDB Foundation do not vet the code within community extensions and, therefore, cannot guarantee that DuckDB community extensions are safe to use. "

There was an option to build the community extension locally - effectively to to maintain an inernal fork of it. Just we don't have anybody with C++ knowledge. All of our projects are in Java. So that possibility was never seriously considered. Our internal security audits are very strict, we get anywhere from a day to few days depending on issue severity. So when I presented the POC with the `mongo` community extension internally - we decided we want to exhaust other options first.

So we chose to write our own ingestion pipeline from scratch using Java. 

I forgot to mention, duckdb was configured to use 4 threads and 12GB memory. The community extension set the benchmark for all the different methods I tried.

Also I want to add one more thing. In my initial POC using `mongo` community extension my intial database file size was around ~19GB, and with sorting it went down to ~15GB. But when I set `storage_compatibility_version` to latest it went down dramatically to 3.34GB. I was confused at first whether I made some mistake but it was just the storage improvements in the latest DuckDB.

## Plain inserts

Initial attempt on the data import with Java was done with using plain `INSERT` queries. That attempt did not go too far - it was quickly discovered, that the `executeBatch()` approach does not do the batching on the database/storage level. JDBC driver tries to lower the overhead, by placing the whole batch into a single transaction and preparing the query only once per-batch. But the insertion is still done record by record and that is not well suited when importing large amounts of data for analytics.

## Appender

Next attemp was in using the [Appender](https://duckdb.org/docs/current/clients/java/data_import#appender) interface.

My plan with `Appender` was to first write all the data to the table. Then, once all data is imported, to use `CREATE TABLE AS SELECT` to sort and recerate the table. 

I tried first with a  single `Appender` writer thread reading from a queue and 4 reader threads to read from MongoDB and write to a queue. And the `Appender` was not able to keep up. The queue size was 50000 and `Appender` was not able to exhaust the queue faster then the writer could fill the queue. It took me 22 min to write 2.7 million records. JVM has 4GB RAM. DuckDB has 4 threads, 12GB RAM. 

Then I tried with 4 `Appender` writer threads, each with their own duplicate connection and transaction. And 4 reader threads to read from MongoDB and write to 4 queue 1 for each `Appender` writer thread. I had to implement logic to stop other threads if any one of the threads threw and exception. I also had to implement logic to commit if none of the threads threw an exception or rollback if any did.
The implementation made my head hurt and took 18 min. Very minor improvement compared to the complexity involved.

I abandoned Appenders because if the first step itself was taking 18 min then the next step will just add more time and I will never be able to beat the benchmark set by the `mongo` community extension.

## External Files

Next I tried exporting the MongoDB data to both NDJSON and CSV and importing from them.

I wrote 4 json files in parallel which took 14 minutes for 2.7 million records. The total file size was 24 GB. The final step of importing the data into DuckDB took more than 20 minutes before failing due to insufficient space. I have limited space in my work machine.

As for CSV, it took 8 minutes to write 4 files in parallel and the import query ran forever before failing due to insufficient space. Total file size was 21GB.

Replacing Mongo's `RawBsonDocument.toJson()` with [Apache Fory](https://fory.apache.org/) for the JSON serialization cut down the writing time to  9 minutes.

I tried writing as compressed files using ZSTD and it actually saved me 1 minutes each in writing time. But still the import query ran forever.

Also, the final database file size even with sorting while importing JSON or CSV, was above 10GB before failure. Which was far higher than the final DB size of 3.34GB

## Table Functions

The performance degradation I mentioned earlier led me to the DuckDB discord to find answers or solutions for this 1 issue in otherwise excellent experience with DuckDB and that's where I found this benchmark - https://sqg.dev/blog/java-duckdb-benchmark/. I looked the numbers and thought to use UDF but I couldn't understand the provided examples and thought it was too complex and did not check it further (which was mistake as it would have saved me many days). I wanted to exhaust options in DuckDB first before pursuing other formats like Arrow or Parquet so I started checking the `Appender`. 

After accepting defeat with the `Appender` and on the verge of giving up, thinking I cannot beat the mongo extension, I did what I should have done much earlier. I asked CoPilot to read the `mongo` community extension code what it is doing internally so I can redo it in Java. It told me that the extension was using user-defined table functions. So I searched properly regarding table functions for the first time. I immediately came across this blog post: https://duckdb.org/2026/08/25/table-functions-in-java, which was posted on 25th August, excellent timing. The blog was very easy to follow. I was quickly able to implement my requirement as a single-threaded table function. 

I was able to cut down my 3 step process fetch from MongoDB, append to DuckDB, sort the data into a single query which now takes 20 minutes compared to 22 min just for appending data.  Compared to multi-threaded Appenders this was easier to implement.

I have parallelized the UDF overriding the localInit and setting max threads - TODO.
