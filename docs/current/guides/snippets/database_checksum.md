---
layout: docu
title: Calculating a Database Checksum
---

To calculate a database checksum, use a commutative operation such as `bit_xor` on all columns, all rows, and all tables.

First, create a table macro that performs this for each table:

```sql
CREATE OR REPLACE MACRO table_checksum(table_name) AS TABLE
    SELECT bit_xor(value) AS table_checksum
    FROM (
        UNPIVOT (
            SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
            FROM query_table(table_name)
        )
        ON columns(*)
    );
```

You need to call this macro for all tables. In the CLI, you can do so by dynamically generating a SQL file:

```sql
.mode list
.header off
.once checksum_all_tables.sql
SELECT printf('CREATE OR REPLACE TABLE table_checksums (checksum UHUGEINT);')
UNION ALL
SELECT printf('INSERT INTO table_checksums FROM table_checksum(''%s'');', table_name)
FROM duckdb_tables()
WHERE NOT internal;
.mode duckbox
```

Read the SQL file back and calculate the checksum for the database:

```sql
.read checksum_all_tables.sql
SELECT bit_xor(checksum) AS database_checksum
FROM table_checksums;
```
