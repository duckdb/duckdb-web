---
layout: docu
redirect_from:
- /docs/guides/sql_features/streaming_patterns
title: Streaming Patterns
---

Streaming analytics is the process of updating an analytical view of your data at near-real-time speed as new data arrives. While DuckDB is not a streaming database, its high performance for both analytical queries and transactional workloads makes it effective for implementing streaming patterns.

This guide covers practical patterns for using DuckDB in streaming analytics scenarios.

## Streaming Analytics Patterns

There are three common architectural patterns for streaming analytics:

| Pattern | Description | Latency | Complexity |
|---------|-------------|---------|------------|
| **Materialized View Pattern** | Raw events sink to a table, periodic queries update aggregated views | Medium | Low |
| **Streaming Engine Pattern** | External engine (Spark, Flink) processes streams, sinks to DuckDB | Low | High |
| **Streaming Database Pattern** | Database directly consumes streams and maintains views | Low | Medium |

DuckDB works well with the first two patterns. This guide focuses on the Materialized View Pattern, which is sufficient for most use cases.

## Materialized View Pattern

The Materialized View Pattern involves:

1. Sinking raw events to a table.
2. Periodically running a query to aggregate new data.
3. Updating an analytical view with the delta.

### Setting Up the Tables

Create a table for raw events and an aggregated view table:

```sql
-- Raw events table (populated by your ingestion process)
CREATE TABLE raw_events (
    event_id INTEGER,
    user_id INTEGER,
    user_name VARCHAR,
    event_type VARCHAR,
    timestamp TIMESTAMPTZ,
    metadata JSON
);

-- Aggregated view table
CREATE TABLE user_clicks (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR,
    count_of_clicks BIGINT,
    updated_at TIMESTAMPTZ
);
```

### Delta Processing with MERGE

Use the [`MERGE` statement]({% link docs/stable/sql/statements/merge_into.md %}) to efficiently update the aggregated view with only new events:

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
      AND timestamp > ?  -- Pass the last processed timestamp
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

The key components:

* **Source subquery**: Aggregates only events newer than the last processed timestamp.
* **WHEN MATCHED**: Increments the count for existing users.
* **WHEN NOT MATCHED**: Inserts new users.

### Tracking the Last Processed Timestamp

Store the last processed timestamp to know where to resume:

```sql
-- Create a metadata table
CREATE TABLE processing_metadata (
    key VARCHAR PRIMARY KEY,
    value TIMESTAMPTZ
);

-- After each MERGE, update the timestamp
INSERT OR REPLACE INTO processing_metadata
VALUES ('last_processed_timestamp', ?);
```

## With DuckLake

When using [DuckLake](https://ducklake.select) as your lakehouse format, you can take advantage of additional features:

### Data Inlining

DuckLake's [data inlining](https://ducklake.select/docs/stable/duckdb/advanced_features/data_inlining) speeds up high-frequency inserts by storing small amounts of data directly in the metadata catalog, avoiding the creation of many small Parquet files.

### Change Data Feed

DuckLake's [change data feed](https://ducklake.select/docs/stable/duckdb/advanced_features/data_change_feed) tracks row-level changes, allowing your delta processor to query only the changed data without scanning the entire table.

## Streaming Engine Pattern

For lower latency requirements, you can use a streaming engine like Apache Spark Streaming or Apache Flink to process events and sink results to DuckDB via JDBC.

This pattern:

* Processes events in micro-batches or continuously.
* Maintains state in the streaming engine.
* Writes aggregated results to DuckDB.

The tradeoff is increased operational complexity for managing the streaming infrastructure.

## Best Practices

**The Materialized View Pattern is usually sufficient.** Most analytics use cases don't require sub-second latency. DuckDB can handle high insert throughput, making it suitable for many streaming scenarios.

**Partition by timestamp.** If using a lakehouse format, partition your raw events by timestamp to enable efficient filter pushdowns and file pruning during delta queries.

**Consider your latency requirements.** If you need true real-time streaming with sub-second latency, consider a dedicated streaming database. For near-real-time (seconds to minutes), the patterns in this guide work well.

## Related Resources

* [MERGE Statement]({% link docs/stable/sql/statements/merge_into.md %}) – SQL reference for the MERGE statement
* [MERGE Statement for SCD Type 2]({% link docs/stable/guides/sql_features/merge.md %}) – Guide on using MERGE for slowly changing dimensions
* [tributary extension]({% link community_extensions/extensions/tributary.md %}) – Community extension for querying Kafka topics directly
* [DuckLake Documentation](https://ducklake.select/docs/stable/) – DuckLake lakehouse format documentation
