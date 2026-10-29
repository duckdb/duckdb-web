---
github_repository: https://github.com/duckdb/duckdb-postgres
layout: docu
redirect_from:
- /docs/extensions/postgres
- /docs/stable/extensions/postgres
- /docs/current/core_extensions/postgres
- /docs/stable/core_extensions/postgres
- /docs/stable/core_extensions/postgres/overview
- /docs/current/core_extensions/postgres/overview
- /docs/lts/core_extensions/postgres/overview
- /docs/preview/core_extensions/postgres/overview
title: PostgreSQL Extension
---

The `postgres` extension allows DuckDB to directly read and write data from a running PostgreSQL database instance. The data can be queried directly from the underlying PostgreSQL database. Data can be loaded from PostgreSQL tables into DuckDB tables, or vice versa. See the [official announcement]({% post_url 2022-09-30-postgres-scanner %}) for implementation details and background.

## Installing and Loading

The `postgres` extension will be transparently [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD postgres;
```

## Connecting

To make a PostgreSQL database accessible to DuckDB, use the [`ATTACH` command]({% link docs/2.0/sql/statements/attach.md %}) with the `postgres` or `postgres_scanner` type.

To connect to the `public` schema of the PostgreSQL instance running on localhost in read-write mode, run:

```sql
ATTACH '' AS postgres_db (TYPE postgres);
```

To connect to the PostgreSQL instance with the given parameters in read-only mode, run:

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, READ_ONLY);
```

By default, all schemas are attached. When working with large instances, it can be useful to only attach a specific schema. This can be accomplished using the `SCHEMA` command.

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, SCHEMA 'public');
```

The transaction isolation level can be set with the `ISOLATION_LEVEL` option. Supported values are `READ COMMITTED`, `REPEATABLE READ`, and `SERIALIZABLE`; the default is `REPEATABLE READ`.

```sql
ATTACH 'dbname=postgres user=postgres host=127.0.0.1' AS db (TYPE postgres, ISOLATION_LEVEL 'READ COMMITTED');
```

> Warning Avoid including credentials, such as a password, directly in the connection string. If a connection error occurs, the full connection string, including your credentials, may appear in the resulting error message. For better security, store credentials using [secrets]({% link docs/2.0/configuration/secrets_manager.md %}) instead, as described in [Configuring via Secrets](#configuring-via-secrets).

> Deprecated The old `postgres_attach` function was removed in DuckDB 2.0. Use the `ATTACH` statement instead.

### Configuration

The `ATTACH` command takes as input either a [`libpq` connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
or a [PostgreSQL URI](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS).

Below are some example connection strings and commonly used parameters. A full list of available parameters can be found in the [PostgreSQL documentation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

```text
dbname=postgresscanner
host=localhost port=5432 dbname=mydb connect_timeout=10
```

| Name       | Description                          | Default        |
| ---------- | ------------------------------------ | -------------- |
| `dbname`   | Database name                        | [user]         |
| `host`     | Name of host to connect to           | `localhost`    |
| `hostaddr` | Host IP address                      | `localhost`    |
| `passfile` | Name of file passwords are stored in | `~/.pgpass`    |
| `password` | PostgreSQL password                  | (empty)        |
| `port`     | Port number                          | `5432`         |
| `user`     | PostgreSQL user name                 | _current user_ |

An example URI is `postgresql://username@hostname/dbname`.

### Configuring via Secrets

PostgreSQL connection information can also be specified with [secrets]({% link docs/2.0/configuration/secrets_manager.md %}), see details on the [corresponding page]({% link docs/2.0/core_extensions/postgres/secrets.md %}).

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
ATTACH '' AS p (TYPE postgres);
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

In addition to reading data from PostgreSQL, the extension allows you to create tables, ingest data into PostgreSQL, and make other modifications to a PostgreSQL database using standard SQL queries.

This allows you to use DuckDB to, for example, export data that is stored in a PostgreSQL database to Parquet, or read data from a Parquet file into PostgreSQL.

