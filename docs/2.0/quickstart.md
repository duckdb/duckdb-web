---
layout: docu
breadcrumbs: false
title: Quickstart
---

Run your first query and read a CSV file using the DuckDB command line interface (CLI). To try SQL without installing anything, open [DuckDB in your browser](https://shell.duckdb.org).

## Install DuckDB

Follow the [installation instructions]({% link docs/2.0/installation.html %}?environment=cli) for your platform.
If you prefer to use DuckDB from a programming language, see the [client APIs]({% link docs/2.0/clients/overview.md %}).

## Open a Database

In your terminal, run:

```bash
duckdb quickstart.duckdb
```

This creates a database file called `quickstart.duckdb` in the current directory, or opens it if it already exists.
Tables you create in this database are saved to the file.

## Run a Query

At the DuckDB prompt, enter:

```sql
SELECT 6 * 7 AS answer;
```

The result is `42`.

## Read a CSV File

Save the following text as `sales.csv` in the directory where you started DuckDB:

```text
product,quantity,price
Notebook,2,5.00
Pencil,3,1.50
Notebook,1,5.00
```

Query the file directly:

```sql
SELECT product, sum(quantity * price) AS revenue
FROM read_csv('sales.csv')
GROUP BY product
ORDER BY revenue DESC;
```

The result contains `Notebook` with revenue of `15.00` and `Pencil` with revenue of `4.50`.
DuckDB detects the CSV header and column types automatically.

To save the data as a table in your database:

```sql
CREATE TABLE sales AS SELECT * FROM read_csv('sales.csv');
```

Enter `.exit` to close the CLI. Run `duckdb quickstart.duckdb` again to reopen the database and query the `sales` table.

## Next Steps

* [How-to Guides]({% link docs/2.0/guides/overview.md %}) for specific tasks
* [Import and export]({% link docs/2.0/data/overview.md %}) for CSV, Parquet and other data sources
* [SQL introduction]({% link docs/2.0/sql/introduction.md %}) for more query examples
* [Connecting to DuckDB]({% link docs/2.0/connect/overview.md %}) for persistent and in-memory databases
