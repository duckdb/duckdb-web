---
layout: docu
railroad: statements/attach.js
title: ATTACH and DETACH Statements
---

DuckDB allows attaching to and detaching from database files.

## Examples

Attach the database `file.db` with the alias inferred from the name (`file`):

```sql
ATTACH 'file.db';
```

Attach the database `file.db` with an explicit alias (`file_db`):

```sql
ATTACH 'file.db' AS file_db;
```

Attach the database `file.db` in read only mode:

```sql
ATTACH 'file.db' (READ_ONLY);
```

Attach the database `file.db` with a block size of 16 kB:

```sql
ATTACH 'file.db' (BLOCK_SIZE 16_384);
```

Attach a SQLite database for reading and writing (see the [`sqlite` extension]({% link docs/preview/extensions/sqlite.md %}) for more information):

```sql
ATTACH 'sqlite_file.db' AS sqlite_db (TYPE sqlite);
```

Attach the database `file.db` if inferred database alias `file` does not yet exist:

```sql
ATTACH IF NOT EXISTS 'file.db';
```

Attach the database `file.db` if explicit database alias `file_db` does not yet exist:

```sql
ATTACH IF NOT EXISTS 'file.db' AS file_db;
```

Create a table in the attached database with alias `file`:

```sql
CREATE TABLE file.new_table (i INTEGER);
```

Detach the database with alias `file`:

```sql
DETACH file;
```

Show a list of all attached databases:

```sql
SHOW DATABASES;
```

Change the default database that is used to the database `file`:

```sql
USE file;
```

## `ATTACH`

The `ATTACH` statement adds a new database file to the catalog that can be read from and written to.
Note that attachment definitions are not persisted between sessions: when a new session is launched, you have to re-attach to all databases.

### Attach Syntax

<div id="rrdiagram1"></div>

`ATTACH` allows DuckDB to operate on multiple database files, and allows for transfer of data between different database files.

`ATTACH` supports HTTP and S3 endpoints. For these, it creates a read-only connection by default.
Therefore, the following two commands are equivalent:

```sql
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db;
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

Similarly, the following two commands connecting to S3 are equivalent:

```sql
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db;
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

> Prior to DuckDB version 1.1.0, it was necessary to specify the `READ_ONLY` flag for HTTP and S3 endpoints.

### Explicit Storage Versions