Below is a brief example of how to create a new table in PostgreSQL and load data into it.

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
CREATE TABLE postgres_db.tbl (id INTEGER, name VARCHAR);
INSERT INTO postgres_db.tbl VALUES (42, 'DuckDB');
```

Many operations on PostgreSQL tables are supported. All these operations directly modify the PostgreSQL database, and the result of subsequent operations can then be read using PostgreSQL.
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
COPY 'data.parquet' TO 'pg.bin' WITH (FORMAT postgres_binary);
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

You may also create a full copy of the database using the [`COPY FROM DATABASE` statement]({% link docs/2.0/sql/statements/copy.md %}#copy-from-database--to):

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

| brand        | model      | color |
| ------------ | ---------- | ----- |
| Ferrari      | Testarossa | red   |
| Aston Martin | DB2        | blue  |
| Bentley      | Mulsanne   | gray  |

### The `postgres_execute` Function

The `postgres_execute` function allows running arbitrary queries within PostgreSQL, including statements that update the schema and content of the database.

```sql
ATTACH 'dbname=postgresscanner' AS postgres_db (TYPE postgres);
CALL postgres_execute('postgres_db', 'CREATE TABLE my_table (i INTEGER)');
```

### Routing a Session to PostgreSQL

> New As of DuckDB 2.0, you can route an entire session to an attached PostgreSQL database with the [`CONNECT` statement]({% link docs/2.0/sql/statements/connect.md %}). While connected, the remote pushdown optimizer ships queries directly to the PostgreSQL server instead of pulling tables over the wire, and `DISCONNECT` returns the session to the local database.

## Settings

The extension exposes the following configuration parameters.

| Name | Description | Default |
| --- | --- | --- |
| `pg_array_as_varchar` | Read PostgreSQL arrays as varchar - enables reading mixed dimensional arrays | `false` |
| `pg_connection_cache` | Deprecated: whether or not to use connection pooling. To disable pooling, use `SET pg_pool_max_connections = 0` instead (see [Connection Pool]({% link docs/2.0/core_extensions/postgres/connection_pool.md %})) | `true` |
| `pg_connection_limit` | Deprecated: the maximum amount of concurrent PostgreSQL connections. Use `pg_pool_max_connections` instead (see [Connection Pool]({% link docs/2.0/core_extensions/postgres/connection_pool.md %})) | depends on the number of CPU cores |
| `pg_debug_show_queries` | DEBUG SETTING: print all queries sent to PostgreSQL to stdout | `false` |
| `pg_enable_filter_pushdown` | Whether or not to use filter pushdown | `true` |
| `pg_idle_in_transaction_timeout_millis` | PostgreSQL `idle_in_transaction_session_timeout` in milliseconds to set on scan connections | `NULL` |
| `pg_null_byte_replacement` | When writing NULL bytes to PostgreSQL, replace them with the given character | `NULL` |
| `pg_numeric_as_varchar` | Read PostgreSQL `NUMERIC` values without precision and scale or with precision greater than 38 as `VARCHAR` instead of `DOUBLE` | `false` |
| `pg_numeric_nan_as_null` | Read PostgreSQL `NUMERIC` `NaN` values as `NULL` instead of throwing an error | `true` |
| `pg_oauth_token` | OAuth bearer token for PostgreSQL `OAUTHBEARER` authentication. Takes priority over the `PGOAUTHTOKEN` environment variable | `NULL` |
| `pg_pages_per_task` | The amount of pages per task | `1000` |
| `pg_query_mode` | Query mode used to read data, one of `'AUTO'`, `'COPY_BINARY'`, `'PLAIN_QUERY_BINARY'`, `'PLAIN_QUERY_TEXT'` | `AUTO` |
| `pg_statement_timeout_millis` | PostgreSQL statement timeout in milliseconds to set on scan connections | `NULL` |
| `pg_use_binary_copy` | Whether or not to use BINARY copy to read data | `true` |
| `pg_use_ctid_scan` | Whether or not to parallelize scanning using table ctids | `true` |
| `pg_use_information_schema_introspection` | Use the SQL-standard `information_schema` views instead of `pg_catalog` for schema discovery at `ATTACH` time. Useful for PostgreSQL-wire-compatible databases (e.g., Spanner, CockroachDB, Redshift) | `false` |
| `pg_use_text_protocol` | Whether or not to use the text protocol to read data. This is slower, but provides better compatibility with non-PostgreSQL systems | `false` |

The connection pool settings (`pg_pool_*`) are documented on the [Connection Pool page]({% link docs/2.0/core_extensions/postgres/connection_pool.md %}) and the schema cache settings (`pg_staleness_query`, `pg_staleness_query_enabled`) in the [Schema Cache](#schema-cache) section.

## Schema Cache

To avoid having to continuously fetch schema data from PostgreSQL, DuckDB keeps schema information – such as the names of tables, their columns, etc. – cached. If changes are made to the schema through a different connection to the PostgreSQL instance, such as new columns being added to a table, the cached schema information might be outdated. In this case, the function `postgres_clear_cache` can be executed to clear the internal caches.

```sql
CALL postgres_clear_cache();
```

In version 1.5.5 a support for automatic detection of schema changes was added using a "staleness query"
(contributed by Brandon Freeman in [duckdb/duckdb-postgres#514](https://github.com/duckdb/duckdb-postgres/pull/514)):

 - when `pg_staleness_query_enabled` option (`BOOLEAN`, default: enabled for PostgreSQL, disabled when `pg_use_information_schema_introspection` is set) is enabled, on every catalog access a query is run that
   checks Postgres' `pg_class.xmin` column value in every table and reloads the cache automatically, if a change is detected

 - for Postgres-wire-compatible databases a custom "staleness query" can be set using `pg_staleness_query` option.

## Working with hstore Columns

DuckDB will return data from [hstore](https://www.postgresql.org/docs/current/hstore.html) columns as `VARCHAR` of their text representation, like `key=>value, foo=>bar`.
You can use the [postgres_hstore_get]({% link docs/2.0/core_extensions/postgres/functions.md %}#postgres_hstore_get)
function to read the value for a given key, or [postgres_hstore_to_json]({% link docs/2.0/core_extensions/postgres/functions.md %}#postgres_hstore_to_json)
to convert the whole set of key/value pairs to JSON for further processing.

```sql
SELECT postgres_hstore_get('a=>b, c=>d', 'a');
-- b

SELECT postgres_hstore_get('a=>b, c=>d', 'missingkey');
-- NULL

SELECT postgres_hstore_to_json('a=>b, c=>d, e => null');
-- {"a": "b", "c": "d", e: null}
```
