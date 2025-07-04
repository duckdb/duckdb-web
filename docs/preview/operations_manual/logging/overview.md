---
layout: docu
title: Logging
---

DuckDB contains a logging mechanism to provide additional information to users, such as query execution details,
performance metrics, and system events.

## Basics

DuckDB's logging mechanism can be enabled or disabled using pragmas. By default, logs are stored in a special table
called `duckdb_logs` that can be queried like any other table.

Example:

```sql
PRAGMA enable_logging;
-- Run some queries..
SELECT * FROM duckdb_logs;
```

## Log Level

DuckDB supports different logging levels that control the verbosity of the logs:

* `ERROR`: Only logs error messages
* `WARNING`: Logs warnings and errors
* `INFO`: Logs general information, warnings and errors (default)
* `DEBUG`: Logs detailed debugging information
* `TRACE`: Logs very detailed tracing information

The log level can be set using:

```sql
PRAGMA enable_logging;
SET logging_level = 'TRACE';
```

## Log Types

In DuckDB, log messages can have an associated log type. Log types have 2 main goals. Firstly, they allow using includelists and excludelist to limit which types of log messages are logged. Secondly, log types can have a predetermined message schema which allows DuckDB to automatically parse the messages back into a structured data type.

### Logging-Specific Types

To log only messages of a specific type:

```sql
PRAGMA enable_logging('HTTP');
```

The above pragma will automatically set the correct log level, and will add the `HTTP` type to the `enabled_log_types` settings.

### Structured Logging

Some log types like `HTTP` will have an associated message schema. To make DuckDB automatically parse the message, use the `duckdb_logs_parsed()` macro. For example:

```sql
SELECT request.headers FROM duckdb_logs_parsed('HTTP');
```

### List of Available Log Types

This is a (non-exhaustive) list of the available log types in DuckDB.

| Log Type     | Description                                              | Structured |
|--------------|----------------------------------------------------------|------------|
| `QueryLog`   | Logs which queries are executed in DuckDB                | No         |
| `FileSystem` | Logs all FileSystem interaction with DuckDB's Filesystem | Yes        |
| `HTTP`       | Logs all HTTP traffic from DuckDB's internal HTTP client | Yes        |

## Log Storage

By default, DuckDB logs to an in-memory log storage. Alternatively, DuckDB can log straight to `stdout` using:

```sql
PRAGMA enable_logging;
SET logging_storage = 'stdout';
```