---
layout: docu
railroad: statements/alter_database.js
redirect_from:
- /docs/stable/sql/statements/alter_database
title: ALTER DATABASE Statement
---

> Warning The `ALTER DATABASE` statement is not supported in DuckDB 2.0.0: `ALTER DATABASE ⟨old_name⟩ RENAME TO ⟨new_name⟩` fails with `Parser Error: syntax error at or near "RENAME"`. To rename an attached database, `DETACH` it and `ATTACH` it again with a different alias.

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
