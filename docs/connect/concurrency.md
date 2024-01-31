---
layout: docu
title: Concurrency
---

## Handling Concurrency

DuckDB has two configurable options for concurrency:

1. One process can both read and write to the database.
2. Multiple processes can read from the database, but no processes can write ([`access_mode = 'READ_ONLY'`](../sql/configuration#configuration-reference)).

When using option 1, DuckDB supports multiple writer threads using a combination of [MVCC (Multi-Version Concurrency Control)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) and optimistic concurrency control (see [Concurrency within a Single Process](#concurrency-within-a-single-process)), but all within that single writer process. The reason for this concurrency model is to allow for the caching of data in RAM for faster analytical queries, rather than going back and forth to disk during each query. It also allows the caching of functions pointers, the database catalog, and other items so that subsequent queries on the same connection are faster.

> DuckDB is optimized for bulk operations, so executing many small transactions is not a primary design goal.

## Concurrency within a Single Process

DuckDB supports concurrency within a single process according to the following rules. As long as there are no write conflicts, multiple concurrent writes will succeed. Appends will never conflict, even on the same table. Multiple threads can also simultaneously update separate tables or separate subsets of the same table. Optimistic concurrency control comes into play when two threads attempt to edit (update or delete) the same row at the same time. In that situation, the second thread to attempt the edit will fail with a conflict error.

## Writing to DuckDB from Multiple Processes

Writing to DuckDB from multiple processes is not supported automatically and is not a primary design goal (see [Handling Concurrency](#handling-concurrency)).

If multiple processes must write to the same file, several design patterns are possible, but would need to be implemented in application logic. For example, each process could acquire a cross-process mutex lock, then open the database in read/write mode and close it when the query is complete. Instead of using a mutex lock, each process could instead retry the connection if another process is already connected to the database (being sure to close the connection upon query completion). Another alternative would be to do multi-process transactions on a MySQL, PostgreSQL, or SQLite database, and use DuckDB's [MySQL](../extensions/mysql), [PostgreSQL](../extensions/postgres), or [SQLite](../extensions/sqlite) extensions to execute analytical queries on that data periodically.

Additional options include writing data to Parquet files and using DuckDB's ability to [read multiple Parquet files](../data/parquet), taking a similar approach with [CSV files](../data/csv), or creating a web server to receive requests and manage reads and writes to DuckDB.