[DuckDB v1.2.0 introduced the `STORAGE_VERSION` option]({% post_url 2025-02-05-announcing-duckdb-120 %}#explicit-storage-versions), which allows explicilty specifying the storage version.
Using this, you can opt-in to newer forwards-incompatible features:

```sql
ATTACH 'file.db' (STORAGE_VERSION 'v1.2.0');
```

This setting specifies the minimum DuckDB version that should be able to read the database file. When database files are written with this option, the resulting files cannot be opened by older DuckDB released versions than the specified version. They can be read by the specified version and all newer versions of DuckDB.

For more details, see the [“Storage” page]({% link docs/preview/internals/storage.md %}#explicit-storage-versions).

## `DETACH`

The `DETACH` statement allows previously attached database files to be closed and detached, releasing any locks held on the database file.

Note that it is not possible to detach from the default database: if you would like to do so, issue the [`USE` statement]({% link docs/preview/sql/statements/use.md %}) to change the default database to another one. For example, if you are connected to a persistent database, you may change to an in-memory database by issuing:

```sql
ATTACH ':memory:' AS memory_db;
USE memory_db;
```

> Warning Closing the connection, e.g., invoking the [`close()` function in Python]({% link docs/preview/clients/python/dbapi.md %}#connection), does not release the locks held on the database files as the file handles are held by the main DuckDB instance (in Python's case, the `duckdb` module).

### Detach Syntax

<div id="rrdiagram2"></div>

## Options

| Name                        | Description                                                                                                                 | Type      | Default value |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------|-----------|---------------|
| `access_mode`               | Access mode of the database (**AUTOMATIC**, **READ_ONLY**, or **READ_WRITE**).                                              | `VARCHAR` | `automatic`   |
| `type`                      | The file type (**DUCKDB** or **SQLITE**), or deduced from the input string literal (MySQL, PostgreSQL).                     | `VARCHAR` | `DUCKDB`      |
| `block_size`                | The block size of a new database file. Must be a power of two and within [16384, 262144]. Cannot be set for existing files. | `UBIGINT` | `262144`      |

## Name Qualification

The fully qualified name of catalog objects contains the *catalog*, the *schema* and the *name* of the object. For example:

Attach the database `new_db`:

```sql
ATTACH 'new_db.db';
```

Create the schema `my_schema` in the database `new_db`:

```sql
CREATE SCHEMA new_db.my_schema;
```

Create the table `my_table` in the schema `my_schema`:

```sql
CREATE TABLE new_db.my_schema.my_table (col INTEGER);
```

Refer to the column `col` inside the table `my_table`:

```sql
SELECT new_db.my_schema.my_table.col FROM new_db.my_schema.my_table;
```

Note that often the fully qualified name is not required. When a name is not fully qualified, the system looks for which entries to reference using the *catalog search path*. The default catalog search path includes the system catalog, the temporary catalog and the initially attached database together with the `main` schema.

Also note the rules on [identifiers and database names in particular]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#database-names).

### Default Database and Schema

When a table is created without any qualifications, the table is created in the default schema of the default database. The default database is the database that is launched when the system is created – and the default schema is `main`.

Create the table `my_table` in the default database:

```sql
CREATE TABLE my_table (col INTEGER);
```

### Changing the Default Database and Schema

The default database and schema can be changed using the `USE` command.

Set the default database schema to `new_db.main`:

```sql
USE new_db;
```

Set the default database schema to `new_db.my_schema`:

```sql
USE new_db.my_schema;
```

### Resolving Conflicts

When providing only a single qualification, the system can interpret this as *either* a catalog *or* a schema, as long as there are no conflicts. For example:

```sql
ATTACH 'new_db.db';
CREATE SCHEMA my_schema;
```

Creates the table `new_db.main.tbl`:

```sql
CREATE TABLE new_db.tbl (i INTEGER);
```

Creates the table `default_db.my_schema.tbl`:

```sql
CREATE TABLE my_schema.tbl (i INTEGER);
```

If we create a conflict (i.e., we have both a schema and a catalog with the same name) the system requests that a fully qualified path is used instead:

```sql
CREATE SCHEMA new_db;
CREATE TABLE new_db.tbl (i INTEGER);
```

```console
Binder Error:
Ambiguous reference to catalog or schema "new_db" - use a fully qualified path like "memory.new_db"
```

### Changing the Catalog Search Path

The catalog search path can be adjusted by setting the `search_path` configuration option, which uses a comma-separated list of values that will be on the search path. The following example demonstrates searching in two databases:

```sql
ATTACH ':memory:' AS db1;
ATTACH ':memory:' AS db2;
CREATE table db1.tbl1 (i INTEGER);
CREATE table db2.tbl2 (j INTEGER);
```

Reference the tables using their fully qualified name:

```sql
SELECT * FROM db1.tbl1;
SELECT * FROM db2.tbl2;
```

Or set the search path and reference the tables using their name:

```sql
SET search_path = 'db1,db2';
SELECT * FROM tbl1;
SELECT * FROM tbl2;
```

## Transactional Semantics

When running queries on multiple databases, the system opens separate transactions per database. The transactions are started *lazily* by default – when a given database is referenced for the first time in a query, a transaction for that database will be started. `SET immediate_transaction_mode = true` can be toggled to change this behavior to eagerly start transactions in all attached databases instead.

While multiple transactions can be active at a time – the system only supports *writing* to a single attached database in a single transaction. If you try to write to multiple attached databases in a single transaction the following error will be thrown:

```console
Attempting to write to database "db2" in a transaction that has already modified database "db1" -
a single transaction can only write to a single attached database.
```

The reason for this restriction is that the system does not maintain atomicity for transactions across attached databases. Transactions are only atomic *within* each database file. By restricting the global transaction to write to only a single database file the atomicity guarantees are maintained.