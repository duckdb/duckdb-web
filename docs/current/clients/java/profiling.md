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

On a [JFR-capable JVM](#requirements), the driver can emit [Java Flight Recorder](https://openjdk.org/jeps/328) events describing DuckDB's internal memory usage, so that any JFR-aware tool — JDK Mission Control, the `jfr` command line tool, continuous profilers — can ingest DuckDB memory metrics alongside the rest of the JVM signal. The feature is strictly opt-in and is a silent no-op on JVMs without JFR support: nothing is emitted unless the application both sets the JDBC property on a connection and has an active JFR recording that enables the event.

### Enabling Emission

Monitoring is opt-in per connection: set the `jdbc_jfr_memory_monitor` property to an identifier for the connection's database instance. The value is an arbitrary label that is attached to every event as its `component` field, so that operators can attribute memory to logical components. An absent or empty value leaves monitoring disabled.

```java
Properties props = new Properties();
props.setProperty("jdbc_jfr_memory_monitor", "analytics-db");
try (Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", props)) {
    // work with the connection while a JFR recording is active
}
```

The same option can be set in the URL:

```text
jdbc:duckdb:/tmp/my_database;jdbc_jfr_memory_monitor=analytics-db
```

<div class="monospace_table"></div>

| Property value | Effect |
|--|--|
| absent | No events emitted for this connection. |
| empty string | No events emitted, the same as absent. |
| non-empty string | Events emitted, tagged with the given value. |

The JDBC property is only an enable and label switch. It does not control whether JFR is recording or the sampling period; those are governed by the JFR recording settings.

### Controlling the Period and Enabled State

The sampling rate and enabled state are JFR-native settings. Configure them in a `.jfc` profile, through JMC, or programmatically with the `jdk.jfr.Recording` API:

```java
try (Recording r = new Recording()) {
    r.enable("duckdb.MemoryUsage").withPeriod(Duration.ofSeconds(1));
    r.start();
    // ... application work ...
    r.stop();
    r.dump(Path.of("app.jfr"));
}
```

The equivalent `.jfc` snippet:

```xml
<event name="duckdb.MemoryUsage">
  <setting name="enabled">true</setting>
  <setting name="period">1 s</setting>
</event>
```

When no recording enables the event, the driver does no work: the underlying `duckdb_memory()` query is never issued.

### Event Schema

While a recording is active with the event enabled, the driver emits one `duckdb.MemoryUsage` event per DuckDB memory tag per JFR tick, with the following fields:

<div class="monospace_table"></div>

| Field | Type | Description |
|--|--|--|
| `component` | `String` | Application-supplied identifier, the `jdbc_jfr_memory_monitor` value. |
| `tag` | `String` | DuckDB memory tag, such as `BASE_TABLE`, `HASH_TABLE`, or `ALLOCATOR`. |
| `dbAddress` | `long` | Native address of the DuckDB instance, a stable per-instance identifier. |
| `memoryUsageBytes` | `long` | Bytes currently allocated for this tag. |
| `temporaryStorageBytes` | `long` | Bytes spilled to temporary storage for this tag. |

The standard JFR `startTime`, `duration`, and `eventThread` fields are also present. Stack traces are disabled for this event.

### Attribution

The monitor is keyed on the native DuckDB instance address, the `dbAddress` field, not on the JDBC connection. There is one sample stream per distinct instance, so shared memory is not double-counted. The `component` label is captured from the first opted-in connection to an instance, and later opted-in connections to the same instance do not change it. The monitor is created when the first opted-in connection opens and torn down when the last one closes; opening a new opted-in connection afterward starts a fresh monitor.

Whether two `getConnection` calls share a `dbAddress` follows the same rules as [instance caching]({% link docs/current/clients/java/connecting.md %}#database-instances-and-instance-caching):

<div class="monospace_table"></div>

| URL or operation | Same `dbAddress`? |
|--|--|
| `jdbc:duckdb:` (unnamed in-memory) | No — a fresh instance per call. |
| `jdbc:duckdb:memory:⟨label⟩` | Yes, when `⟨label⟩` matches. |
| `jdbc:duckdb:⟨path⟩` | Yes, when the path matches. |
| `conn.duplicate()` | Yes, always. |

Because connections that share a database instance also share a `dbAddress`, and therefore a single `component` label, per-component attribution requires each component to open a connection that resolves to a distinct instance. An unnamed in-memory `jdbc:duckdb:` URL creates a connection-private instance, which makes it the simplest choice; give each such connection a distinct `jdbc_jfr_memory_monitor` value.

### Requirements

The feature needs a JFR-capable JVM:

* OpenJDK and HotSpot 11 and later include JFR.
* Amazon Corretto 8, OpenJDK 8u272 and later, and several other Java 8 distributions include the JFR backport (the `jdk.jfr` package).
* On a JVM without `jdk.jfr`, such as some stripped Java 8 builds, the feature is a silent no-op: the `jdbc_jfr_memory_monitor` property is ignored and no classes that depend on `jdk.jfr` are loaded.

No additional JVM flags are required.

### Inspecting a Recording

Inspect a captured recording with [JDK Mission Control](https://www.oracle.com/java/technologies/jdk-mission-control.html) or the `jfr` command line tool bundled with the JDK:

```bash
jfr summary app.jfr | grep duckdb.MemoryUsage
jfr print --events duckdb.MemoryUsage app.jfr
jfr metadata app.jfr | sed -n '/class MemoryUsage/,/^}/p'
```
