---
layout: docu
redirect_from:
- /docs/stable/clients/python/migration
title: Migrating Python Code to DuckDB 2.0
---

This page lists what Python code written for DuckDB 1.x must change to run on DuckDB 2.0. Each item gives the 1.x form, the 2.0 form, and the page that explains it. For changes outside the Python client, see [Migrating to DuckDB 2.0]({% link docs/2.0/operations_manual/migration.md %}).

* **Python version.** DuckDB 2.0 requires Python 3.11 or newer; free-threaded builds of CPython are not supported. On Python 3.10, `pip install duckdb` installs a 1.x release. See [Installation]({% link docs/2.0/clients/python/overview.md %}#installation).

* **Arrow and Polars output of `execute()`.** 1.x: `con.execute(query).fetch_arrow_table()`, `fetch_record_batch()`, `arrow()`, and `pl()`. 2.0: these methods are gone from `execute()` results, and `to_arrow_table()` and `to_arrow_reader()` there copy the rows and warn. Use a relation: `con.sql(query).to_arrow_table()`, `con.sql(query).to_arrow_reader()`, or `con.sql(query).pl()`. See [Arrow and Polars Output]({% link docs/2.0/clients/python/dbapi.md %}#arrow-and-polars-output).

* **Fetching from a relation.** 1.x: `rel.fetchone()`, `rel.fetchmany(n)`, `rel.execute()`, and `rel.fetch_df_chunk()`. 2.0: these methods are gone, because a relation keeps no result between calls and runs its query again on every read. To keep a `fetchone()` or `fetchmany()` loop for a SQL query, create its result with [`con.execute(query)`]({% link docs/2.0/clients/python/dbapi.md %}#querying) instead of `con.sql(query)`. To iterate over an existing relation, use `for row in rel.iter_rows(): ...`; this keeps the complete result in engine memory. For streamed batches, use [`rel.to_arrow_reader()`]({% link docs/2.0/clients/python/relational_api.md %}#to_arrow_reader). Replace `rel.execute()` with [`rel.materialize()`]({% link docs/2.0/clients/python/relational_api.md %}#materialize) when you want to compute and retain the rows.

* **Plain strings in expressions.** 1.x: in `ColumnExpression("s") == "x"` and in `rel.update(set={"a": "x"})`, the string `"x"` named a column. 2.0: in an expression a plain string is a value, so the comparison tests `s` against the text `x` and warns when `x` is also a column name; `update()` refuses a plain string with a `TypeError`. Write `col("x")` for the column and `lit("x")` for the text. See the [Expression API]({% link docs/2.0/clients/python/expression.md %}) and [`update`]({% link docs/2.0/clients/python/relational_api.md %}#update).

* **Dotted column names.** 1.x: `ColumnExpression("t.x")` was the column `x` of `t`. 2.0: a name is never split at a dot, so `"t.x"` is one column name, and a query without a column of that name raises a `BinderException`. Write `col("t", "x")`. See [Column Expression]({% link docs/2.0/clients/python/expression.md %}#column-expression).

* **Dicts with keys that are not strings.** 1.x: `con.values({1: "a"})` made a `STRUCT` with a field named `1`. 2.0: in `values()` and in expressions, such a dict becomes a `MAP`, here `MAP(INTEGER, VARCHAR)`. Use string keys for a `STRUCT`. See [`dict`]({% link docs/2.0/clients/python/conversion.md %}#dict).

* **Columns named like new relation methods.** 1.x: `rel.offset` was the column `offset` of `rel`. 2.0: relations have new methods such as `offset`, `sample`, `head`, `rename`, `pivot`, `drop`, `unnest`, `unpivot`, `preview`, and `group_by`, so `rel.offset` is the method. Write `rel["offset"]` for the column. See the [Relational API]({% link docs/2.0/clients/python/relational_api.md %}).

* **`sql()` of statements that do not read.** 1.x: `con.sql("CREATE TABLE t (i INTEGER)")` returned `None`. 2.0: it returns a relation over what the statement returned, which a REPL or notebook prints; the statement still runs at the call. Use `con.execute()` for DDL and DML. Printing a relation runs its query, every time. See [Basic API Usage]({% link docs/2.0/clients/python/overview.md %}#basic-api-usage).

* **Open `execute()` results.** 1.x: other queries on the connection ran while a result was partly read. 2.0: running another query on the connection raises a `ResourceInUseException` until the result is read to its end or ended with `con.complete()` or `con.abort()`, and the next `execute()` replaces the open result. See [Open Results]({% link docs/2.0/clients/python/dbapi.md %}#open-results).

* **One connection in several threads.** 1.x: calls from several threads on one connection waited for each other. 2.0: a call while another thread uses the connection raises a `ResourceInUseException`. Give each thread its own `con.cursor()`. See [Using Connections in Parallel Python Programs]({% link docs/2.0/clients/python/overview.md %}#using-connections-in-parallel-python-programs).

* **Failed statements in a transaction.** 1.x: after `con.begin()`, a statement run with `execute()` that failed with a catalog, binder, or parser error left the transaction usable. 2.0: any statement run with `execute()` that fails aborts the transaction: `con.commit()` then rolls it back, and any other statement raises a `TransactionException` until `con.rollback()`. See [Transactions]({% link docs/2.0/clients/python/dbapi.md %}#transactions).

* **Writing files with `overwrite=False`.** 1.x: `rel.write_csv(path, overwrite=False)` and `rel.write_parquet(path, overwrite=False)` replaced an existing file. 2.0: they raise an `IOException`. Leave `overwrite` out to replace the file. See [`write_csv`]({% link docs/2.0/clients/python/relational_api.md %}#write_csv) and [`write_parquet`]({% link docs/2.0/clients/python/relational_api.md %}#write_parquet).

* **`Decimal` values with a positive exponent.** 1.x: `Decimal("1E+2")` became `1.00` of type `DECIMAL(3,2)`. 2.0: it is `100` of type `DECIMAL(3,0)`. See [Conversion between DuckDB and Python]({% link docs/2.0/clients/python/conversion.md %}).

* **Arrow batch size.** 1.x: the Arrow output of a relation came in batches of 1000000 rows by default. 2.0: the default is 131072 rows. Pass `batch_size` to `to_arrow_table()` or `to_arrow_reader()` for another size. See [`to_arrow_reader`]({% link docs/2.0/clients/python/relational_api.md %}#to_arrow_reader).

* **Database files.** 1.x: a database file that DuckDB 1.5 wrote opens in DuckDB 1.5. 2.0: DuckDB 1.5 cannot open a file that DuckDB 2.0 writes in its default format; to keep a file readable by DuckDB 1.5, connect with `config={"storage_compatibility_version": "v1.5.0"}`. See [Configuration]({% link docs/2.0/clients/python/overview.md %}#configuration) and [Storage Format]({% link docs/2.0/operations_manual/migration.md %}#storage-format).
