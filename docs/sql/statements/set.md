---
layout: docu
title: Set/Reset
selected: Documentation/SQL/Set
expanded: SQL
railroad: statements/set.js
---

The `SET` statement modifies the provided DuckDB configuration option at the specified scope.

### Examples
```sql
-- Update the `memory_limit` configuration value.
set memory_limit='10GB';
-- configure the system to use 1 thread
SET threads TO 1;
-- Change configuration option to default value
RESET threads;
```

### Syntax
<div id="rrdiagram1"></div>

`SET` updates a DuckDB configuration option to the provided value.

### Reset
<div id="rrdiagram2"></div>

The `RESET` statement changes the given DuckDB configuration option to the default value.

### Scopes
* local - Not yet implemented.
* session - Configuration value is used (or reset) only for the current session attached to a DuckDB instance.
* global - Configuration value is used (or reset) across the entire DuckDB instance.

### Configuration
See the [Configuration](../configuration) page for the full list of configuration options.
