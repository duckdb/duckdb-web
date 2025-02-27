---
layout: docu
redirect_from:
- /docs/guides/snippets/sharing_macros
title: Sharing Macros
---

DuckDB has a powerful [macro mechanism]({% link docs/stable/sql/statements/create_macro.md %}) that allows creating shorthands for common tasks. For example, we can define a macro that pretty-prints a non-negative integer as a short string that contains billions, millions, and thousands (without rounding) as follows:

```bash
duckdb pretty_print_integer_macro.duckdb
```

```sql
CREATE MACRO pretty_print_integer(n) AS
    CASE
        WHEN n >= 1_000_000_000 THEN printf('%dB', n // 1_000_000_000)
        WHEN n >= 1_000_000     THEN printf('%dM', n // 1_000_000)
        WHEN n >= 1_000         THEN printf('%dk', n // 1_000)
        ELSE printf('%d', n)
    END;

SELECT pretty_print_integer(25_500_000) AS x;
```

```text
┌─────────┐
│    x    │
│ varchar │
├─────────┤
│ 25M     │
└─────────┘
```

As one would expect, the macro gets persisted in the database.
But this also means that we can host it on an HTTPS endpoint and share it with anyone!
We have published this macro on `blobs.duckdb.org`. Let's start a new DuckDB session and try it:

```bash
duckdb
```

We can now attach to the remote endpoint and use the macro:

```sql
ATTACH 'https://blobs.duckdb.org/data/pretty_print_integer_macro.duckdb' AS db;
USE db;
SELECT pretty_print_integer(42_123) AS x;
```

```text
┌─────────┐
│    x    │
│ varchar │
├─────────┤
│ 42k     │
└─────────┘
```