---
layout: docu
redirect_from:
- /docs/current/guides/sql_editors/orcaq
- /docs/lts/guides/sql_editors/orcaq
- /docs/preview/guides/sql_editors/orcaq
- /docs/stable/guides/sql_editors/orcaq
title: OrcaQ SQL Editor
how_to_topic: tools-meta
---

[OrcaQ](https://github.com/cin12211/orca-q) is a free, open-source (MIT) database editor for macOS and Linux. Besides DuckDB, it connects to PostgreSQL, MySQL, SQLite, SQL Server, Redis, MongoDB and other databases. OrcaQ opens DuckDB database files through the official [DuckDB Node.js client](https://www.npmjs.com/package/@duckdb/node-api), so no separate driver is needed.

> DuckDB support in OrcaQ is in beta, and it is available in the desktop app only. On macOS it requires Apple Silicon.

## Installing OrcaQ

Download the latest desktop build (`.dmg` for macOS, `.AppImage` or `.deb` for Linux) from the [OrcaQ releases page](https://github.com/cin12211/orca-q/releases/latest) and install it.

## Connecting to a DuckDB Database

1. Open OrcaQ, create or open a workspace, and click **Add Connection**.
2. In **Select Database Type**, choose **DuckDB** and click **Next**.
3. Give the connection a name, then click **Browse** next to **Database File** and select your `.duckdb` file. To start from an empty database, click **New database file**, pick a file name and a folder, and OrcaQ creates the file for you.
4. Click **Test** to check that the file can be opened, then click **Create**.

    > DuckDB allows only one process to write to a database file at a time. Close other programs that have the file open, such as the DuckDB CLI, before you connect.

5. Open the connection. The sidebar lists the schemas of the database with their tables, views and macros.
6. Open a raw query tab, write SQL, and run it. Large results are streamed to the result grid, and a running query can be cancelled.

Now you are ready to query DuckDB with OrcaQ.
