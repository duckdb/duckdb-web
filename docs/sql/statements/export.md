---
layout: docu
title: Export & Import Database
selected: Documentation/SQL/Export
expanded: SQL
railroad: statements/export.js
---
The EXPORT DATABASE command allows you to export the contents of the database to a specific directory. The IMPORT DATABASE command allows you to then read the contents again.

### Examples
```sql
-- export the database to the target directory
EXPORT DATABASE 'target_directory';
-- export the table contents with the given options
EXPORT DATABASE 'target_directory' (FORMAT CSV, DELIMITER '|');
-- export the table contents as parquet
EXPORT DATABASE 'target_directory' (FORMAT PARQUET);

--reload the database again
IMPORT DATABASE 'target_directory'
```

### Syntax
<div id="rrdiagram"></div>

The EXPORT DATABASE command exports the full contents of the database - including schema information, tables, views and sequences - to a specific directory that can then be loaded again. The created directory will be structured as follows:

```
target_directory/schema.sql
target_directory/load.sql
target_directory/t_1.csv
...
target_directory/t_n.csv
```

The `schema.sql` file contains the schema statements that are found in the database. It contains any CREATE SCHEMA, CREATE TABLE, CREATE VIEW and CREATE SEQUENCE commands that are necessary to re-construct the database.

The `load.sql` file contains a set of `COPY` statements that can be used to read the data from the CSV files again. The file contains a single `COPY` statement for every table found in the schema.

The database can be reloaded by using the IMPORT DATABASE command again, or manually by running `schema.sql` followed by `load.sql` to re-load the data.
