---
layout: docu
redirect_from:
- /docs/guides/snippets/sharing_macros
- /docs/stable/guides/snippets/sharing_macros
- /docs/current/guides/snippets/sharing_macros
- /docs/lts/guides/snippets/sharing_macros
- /docs/preview/guides/snippets/sharing_macros
title: Sharing Macros
---

DuckDB has a powerful [macro mechanism]({% link docs/2.0/sql/statements/create_macro.md %}) that allows creating shorthands for common tasks.

## Sharing a Scalar Macro

First, we define a macro that pretty-prints a non-negative integer as a short string with thousands, millions, and billions (without rounding) as follows:

```batch
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
We have published this macro on `blobs.duckdb.org`.

You can try it from DuckDB:

```batch
duckdb
```

Make sure that the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}) is installed:

```sql
INSTALL httpfs;
```

You can now attach to the remote endpoint and use the macro:

```sql
ATTACH 'https://blobs.duckdb.org/data/pretty_print_integer_macro.duckdb'
    AS pretty_print_macro_db;

SELECT pretty_print_macro_db.pretty_print_integer(42_123) AS x;
```

```text
┌─────────┐
│    x    │
│ varchar │
├─────────┤
│ 42k     │
└─────────┘
```

## Sharing a Table Macro

It's also possible to share table macros. For example, we created the [`checksum` macro]({% post_url 2024-10-11-duckdb-tricks-part-2 %}#computing-checksums-for-columns) as follows:

```batch
duckdb compute_table_checksum.duckdb
```

```sql
CREATE MACRO checksum(table_name) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(table_name);
```

To use it, make sure that the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}) is installed:

```sql
INSTALL httpfs;
```

You can attach to the remote endpoint and use the macro:

```sql
ATTACH 'https://blobs.duckdb.org/data/compute_table_checksum.duckdb'
    AS compute_table_checksum_db;

CREATE TABLE stations AS
    FROM 'https://blobs.duckdb.org/stations.parquet';

.mode line
FROM compute_table_checksum_db.checksum('stations');
```

```text
         id = 207501589970998739957162925925638303138
       code = 126327004005066229305810236187733612209
        uic = 194659031858447341987368539307022394076
 name_short = 225741449355216776462496463050578341773
name_medium = 339714102140420031901247247513112906072
  name_long = 126079956280724674884063510870679874110
       slug = 286823566458906756841161390341104965945
    country = 143068442936912051858689770843609587944
       type = 5665662315470785456147400604088879751
    geo_lat = 160608116135251821259126521573759502306
    geo_lng = 201985085848282999780447884260076663724
```
