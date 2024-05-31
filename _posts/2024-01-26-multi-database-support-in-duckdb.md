---
layout: post
title:  "Multi-Database Support in DuckDB"
author: Mark Raasveldt
thumb: "/images/blog/thumbs/240126.png"
excerpt: DuckDB can attach MySQL, Postgres, and SQLite databases in addition to databases stored in its own format. This allows data to be read into DuckDB and moved between these systems in a convenient manner.
---

<img src="/images/blog/duckdb-multidb-support.png"
     alt="DuckDB supports reading and writing to MySQL, Postgres, and SQLite"
     width=700
/>

In modern data analysis, data must often be combined from a wide variety of different sources. Data might sit in CSV files on your machine, in Parquet files in a data lake, or in an operational database. DuckDB has strong support for moving data between many different data sources. However, this support has previously been limited to reading data and writing data to files.

DuckDB supports advanced operations on its own native storage format – such as deleting rows, updating values, or altering the schema of a table. It supports all of these operations using ACID semantics. This guarantees that your database is always left in a sane state – operations are atomic and do not partially complete.

DuckDB now has a pluggable storage and transactional layer. This flexible layer allows new storage back-ends to be created by DuckDB extensions. These storage back-ends can support all database operations in the same way that DuckDB supports them, including inserting data and even modifying schemas.

The [MySQL](/docs/extensions/mysql), [Postgres](/docs/extensions/postgres), and [SQLite](/docs/extensions/sqlite) extensions implement this new pluggable storage and transactional layer, allowing DuckDB to connect to those systems and operate on them in the same way that it operates on its own native storage engine.

These extensions enable a number of useful features. For example, using these extensions you can:

* Export data from SQLite to JSON
* Read data from Parquet into Postgres
* Move data from MySQL to Postgres

... and much more.


## Attaching Databases

The [`ATTACH` statement](/docs/sql/statements/attach) can be used to attach a new database to the system. By default, a native DuckDB file will be attached. The `TYPE` parameter can be used to specify a different storage type. Alternatively, the `{type}:` prefix can be used.

