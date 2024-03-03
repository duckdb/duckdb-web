---
layout: docu
redirect_from:
- docs/archive/0.9.2/guides/import/query_sqlite
- docs/archive/0.9.1/guides/import/query_sqlite
title: SQLite Import
---

To run a query directly on a SQLite file, the `sqlite` extension is required.  This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL sqlite;
```

To load the `sqlite` extension for usage, use the `LOAD` SQL command:

```sql
LOAD sqlite;
```

After the SQLite extension is installed, tables can be queried from SQLite using the `sqlite_scan` function:

```sql
-- scan the table "tbl_name" from the SQLite file "test.db"
SELECT * FROM sqlite_scan('test.db', 'tbl_name');
```

Alternatively, the entire file can be attached using the `ATTACH` command. This allows you to query all tables stored within a SQLite database file as if they were a regular database.

```sql
-- attach the SQLite file "test.db"
ATTACH 'test.db' AS test (TYPE sqlite);
-- the table "tbl_name" can now be queried as if it is a regular table
SELECT * FROM test.tbl_name;
-- switch the active database to "test"
USE test;
-- list all tables in the file
SHOW TABLES;
```

For more information see the [SQLite extension documentation](../../extensions/sqlite).