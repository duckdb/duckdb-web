---
layout: docu
title: Importing Data
---

The first step to using a database system is to insert data into that system.
DuckDB provides can directly connect to [many popular data sources]({% link docs/1.1/data/data_sources.md %}) and offers several data ingestion methods that allow you to easily and efficiently fill up the database.
On this page, we provide an overview of these methods so you can select which one is best suited for your use case.

## `INSERT` Statements

`INSERT` statements are the standard way of loading data into a database system. They are suitable for quick prototyping, but should be avoided for bulk loading as they have significant per-row overhead.

```sql
INSERT INTO people VALUES (1, 'Mark');
```

For a more detailed description, see the [page on the `INSERT statement`]({% link docs/1.1/data/insert.md %}).

## CSV Loading

Data can be efficiently loaded from CSV files using several methods. The simplest is to use the CSV file's name:

```sql
SELECT * FROM 'test.csv';
```

Alternatively, use the [`read_csv` function]({% link docs/1.1/data/csv/overview.md %}) to pass along options:

```sql
SELECT * FROM read_csv('test.csv', header = false);
```

Or use the [`COPY` statement]({% link docs/1.1/sql/statements/copy.md %}#copy--from):

```sql
COPY tbl FROM 'test.csv' (HEADER false);
```

It is also possible to read data directly from **compressed CSV files** (e.g., compressed with [gzip](https://www.gzip.org/)):

```sql
SELECT * FROM 'test.csv.gz';
```

DuckDB can create a table from the loaded data using the [`CREATE TABLE ... AS SELECT` statement]({% link docs/1.1/sql/statements/create_table.md %}#create-table--as-select-ctas):

```sql
CREATE TABLE test AS
    SELECT * FROM 'test.csv';
```

For more details, see the [page on CSV loading]({% link docs/1.1/data/csv/overview.md %}).

## Parquet Loading

Parquet files can be efficiently loaded and queried using their filename:

```sql
SELECT * FROM 'test.parquet';
```

Alternatively, use the [`read_parquet` function]({% link docs/1.1/data/parquet/overview.md %}):

```sql
SELECT * FROM read_parquet('test.parquet');
```

Or use the [`COPY` statement]({% link docs/1.1/sql/statements/copy.md %}#copy--from):

```sql
COPY tbl FROM 'test.parquet';
```

For more details, see the [page on Parquet loading]({% link docs/1.1/data/parquet/overview.md %}).

## JSON Loading

JSON files can be efficiently loaded and queried using their filename:

```sql
SELECT * FROM 'test.json';
```

Alternatively, use the [`read_json_auto` function]({% link docs/1.1/data/json/overview.md %}):

```sql
SELECT * FROM read_json_auto('test.json');
```

Or use the [`COPY` statement]({% link docs/1.1/sql/statements/copy.md %}#copy--from):

```sql
COPY tbl FROM 'test.json';
```

For more details, see the [page on JSON loading]({% link docs/1.1/data/json/overview.md %}).

## Appender

In several APIs (C, C++, Go, Java, and Rust), the [Appender]({% link docs/1.1/data/appender.md %}) can be used as an alternative for bulk data loading.
This class can be used to efficiently add rows to the database system without using SQL statements.