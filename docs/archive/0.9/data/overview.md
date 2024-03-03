---
layout: docu
redirect_from:
- docs/archive/0.9.2/data/overview
- docs/archive/0.9.2/data
- docs/archive/0.9.1/data/overview
- docs/archive/0.9.1/data
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

Data can be efficiently loaded from CSV files using the `read_csv_auto` function or the `COPY` statement.

```sql
SELECT * FROM read_csv_auto('test.csv');
```

You can also load data from **compressed** (e.g., compressed with [gzip](https://www.gzip.org/)) CSV files, for example:

```sql
SELECT * FROM read_csv_auto('test.csv.gz');
```

For more details, see the [page on CSV loading](../data/csv).

## Parquet Loading

Parquet files can be efficiently loaded and queried using the `read_parquet` function.

```sql
SELECT * FROM read_parquet('test.parquet');
```

For more details, see the [page on Parquet loading](../data/parquet).

## JSON Loading

JSON files can be efficiently loaded and queried using the `read_json_auto` function.

```sql
SELECT * FROM read_json_auto('test.json');
```

For more details, see the [page on JSON loading](../data/json).

## Appender (C++ and Java)

In C++ and Java, the appender can be used as an alternative for bulk data loading. This class can be used to efficiently add rows to the database system without needing to use SQL.

C++:

```cpp
Appender appender(con, "people");
appender.AppendRow(1, "Mark");
appender.Close();
```

Java:

```java
con.createAppender("main", "people");
appender.beginRow();
appender.append("Mark");
appender.endRow();
appender.close();
```

For a detailed description, see the [page on the C++ appender](../data/appender).