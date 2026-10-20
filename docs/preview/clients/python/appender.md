---
layout: docu
title: Appender
---

Use an appender to insert rows that your Python code produces. It collects rows and writes them together in one SQL statement; this is called flushing. The `with` block below flushes on successful exit:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE people (id INTEGER PRIMARY KEY, name VARCHAR)")

with con.appender("people") as appender:
    appender.append_row(1, "Mark")
    appender.append_rows([(2, "Hannes"), (3, "Gabor")])

print(con.sql("SELECT * FROM people ORDER BY id").fetchall())
```

```text
[(1, 'Mark'), (2, 'Hannes'), (3, 'Gabor')]
```

For data already in a DataFrame or Arrow table, `INSERT INTO people SELECT * FROM df` is faster than the appender. For pandas DataFrames, `con.append("people", df)` is also faster. See [Directly Accessing DataFrames and Arrow Objects]({% link docs/preview/clients/python/data_ingestion.md %}#directly-accessing-dataframes-and-arrow-objects).

Use `con.appender(table)` for table operations or `con.query_appender(statement, columns)` for custom SQL. For the appender in other clients, see the [Appender page]({% link docs/preview/data/appender.md %}).

Both functions are also available on the `duckdb` module. They use the default connection unless you supply the `connection` argument.

## Appending to a Table

`con.appender(table)` resolves the table once, when the appender is created, the way SQL resolves a table name. It appends to the table's columns in declared order and skips generated columns. `append_row` takes one value per column, and `append_rows` takes any iterable of rows. Values are converted exactly as [`executemany` parameters]({% link docs/preview/clients/python/dbapi.md %}#prepared-statements) are.

To append to some of the columns, list them in `columns`. The other columns take their default value, per row:

```python
con.execute("CREATE SEQUENCE event_ids")
con.execute(
    "CREATE TABLE events (id INTEGER DEFAULT nextval('event_ids'), kind VARCHAR, note VARCHAR DEFAULT 'none')"
)

appender = con.appender("events", columns=["kind"])
appender.append_row("login")
appender.append_row("logout")
appender.flush()
```

## Updates, Upserts and Deletes

The `action` argument picks the statement: `"insert"` (the default), `"upsert"`, `"update"` or `"delete"`. An upsert inserts new rows and updates existing rows that have the same primary key or unique key.

```python
con.execute("CREATE TABLE stock (sku VARCHAR PRIMARY KEY, qty INTEGER)")
con.execute("INSERT INTO stock VALUES ('widget', 3), ('gadget', 5)")

with con.appender("stock", action="upsert") as appender:
    appender.append_row("widget", 10)
    appender.append_row("gizmo", 1)

with con.appender("stock", action="update", key=["sku"]) as appender:
    appender.append_row("gadget", 0)

with con.appender("stock", action="delete", key=["sku"]) as appender:
    appender.append_row("gizmo")

print(con.sql("SELECT * FROM stock ORDER BY sku").fetchall())
```

```text
[('gadget', 0), ('widget', 10)]
```

* `upsert` runs an [`INSERT OR REPLACE`]({% link docs/preview/sql/statements/insert.md %}#insert-or-replace-into), so the table needs exactly one primary key or unique constraint. It takes `columns` like an insert; on a conflict, only the listed columns change.
* `update` matches rows on the `key` columns and sets every other appended column. Use `columns` to choose the appended columns.
* `delete` appends only the `key` columns, in the order of `key`, and deletes the rows that match.
* A `NULL` key matches nothing.
* A plain insert writes the rows in append order while [`preserve_insertion_order`]({% link docs/preview/configuration/overview.md %}) is on, which is the default. An upsert does not keep append order.
* When a flush contains duplicate keys, an upsert keeps one row per key value, including `NULL`; an update applies one input row; and `MERGE INTO` raises an error.

## Custom Statements

`con.query_appender` runs your SQL statement when you flush. Declare the appended columns as a dictionary of names to types. Your statement reads the appended rows as `appender_data`.

To transform the rows first, supply a `source` query. This query reads the appended rows as `appender_buffer`, and your statement reads its result as `appender_data`. The example below uses `source` to look up the product ID for each product code (`sku`). The `source` can be any query that returns rows; DuckDB runs it as you wrote it.

```python
con.execute("CREATE TABLE products (id INTEGER, sku VARCHAR)")
con.execute("INSERT INTO products VALUES (1, 'widget'), (2, 'gadget')")
con.execute("CREATE TABLE orders (product_id INTEGER, qty INTEGER)")

appender = con.query_appender(
    "INSERT INTO orders FROM appender_data",
    {"sku": "VARCHAR", "qty": "INTEGER"},
    source="SELECT p.id AS product_id, b.qty FROM appender_buffer AS b JOIN products AS p USING (sku)",
)
appender.append_row("gadget", 4)
appender.append_row("widget", 2)
appender.flush()
```

* The statement is one `INSERT` (including `INSERT OR REPLACE` and `ON CONFLICT`), `UPDATE`, `DELETE` or [`MERGE INTO`]({% link docs/preview/sql/statements/merge_into.md %}).
* A type is anything the [Types API]({% link docs/preview/clients/python/types.md %}) accepts, such as `"INTEGER"`, `duckdb.sqltypes.INTEGER` or `int`.
* A declared column that the statement does not read is allowed.
* DataFrames and other Python objects named in `source` or in the statement are looked up once, where the appender is created, and reused at every flush. If you later create a DuckDB table with the same name, later flushes use that table instead.

## Flushing

Each `flush()` applies the rows collected since the previous flush. It runs in your transaction if you started one with `BEGIN` or `con.begin()`, and otherwise commits by itself. A flush with no rows does nothing.

A `with` block flushes on successful exit. When an exception leaves the block, the buffered rows are discarded and the exception propagates. Outside a `with` block, call `flush()` to write the rows and `clear()` to discard them. There is no `close()` method. The appender remains usable after `flush()`, `clear()` or leaving a `with` block.

> Warning Garbage collection discards buffered rows and emits a `ResourceWarning`. Call `flush()` or use a `with` block to write the rows.

## Errors and Retrying

* The appender checks its statement when you create it, without running it. Invalid SQL, incorrect column counts, unsupported statement types, `RETURNING` clauses and SQL parameter placeholders such as `?` raise an exception at creation. These errors leave the transaction usable. Cast errors and constraint violations raise an exception during `flush()`.
* A flush that raises because an earlier result is still open or another call is running on the connection keeps its buffered rows, and so does an interrupted flush. Finish the result or wait for the other call, then call `flush()` again. Other failures discard the rows and raise an exception.
* An interrupted flush inside your transaction keeps its buffered rows but aborts the transaction. Roll back before retrying. Start a new transaction if the retry must be part of one.
* If you press Ctrl-C while a Python function called from SQL is running during a flush, DuckDB treats it as an error in that function and discards the buffered rows.

## Memory Use

The rows waiting to be flushed count toward DuckDB's `memory_limit`. When they no longer fit in memory, DuckDB can store them in temporary files. If DuckDB has no temporary directory, a full buffer makes every query on the connection raise an `OutOfMemoryException` until you call `flush()` or `clear()`. If a write into the buffer fails, `append_row`, `append_rows` and `flush()` raise an exception until you call `clear()`.

## Connections and Threads

Concurrent calls on the same appender raise an exception rather than wait. Calls from a callback during a flush also raise an exception. Use a separate appender for each thread. You can append rows or call `clear()` while an `execute()` result is open, but must finish that result before calling `flush()`: call `con.fetchall()`, call `con.fetchone()` repeatedly until it returns `None`, or call `con.complete()` or `con.abort()`.
