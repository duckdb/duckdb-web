---
layout: docu
redirect_from: null
title: Logging
---

DuckDB contains a logging mechanism to provide additional information to users, such as query execution details,
performance metrics, and system events.

## Basics

DuckDB's logging mechanism can be enabled or disabled using pragmas. By default, logs are stored in a special view
called `duckdb_logs` that can be queried like any other table.

Example:

```sql
CALL enable_logging();
-- Run some queries...
SELECT * FROM duckdb_logs;
```

## Log Level

DuckDB supports different logging levels that control the verbosity of the logs:

* `ERROR`: Only logs error messages
* `WARN`: Logs warnings and errors
* `INFO`: Logs general information, warnings and errors (default)
* `DEBUG`: Logs detailed debugging information
* `TRACE`: Logs very detailed tracing information

The log level can be set using:

```sql
CALL enable_logging(level='debug')
```

## Log Types

In DuckDB, log messages can have an associated log type. Log types allow two main things:

- fine-grained control over which log messages get created
- structured logging

### Logging-Specific Types

To log only messages of a specific type:

```sql
PRAGMA enable_logging('HTTP');
```

The above pragma will automatically set the correct log level, and will add the `HTTP` type to the `enabled_log_types` settings. This ensures
only log messages of the 'HTTP' type will be written to the log.

To enable multiple log types, simply pass:

```sql
PRAGMA enable_logging(['HTTP', 'QueryLog']);
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

| Log Type     | Description                                              | Structured |
|--------------|----------------------------------------------------------|------------|
| `QueryLog`   | Logs which queries are executed in DuckDB                | No         |
| `FileSystem` | Logs all FileSystem interaction with DuckDB's Filesystem | Yes        |
| `HTTP`       | Logs all HTTP traffic from DuckDB's internal HTTP client | Yes        |

## Log Storages

By default, DuckDB logs to an in-memory log storage (`memory`). DuckDB supports different types of log storage. Currently
the following log storage types are implemented in core DuckDB


| Log Storage | Description                                               |
|-------------|-----------------------------------------------------------|
| `memory`    | (default) Log to an in-memory buffer                      |
| `stdout`    | Log to the stdout of the current process (in CSV format)  |
| `file`      | Log to (a) csv file(s)                                    |


### Logging to stdout
```sql
CALL enable_logging(storage='stdout');
```


### Logging to file 

```sql
CALL enable_logging(storage='file', storage_config={'path': 'path/to/store/logs'});
```
or using the equivalent shorthand
```sql
CALL enable_logging(storage_config='path': 'path/to/store/logs');
```


## Advanced usage

### Buffer size
The log storage in DuckDB uses a buffering mechanism to improve logging performance. What this means though is that there
may be a delay between when a message is logged and when it is written out by the log storage. This can be annoying because it 
obfuscates when the message was actually written. Especially when debugging crashes in DuckDB this is problematic because log
message right before the crash may never get written. Fortunately, the buffer size can be adjusted to work around this:

```sql
CALL enable_logging(storage_config={'buffer_size': 0});
```

or using the equivalent shorthand:

```sql
CALL enable_logging(storage_buffer_size=0);
```

Note that the default buffer size is different for different log storages:


| Log Storage | Default buffer size         |
|-------------|-----------------------------|
| `memory`    | STANDARD_VECTOR_SIZE (2048) |
| `file`      | STANDARD_VECTOR_SIZE (2048) |
| `stdout`    | Disabled (0)                |

So for example, if you want to increase your `stdout` logging performance, simply enable buffering to greatly (>10x) speed up 
your logging:

```SQL
CALL enable_logging(storage='stdout', storage_buffer_size=2048);
```

Or imagine you are debugging a crash in DuckDB and you want to use the `file` logger to understand what's going on: simply disable the
buffering using:

```sql
CALL enable_logging(storage_path='/tmp/mylogs', storage_buffer_size=2048);
```

### Syntactic sugar
DuckDB contains some syntactic sugar to make common paths

The following statements are all equal 
```sql
-- regular invocation 
CALL enable_logging(storage='file', storage_config={'path': 'path/to/store/logs'});
-- using shorthand for common path storage config param 
CALL enable_logging(storage='file', storage_path='path/to/store/logs');
-- omitting `storage='file'` -> is implied from presence of `storage_config`
CALL enable_logging(storage_config='path': 'path/to/store/logs');
```
