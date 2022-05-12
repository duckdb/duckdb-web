---
layout: docu
title: Create Table
selected: Documentation/SQL/Create Table
expanded: SQL
railroad: statements/createtable.js
---
The `CREATE TABLE` statement creates a table in the catalog.

### Examples
```sql
-- create a table with two integer columns (i and j)
CREATE TABLE t1(i INTEGER, j INTEGER);
-- create a table with a primary key
CREATE TABLE t1(id INTEGER PRIMARY KEY, j VARCHAR);
-- create a table with a composite primary key
CREATE TABLE t1(id INTEGER, j VARCHAR, PRIMARY KEY(id, j));
-- create a table with various different types and constraints
CREATE TABLE t1(i INTEGER NOT NULL, decimalnr DOUBLE CHECK(decimalnr<10), date DATE UNIQUE, time TIMESTAMP);
-- create a table from the result of a query
CREATE TABLE t1 AS SELECT 42 AS i, 84 AS j;
-- create a table from a CSV file using AUTO-DETECT (i.e., Automatically detecting column names and types)
CREATE TABLE t1 AS SELECT * FROM read_csv_auto ('path/file.csv');
```

Temporary tables can be created using a `CREATE TEMP TABLE` statement (see diagram below). 
Temporary tables are session scoped (similar to Postgres for example), meaning that only the specific connection that created them can access them, and once the connection to DuckDB is closed they will be automatically dropped. 
Temporary tables reside in memory rather than on disk (even when connecting to a persistent DuckDB), but if the `temp_directory` [configuration](/docs/sql/configuration) is set when connecting or with a `SET` command, data will be spilled to disk if memory becomes constrained. 

```sql
-- create a temporary table from a CSV file using AUTO-DETECT (i.e., Automatically detecting column names and types)
CREATE TEMP TABLE t1 AS SELECT * FROM read_csv_auto ('path/file.csv');

-- allow temporary tables to off-load excess memory to disk
SET temp_directory='/path/to/directory/';
```

The `CREATE OR REPLACE` syntax allows a new table to be created or for an existing table to be overwritten by the new table. This is shorthand for dropping the existing table and then creating the new one.

```sql
-- create a table with two integer columns (i and j) even if t1 already exists
CREATE OR REPLACE TABLE t1(i INTEGER, j INTEGER);
```

The `IF NOT EXISTS` syntax will only proceed with the creation of the table if it does not already exist. If the table already exists, no action will be taken and the existing table will remain in the database. 

```sql
-- create a table with two integer columns (i and j) only if t1 does not exist yet. 
CREATE TABLE IF NOT EXISTS t1(i INTEGER, j INTEGER);
```

### Syntax
<div id="rrdiagram"></div>
