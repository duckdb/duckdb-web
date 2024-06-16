---
layout: docu
title: HTTP(S) Support
---

With the `httpfs` extension, it is possible to directly query files over the HTTP(S) protocol. This works for all files supported by DuckDB or its various extensions, and provides read-only access.

```sql
SELECT *
FROM 'https://domain.tld/file.extension';
```

## Partial Reading

For CSV files, files will be downloaded entirely in most cases, due to the row-based nature of the format.
For Parquet files, DuckDB supports [partial reading]({% link docs/data/parquet/overview.md %}#partial-reading), i.e., it can use a combination of the Parquet metadata and [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) to only download the parts of the file that are actually required by the query. For example, the following query will only read the Parquet metadata and the data for the `column_a` column:

```sql
SELECT column_a
FROM 'https://domain.tld/file.parquet';
```

In some cases, no actual data needs to be read at all as they only require reading the metadata:

```sql
SELECT count(*)
FROM 'https://domain.tld/file.parquet';
```

## Scanning Multiple Files

Scanning multiple files over HTTP(S) is also supported:

```sql
SELECT *
FROM read_parquet([
    'https://domain.tld/file1.parquet',
    'https://domain.tld/file2.parquet'
]);
```

## Using a Custom Certificate File

> This feature is currently only available in the nightly build. It will be [released]({% link docs/dev/release_calendar.md %}) in version 0.10.1.

To use the `httpfs` extension with a custom certificate file, set the following [configuration options]({% link docs/configuration/pragmas.md %}) prior to loading the extension:

```sql
LOAD httpfs;
SET ca_cert_file = '⟨certificate_file⟩';
SET enable_server_cert_verification = true;
```
