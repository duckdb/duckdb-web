---
layout: docu
title: PostgreSQL Extension
github_repository: https://github.com/duckdb/postgres_scanner
redirect_from:
  - docs/extensions/postgres_scanner
  - docs/extensions/postgresql
---

The `postgres` extension allows DuckDB to directly read and write data from a running Postgres database instance. The data can be queried directly from the underlying Postgres database. Data can be loaded from Postgres tables into DuckDB tables, or vice versa.See the [official announcement](/2022/09/30/postgres-scanner) for implementation details and background.

## Installing and Loading

To install the `postgres` extension, run:

```sql
INSTALL postgres;
```

The extension is loaded automatically upon first use. If you prefer to load it manually, run:

```sql
LOAD postgres;
```

## Connecting

To make a PostgreSQL database accessible to DuckDB, use the `ATTACH` command:

```sql
-- connect to the "public" schema of the postgres instance running on localhost in read-write mode
ATTACH '' AS postgres_db (TYPE postgres);
```

```sql
-- connect to the Postgres instance with the given parameters in read-only mode
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, READ_ONLY);
```

### Configuration

The `ATTACH` command takes as input either a [`libpq` connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
or a [PostgreSQL URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS).

Below are some example connection strings and commonly used parameters. A full list of available parameters can be found [in the Postgres documentation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

```text
dbname=postgresscanner
host=localhost port=5432 dbname=mydb connect_timeout=10
```

|    Name    |             Description              |     Default      |
|------------|--------------------------------------|------------------|
| `dbname`   | Database name                        | [user]           |
| `host`     | Name of host to connect to           | `localhost`      |
| `hostaddr` | Host IP address                      | `localhost`      |
| `passfile` | Name of file passwords are stored in | `~/.pgpass`      |
| `password` | Postgres password                    | (empty)          |
| `port`     | Port number                          | `5432`           |
| `user`     | Postgres user name                   | current user     |

An example URI is `postgresql://username@hostname/dbname`.

### Configuring via Environment Variables

Postgres connection information can also be specified with [environment variables](https://www.postgresql.org/docs/current/libpq-envars.html).
This can be useful in a production environment where the connection information is managed externally
and passed in to the environment.

```bash
export PGPASSWORD="secret"
export PGHOST=localhost
export PGUSER=owner
export PGDATABASE=mydatabase
```

Then, to connect, start the `duckdb` process and run:

```sql
ATTACH '' AS p (TYPE postgres);
```

## Usage

The tables in the PostgreSQL database can be read as if they were normal DuckDB tables, but the underlying data is read directly from Postgres at query time.

```sql
SHOW TABLES;
```

| name  |
|-------|
| uuids |

```sql
SELECT * FROM uuids;
```

|                  u                   |
|--------------------------------------|
| 6d3d2541-710b-4bde-b3af-4711738636bf |
| NULL                                 |
| 00000000-0000-0000-0000-000000000001 |
| ffffffff-ffff-ffff-ffff-ffffffffffff |

It might be desirable to create a copy of the Postgres databases in DuckDB to prevent the system from re-reading the tables from Postgres continuously, particularly for large tables.

Data can be copied over from Postgres to DuckDB using standard SQL, for example:

```sql
CREATE TABLE duckdb_table AS FROM postgres_db.postgres_tbl;
```

## Writing Data to Postgres

In addition to reading data from Postgres, the extension allows you to create tables, ingest data into Postgres and make other modifications to a Postgres database using standard SQL queries.

This allows you to use DuckDB to, for example, export data that is stored in a Postgres database to Parquet, or read data from a Parquet file into Postgres.

Below is a brief example of how to create a new table in Postgres and load data into it.

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
CREATE TABLE postgres_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO postgres_db.tbl VALUES (42, 'DuckDB');
```

Many operations on Postgres tables are supported. All these operations directly modify the Postgres database, and the result of subsequent operations can then be read using Postgres.
Note that if modifications are not desired, `ATTACH` can be run with the `READ_ONLY` property which prevents making modifications to the underlying database. For example:

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres, READ_ONLY);
```

Below is a list of supported operations.

### `CREATE TABLE`

```sql
CREATE TABLE postgres_db.tbl (id INTEGER, name VARCHAR);
```

### `INSERT INTO`

```sql
INSERT INTO postgres_db.tbl VALUES (42, 'DuckDB');
```

### `SELECT`

```sql
SELECT * FROM postgres_db.tbl;
```

| id |  name  |
|---:|--------|
| 42 | DuckDB |

### `COPY`

You can copy tables back and forth between PostgreSQL and DuckDB:

```sql
COPY postgres_db.tbl TO 'data.parquet';
COPY postgres_db.tbl FROM 'data.parquet';
```

You may also create a full copy of the database using the [`COPY FROM DATABASE` statement](../sql/statements/copy#copy-from-database--to):

```sql
COPY FROM DATABASE postgres_db TO my_duckdb_db;
```

### `UPDATE`

```sql
UPDATE postgres_db.tbl
SET name = 'Woohoo'
WHERE id = 42;
```

### `DELETE`

```sql
DELETE FROM postgres_db.tbl
WHERE id = 42;
```

### `ALTER TABLE`

```sql
ALTER TABLE postgres_db.tbl
ADD COLUMN k INTEGER;
```

### `DROP TABLE`

```sql
DROP TABLE postgres_db.tbl;
```

### `CREATE VIEW`

```sql
CREATE VIEW postgres_db.v1 AS SELECT 42;
```

### `CREATE SCHEMA` / `DROP SCHEMA`

```sql
CREATE SCHEMA postgres_db.s1;
CREATE TABLE postgres_db.s1.integers (i INT);
INSERT INTO postgres_db.s1.integers VALUES (42);
SELECT * FROM postgres_db.s1.integers;
```

| i  |
|---:|
| 42 |

```sql
DROP SCHEMA postgres_db.s1;
```

## `DETACH`

```sql
DETACH postgres_db;
```

### Transactions

```sql
CREATE TABLE postgres_db.tmp (i INTEGER);
BEGIN;
INSERT INTO postgres_db.tmp VALUES (42);
SELECT * FROM postgres_db.tmp;
```

This returns:

| i  |
|---:|
| 42 |

```sql
ROLLBACK;
SELECT * FROM postgres_db.tmp;
```

This returns an empty table.

## Running SQL Queries in Postgres

### The `postgres_query` Table Function

The `postgres_query` table function allows you to run arbitrary read queries within an attached database. `postgres_query` takes the name of the attached Postgres database to execute the query in, as well as the SQL query to execute. The result of the query is returned. Single-quote strings are escaped by repeating the single quote twice.

```sql
postgres_query(attached_database::VARCHAR, query::VARCHAR)
```

For example:

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
SELECT * FROM postgres_query('postgres_db', 'SELECT * FROM cars LIMIT 3');
```

<!--
    CREATE TABLE cars (brand VARCHAR, model VARCHAR, color VARCHAR);
    INSERT INTO cars VALUES
      ('Ferrari', 'Testarossa', 'red'),
      ('Aston Martin', 'DB2', 'blue'),
      ('Bentley', 'Mulsanne', 'gray')
    ;
-->

|    brand     |   model    | color |
|--------------|------------|-------|
| Ferrari      | Testarossa | red   |
| Aston Martin | DB2        | blue  |
| Bentley      | Mulsanne   | gray  |

### The `postgres_execute` Function

The `postgres_execute` function allows running arbitrary queries within Postgres, including statements that update the schema and content of the database.

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
CALL postgres_execute('postgres_db', 'CREATE TABLE my_table (i INTEGER)');
```

> Warning This function is only available on DuckDB v0.10.1, using the latest Postgres extension.
> To upgrade your extension, run `FORCE INSTALL postgres;`.

## Settings

The extension exposes the following configuration parameters.

|               Name                |                                Description                                 |  Default  |
|-----------------------------------|----------------------------------------------------------------------------|-----------|
| `pg_debug_show_queries`           | DEBUG SETTING: print all queries sent to Postgres to stdout                | `false`   |
| `pg_connection_cache`             | Whether or not to use the connection cache                                 | `true`    |
| `pg_experimental_filter_pushdown` | Whether or not to use filter pushdown (currently experimental)             | `false`   |
| `pg_array_as_varchar`             | Read Postgres arrays as varchar - enables reading mixed dimensional arrays | `false`   |
| `pg_connection_limit`             | The maximum amount of concurrent Postgres connections                      | `64`      |
| `pg_pages_per_task`               | The amount of pages per task                                               | `1000`    |
| `pg_use_binary_copy`              | Whether or not to use BINARY copy to read data                             | `true`    |

## Schema Cache

To avoid having to continuously fetch schema data from Postgres, DuckDB keeps schema information - such as the names of tables, their columns, etc. - cached. If changes are made to the schema through a different connection to the Postgres instance, such as new columns being added to a table, the cached schema information might be outdated. In this case, the function `pg_clear_cache` can be executed to clear the internal caches.

```sql
CALL pg_clear_cache();
```

> Deprecated The old `postgres_attach` function is deprecated. It is recommended to switch over to the new `ATTACH` syntax.
