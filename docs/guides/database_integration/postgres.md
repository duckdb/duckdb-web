---
layout: docu
title: PostgreSQL Import
redirect_from:
  - /docs/guides/import/query_postgres
---

To run a query directly on a running PostgreSQL database, the [`postgres` extension](../../extensions/postgres_scanner) is required.

## Installation and Loading

The extension can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL postgres;
```

To load the `postgres` extension for usage, use the `LOAD` SQL command:

```sql
LOAD postgres;
```

## Usage

After the `postgres` extension is installed, tables can be queried from PostgreSQL using the `postgres_scan` function:

```sql
-- scan the table "mytable" from the schema "public" in the database "mydb"
SELECT * FROM postgres_scan('host=localhost port=5432 dbname=mydb', 'public', 'mytable');
```

The first parameter to the `postgres_scan` function is the [PostgreSQL connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING), a list of connection arguments provided in `{key}={value}` format. Below is a list of valid arguments.

<div class="narrow_table"></div>


|    Name    |             Description              |    Default     |
|------------|--------------------------------------|----------------|
| `host`     | Name of host to connect to           | `localhost`    |
| `hostaddr` | Host IP address                      | `localhost`    |
| `port`     | Port number                          | `5432`         |
| `user`     | Postgres user name                   | [OS user name] |
| `password` | Postgres password                    |                |
| `dbname`   | Database name                        | [user]         |
| `passfile` | Name of file passwords are stored in | `~/.pgpass`    |

Alternatively, the entire database can be attached using the `ATTACH` command. This allows you to query all tables stored within the PostgreSQL database as if it was a regular database.

```sql
-- Attach the Postgres database using the given connection string
ATTACH 'host=localhost port=5432 dbname=mydb' AS test (TYPE postgres);
-- The table "tbl_name" can now be queried as if it is a regular table
SELECT * FROM test.tbl_name;
-- Switch the active database to "test"
USE test;
-- List all tables in the file
SHOW TABLES;
```

For more information see the [PostgreSQL extension documentation](../../extensions/postgres).
