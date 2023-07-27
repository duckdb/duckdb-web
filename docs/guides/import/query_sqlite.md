---
layout: docu
title: SQLite Import
selected: SQLite Import
---

# How to run a query directly on a SQLite file

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

Alternatively, the entire file can be attached using the `sqlite_attach` command. This creates views over all of the tables in the file that allow you to query the tables using regular SQL syntax.

```sql
-- attach the SQLite file "test.db"
CALL sqlite_attach('test.db');
-- the table "tbl_name" can now be queried as if it is a regular table
SELECT * FROM tbl_name;
```

For more information see the [SQLite scanner documentation](/docs/extensions/sqlite_scanner).
