---
layout: docu
title: PostgreSQL Extension
github_repository: https://github.com/duckdb/duckdb-postgres
redirect_from:
  - /docs/extensions/postgres_scanner
  - /docs/extensions/postgres_scanner/
  - /docs/extensions/postgresql
  - /docs/extensions/postgresql/
---

The `postgres` extension allows DuckDB to directly read and write data from a running PostgreSQL database instance. The data can be queried directly from the underlying PostgreSQL database. Data can be loaded from PostgreSQL tables into DuckDB tables, or vice versa. See the [official announcement]({% post_url 2022-09-30-postgres-scanner %}) for implementation details and background.

## Installing and Loading

The `postgres` extension will be transparently [autoloaded]({% link docs/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL postgres;
LOAD postgres;
```

## Connecting

To make a PostgreSQL database accessible to DuckDB, use the `ATTACH` command with the `POSTGRES` or `POSTGRES_SCANNER` type.

To connect to the `public` schema of the PostgreSQL instance running on localhost in read-write mode, run:

```sql
ATTACH '' AS postgres_db (TYPE POSTGRES);
```

To connect to the PostgreSQL instance with the given parameters in read-only mode, run:

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE POSTGRES, READ_ONLY);
```

By default, all schemas are attached. When working with large instances, it can be useful to only attach a specific schema. This can be accomplished using the `SCHEMA` command.

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE POSTGRES, SCHEMA 'public');
```

### Configuration

The `ATTACH` command takes as input either a [`libpq` connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
or a [PostgreSQL URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS).

Below are some example connection strings and commonly used parameters. A full list of available parameters can be found in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

```text
dbname=postgresscanner
host=localhost port=5432 dbname=mydb connect_timeout=10
```

| Name       | Description                          | Default      |
| ---------- | ------------------------------------ | ------------ |
| `dbname`   | Database name                        | [user]       |
| `host`     | Name of host to connect to           | `localhost`  |
| `hostaddr` | Host IP address                      | `localhost`  |
| `passfile` | Name of file passwords are stored in | `~/.pgpass`  |
| `password` | PostgreSQL password                  | (empty)      |
| `port`     | Port number                          | `5432`       |
| `user`     | PostgreSQL user name                 | current user |

An example URI is `postgresql://username@hostname/dbname`.

### Configuring via Secrets

PostgreSQL connection information can also be specified with [secrets](/docs/configuration/secrets_manager). The following syntax can be used to create a secret.

```sql
CREATE SECRET (
    TYPE POSTGRES,
    HOST '127.0.0.1',
    PORT 5432,
    DATABASE postgres,
    USER 'postgres',
    PASSWORD ''
);
```

The information from the secret will be used when `ATTACH` is called. We can leave the Postgres connection string empty to use all of the information stored in the secret.

```sql
ATTACH '' AS postgres_db (TYPE POSTGRES);
```

We can use the Postgres connection string to override individual options. For example, to connect to a different database while still using the same credentials, we can override only the database name in the following manner.

```sql
ATTACH 'dbname=my_other_db' AS postgres_db (TYPE POSTGRES);
```

By default, created secrets are temporary. Secrets can be persisted using the [`CREATE PERSISTENT SECRET` command]({% link docs/configuration/secrets_manager.md %}#persistent-secrets). Persistent secrets can be used across sessions.

#### Managing Multiple Secrets

Named secrets can be used to manage connections to multiple Postgres database instances. Secrets can be given a name upon creation.

```sql
CREATE SECRET postgres_secret_one (
    TYPE POSTGRES,
    HOST '127.0.0.1',
    PORT 5432,
    DATABASE postgres,
    USER 'postgres',
    PASSWORD ''
);
```

The secret can then be explicitly referenced using the `SECRET` parameter in the `ATTACH`.

```sql
ATTACH '' AS postgres_db_one (TYPE POSTGRES, SECRET postgres_secret_one);
```

### Configuring via Environment Variables

PostgreSQL connection information can also be specified with [environment variables](https://www.postgresql.org/docs/current/libpq-envars.html).
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
ATTACH '' AS p (TYPE POSTGRES);
```

## Usage

The tables in the PostgreSQL database can be read as if they were normal DuckDB tables, but the underlying data is read directly from PostgreSQL at query time.

```sql
SHOW ALL TABLES;
```

<div class="monospace_table"></div>

| name  |
| ----- |
| uuids |

```sql
SELECT * FROM uuids;
```

<div class="monospace_table"></div>

| u                                    |
| ------------------------------------ |
| 6d3d2541-710b-4bde-b3af-4711738636bf |
| NULL                                 |
| 00000000-0000-0000-0000-000000000001 |
| ffffffff-ffff-ffff-ffff-ffffffffffff |

It might be desirable to create a copy of the PostgreSQL databases in DuckDB to prevent the system from re-reading the tables from PostgreSQL continuously, particularly for large tables.

Data can be copied over from PostgreSQL to DuckDB using standard SQL, for example:

```sql
CREATE TABLE duckdb_table AS FROM postgres_db.postgres_tbl;
```

## Writing Data to PostgreSQL

In addition to reading data from PostgreSQL, the extension allows you to create tables, ingest data into PostgreSQL and make other modifications to a PostgreSQL database using standard SQL queries.

This allows you to use DuckDB to, for example, export data that is stored in a PostgreSQL database to Parquet, or read data from a Parquet file into PostgreSQL.

Below is a brief example of how to create a new table in PostgreSQL and load data into it.

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE POSTGRES);
CREATE TABLE postgres_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO postgres_db.tbl VALUES (42, 'DuckDB');
```

Many operations on PostgreSQL tables are supported. All these operations directly modify the PostgreSQL database, and the result of subsequent operations can then be read using PostgreSQL.
Note that if modifications are not desired, `ATTACH` can be run with the `READ_ONLY` property which prevents making modifications to the underlying database. For example:

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE POSTGRES, READ_ONLY);
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

|   id | name   |
| ---: | ------ |
|   42 | DuckDB |

### `COPY`

You can copy tables back and forth between PostgreSQL and DuckDB:

```sql
COPY postgres_db.tbl TO 'data.parquet';
COPY postgres_db.tbl FROM 'data.parquet';
```

These copies use [PostgreSQL binary wire encoding](https://www.postgresql.org/docs/current/sql-copy.html).
DuckDB can also write data using this encoding to a file which you can then load into PostgreSQL using a client of your choosing if you would like to do your own connection management:

```sql
COPY 'data.parquet' TO 'pg.bin' WITH (FORMAT POSTGRES_BINARY);
```

The file produced will be the equivalent of copying the file to PostgreSQL using DuckDB and then dumping it from PostgreSQL using `psql` or another client:

DuckDB:

```sql
COPY postgres_db.tbl FROM 'data.parquet';
```

PostgreSQL:

```sql
\copy tbl TO 'data.bin' WITH (FORMAT BINARY);
```

You may also create a full copy of the database using the [`COPY FROM DATABASE` statement]({% link docs/sql/statements/copy.md %}#copy-from-database--to):

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
CREATE TABLE postgres_db.s1.integers (i INTEGER);
INSERT INTO postgres_db.s1.integers VALUES (42);
SELECT * FROM postgres_db.s1.integers;
```

|    i |
| ---: |
|   42 |

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

|    i |
| ---: |
|   42 |

```sql
ROLLBACK;
SELECT * FROM postgres_db.tmp;
```

This returns an empty table.

## Running SQL Queries in PostgreSQL

### The `postgres_query` Table Function

The `postgres_query` table function allows you to run arbitrary read queries within an attached database. `postgres_query` takes the name of the attached PostgreSQL database to execute the query in, as well as the SQL query to execute. The result of the query is returned. Single-quote strings are escaped by repeating the single quote twice.

```sql
postgres_query(attached_database::VARCHAR, query::VARCHAR)
```

For example:

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE POSTGRES);
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

| brand        | model      | color |
| ------------ | ---------- | ----- |
| Ferrari      | Testarossa | red   |
| Aston Martin | DB2        | blue  |
| Bentley      | Mulsanne   | gray  |

### The `postgres_execute` Function

The `postgres_execute` function allows running arbitrary queries within PostgreSQL, including statements that update the schema and content of the database.

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE POSTGRES);
CALL postgres_execute('postgres_db', 'CREATE TABLE my_table (i INTEGER)');
```

## Settings

The extension exposes the following configuration parameters.

| Name                              | Description                                                                  | Default |
| --------------------------------- | ---------------------------------------------------------------------------- | ------- |
| `pg_array_as_varchar`             | Read PostgreSQL arrays as varchar - enables reading mixed dimensional arrays | `false` |
| `pg_connection_cache`             | Whether or not to use the connection cache                                   | `true`  |
| `pg_connection_limit`             | The maximum amount of concurrent PostgreSQL connections                      | `64`    |
| `pg_debug_show_queries`           | DEBUG SETTING: print all queries sent to PostgreSQL to stdout                | `false` |
| `pg_experimental_filter_pushdown` | Whether or not to use filter pushdown (currently experimental)               | `false` |
| `pg_pages_per_task`               | The amount of pages per task                                                 | `1000`  |
| `pg_use_binary_copy`              | Whether or not to use BINARY copy to read data                               | `true`  |
| `pg_null_byte_replacement`        | When writing NULL bytes to Postgres, replace them with the given character   | `NULL`  |
| `pg_use_ctid_scan`                | Whether or not to parallelize scanning using table ctids                     | `true`  |

## Schema Cache

To avoid having to continuously fetch schema data from PostgreSQL, DuckDB keeps schema information – such as the names of tables, their columns, etc. – cached. If changes are made to the schema through a different connection to the PostgreSQL instance, such as new columns being added to a table, the cached schema information might be outdated. In this case, the function `pg_clear_cache` can be executed to clear the internal caches.

```sql
CALL pg_clear_cache();
```

> Deprecated The old `postgres_attach` function is deprecated. It is recommended to switch over to the new `ATTACH` syntax.
