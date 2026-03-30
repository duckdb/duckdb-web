---
layout: docu
redirect_from:
- /docs/stable/guides/file_formats/read_duckdb
title: Directly Read DuckDB Databases
---

DuckDB allows directly reading DuckDB files through the `read_duckdb` function:

```sql
read_duckdb(⟨'path_to_database'⟩, table_name = ⟨'table_to_read'⟩);
```

Using this function is equivalent to performing the following steps:

* Attaching to the database using a read-only connection.
* Querying the table specified through the `table_name` argument.
* Closing the connection to the database database.

## Examples

### Reading a Specific Table

To read the `region` table from the TPC-H dataset, run:

```sql
SELECT r_regionkey, r_name
FROM read_duckdb('https://blobs.duckdb.org/data/tpch-sf10.db', table_name = 'region');
```

```text
┌─────────────┬─────────────┐
│ r_regionkey │   r_name    │
│    int32    │   varchar   │
├─────────────┼─────────────┤
│           0 │ AFRICA      │
│           1 │ AMERICA     │
│           2 │ ASIA        │
│           3 │ EUROPE      │
│           4 │ MIDDLE EAST │
└─────────────┴─────────────┘
```

### Reading from Multiple Databases

You can use [globbing]({% link docs/current/sql/functions/pattern_matching.md %}#globbing) to read from multiple databases.
Two illustrate this, let's create two tables:

```bash
duckdb my-1.duckdb \
    -c "CREATE TABLE numbers AS SELECT 42 AS x;" \
    -c "CREATE TABLE letters AS SELECT 'm' AS a;"

duckdb my-2.duckdb \
    -c "CREATE TABLE numbers AS SELECT 43 AS x;"
```

Then, in DuckDB, you can run:

```sql
SELECT x FROM read_duckdb('my-*.duckdb', table_name = 'numbers');
```

```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│    42 │
│    43 │
└───────┘
```

### Reading from Databases with a Single Table

If all databases in `read_duckdb`'s argument have a single table, the `table_name` argument is optional:

```sql
FROM read_duckdb('my-2.duckdb');
```

```text
┌───────┐
│   x   │
│ int32 │
├───────┤
│     3 │
└───────┘
```

If the extension is `.db` or `.duckdb`, you can also omit the `read_duckdb` call (similarly to how you can omit `read_csv` and `read_parquet`):

```sql
FROM 'my-2.duckdb';
```

## Limitations

`read_duckdb` currently only supports reading from tables.
Reading from views is not yet supported.
