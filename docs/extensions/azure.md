---
layout: docu
title: Azure Extension
---

The `azure` extension adds a filesystem abstraction for the [Azure Blob storage](https://azure.microsoft.com/en-us/products/storage/blobs) to DuckDB.

> This extension is currently in an experimental state. Feel free to try it out, but be aware some things may not work as expected.

## Usage

Authentication is done by setting the connection string:

```sql
SET azure_storage_connection_string = '<your_connection_string>';
```

After setting the connection string, the Azure Blob Storage can be queried:

```sql
SELECT count(*) FROM 'azure://<my_container>/<my_file>.<parquet_or_csv>';
```

Blobs are also supported:

```sql
SELECT * from 'azure://<my_container>/*.csv';
```

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdblabs/duckdb_azure)
