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

Attach the database `file.db` with a row group size of 2048 rows:

```sql
ATTACH 'file.db' (ROW_GROUP_SIZE 2048);
```

Attach a SQLite database for reading and writing (see the [`sqlite` extension]({% link docs/preview/core_extensions/sqlite.md %}) for more information):

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

Attach the database `file2.db` as alias `file_db` detaching and replacing the existing alias if it exists:

```sql
ATTACH OR REPLACE 'file2.db' AS file_db;
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

### `ATTACH` Syntax

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
ATTACH 's3://⟨blobs-duckdb⟩/databases/stations.duckdb' AS stations_db;
ATTACH 's3://⟨blobs-duckdb⟩/databases/stations.duckdb' AS stations_db (READ_ONLY);
```

### Explicit Storage Versions

[DuckDB v1.2.0 introduced the `STORAGE_VERSION` option]({% post_url 2025-02-05-announcing-duckdb-120 %}#explicit-storage-versions), which allows explicitly specifying the storage version.
Using this, you can opt-in to newer forwards-incompatible features:

```sql
ATTACH 'file.db' (STORAGE_VERSION 'v1.2.0');
```

This setting specifies the minimum DuckDB version that should be able to read the database file. When database files are written with this option, the resulting files cannot be opened by older DuckDB versions than the specified version. They can be read by the specified version and all newer versions of DuckDB.

For more details, see the [“Storage” page]({% link docs/preview/internals/storage.md %}#explicit-storage-versions).

### Database Encryption

DuckDB supports database encryption. By default, it uses [AES encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) with a key length of 256 bits using the recommended [GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode) mode. The encryption covers the main database file, the write-ahead-log (WAL) file, and even temporary files. To attach to an encrypted database, use the `ATTACH` statement with an `ENCRYPTION_KEY`.

```sql
ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'quack_quack');
```

To encrypt data, DuckDB can use either the built-in `mbedtls` library or the OpenSSL library from the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}). Note that the OpenSSL versions are much faster due to hardware acceleration, so make sure to load the `httpfs` for good encryption performance:

```sql
LOAD httpfs;
ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'quack_quack'); -- will be faster thanks to httpfs
```

To change the AES mode to [CBC](<https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)>) or [CTR](<https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR)>), use the `ENCRYPTION_CIPHER` option:

```sql
ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'quack_quack', ENCRYPTION_CIPHER 'CBC');
ATTACH 'encrypted.db' AS enc_db (ENCRYPTION_KEY 'quack_quack', ENCRYPTION_CIPHER 'CTR');
```

Database encryption implies using [storage version](#explicit-storage-versions) 1.4.0 or later.

> DuckDB's encryption does not yet meet the official [NIST requirements](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines).
> Please follow issue [`#20162` “Store and verify tag for canary encryption”](https://github.com/duckdb/duckdb/issues/20162) to track our progress towards NIST-compliance.

### Options

Zero or more copy options may be provided within parentheses following the `ATTACH` statement. Parameter values can be passed in with or without wrapping in single quotes. Arbitrary expressions may be used for parameter values.

| Name                | Description                                                                                                                 | Type      | Default value |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------- | ------------- |
| `ACCESS_MODE`       | Access mode of the database (`AUTOMATIC`, `READ_ONLY`, or `READ_WRITE`).                                                    | `VARCHAR` | `automatic`   |
| `COMPRESS`          | Whether the database is compressed. Only applicable for in-memory databases.                                                | `VARCHAR` | `false`       |
| `TYPE`              | The file type (`DUCKDB` or `SQLITE`), or deduced from the input string literal (MySQL, PostgreSQL).                         | `VARCHAR` | `DUCKDB`      |
| `BLOCK_SIZE`        | The block size of a new database file. Must be a power of two and within [16384, 262144]. Cannot be set for existing files. | `UBIGINT` | `262144`      |
| `ROW_GROUP_SIZE`    | The row group size of a new database file.                                                                                  | `UBIGINT` | `122880`      |
| `STORAGE_VERSION`   | The version of the storage used.                                                                                            | `VARCHAR` | `v1.0.0`      |
| `ENCRYPTION_KEY`    | The encryption key used for encrypting the database.                                                                        | `VARCHAR` | -             |
| `ENCRYPTION_CIPHER` | The encryption cipher used for encrypting the database (`CBC`, `CTR` or `GCM`).                                             | `VARCHAR` | -             |

## `DETACH`

The `DETACH` statement allows previously attached database files to be closed and detached, releasing any locks held on the database file.

Note that it is not possible to detach from the default database: if you would like to do so, issue the [`USE` statement]({% link docs/preview/sql/statements/use.md %}) to change the default database to another one. For example, if you are connected to a persistent database, you may change to an in-memory database by issuing:

```sql
ATTACH ':memory:' AS memory_db;
USE memory_db;
```

> Warning Closing the connection, e.g., invoking the [`close()` function in Python]({% link docs/preview/clients/python/dbapi.md %}#connection), does not release the locks held on the database files as the file handles are held by the main DuckDB instance (in Python's case, the `duckdb` module).

### `DETACH` Syntax

<div id="rrdiagram2"></div>

## Name Qualification

The fully qualified name of catalog objects contains the _catalog_, the _schema_ and the _name_ of the object. For example:

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

Note that often the fully qualified name is not required. When a name is not fully qualified, the system looks for which entries to reference using the _catalog search path_. The default catalog search path includes the system catalog, the temporary catalog and the initially attached database together with the `main` schema.

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

When providing only a single qualification, the system can interpret this as _either_ a catalog _or_ a schema, as long as there are no conflicts. For example:

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

When running queries on multiple databases, the system opens separate transactions per database. The transactions are started _lazily_ by default – when a given database is referenced for the first time in a query, a transaction for that database will be started. `SET immediate_transaction_mode = true` can be toggled to change this behavior to eagerly start transactions in all attached databases instead.

While multiple transactions can be active at a time – the system only supports _writing_ to a single attached database in a single transaction. If you try to write to multiple attached databases in a single transaction the following error will be thrown:

```console
Attempting to write to database "db2" in a transaction that has already modified database "db1" -
a single transaction can only write to a single attached database.
```

The reason for this restriction is that the system does not maintain atomicity for transactions across attached databases. Transactions are only atomic _within_ each database file. By restricting the global transaction to write to only a single database file the atomicity guarantees are maintained.
