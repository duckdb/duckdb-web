---
layout: docu
redirect_from:
- /docs/stable/operations_manual/logging/overview
- /docs/current/operations_manual/logging/overview
- /docs/lts/operations_manual/logging/overview
- /docs/preview/operations_manual/logging/overview
title: Logging
---

DuckDB implements a logging mechanism that provides users with detailed information about events such as query execution,
performance metrics and system events.

> Warning Logs may contain sensitive information, including secrets and credentials. Enable logging with care and consider where logs are stored and who can access them. Review their contents before sharing them.

## Basics

The DuckDB logging mechanism can be enabled or disabled using a special function, `enable_logging`. Logs are stored in a special view
named `duckdb_logs`, which can be queried like any standard table.

Example:

```sql
CALL enable_logging(storage = 'memory');
-- Run some queries...
SELECT * FROM duckdb_logs;
```

> In the [CLI client]({% link docs/2.0/clients/cli/overview.md %}), the default log storage is `shell_log_storage`, which prints log messages to the console but does not support querying. Therefore, the example above passes `storage = 'memory'`. In other clients, the default log storage is `memory`, so `CALL enable_logging();` suffices. See [Log Storages](#log-storages) for details.

To disable logging, run

```sql
CALL disable_logging();
```

To clear the current log, run

```sql
CALL truncate_duckdb_logs();
```

## Log Level

DuckDB supports different logging levels that control the verbosity of the logs:

* `FATAL`: Only logs fatal errors
* `ERROR`: Logs error messages
* `WARNING`: Logs warnings and errors
* `INFO`: Logs general information, warnings and errors (default)
* `DEBUG`: Logs detailed debugging information
* `TRACE`: Logs very detailed tracing information

The log level can be set using:

```sql
CALL enable_logging(level = 'debug');
```

## Warnings

DuckDB emits warnings, for example when you use deprecated syntax or a deprecated setting, through the logging system at the `WARNING` level. In the CLI, warnings are printed by default. To capture them from any client, or to inspect them after the fact, enable logging and query the `duckdb_logs` view, filtering on the log level:

```sql
CALL enable_logging(level = 'warning', storage = 'memory');
-- Run some queries that may emit warnings...
SELECT timestamp, message
FROM duckdb_logs
WHERE log_level = 'WARNING';
```

The default log level is `INFO`, which already includes warnings, so calling `enable_logging()` without a `level` also captures warnings. Setting `level = 'warning'` excludes lower-severity `INFO` messages.

> Note Switching the CLI to a log storage other than `shell_log_storage` means that warnings are no longer printed to the console. To restore the default behavior, run `CALL enable_logging(storage = 'shell_log_storage')`.

## Log Types

In DuckDB, log messages can have an associated log type. Log types allow two main things:

* Fine-grained control over log message generation
* Support for structured logging

### Logging-Specific Types

To log only messages of a specific type:

```sql
CALL enable_logging('HTTP');
```

The above function will automatically set the correct log level and will add the `HTTP` type to the `enabled_log_types` settings. This ensures
only log messages of the `HTTP` type will be written to the log.

> New As of DuckDB 2.0, the dedicated `enable_http_logging` and `http_logging_output` settings have been removed. Use the unified logging framework shown here (`CALL enable_logging('HTTP')` together with `duckdb_logs_parsed('HTTP')`) instead. The `redact_http_logs` setting (default `true`) controls whether HTTP header values are redacted in the logs.

To enable multiple log types, simply pass:

```sql
CALL enable_logging(['HTTP', 'QueryLog']);
```

### Structured Logging

Some log types like `HTTP` will have an associated message schema. To make DuckDB automatically parse the message, use the `duckdb_logs_parsed()` macro. For example:

```sql
SELECT request.headers FROM duckdb_logs_parsed('HTTP');
```

To view the schema of each structure log type simply run:

```sql
DESCRIBE FROM duckdb_logs_parsed('HTTP');
```

### List of Available Log Types

This is a (non-exhaustive) list of the available log types in DuckDB.

| Log Type           | Description                                              | Structured |
|--------------------|----------------------------------------------------------|------------|
| `QueryLog`         | Logs which queries are executed in DuckDB                | No         |
| `FileSystem`       | Logs all FileSystem interaction with DuckDB's Filesystem | Yes        |
| `HTTP`             | Logs all HTTP traffic from DuckDB's internal HTTP client | Yes        |
| `PhysicalOperator` | Logs events emitted by physical operators during query execution | Yes |
| `Metrics`          | Logs profiling metrics collected during query execution  | Yes        |

The structured log types expose the following schemas, which you can inspect at any time with
`DESCRIBE FROM duckdb_logs_parsed(⟨log_type⟩)`{:.language-sql .highlight}:

<div class="monospace_table"></div>

| Log Type           | Schema |
|--------------------|--------|
| `FileSystem`       | `fs VARCHAR`, `path VARCHAR`, `op VARCHAR`, `bytes BIGINT`, `pos BIGINT` |
| `HTTP`             | `request STRUCT(type, url, start_time, duration_ms, headers MAP)`, `response STRUCT(status, reason, headers MAP)` |
| `PhysicalOperator` | `operator_type VARCHAR`, `parameters MAP(VARCHAR, VARCHAR)`, `class VARCHAR`, `event VARCHAR`, `info MAP(VARCHAR, VARCHAR)` |
| `Metrics`          | `metric VARCHAR`, `value VARCHAR` |

## Log Storages

By default, DuckDB logs to an in-memory log storage (`memory`), except in the CLI client, which uses `shell_log_storage`. DuckDB supports different types of log storage. Currently,
the following log storage types are implemented in core DuckDB.

| Log storage         | Description                                                               |
|---------------------|---------------------------------------------------------------------------|
| `memory`            | Log to an in-memory buffer (default in clients other than the CLI)        |
| `stdout`            | Log to the stdout of the current process (in CSV format)                  |
| `file`              | Log to (a) csv file(s)                                                    |
| `shell_log_storage` | Print log messages to the console (default in the CLI)                    |

The `shell_log_storage` cannot be queried: `duckdb_logs`, `duckdb_logs_parsed()` and `truncate_duckdb_logs()` all return an error. It also does not accept configuration options such as `storage_config` or `storage_buffer_size`. To query logs in the CLI, switch to a queryable storage such as `memory` or `file`:

```sql
CALL enable_logging(storage = 'memory');
```


Note that the `duckdb_logs` view is automatically updated to target the currently active log storage. This means that switching
the log storage may influence what is returned by the `duckdb_logs` function.

### Logging to stdout

```sql
CALL enable_logging(storage = 'stdout');
```

### Logging to File 

```sql
CALL enable_logging(storage = 'file', storage_config = {'path': 'path/to/store/logs'});
```

or using the equivalent shorthand:

```sql
CALL enable_logging(storage_path = 'path/to/store/logs');
```

## Advanced Usage

### Normalized vs. Denormalized Logging

DuckDB's log storages can log in two ways: normalized vs. denormalized.

In denormalized logging, the log context information is appended directly to each log entry, while in normalized logging
the log entries are stored separately with `context_id`s referencing the context information.

| Log storage | Normalized   |
|-------------|--------------|
| `memory`    | yes          |
| `file`      | configurable |
| `stdout`    | no           |

For file storage, you can switch between normalized and denormalized by providing a path to a directory (for normalized)
or a path ending in `.csv` (for denormalized). For file logging, denormalized is generally recommended since this increases performance 
and reduces the total size of the logs. To configure normalization of `file` log storage:

```sql
-- normalized: creates `/tmp/duckdb_log_contexts.csv` and `/tmp/duckdb_log_entries.csv`
CALL enable_logging(storage_path = '/tmp');
-- denormalized: creates `/tmp/logs.csv`
CALL enable_logging(storage_path = '/tmp/logs.csv');
```

Note that the difference between normalized and denormalized is typically hidden from users through the `duckdb_logs` function,
which automatically joins normalized tables into a single unified result. To illustrate, both configurations above will be
queryable using `FROM duckdb_logs;` and will produce identical results.

### Buffer Size

The log storage in DuckDB implements a buffering mechanism to optimize logging performance. This implementation
introduces a potential delay between message logging and storage writing. This delay can obscure the actual message writing time,
which is particularly problematic when debugging crashes, as messages generated immediately before a crash might not be
written. To address this, the buffer size can be configured as follows:

```sql
CALL enable_logging(storage = 'memory', storage_config = {'buffer_size': 0});
```

or using the equivalent shorthand:

```sql
CALL enable_logging(storage = 'memory', storage_buffer_size = 0);
```

Note that the default buffer size is different for different log storages:

| Log storage | Default buffer size           |
|-------------|-------------------------------|
| `memory`    | `STANDARD_VECTOR_SIZE` (2048) |
| `file`      | `STANDARD_VECTOR_SIZE` (2048) |
| `stdout`    | Disabled (0)                  |

So for example, if you want to increase your `stdout` logging performance, simply enable buffering to greatly (>10x) speed up 
your logging:

```sql
CALL enable_logging(storage = 'stdout', storage_buffer_size = 2048);
```

Or imagine you are debugging a crash in DuckDB and you want to use the `file` logger to understand what's going on.
Simply disable the buffering using:

```sql
CALL enable_logging(storage_path = '/tmp/mylogs', storage_buffer_size = 0);
```

### Syntactic Sugar

DuckDB contains some syntactic sugar to make common paths easier. For example, the following statements are all equal:

```sql
-- regular invocation 
CALL enable_logging(storage = 'file', storage_config = {'path': 'path/to/store/logs'});
-- using shorthand for common path storage config param 
CALL enable_logging(storage = 'file', storage_path = 'path/to/store/logs');
-- omitting `storage = 'file'` -> is implied from presence of `storage_config`
CALL enable_logging(storage_config = {'path': 'path/to/store/logs'});
```