For example, using the SQLite extension, we can open [a SQLite database file](https://github.com/duckdb/sqlite_scanner/raw/main/data/db/sakila.db) and query it as we would query a DuckDB database.

```sql
ATTACH 'sakila.db' AS sakila (TYPE sqlite);
SELECT title, release_year, length FROM sakila.film LIMIT 5;
```
```text
┌──────────────────┬──────────────┬────────┐
│      title       │ release_year │ length │
│     varchar      │   varchar    │ int64  │
├──────────────────┼──────────────┼────────┤
│ ACADEMY DINOSAUR │ 2006         │     86 │
│ ACE GOLDFINGER   │ 2006         │     48 │
│ ADAPTATION HOLES │ 2006         │     50 │
│ AFFAIR PREJUDICE │ 2006         │    117 │
│ AFRICAN EGG      │ 2006         │    130 │
└──────────────────┴──────────────┴────────┘
```

The `USE` command switches the main database.

```sql
USE sakila;
SELECT first_name, last_name FROM actor LIMIT 5;
```
```text
┌────────────┬──────────────┐
│ first_name │  last_name   │
│  varchar   │   varchar    │
├────────────┼──────────────┤
│ PENELOPE   │ GUINESS      │
│ NICK       │ WAHLBERG     │
│ ED         │ CHASE        │
│ JENNIFER   │ DAVIS        │
│ JOHNNY     │ LOLLOBRIGIDA │
└────────────┴──────────────┘
```

The SQLite database can be manipulated as if it were a native DuckDB database. For example, we can create a new table, populate it with values from a Parquet file, delete a few rows from the table and alter the schema of the table.

```sql
CREATE TABLE lineitem AS FROM 'lineitem.parquet' LIMIT 1000;
DELETE FROM lineitem WHERE l_returnflag = 'N';
ALTER TABLE lineitem DROP COLUMN l_comment;
```

The `duckdb_databases` table contains a list of all attached databases and their types.

```sql
SELECT database_name, path, type FROM duckdb_databases;
```
```text
┌───────────────┬───────────┬─────────┐
│ database_name │   path    │  type   │
│    varchar    │  varchar  │ varchar │
├───────────────┼───────────┼─────────┤
│ sakila        │ sakila.db │ sqlite  │
│ memory        │ NULL      │ duckdb  │
└───────────────┴───────────┴─────────┘
```

## Mix and Match

While attaching to different database types is useful – it becomes even more powerful when used in combination. For example, we can attach both a SQLite, MySQL and a Postgres database.

```sql
ATTACH 'sqlite:sakila.db' AS sqlite;
ATTACH 'postgres:dbname=postgresscanner' AS postgres;
ATTACH 'mysql:user=root database=mysqlscanner' AS mysql;
```

Now we can move data between these attached databases and query them together. Let's copy the `film` table to MySQL, and the `actor` table to Postgres:

```sql
CREATE TABLE mysql.film AS FROM sqlite.film;
CREATE TABLE postgres.actor AS FROM sqlite.actor;
```

We can now join tables from these three attached databases together. Let's find all of the actors that starred in `Ace Goldfinger`.

```sql
SELECT first_name, last_name
FROM mysql.film
JOIN sqlite.film_actor ON (film.film_id = film_actor.film_id)
JOIN postgres.actor ON (actor.actor_id = film_actor.actor_id)
WHERE title = 'ACE GOLDFINGER';
```
```text
┌────────────┬───────────┐
│ first_name │ last_name │
│  varchar   │  varchar  │
├────────────┼───────────┤
│ BOB        │ FAWCETT   │
│ MINNIE     │ ZELLWEGER │
│ SEAN       │ GUINESS   │
│ CHRIS      │ DEPP      │
└────────────┴───────────┘
```

Running `EXPLAIN` on the query shows how the data from the different engines is combined into the final query result.

```text
┌───────────────────────────┐                                                          
│         PROJECTION        │                                                          
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                                                          
│         first_name        │                                                          
│         last_name         │                                                          
└─────────────┬─────────────┘                                                          
┌─────────────┴─────────────┐                                                          
│         HASH_JOIN         │                                                          
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                                                          
│           INNER           │                                                          
│     film_id = film_id     ├───────────────────────────────────────────┐              
└─────────────┬─────────────┘                                           │              
┌─────────────┴─────────────┐                             ┌─────────────┴─────────────┐
│         HASH_JOIN         │                             │           FILTER          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           INNER           │                             │ (title = 'ACE GOLDFINGER')│
│    actor_id = actor_id    ├──────────────┐              │                           │
└─────────────┬─────────────┘              │              └─────────────┬─────────────┘
┌─────────────┴─────────────┐┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│        SQLITE_SCAN        ││       POSTGRES_SCAN       ││        MYSQL_SCAN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│    sakila.db:film_actor   ││           actor           ││            film           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          film_id          ││          actor_id         ││          film_id          │
│          actor_id         ││         first_name        ││           title           │
│                           ││         last_name         ││                           │
└───────────────────────────┘└───────────────────────────┘└───────────────────────────┘
```

## Transactions

All statements executed within DuckDB are executed within a transaction. If an explicit `BEGIN TRANSACTION` is not called, every statement will execute in its own transaction. This also applies to queries that are executed over other storage engines. These storage engines also support explicit `BEGIN`, `COMMIT` and `ROLLBACK` statements.

For example, we can begin a transaction within our attached `SQLite` database, make a change, and then roll it back. The original data will be restored.

```sql
BEGIN;
TRUNCATE film;
SELECT title, release_year, length FROM film;
```
```text
┌─────────┬──────────────┬────────┐
│  title  │ release_year │ length │
│ varchar │   varchar    │ int64  │
├─────────────────────────────────┤
│             0 rows              │
└─────────────────────────────────┘
```
```sql
ROLLBACK;
SELECT title, release_year, length FROM film LIMIT 5;
```
```text
┌──────────────────┬──────────────┬────────┐
│      title       │ release_year │ length │
│     varchar      │   varchar    │ int64  │
├──────────────────┼──────────────┼────────┤
│ ACADEMY DINOSAUR │ 2006         │     86 │
│ ACE GOLDFINGER   │ 2006         │     48 │
│ ADAPTATION HOLES │ 2006         │     50 │
│ AFFAIR PREJUDICE │ 2006         │    117 │
│ AFRICAN EGG      │ 2006         │    130 │
└──────────────────┴──────────────┴────────┘
```

### Multi-Database Transactions

Every storage engine has their own transactions that are stand-alone and managed by the storage engine itself. Opening a transaction in Postgres, for example, calls `BEGIN TRANSACTION` in the Postgres client. The transaction is managed by Postgres itself. Similarly, when the transaction is committed or rolled back, the storage engine handles this by itself.

Transactions are used both for **reading** and for **writing** data. For reading data, they are used to provide a consistent snapshot of the database. For writing, they are used to ensure all data in a transaction is packed together and written at the same time.

When executing a transaction that involves multiple attached databases we need to open multiple transactions: one per attached database that is used in the transaction. While this is not a problem when **reading** from the database, it becomes complicated when **writing**. In particular, when we want to `COMMIT` a transaction it is challenging to ensure that either (a) every database has successfully committed, or (b) every database has rolled back.

For that reason, it is currently not supported to **write** to multiple attached databases in a single transaction. Instead, an error is thrown when this is attempted:

```sql
BEGIN;
CREATE TABLE postgres.new_table(i INT);
CREATE TABLE mysql.new_table(i INT);
```
```text
Error: Attempting to write to database "mysql" in a transaction that has
already modified database "postgres" – a single transaction can only write
to a single attached database.
```

## Copying Data Between Databases

`CREATE TABLE AS`, `INSERT INTO` and `COPY` can be used to copy data between different attached databases. The dedicated [`COPY FROM DATABASE ... TO`](https://duckdb.org/docs/sql/statements/copy.html#copy-from-database--to) can be used to copy all data from one database to another. This includes all tables and views that are stored in the source database.

```sql
-- attach a Postgres database
ATTACH 'postgres:dbname=postgresscanner' AS postgres;
-- attach a DuckDB file
ATTACH 'database.db' AS ddb;
-- export all tables and views from the Postgres database to the DuckDB file
COPY FROM DATABASE postgres TO ddb;
```

Note that this statement is currently only available in the development build. It will be available in the next DuckDB release (v0.10).

## Directly Opening a Database

The explicit `ATTACH` statement is not required to connect to a different database type. When instantiating a DuckDB instance a connection can be made directly to a different database type using the `{type}:` prefix. For example, to connect to a SQLite file, use `sqlite:file.db`. To connect to a Postgres instance, use `postgres:dbname=postgresscanner`. This can be done in any client, including the CLI. For instance:

**CLI:**

```bash
duckdb sqlite:file.db
```

**Python:**

```python
import duckdb
con = duckdb.connect('sqlite:file.db')
```

This is equivalent to attaching the storage engine and running `USE` afterwards.

## Conclusion

DuckDB's pluggable storage engine architecture enables many use cases. By attaching multiple databases, data can be extracted in a transactionally safe manner for bulk ETL or ELT workloads, as well as for on-the-fly data virtualization workloads. These techniques also work well in combination, for example, by moving data in bulk on a regular cadence, while filling in the last few data points on the fly.

Pluggable storage engines also unlock new ways to handle concurrent writers in a data platform. Each separate process could write its output to a transactional database, and the results could be combined within DuckDB – all in a transactionally safe manner. Then, data analysis tasks can occur on the centralized DuckDB database for improved performance.

We look forward to hearing the many creative ways you are able to use this feature!

## Future Work

We intend to continue enhancing the performance and capabilities of the existing extensions. In addition, all of these features can be leveraged by the community to connect to other databases.
