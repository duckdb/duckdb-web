---
layout: docu
title: SQLite Import
redirect_from:
  - /docs/guides/import/query_sqlite
---

To run a query directly on a SQLite file, the `sqlite` extension is required.

## Installation and Loading

The extension can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL sqlite;
```

To load the `sqlite` extension for usage, use the `LOAD` SQL command:

```sql
LOAD sqlite;
```

## Usage

After the SQLite extension is installed, tables can be queried from SQLite using the `sqlite_scan` function:

```sql
-- Scan the table "tbl_name" from the SQLite file "test.db"
SELECT * FROM sqlite_scan('test.db', 'tbl_name');
```

Alternatively, the entire file can be attached using the `ATTACH` command. This allows you to query all tables stored within a SQLite database file as if they were a regular database.

```sql
-- Attach the SQLite file "test.db"
ATTACH 'test.db' AS test (TYPE sqlite);
-- The table "tbl_name" can now be queried as if it is a regular table
SELECT * FROM test.tbl_name;
-- Switch the active database to "test"
USE test;
-- List all tables in the file
SHOW TABLES;
```

For more information see the [SQLite extension documentation]({% link docs/extensions/sqlite.md %}).
