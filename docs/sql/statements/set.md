---
layout: docu
title: SET/RESET Statements
railroad: statements/set.js
---

The `SET` statement modifies the provided DuckDB configuration option at the specified scope.

## Examples

```sql
-- Update the memory_limit configuration value
SET memory_limit = '10GB';
-- Configure the system to use 1 thread
SET threads = 1;
-- Or use the 'TO' keyword
SET threads TO 1;
-- Change configuration option to default value
RESET threads;
-- Retrieve configuration value
SELECT current_setting('threads');
-- Set the default catalog search path globally
SET GLOBAL search_path = 'db1,db2'
-- Set the default collation for the session
SET SESSION default_collation = 'nocase';
```

## Syntax

<div id="rrdiagram1"></div>

`SET` updates a DuckDB configuration option to the provided value.

## `RESET`

<div id="rrdiagram2"></div>

The `RESET` statement changes the given DuckDB configuration option to the default value.

## Scopes

Configuration options can have different scopes:

* `GLOBAL`: Configuration value is used (or reset) across the entire DuckDB instance.
* `SESSION`: Configuration value is used (or reset) only for the current session attached to a DuckDB instance.
* `LOCAL`: Not yet implemented.

When not specified, the default scope for the configuration option is used. For most options this is `GLOBAL`.

## Configuration

See the [Configuration](../../configuration/overview) page for the full list of configuration options.
