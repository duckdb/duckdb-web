---
layout: docu
redirect_from:
- /docs/clients/java/profiling
- /docs/preview/clients/java/profiling
- /docs/stable/clients/java/profiling
title: Profile and Monitor
---

## Overview

The JDBC driver exposes several ways to observe a running or completed query: cancelling and timing out queries, polling query progress, retrieving profiling output, and emitting memory-usage events through [Java Flight Recorder](https://openjdk.org/jeps/328). This page covers each of them.

## Query Progress and Cancellation

A running query can be cancelled from another thread with the standard JDBC `Statement.cancel()` method, which interrupts the query executing on the statement's connection. Setting `Statement.setQueryTimeout(seconds)` arms an automatic cancellation after the given number of seconds.

For long-running queries, `DuckDBPreparedStatement.getQueryProgress()` returns a `QueryProgress` snapshot while the query executes. It is intended to be called from a separate thread and exposes `getPercentage()`, `getRowsProcessed()`, and `getTotalRowsToProcess()`.

```java
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.concurrent.CompletableFuture;
import org.duckdb.DuckDBConnection;
import org.duckdb.DuckDBPreparedStatement;
import org.duckdb.QueryProgress;

try (DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
     DuckDBPreparedStatement ps =
         (DuckDBPreparedStatement) conn.prepareStatement("SELECT count(*) FROM range(1_000_000_000)")) {
    // Run the query on a background thread so its progress can be polled while it executes.
    CompletableFuture<Void> query = CompletableFuture.runAsync(() -> {
        try {
            ps.executeQuery().close();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    });

    while (!query.isDone()) {
        QueryProgress progress = ps.getQueryProgress();
        System.out.printf("%.1f%% (%d / %d rows)%n", progress.getPercentage(),
            progress.getRowsProcessed(), progress.getTotalRowsToProcess());
        Thread.sleep(100);
    }
    query.join();
}
```

## Profiling

Cast a connection to `DuckDBConnection` and call `getProfilingInformation(ProfilerPrintFormat)` to retrieve profiling output for the most recent query on that connection, after enabling profiling with `PRAGMA enable_profiling`. The `ProfilerPrintFormat` enum selects the output format: `DEFAULT`, `TEXT`, `QUERY_TREE`, `QUERY_TREE_OPTIMIZER`, `NO_OUTPUT`, `JSON`, `HTML`, `GRAPHVIZ`, `YAML`, and `MERMAID`.

```java
try (DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
     Statement stmt = conn.createStatement()) {
    stmt.execute("PRAGMA enable_profiling = 'json'");
    stmt.executeQuery("SELECT count(*) FROM range(1000)").close();
    String profile = conn.getProfilingInformation(ProfilerPrintFormat.JSON);
    System.out.println(profile);
}
```

## Memory Monitoring with JFR

On a JFR-capable JVM (Java 11 or later, or [Amazon Corretto](https://aws.amazon.com/corretto/) 8u272 and later), the driver can emit [Java Flight Recorder](https://openjdk.org/jeps/328) events describing DuckDB's internal memory usage. Monitoring is opt-in per connection: set the `jdbc_jfr_memory_monitor` property to an identifier for the connection's database instance. An absent or empty value leaves monitoring disabled.

```java
Properties props = new Properties();
props.setProperty("jdbc_jfr_memory_monitor", "analytics-db");
try (Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", props)) {
    // work with the connection while a JFR recording is active
}
```

While a JFR recording is active with the `duckdb.MemoryUsage` event enabled, the driver periodically emits one event per DuckDB memory tag, carrying the component identifier, the memory tag, the native database address, the bytes allocated, and the bytes spilled to temporary storage. The JDBC property is only an enable and label switch; the sampling period and the enabled state are controlled by the JFR recording settings. Inspect the events with [JDK Mission Control](https://www.oracle.com/java/technologies/jdk-mission-control.html) or the `jfr` command line tool.
