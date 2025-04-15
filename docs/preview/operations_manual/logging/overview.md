---
layout: docu
title: Logging
---

## HTTP Logging

DuckDB supports HTTP logging. To enable it, set the `enable_http_logging` option to `true`:

```sql
SET enable_http_logging = true;
```

To disable logging, run:

```sql
SET enable_http_logging = false;
```

The logging can be redirected to a file using the `http_logging_output` configuration option:

```sql
SET http_logging_output = 'http-log.txt';
```

### Logging File Access

The logger logs the HTTP requests for file access operations.
For example, if we query the full content of the <https://blobs.duckdb.org/stations.parquet> file (29 kB),
the logger prints four HTTP Request–Response pairs:

```sql
SET enable_http_logging = true;
FROM 'https://blobs.duckdb.org/stations.parquet';
```

```text
HTTP Request:
	HEAD /stations.parquet
	Accept: */*
	Host: blobs.duckdb.org
	User-Agent: cpp-httplib/0.14.3

HTTP Response:
	200 OK
	...

HTTP Request:
	GET /stations.parquet
	Accept: */*
	Host: blobs.duckdb.org
	Range: bytes=29204-29211
	User-Agent: cpp-httplib/0.14.3

HTTP Response:
	206 Partial Content
	...

...
```

### Logging Extension Installs

The logging also works for installing extensions. For example:

```sql
SET enable_http_logging = true;
INSTALL vss;
```

```text
HTTP Request:
	GET /v1.2.1/osx_arm64/vss.duckdb_extension.gz
    ...

HTTP Response:
	200 OK
	Accept-Ranges: bytes
    ...
```