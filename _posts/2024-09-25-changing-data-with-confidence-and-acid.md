---
layout: post
title: "Changing Data with Confidence and ACID"
author: "Hannes Mühleisen and Mark Raasveldt"
thumb: "/images/blog/thumbs/acid.svg"
image: "/images/blog/thumbs/acid.png"
excerpt: "Transactions are key features in database management systems and are also beneficial for data analysis workloads. DuckDB supports fully ACID transactions, confirmed by the TPC-H benchmark's test suite."
tags: ["using DuckDB"]
---

The great quote “Everything changes and nothing stays the same” from [Heraclitus, according to Socrates, according to Plato](https://latin.stackexchange.com/a/9473) is not very controversial: change is as old as the universe. Yet somehow, when dealing with data, we often consider change as merely an afterthought.

Static datasets are split-second snapshots of whatever the world looked like at one moment. But very quickly, the world moves on, and the dataset needs to catch up to remain useful. In the world of tables, new rows can be added, old rows may be deleted and sometimes rows have to be changed to reflect a new situation. Often, changes are interconnected. A row in a table that maps orders to customers is not very useful without the corresponding entry in the `orders` table. Most, if not all, datasets eventually get changed. As a data management system, managing change is thus not optional. However, managing changes properly is difficult.

Early data management systems researchers invented a concept called “transactions”, the notions of which were [first formalized](https://dl.acm.org/doi/abs/10.5555/48751.48761) [in the 1980s](https://dl.acm.org/doi/10.1145/289.291). In essence, transactionality and the well-known ACID principles describe a set of guarantees that a data management system has to provide in order to be considered safe. ACID is an acronym that stands for Atomicity, Consistency, Isolation and Durability.

The ACID principles are not a theoretical exercise. Much like the rules governing airplanes or trains, they have been “written in blood” – they are hard-won lessons from decades of data management practice. It is very hard for an application to reason correctly when dealing with non-ACID systems. The end result of such problems is often corrupted data or data that no longer reflects reality accurately. For example, rows can be duplicated or missing.

DuckDB provides full ACID guarantees by default without additional configuration. In this blog post, we will describe in detail what that means together with concrete examples, and show how you can take advantage of this functionality.

### Atomicity

**Atomicity** means that *either all changes in a set of updates happen or none of them happen*. Consider the example below, where we insert two rows in two separate tables. The inserts themselves are separate statements, but they can be made atomic by wrapping them in a transaction:

```sql
CREATE TABLE customer (id INTEGER, name VARCHAR);
CREATE TABLE orders (customer_id INTEGER, item VARCHAR);

BEGIN TRANSACTION;
INSERT INTO customer VALUES (42, 'DuckDB Labs');
INSERT INTO orders VALUES (42, 'stale bread');
COMMIT;

SELECT * FROM orders;
```

```text
┌─────────────┬─────────────┐
│ customer_id │    item     │
│    int32    │   varchar   │
├─────────────┼─────────────┤
│          42 │ stale bread │
└─────────────┴─────────────┘
```

By wrapping the changes in a transaction, we can be sure that *either both rows are written, or none of them are written*. The `BEGIN TRANSACTION` statement signifies all following statements belong to that transaction. The `COMMIT` signifies the end of the transaction – and will persist the changes to disk.

It is also possible to undo a set of changes by issuing a `ROLLBACK` at the end of a transaction. This will ensure that none of the changes made in the transaction are persisted.

```sql
BEGIN TRANSACTION;
INSERT INTO orders VALUES (42, 'iceberg lettuce');
INSERT INTO orders VALUES (42, 'dried worms');
ROLLBACK;
SELECT * FROM orders;
```

```text
┌─────────────┬─────────────┐
│ customer_id │    item     │
│    int32    │   varchar   │
├─────────────┼─────────────┤
│          42 │ stale bread │
└─────────────┴─────────────┘
```

As we can see, the two new rows have not been inserted permanently.

Atomicity is great to have because it allows the application to move the database from one consistent state to another consistent state without ever having to worry about intermediate states being visible to an application.

We should note that queries by default run in the so-called “auto-commit” mode, where each query will automatically be run in its own transaction. That said, even for these single-statement queries, transactions are very useful. For example, when bulk loading data into a table using an `INSERT` or `COPY` command, either _all_ of the data is loaded, or _none_ of the data is loaded. The system will not partially load a CSV file into a table.

We should also note that in DuckDB *schema changes are also transactional*. This means that you can create or delete tables, as well as alter the schema of a table, all within the safety of a transaction. It also means that you can undo any of these operations by issuing a `ROLLBACK`.

### Consistency

**Consistency** means that all of [the constraints that are defined in the database]({% link docs/sql/constraints.md %}) must always hold, both before and after a transaction. The constraints can never be violated. Examples of constraints are `PRIMARY KEY` or `FOREIGN KEY` constraints.

```sql
CREATE TABLE customer (id INTEGER, name VARCHAR, PRIMARY KEY (id));

INSERT INTO customer VALUES (42, 'DuckDB Labs');
INSERT INTO customer VALUES (42, 'Wilbur the Duck');
```

In the example above, the `customer` table requires the `id` column to be unique for all entries, otherwise multiple customers would be associated with the same orders. We can enforce this constraint by defining a so-called `PRIMARY KEY` on that column. When we insert two entries with the same id, the consistency check fails, and we get an error message:

```console
Constraint Error: Duplicate key "id: 42" violates primary key
constraint. (...)
```

Having these kinds of constraints in place is a great way to make sure data *remains* consistent even after many updates have taken place.

### Isolation

**Isolation** means that concurrent transactions are isolated from one another. A database can have many clients interacting with it *at the same time,* causing many transactions to happen all at once. An easy way of isolating these transactions is to execute them one after another. However, that would be prohibitively slow. Thousands of requests might have to wait for one particularly slow one.

To avoid this problem, transactions are typically executed *interleaved*. However, as those transactions change data, one must ensure that each transaction is logically *isolated* – it only ever sees a consistent state of the database and can – for example – never read data from a transaction that has not yet committed.

DuckDB does not have connections in the typical sense – as it is not a client/server database that allows separate applications to connect to it. However, DuckDB has [full multi-client support]({% link docs/connect/concurrency.md %}) within a single application. The user can create multiple clients that all connect to the same DuckDB instance. The transactions can be run concurrently and they are isolated using [Snapshot Isolation](https://jepsen.io/consistency/models/snapshot-isolation).

The way that multiple connections are created differs per client. Below is an example where we showcase the transactionality of the system using the Python client.

```python
import duckdb

con1 = duckdb.connect(":memory:mydb")
con1.sql("CREATE TABLE customer (id INTEGER, name VARCHAR)")

con1.sql("INSERT INTO customer VALUES (42, 'DuckDB Labs')")

con1.begin()
con1.sql("INSERT INTO customer VALUES (43, 'Wilbur the Duck')")
# no commit!

# start a new connection
con2 = duckdb.connect(":memory:mydb")
con2.sql("SELECT name FROM customer").show()

# ┌─────────────┐
# │    name     │
# │   varchar   │
# ├─────────────┤
# │ DuckDB Labs │
# └─────────────┘

# commit from the first connection
con1.commit()

# now the changes are visible
con2.sql("SELECT name FROM customer").show()

# ┌─────────────────┐
# │      name       │
# │     varchar     │
# ├─────────────────┤
# │ DuckDB Labs     │
# │ Wilbur the Duck │
# └─────────────────┘
```

As you can see, we have two connections to the same database, and the first connection inserts the `Wilbur the Duck` customer but *does not yet commit the change*. Meanwhile, the second connection reads from the customer table. The result does not yet show the new entry, because the two transactions are isolated from each other with regards to uncommitted changes. After the first connection commits, the second connection can read its changes.

### Durability

Finally, **durability** is the behavior of a system under failure. This is important as a process might crash or power to a computer may be lost. A database system now needs to ensure that _all committed transactions_ are durable, meaning their effects will be visible after restarting the database. Transactions that have not yet completed cannot leave any visible traces behind. Databases typically guarantee this property by keeping close tabs on the various caches, for example by using `fsync` to force changes to disk as transactions complete. Skipping the `fsync` is a common “optimization” that endangers durability.

Here is an example, again using Python:

```python
import duckdb
import os
import signal

con = duckdb.connect("mydb.duckdb")
con.sql("CREATE TABLE customer (id INTEGER, name VARCHAR)")
con.sql("INSERT INTO customer VALUES (42, 'DuckDB Labs')")

# begin a transaction
con.begin()
con.sql("INSERT INTO customer VALUES (43, 'Wilbur the Duck')")
# no commit!

os.kill(os.getpid(), signal.SIGKILL)
```

After restarting, we can check the `customer` table:

```python
import duckdb

con = duckdb.connect("mydb.duckdb")
con.sql("SELECT name FROM customer").show()
```

```text
┌─────────────┐
│    name     │
│   varchar   │
├─────────────┤
│ DuckDB Labs │
└─────────────┘
```

In this example, we first create the customer table in the database file `mydb.duckdb`. We then insert a single row with DuckDB Labs as a first transaction. Then, we begin but *do not commit* a second transaction that adds the `Wilbur the Duck` entry. If we then kill the process and with it the database, we can see that upon restart only the `DuckDB Labs` entry has survived. This is because the second transaction was not committed and hence not subject to durability. Of course, this gets more complicated when non-clean exits such as operating system crashes have to be considered. DuckDB also guarantees durability in those circumstances, some more on this below.

## Why ACID in OLAP?

There are two main classes of data management systems, transactional systems (OLTP) and analytical systems (OLAP). As the name implies, transactional systems are far more concerned with guaranteeing the ACID properties than analytical ones. Systems like the venerable PostgreSQL deservedly pride themselves on doing the “right thing” with regard to providing transactional guarantees by default. Even NoSQL transactional systems such as MongoDB that swore off guaranteeing the ACID principles “for performance” early on had to eventually [“roll back” to offering ACID guarantees](https://www.mongodb.com/resources/basics/databases/acid-transactions) with [one or two hurdles along the way](https://jepsen.io/analyses/mongodb-4.2.6).

Analytical systems such as DuckDB – in principle – have less of a imperative to provide strong transactional guarantees. They are often not the so-called “system of record”, which is the data management system that is considered the source truth. In fact, DuckDB offers various connectors to load data from systems of record, like the [PostgreSQL scanner]({% link docs/extensions/postgres.md %}). If an OLAP database would become corrupted, it is often possible to recover from that source of truth. Of course, that first requires that users notice that something has gone wrong, which is not always simple to detect. For example, a common mistake is ingesting data from the same CSV file twice into a database because the first attempt went wrong at some point. This can lead to duplicate rows causing incorrect aggregate results. ACID prevents these kinds of problems. ACID properties enable  useful functionality in OLAP systems. For example:

**Concurrent Ingestion and Reporting.** As change is continuous, we often have data ingestion streams adding new data to a database system. In analytical systems, it is common to have a single connection append new data to a database, while other connections read from the database in order to e.g., generate graphs and reports. If these connections are isolated, then the generated graphs and aggregates will always be executed over a complete and consistent snapshot of the database, ensuring that the generated graphs and aggregates are correct.

**Rolling Back Incorrect Transformations.** When analyzing data, a common pattern is loading data from data sets stored in flat files followed by performing a number of transformations on that data. For example, we might load a data set from a CSV file, followed by cleaning up `NULL` values and then deleting incomplete rows. If we make an incorrect transformation, it is possible we accidentally delete too many rows.

This is not the end of the world, as we can recover by re-reading from the original CSV files. However, we can save ourselves a lot of time by wrapping the transformations in a transaction and rolling back when something goes wrong. For example:

```sql
CREATE TABLE people AS SELECT * FROM 'people.csv';

BEGIN TRANSACTION;
UPDATE people SET age = NULL WHERE age = -99;
-- oops, we deleted all rows!
DELETE FROM people WHERE name <> 'non-existent name';
-- we can recover our original table by rolling back the delete
ROLLBACK;
```

**SQL Assertions.** When a (non-syntax) error occurs in a transaction, the transaction is automatically aborted, and the changes cannot be committed. We can use this property of transactions to add assertions to our transactions. When one of these assertions is triggered, an error is raised, and the transaction cannot be committed. We can use the `error` function to define our own `assert` macro:

```sql
CREATE MACRO assert(condition, message) AS
    CASE WHEN NOT condition THEN error(message) END;
```

We can then use this `assert` macro to assert that the `people` table is not empty:

```sql
CREATE TABLE people AS SELECT * FROM 'people.csv';

BEGIN TRANSACTION;
UPDATE people SET age = NULL WHERE age = -99;
-- oops, we deleted all rows!
DELETE FROM people WHERE name <> 'non-existent name';
SELECT assert(
           (SELECT count(*) FROM people) > 0,
           'People should not be empty'
       );
COMMIT;
```

When the assertion triggers, the transaction is automatically aborted, and the changes are rolled back.

## Full TPC-H Benchmark Implementation

The [Transaction Processing Performance Council (TPC)](https://www.tpc.org/tpch/) is an industry association of data management systems and hardware vendors. TPC publishes database benchmark specifications and oversees auditing of benchmark results, which it then publishes on its website. There are various benchmarks aimed at different use cases. The [TPC-H decision support benchmark](https://www.tpc.org/tpch/) is specifically aimed at analytical query processing on large volumes of data. Its famous 22 SQL queries and data generator specifics have been thourougly analyzed by both database vendors and [academics](https://homepages.cwi.nl/~boncz/snb-challenge/chokepoints-tpctc.pdf) ad nauseam.

It is less well known that the official TPC-H benchmark includes *data modification transactions* that require ACID compliance, which is not too-surprising given the name of the organization. For one-off performance shoot-outs, the updates are typically ignored and only the run-times of the 22 queries on a static dataset are reported. Such results are purely informational and cannot be audited or formally published by the TPC. But as we have argued above, change is inevitable, so let's perform the TPC-H experiments *with updates* with DuckDB.

TPC-H generates data for a fictional company selling things. The largest tables are `orders` and `lineitem`, which contains elements of each order. The benchmark can generate data of different sizes, the size is controlled by a so-called “scale factor” (SF). The specification defines two “refresh functions”, that modify the database. The first refresh function will add `SF * 1500` new rows into the `orders` table, and randomly between 1 and 7 new entries for each order into the `lineitem` table. The second refresh function will delete `SF * 1500` entries from the `orders` table along with the associated `lineitem` entries. The benchmark data generator `dbgen` can generate an arbitrary amount of refresh function CSV files with new entries for `orders` and `lineitem` along with rows to be deleted.

### Metrics

TPC-H's main benchmark metric is combined from both a “power” and a “throughput” test result.

The power test will run the first refresh function and time it, then run the 22 queries, then run the second refresh function, and calculate the geometric mean of all timings. With a scale factor of 100 and DuckDB 1.1.1 on a MacBook Pro with an M3 Max CPU and 64 GB of RAM, we get a *Power@Size value of 650&nbsp;536*.

The throughput test will run a number of concurrent query “streams” that execute the 22 benchmark queries in shuffled order in parallel. In addition, a single refresh stream will run both refresh functions a number of times. The number of query streams and refresh sets is derived from the scale factor. For SF100, there are 5 query streams and 10 refresh sets. For our experiment, we get a *Throughput@Size of 452&nbsp;571*. Results are hard to compare, but the result does not look too shabby when compared with the [official result list](https://www.tpc.org/tpch/results/tpch_results5.asp?print=false&orderby=tpm&sortby=desc&version=3%).

### ACID Tests

Section 3 of the TPC-H benchmark specification discusses the ACID properties in detail. The specification defines a set of tests to stress the ACID guarantees of a data management system. The spec duly notes that no test can prove that the ACID properties are fully supported, passing them is a “necessary but not sufficient condition” of compliance.  Below, we will give an overview of what is tested.

The tests specify an “ACID Transaction”, which modifies the `lineitem` and `orders` tables in such a way that an invariant holds: the `orders` table contains a total sum of all the prices of all the lineitems that belong to this order. The transaction picks a random order, and modifies the last lineitem to have a new price. It then re-calculates the order total price and updates the `orders` table with that. Finally, the transaction inserts information about which row was updated when and the price delta used in a `history` table.

To test *atomicity*, the ACID transaction is ran for a random order and then committed. It is verified that the database has been changed accordingly with the specified values. The test is repeated but this time the transaction is aborted. It is verified that the database has not been changed.

For *consistency*, a number of threads run the ACID transaction in parallel 100 times on random orders. Before and after the test, a consistency condition is checked, which essentially makes sure that the sum of all lineitem prices for an order is consistent with the sum in the order.

To test *isolation*, one thread will run the transaction, but not commit or rollback yet. Another connection will make sure the changes are not visible to it. Another set of tests will have two threads running transactions on the same order, and ensure that one of them is aborted by the system due to the conflict.

Finally, to test *durability*, a number of threads run the ACID transaction and log the results. They are allowed to complete at least 100 transactions each. Then, a failure is caused, in our case, we simply killed the process (using `SIGKILL`). Then, the database system is allowed to recover the committed changes from the [write-ahead log](https://en.wikipedia.org/wiki/Write-ahead_logging). The log is checked to ensure that there are no log entries that are not reflected in the `history` table and there are no history entries that don't have log entries, minus very few that might have been lost in flight (i.e., persisted by the database but not yet logged by the benchmark driver). Finally, the consistency is checked again.

**We're happy to report that DuckDB passed all tests.**

Our scripts to run the benchmark are [available on GitHub](https://github.com/hannes/duckdb-tpch-power-test). We are planning to perform a formal audit of our results in the future. We will update this post when that happens.

## Conclusion

Change in datasets is inevitable, and data management systems need to be able to safely manage change. DuckDB supports strong ACID guarantees that allow for safe and concurrent data modification. We have run extensive experiments with TPC-H's transactional validation tests and found that they pass.
