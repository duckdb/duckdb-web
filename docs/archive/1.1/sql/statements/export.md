---
layout: docu
railroad: statements/export.js
title: EXPORT and IMPORT DATABASE Statements
---

The `EXPORT DATABASE` command allows you to export the contents of the database to a specific directory. The `IMPORT DATABASE` command allows you to then read the contents again.

## Examples

Export the database to the target directory 'target_directory' as CSV files:

```sql
EXPORT DATABASE 'target_directory';
```

Export to directory 'target_directory', using the given options for the CSV serialization:

```sql
EXPORT DATABASE 'target_directory' (FORMAT CSV, DELIMITER '|');
```

Export to directory 'target_directory', tables serialized as Parquet:

```sql
EXPORT DATABASE 'target_directory' (FORMAT PARQUET);
```

Export to directory 'target_directory', tables serialized as Parquet, compressed with ZSTD, with a row_group_size of 100,000:

```sql
EXPORT DATABASE 'target_directory' (
    FORMAT PARQUET,
    COMPRESSION ZSTD,
    ROW_GROUP_SIZE 100_000
);
```

Reload the database again:

```sql
IMPORT DATABASE 'source_directory';
```

Alternatively, use a `PRAGMA`:

```sql
PRAGMA import_database('source_directory');
```

For details regarding the writing of Parquet files, see the [Parquet Files page in the Data Import section]({% link docs/archive/1.1/data/parquet/overview.md %}#writing-to-parquet-files) and the [`COPY` Statement page]({% link docs/archive/1.1/sql/statements/copy.md %}).

## `EXPORT DATABASE`

The `EXPORT DATABASE` command exports the full contents of the database – including schema information, tables, views and sequences – to a specific directory that can then be loaded again. The created directory will be structured as follows:

```text
target_directory/schema.sql
target_directory/load.sql
target_directory/t_1.csv
...
target_directory/t_n.csv
```

The `schema.sql` file contains the schema statements that are found in the database. It contains any `CREATE SCHEMA`, `CREATE TABLE`, `CREATE VIEW` and `CREATE SEQUENCE` commands that are necessary to re-construct the database.

The `load.sql` file contains a set of `COPY` statements that can be used to read the data from the CSV files again. The file contains a single `COPY` statement for every table found in the schema.

### Syntax

<div id="rrdiagram1"></div>

## `IMPORT DATABASE`

The database can be reloaded by using the `IMPORT DATABASE` command again, or manually by running `schema.sql` followed by `load.sql` to re-load the data.

### Syntax

<div id="rrdiagram2"></div>