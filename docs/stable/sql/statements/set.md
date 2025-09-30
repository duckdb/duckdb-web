---
layout: docu
railroad: statements/set.js
redirect_from:
- /docs/sql/statements/set
title: SET and RESET Statements
---

The `SET` statement modifies the provided DuckDB configuration option at the specified scope.

## Examples

Update the `memory_limit` configuration value:

```sql
SET memory_limit = '10GB';
```

Configure the system to use `1` thread:

```sql
SET threads = 1;
```

Or use the `TO` keyword:

```sql
SET threads TO 1;
```

Change configuration option to default value:

```sql
RESET threads;
```

Retrieve configuration value:

```sql
SELECT current_setting('threads');
```

Set the default collation for the session:

```sql
SET SESSION default_collation = 'nocase';
```

### Set a Global Variable

Set the default sort order globally:

```sql
SET GLOBAL sort_order = 'desc';
```

Set the default threads globally: 

```sql
SET GLOBAL threads = 4;
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

See the [Configuration]({% link docs/stable/configuration/overview.md %}) page for the full list of configuration options.
