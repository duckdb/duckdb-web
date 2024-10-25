---
layout: docu
title: Sharing Macros
---

DuckDB has a powerful [macro mechanism]({% docs/sql/statements/create_macro.md %}).
For example, we can start create a persistent DuckDB database and define a [`checksum` function over all columns]({% post_url 2024-10-11-duckdb-tricks-part-2 }),

```batch
duckdb checksum-macro.duckdb
```

```plsql
CREATE MACRO checksum(table_name) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(table_name);
```

As one would expect, the macro gets persisted in the database.
But this also means that we can host it on an HTTPS endpoint and share it with anyone!

Let's start a new DuckDB session:

```batch
duckdb
```

We can now attach to the remote endpoint and use the macro:

```sql
ATTACH 'https://blobs.duckdb.org/data/checksum-macro.duckdb' AS checksum_macro;
CREATE TABLE tbl AS SELECT unnest([42, 43]) AS x;
SELECT * FROM checksum_macro.checksum('tbl');
```

```sql
CREATE TABLE tbl AS SELECT unnest([42, 43]) AS x;
ATTACH 'https://blobs.duckdb.org/data/checksum-macro.duckdb' AS checksum_macro;
USE checksum_macro;
SELECT * FROM checksum('main.tbl');
```
