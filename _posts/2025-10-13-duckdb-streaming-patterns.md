---
layout: post
title: "Streaming Patterns with DuckDB"
author: "Guillermo Sanchez"
thumb: /images/blog/streaming_patterns/streaming-patterns-wide.svg
image: /images/blog/streaming_patterns/streaming-patterns-wide.svg
excerpt: "DuckDB used for streaming analytics? This post will show you some patterns in which you can use DuckDB to refresh your data at near real-time speed."
tags: ["using duckdb"]
---

The words “DuckDB” and “streaming” don't usually make it into the same sentence. Maybe this is because DuckDB has been positioned as an all powerful (but very lightweight) OLAP database. Or maybe this is because the ecosystem of streaming analytics has centered around names such as Kafka, Flink and Spark Streaming, and most recently players trying to change the game like Materialize or RisingWave. But can DuckDB be used in the context of streaming analytics? What is streaming analytics in the first place?

## Streaming Analytics Patterns

The simplest definition: streaming analytics is the _act of updating an analytical view of your data at near real-time speed as new data comes in._ For example, if three new sessions have just started in your website, the process of gathering those session events and updating the count (+3) is streaming analytics. Streaming analytics is not, in my modest opinion, just about inserting those 3 session events in a table – that would fit well within the realm of a transactional workload. Streaming analytics is also not pushing this events to a Kafka topic and sinking to another system. If you don't update the analytical view of your data, I wouldn't call it streaming analytics. 

Now that we have a definition, let's take a look at three common architectural patterns in streaming analytics. The names given to these patterns are of my own making, but I think they help differentiating them from one another.

![Streaming patterns](/images/blog/streaming_patterns/streaming_patterns.png)

- In the **Materialized View Pattern**, it is very common to use a cloud data warehouse with support for materialized views (such as BigQuery or Snowflake). The stream of events is usually sunk to a raw table and a materialized view is created on top. This pattern is generally conceived as having a higher latency than the next two. However, there is not that much benchmarking around to conclude anything.

- The **Streaming Engine Pattern** uses the more traditional ETL approach. A separate process using a streaming engine consumes the messages from the source, queries are then done on the fly and results are stored in a persisted table. Common engines are Spark Streaming, Flink, Kafka Streams or most recently Arroyo. This has traditionally come with a set of complications (e.g., dealing with watermarks, state management, increased memory load for infinite queries, etc.).

- The **Streaming Database Pattern** is similar to the previous one in terms of latency but drastically simplifies the experience. Streaming databases like RisingWave or Materialize can directly read from the streaming source and update your materialized view on the fly. They aim at keeping ACID consistency and allowing clients to query data using the PostgreSQL wire protocol.

“Where does DuckDB fit in all this?” – you may ask. Well, DuckDB fits well with patterns one and two. Even if DuckDB does not support materialized views ([yet]({% link roadmap.md %})), we can work around this limitation and implement these patterns to still get very good results.

> Interestingly, the streaming engine industry doesn't have many official benchmarks. The [Nexmark](https://github.com/nexmark/nexmark) benchmark seems to be the most common, but there are not many published results comparing engines using this benchmark.

## Materialized View Pattern: Cooking Our Own Materialized View with DuckDB

We know that DuckDB is very fast at aggregating data on the fly and also performs very well in transactional workloads (for an OLAP system). So does DuckLake's lakehouse format, thanks to its [data inlining feature](https://ducklake.select/docs/stable/duckdb/advanced_features/data_inlining). In this section we are going to see both DuckDB and DuckLake in action, acting as a sink for Kafka and calculating new metric values based on deltas.

> All the patterns are going to do the same thing in different ways. That is, read events from a Kafka topic and update the analytical view, which can be a persisted table or a view on top of a raw table. What happens in between is what differentiates these patterns.

### Querying Deltas with DuckDB

![pattern_1_1](/images/blog/streaming_patterns/streaming_pattern_1_1.png)

The key component in this diagram is what I call “Delta Processor”. This component is basically a function that loops periodically and runs a query to aggregate new data inserted in the `raw_events` table and to update the analytical view, in this case a persisted table called `user_clicks`. This is the query that runs periodically to update `user_clicks` with the new delta:

```sql
MERGE INTO user_clicks AS dest
USING (
    SELECT 
        user_id,
        user_name,
        count(*) AS count_of_clicks,
        max(timestamp) AS updated_at
    FROM raw_events
    WHERE event_type = 'CLICK'
      AND (⟨LATEST_UPDATED_AT⟩ IS NULL
       OR timestamp > ⟨LATEST_UPDATED_AT⟩)
    GROUP BY user_id, user_name
) AS src
ON dest.user_id = src.user_id
WHEN MATCHED THEN 
    UPDATE SET 
        count_of_clicks = dest.count_of_clicks + src.count_of_clicks,
        updated_at = src.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, user_name, count_of_clicks, updated_at)
    VALUES (src.user_id, src.user_name, src.count_of_clicks, src.updated_at);
```

