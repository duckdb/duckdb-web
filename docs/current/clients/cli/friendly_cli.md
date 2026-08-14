---
layout: docu
redirect_from:
- /docs/preview/clients/cli/friendly
- /docs/stable/clients/cli/friendly_cli
title: Friendly CLI
---

Along with our [Friendly SQL]({% link docs/current/sql/dialect/friendly_sql.md %}), we provide
**friendly CLI** features.

## Dark/Light Mode

The CLI automatically detects whether the terminal is using a dark or light background and adjusts syntax highlighting colors accordingly. The mode can also be set manually using the `.highlight_mode` command:

```sql
.highlight_mode dark
```

```sql
.highlight_mode light
```

To use a mix of colors suitable for both dark and light backgrounds:

```sql
.highlight_mode mixed
```

## 8-Bit Colors

Since DuckDB v1.5, the CLI supports 8-bit colors corresponding to [Xterm system colors](https://www.ditig.com/256-colors-cheat-sheet#xterm-system-colors):

```.sql
.display_colors
```

```text
darkred1 red darkred2 red3 red4 red1 brightred indianred1 ...
```

## Dynamic Prompt

The default prompts are the following:

```text
-- macOS / Linux
{max_length:40}{color:38,5,208}{color:bold}{setting:current_database_and_schema}{color:reset} D 
-- Windows
{max_length:40}{color:green}{color:bold}{setting:current_database_and_schema}{color:reset} D 
```

## Return the Result of the Last Query Using `_`

You can use the `_` (underscore) table to query the result of the last query:

```sql
SELECT 42 AS x;
```
```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```
```sql
FROM _;
```
```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

If the last query did not return a result (e.g., because it performed an update operation), the CLI throws an error:

```console
Binder Error:
Failed to query last result "_": no result available
```
