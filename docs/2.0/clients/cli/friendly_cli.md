---
layout: docu
redirect_from:
- /docs/stable/clients/cli/friendly_cli
- /docs/current/clients/cli/friendly_cli
- /docs/lts/clients/cli/friendly_cli
- /docs/preview/clients/cli/friendly_cli
title: Friendly CLI
---

Along with our [Friendly SQL]({% link docs/2.0/sql/dialect/friendly_sql.md %}), we provide
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

The mode can also be selected when launching the CLI using the `-dark-mode` and `-light-mode` [command line arguments]({% link docs/2.0/clients/cli/arguments.md %}):

```batch
duckdb -dark-mode
```

```batch
duckdb -light-mode
```

## 8-Bit Colors

Since DuckDB 1.5, the CLI supports 8-bit colors corresponding to [Xterm system colors](https://www.ditig.com/256-colors-cheat-sheet#xterm-system-colors):

```.sql
.display_colors
```

```text
darkred1 red darkred2 red3 red4 red1 brightred indianred1 ...
```

## Dynamic Prompt

The default prompt is the following:

```text
{max_length:50}{highlight_element:prompt_connect}{setting:connect_name_prefix}{highlight_element:prompt}{setting:current_database_and_schema}{color:reset} D 
```

While the session is connected to a remote database with [`CONNECT`]({% link docs/2.0/sql/statements/connect.md %}), `{setting:connect_name_prefix}` shows the remote database's name (or its URI, e.g., `quack:localhost`, for `CONNECT '⟨uri⟩'` and `-connect`); otherwise it is empty.

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
