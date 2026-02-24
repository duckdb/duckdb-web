---
layout: docu
title: Concurrency
---

## Handling Concurrency

DuckDB has two configurable options for concurrency:

1. **Read-write mode:** one process can both read and write to the database.
2. **Read-only mode:** multiple processes can read from the database, but no processes can write ([`access_mode = 'READ_ONLY'`]({% link docs/preview/configuration/overview.md %}#configuration-reference)).

When using read-write mode, DuckDB supports multiple writer threads using a combination of [MVCC (Multi-Version Concurrency Control)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) and optimistic concurrency control (see [Concurrency within a Single Process](#concurrency-within-a-single-process)), but all within that single writer process. The reason for this concurrency model is to allow for the caching of data in RAM for faster analytical queries, rather than going back and forth to disk during each query. It also allows the caching of function pointers, the database catalog, and other items so that subsequent queries on the same connection are faster.

> DuckDB is optimized for bulk operations, so executing many small transactions is not a primary design goal.

## Concurrency within a Single Process

DuckDB supports concurrency within a single process according to the following rules. As long as there are no write conflicts, multiple concurrent writes will succeed. Appends will never conflict, even on the same table. Multiple threads can also simultaneously update separate tables or separate subsets of the same table. Optimistic concurrency control comes into play when two threads attempt to edit (update or delete) the same row at the same time. In that situation, the second thread to attempt the edit will fail with a conflict error.

## Writing to DuckDB from Multiple Processes

Writing to DuckDB from multiple processes is not supported automatically and is not a primary design goal (see [Handling Concurrency](#handling-concurrency)).

If multiple processes must write to the same file, several design patterns are possible, but would need to be implemented in application logic. For example, each process could acquire a cross-process mutex lock, then open the database in read/write mode and close it when the query is complete. Instead of using a mutex lock, each process could instead retry the connection if another process is already connected to the database (being sure to close the connection upon query completion). Another alternative would be to do multi-process transactions on a MySQL, PostgreSQL, or SQLite database, and use DuckDB's [MySQL]({% link docs/preview/core_extensions/mysql.md %}), [PostgreSQL]({% link docs/preview/core_extensions/postgres.md %}), or [SQLite]({% link docs/preview/core_extensions/sqlite.md %}) extensions to execute analytical queries on that data periodically.

Additional options include writing data to Parquet files and using DuckDB's ability to [read multiple Parquet files]({% link docs/preview/data/parquet/overview.md %}), taking a similar approach with [CSV files]({% link docs/preview/data/csv/overview.md %}), or creating a web server to receive requests and manage reads and writes to DuckDB.

> DuckDB handles concurrent database access requests using file locks.
> Exercise extra caution when accessing a DuckDB file in a shared directory (e.g., from different operating systems using different file systems).
> If you cannot guarantee file locking, consider using a DuckLake setup, e.g., [DuckLake with SQLite as the catalog database](https://ducklake.select/docs/stable/duckdb/usage/choosing_a_catalog_database#sqlite).

## Optimistic Concurrency Control

DuckDB uses [optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control), an approach generally considered to be the best fit for read-intensive analytical database systems as it speeds up read query processing. As a result any transactions that modify the same rows at the same time will cause a transaction conflict error:

```console
Transaction conflict: cannot update a table that has been altered!
```

> Tip A common workaround when a transaction conflict is encountered is to rerun the transaction.
