---
layout: docu
railroad: statements/alter_database.js
title: ALTER DATABASE Statement
---

The `ALTER DATABASE` command modifies a DuckDB database. This command can be used to change a database's name without needing to detach and reattach it.

## Syntax

<div id="rrdiagram"></div>

## `RENAME DATABASE`

The following scenarios are not supported when renaming a DuckDB database with `ALTER DATABASE`:

* Renaming a database to certain reserved keywords such as `system` or `temp`.
* Renaming a database to the same name of a database attached in memory.

Rename a database from `old_name` to `new_name`:

```sql
ALTER DATABASE old_name RENAME TO new_name;
```

Check if a database exists and rename it:

```sql
ALTER DATABASE IF EXISTS non_existent RENAME TO something_else;
```
