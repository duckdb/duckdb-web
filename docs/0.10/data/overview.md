---
layout: docu
title: Importing Data
---

The first step to using a database system is to insert data into that system. DuckDB provides several data ingestion methods that allow you to easily and efficiently fill up the database. In this section, we provide an overview of these methods so you can select which one is correct for you.

## Insert Statements

Insert statements are the standard way of loading data into a database system. They are suitable for quick prototyping, but should be avoided for bulk loading as they have significant per-row overhead.

```sql
INSERT INTO people VALUES (1, 'Mark');
```

For a more detailed description, see the [page on the `INSERT statement`](../data/insert).

## CSV Loading

Data can be efficiently loaded from CSV files using several methods. The simplest is to use the CSV file's name:

```sql
SELECT * FROM 'test.csv';
```

Alternatively, use the `read_csv` function or the `COPY` statement to pass along options. For example:

```sql
SELECT * FROM read_csv('test.csv', header = false);
```

It is also possible to read data directly from **compressed CSV files** (e.g., compressed with [gzip](https://www.gzip.org/)):

```sql
SELECT * FROM 'test.csv.gz';
```

DuckDB can create a table from the loaded data using the [`CREATE TABLE ... AS SELECT` statement](../sql/statements/create_table#create-table--as-select-ctas):

```sql
CREATE TABLE test AS
    SELECT * FROM 'test.csv';
```

For more details, see the [page on CSV loading](../data/csv).

## Parquet Loading

Parquet files can be efficiently loaded and queried using their filename:

```sql
SELECT * FROM 'test.parquet';
```

Alternatively, use the `read_parquet` function or the `COPY` statement. For example:

```sql
SELECT * FROM read_parquet('test.parquet');
```

For more details, see the [page on Parquet loading](../data/parquet).

## JSON Loading

JSON files can be efficiently loaded and queried using their filename:

```sql
SELECT * FROM 'test.json';
```

Alternatively, use the `read_json_auto` function or the `COPY` statement. For example:

```sql
SELECT * FROM read_json_auto('test.json');
```

For more details, see the [page on JSON loading](../data/json).

## Appender

In several APIs (C, C++, Go, Java, and Rust), the [Appender](appender) can be used as an alternative for bulk data loading.
This class can be used to efficiently add rows to the database system without using SQL statements.