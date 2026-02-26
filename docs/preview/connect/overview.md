---
layout: docu
title: Connect
---

## Connect or Create a Database

To use DuckDB, you must first create a connection to a database. The exact syntax varies between the [client APIs]({% link docs/preview/clients/overview.md %}) but it typically involves passing an argument to configure persistence.

## Persistence

DuckDB can operate in both persistent mode, where the data is saved to disk, and in in-memory mode, where the entire dataset is stored in the main memory.

> Tip Both persistent and in-memory databases use spilling to disk to facilitate larger-than-memory workloads (i.e., out-of-core-processing).

### Persistent Database

To create or open a persistent database, set the path of the database file, e.g., `my_database.duckdb`, when creating the connection.
This path can point to an existing database or to a file that does not yet exist and DuckDB will open or create a database at that location as needed.
The file may have an arbitrary extension, but `.db` or `.duckdb` are two common choices with `.ddb` also used sometimes.

Starting with v0.10, DuckDB's storage format is [backwards-compatible]({% link docs/preview/internals/storage.md %}#backward-compatibility), i.e., DuckDB is able to read database files produced by an older version of DuckDB.
For example, DuckDB v0.10 can read and operate on files created by the previous DuckDB version, v0.9.
For more details on DuckDB's storage format, see the [storage page]({% link docs/preview/internals/storage.md %}).

### In-Memory Database

DuckDB can operate in in-memory mode. In most clients, this can be activated by passing the special value `:memory:` as the database file or omitting the database file argument. In in-memory mode, no data is persisted to disk, therefore, all data is lost when the process finishes.
