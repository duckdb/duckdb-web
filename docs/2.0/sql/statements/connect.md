---
layout: docu
redirect_from:
- /docs/current/sql/statements/connect
- /docs/lts/sql/statements/connect
- /docs/preview/sql/statements/connect
title: CONNECT and DISCONNECT Statements
---

> New Support for the `CONNECT` and `DISCONNECT` statements was introduced in DuckDB 2.0.

The `CONNECT` statement routes the current session to a remote database, so that subsequent queries execute on that remote and their results stream back. `DISCONNECT` returns the session to the local database.

`CONNECT` is central to using [DuckDB as a server]({% link docs/2.0/quack/overview.md %}): a DuckDB instance can serve its databases over the network, and any other DuckDB can attach to it and route queries there.

## Examples

Attach a remote DuckDB server over the [Quack protocol]({% link docs/2.0/quack/overview.md %}), route queries to it, and disconnect again:

```sql
ATTACH 'quack:server.example.com' AS qk (TOKEN '⟨my_token⟩');

CONNECT qk;
SELECT count(*) FROM events; -- executes on the server, results stream back
DISCONNECT;
```

Connect directly to a remote database using a connection string. For databases other than DuckDB, the connection string must start with the type of the database, e.g., `postgres:`, followed by a connection string for that database (here, a [libpq connection string]({% link docs/2.0/core_extensions/postgres/overview.md %}#configuration)):

```sql
CONNECT 'postgres:dbname=mydb host=localhost';
SELECT count(*) FROM orders; -- runs on the PostgreSQL server
DISCONNECT;
```

## Syntax

```sql
CONNECT { ⟨attached_database⟩ | '⟨connection_string⟩' };
DISCONNECT;
```

`CONNECT` accepts either the alias of a database [attached]({% link docs/2.0/sql/statements/attach.md %}) with `ATTACH`, or a connection string for a remote database. While a connection is active, queries that do not explicitly qualify a different database execute on the remote.

`DISCONNECT` ends the active connection and returns the session to the local database. Issuing `DISCONNECT` without an active connection returns an error.

## Supported Databases

`CONNECT` works with databases that support remote execution, including:

* DuckDB servers reached over the [Quack protocol]({% link docs/2.0/quack/overview.md %}).
* [PostgreSQL]({% link docs/2.0/core_extensions/postgres/overview.md %}) and [MySQL]({% link docs/2.0/core_extensions/mysql.md %}) servers. For these, the remote pushdown optimizer ships SQL directly to the server instead of pulling tables over the wire.

In-process local databases, such as the default in-memory database or a DuckDB database file, do not support `CONNECT`.
