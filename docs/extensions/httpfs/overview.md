---
layout: docu
title: httpfs Extension for HTTP and S3 Support
redirect_from:
  - /docs/extensions/httpfs
  - /docs/extensions/httpfs/
---

The `httpfs` extension is an autoloadable extension implementing a file system that allows reading remote/writing remote files.
For plain HTTP(S), only file reading is supported. For object storage using the S3 API, the `httpfs` extension supports reading/writing/globbing files.

## Installation and Loading

The `httpfs` extension will be, by default, autoloaded on first use of any functionality exposed by this extension.

To manually install and load the `httpfs` extension, run:

```sql
INSTALL httpfs;
LOAD httpfs;
```

## HTTP(S)

The `httpfs` extension supports connecting to [HTTP(S) endpoints](https).

## S3 API

The `httpfs` extension supports connecting to [S3 API endpoints](s3api).

## GitHub

The `httpfs` extension is part of the [main DuckDB repository](https://github.com/duckdb/duckdb/tree/main/extension/httpfs).

## Pages in this Section
