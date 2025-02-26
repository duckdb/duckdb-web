---
layout: docu
title: Copying an In-Memory Database to a File
---

Imagine the following situation – you started DuckDB in in-memory mode but would like to persist the state of your database to disk.
You can achieve this by attaching to a disk-based database and using the [`COPY FROM DATABASE ... TO` command]({% link docs/sql/statements/copy.md %}#copy-from-database--to):

```sql
ATTACH 'my_database.db';
COPY FROM DATABASE memory TO my_database;
DETACH my_database;
```
