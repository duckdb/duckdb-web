---
layout: docu
railroad: statements/export.js
redirect_from:
- /docs/sql/statements/export
title: EXPORT/IMPORT DATABASE Statements
---

The `EXPORT DATABASE` command allows you to export the contents of the database to a specific directory. The `IMPORT DATABASE` command allows you to then read the contents again.

## Examples

```sql
-- export the database to the target directory 'db_name' as CSV files
EXPORT DATABASE 'db_name';
-- export to directory 'db_name', using the given options for the CSV serialization
EXPORT DATABASE 'db_name' (FORMAT CSV, DELIMITER '|');
-- export to directory 'db_name', tables serialized as Parquet
EXPORT DATABASE 'db_name' (FORMAT PARQUET);
-- export to directory 'db_name', tables serialized as Parquet, compressed with ZSTD, with a row_group_size of 100000
EXPORT DATABASE 'db_name' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
-- reload the database again
IMPORT DATABASE 'db_name';
-- alternatively, use a PRAGMA
PRAGMA import_database('db_name');
```

For details regarding the writing of Parquet files, see the [Parquet Files page in the Data Import section](../../data/parquet/overview#writing-to-parquet-files), and the [`COPY` Statement page](copy).

## Syntax

<div id="rrdiagram"></div>

The `EXPORT DATABASE` command exports the full contents of the database - including schema information, tables, views and sequences - to a specific directory that can then be loaded again. The created directory will be structured as follows:

```text
target_directory/schema.sql
target_directory/load.sql
target_directory/t_1.csv
...
target_directory/t_n.csv
```

The `schema.sql` file contains the schema statements that are found in the database. It contains any `CREATE SCHEMA`, `CREATE TABLE`, `CREATE VIEW` and `CREATE SEQUENCE` commands that are necessary to re-construct the database.

The `load.sql` file contains a set of `COPY` statements that can be used to read the data from the CSV files again. The file contains a single `COPY` statement for every table found in the schema.

The database can be reloaded by using the `IMPORT DATABASE` command again, or manually by running `schema.sql` followed by `load.sql` to re-load the data.
