---
layout: docu
title: Sharing Macros
---

DuckDB has a powerful [macro mechanism]({% link docs/preview/sql/statements/create_macro.md %}) that allows creating shorthands for common tasks.

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

Make sure that the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) is installed:

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

To use it, make sure that the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) is installed:

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
         id = -132780776949939723506211681506129908318
       code = 126327004005066229305810236187733612209
        uic = -145623335062491121476006068124745817380
 name_short = -114540917565721687000878144381189869683
name_medium = -568264780518431562127359918655305384
  name_long = 126079956280724674884063510870679874110
       slug = -53458800462031706622213217090663245511
    country = 143068442936912051858689770843609587944
       type = 5665662315470785456147400604088879751
    geo_lat = 160608116135251821259126521573759502306
    geo_lng = -138297281072655463682926723171691547732
```
