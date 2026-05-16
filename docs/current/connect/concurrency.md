---
layout: docu
redirect_from:
- /docs/connect/concurrency
- /docs/preview/connect/concurrency
- /docs/stable/connect/concurrency
title: Concurrency
---

## Handling Concurrency

### Single Process

In in-process mode, DuckDB has two configurable options for concurrency:

1. **Read-write mode:** one process can both read and write to the database.
2. **Read-only mode:** multiple processes can read from the database, but no processes can write ([`access_mode = 'READ_ONLY'`]({% link docs/current/configuration/overview.md %}#configuration-reference)).

When using read-write mode, DuckDB supports multiple writer threads using a combination of [MVCC (Multi-Version Concurrency Control)](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) and optimistic concurrency control (see [Concurrency within a Single Process](#concurrency-within-a-single-process)), but all within that single writer process. The reason for this concurrency model is to allow for the caching of data in RAM for faster analytical queries, rather than going back and forth to disk during each query. It also allows the caching of function pointers, the database catalog, and other items so that subsequent queries on the same connection are faster.

#### Concurrency Model within a Single Process

DuckDB supports concurrency within a single process according to the following rules. As long as there are no write conflicts, multiple concurrent writes will succeed. Appends will never conflict, even on the same table. Multiple threads can also simultaneously update separate tables or separate subsets of the same table. Optimistic concurrency control comes into play when two threads attempt to edit (update or delete) the same row at the same time. In that situation, the second thread to attempt the edit will fail with a conflict error.

### Multiple Processes

Writing to DuckDB's native database format from multiple processes is supported through the [Quack remote protocol]({% link docs/current/quack/overview.md %}), which turns DuckDB into a client-server database. Quack in beta stage as of DuckDB v1.5.2, and is expected to become mature by [DuckDB v2.0 in autumn 2026]({% link release_calendar.md %}).

For a stable solution, consider using the [DuckLake](https://ducklake.select/) format with [PostgreSQL as the catalog database](https://ducklake.select/docs/stable/duckdb/usage/choosing_a_catalog_database#postgresql). By coordinating through a central PostgreSQL catalog, DuckDB instances can achieve concurrent read-writes on the same database. The DuckLake v1.0 specification and its DuckDB implementation, both intended for production use, were [published](https://ducklake.select/2026/04/13/ducklake-10/) in April 2026.

## Optimistic Concurrency Control

DuckDB uses [optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control), an approach generally considered to be the best fit for read-intensive analytical database systems as it speeds up read query processing. As a result any transactions that modify the same rows at the same time will cause a transaction conflict error:

```console
Transaction conflict: cannot update a table that has been altered!
```

> Tip A common workaround when a transaction conflict is encountered is to rerun the transaction.

## Troubleshooting

**File locks.**
DuckDB handles concurrent database access requests using file locks.
Exercise extra caution when accessing a DuckDB database file in a shared directory (e.g., from different operating systems using different file systems or on network attached storage).