You can check the full pipeline in [this repository](https://github.com/guillesd/duckdb-streaming-patterns/blob/main/pipelines/pattern_1_1.py). 

### Using DuckLake's Change Data Feed

![pattern_1_2](/images/blog/streaming_patterns/streaming_pattern_1_2.png)

This pattern is very similar to 1.1 but with some specifics to DuckLake:

1. We are using [DuckLake's Data Inlining](https://ducklake.select/docs/stable/duckdb/advanced_features/data_inlining) to speed up insertion without writing too many small files.
2. The Delta Processor component can take advantage of [DuckLake's Data Change Feed](https://ducklake.select/docs/stable/duckdb/advanced_features/data_change_feed) to avoid scanning unnecessary data.
3. We have an extra component, called “Inline Flusher”, that periodically flushes inlined data from the metadata catalog to parquet files of the specified file size (512 MB by default). This is a maintenance operation that will keep DuckLake performant.

You can check the full pipeline in [this repository](https://github.com/guillesd/duckdb-streaming-patterns/blob/main/pipelines/pattern_1_2.py).

> In order to make better use of filter pushdowns and file pruning, partitioning the data by `timestamp` is recommended

## Streaming Engine Pattern: Streaming Engines and DuckDB

Most established streaming engines (Spark Streaming, Flink, Kafka Streams) are JVM based. They can therefore insert data in DuckDB using the JDBC protocol. This pattern is usually a bit difficult to manage. Long running streaming queries tend to consume a lot of memory and restarting interrupted streaming queries always makes me skip a beat. However, it can be a very low latency solution for very large streams of data.

### Using Spark Streaming and Sink to DuckDB

![pattern_2](/images/blog/streaming_patterns/streaming_pattern_2.png)

In this diagram we can see that most of the components are managed by the Spark Streaming runtime. In Spark Streaming, all of this is contained in a streaming query. When the micro batching mode is being used (like it is the case in this example) you can pass a custom function to the writer that allows you to write each batch in the way you desire. In our case, we just use a JDBC connection and overwrite the destination table (`user_clicks`).

We can also see that there are no intermediate results being saved, meaning in this particular case we do not have a `raw_events` table. This is not a pattern that I love since for auditing purposes I would prefer to store the raw data to ensure that my streaming job isn't doing something funky. In this case, Spark Streaming relies on checkpoints to keep the state and make sure that data is processed just once and queries are able to restart without missing or duplicating data consumed from the Kafka topic.

You can check the full pipeline in [this repository](https://github.com/guillesd/duckdb-streaming-patterns/blob/main/pipelines/pattern_2.py).

## Bonus: Using DuckDB Tributary Extension to Directory Query Kafka

![pattern_bonus](/images/blog/streaming_patterns/streaming_pattern_bonus.png)

This setup is the most similar thing to the Streaming Databases Pattern that you can do right now with DuckDB. Powered by the [`tributary` DuckDB community extension](/community_extensions/extensions/tributary), you can create a view or a table that reads directly from a Kafka topic. To simulate materialized views, we are using views for this specific example. The following query showcases how simple this process is:

```sql
CREATE VIEW IF NOT EXISTS raw_events_view AS
    SELECT
        * EXCLUDE message, 
        decode(message)::JSON AS message 
    FROM tributary_scan_topic(⟨TOPIC⟩, "bootstrap.servers" := "localhost:9092");
```

Currently this extension has no state management. Every time this view is queried, we would be reading the whole topic from offset 0. This is not ideal since Kafka has a limited retention policy, which means that at some point it will start flushing messages. A way around this is to materialize this messages to tables and use the offset (or a timestamp) to keep track of what has been ingested.

You can check the full pipeline in [this repository](https://github.com/guillesd/duckdb-streaming-patterns/blob/main/pipelines/bonus_pattern.py).

> This is an experimental extension from [Query.Farm](https://query.farm/).

## Some Thoughts

Conclusions always feel very subjective, so I rather write about some of my thoughts regarding streaming patterns in general and particularly around DuckDB. 

**The Materialized View Pattern is usually good enough.**
My hot take is that most use cases for analytics are usually covered by the Materialized View Pattern without the need of complexity that comes with other patterns. I believe that DuckDB is very well suited for this pattern because for a small OLAP, it does incredibly well at handling large amounts of streaming inserts. In [this article](https://arrow.apache.org/blog/2025/03/10/fast-streaming-inserts-in-duckdb-with-adbc/) DuckDB was pushed to the limit and was able to handle more than one million rows inserted per second. Also note that **[materialized views are on the DuckDB's long-term roadmap]({% link roadmap.md %}#future-work)**, so this pattern will become even simpler in the near future.

If you are streaming to a lakehouse, you should know that DuckLake's [Data Inlining feature](https://ducklake.select/docs/stable/duckdb/advanced_features/data_inlining) was specifically designed to deal with high-throughput inserts while solving the small file problem. This makes DuckLake a great candidate for this pattern if you have a lakehouse-like architecture.

**Streaming Engines and Streaming Databases can be hard (or expensive).**
At scale, Streaming Engines can be hard to manage. It is an evolving field and some work is being done to make forever running streaming queries easier to operate. For example, [Apache Fluss](https://fluss.apache.org/) is being built with the idea to solve some of the shortcomings described in this post. However, it does add another layer of complexity to an already complex streaming architecture.

Streaming databases are a very elegant solution and have the potential to be very nice to use. However, if you are looking to host the solution, this will require some expertise since these systems are considerably complex (see [RisingWave's architecture](https://docs.risingwave.com/get-started/architecture)). This pushes practitioners to buy rather than host and maintain this complex system, which can be costly.

Whatever you choose for your architecture, make sure that the effort you put into it corresponds to your needs. And next time you think of streaming, make sure you also think about DuckDB.
