---
layout: docu
title: Importing Data
---
The first step to using a database system is to insert data into that system. DuckDB provides several data ingestion methods that allow you to easily and efficiently fill up the database. In this section, we provide an overview of these methods so you can select which one is correct for you.

### Insert Statements
Insert statements are the standard way of loading data into a database system. They are suitable for quick prototyping, but should be avoided for bulk loading as they have significant per-row overhead.

```sql
INSERT INTO people VALUES (1, 'Mark');
```

See [here](../data/insert) for a more detailed description of insert statements.

### CSV Loading
Data can be efficiently loaded from CSV files using the `read_csv_auto` function or the `COPY` statement.

```sql
SELECT * FROM read_csv_auto('test.csv');
```

You can also load data from **compressed** (e.g. compressed with [gzip](https://www.gzip.org/)) CSV files, for example:

```sql
SELECT * FROM read_csv_auto('test.csv.gz');
```

See [here](../data/csv) for a detailed description of CSV loading.

### Parquet Loading
Parquet files can be efficiently loaded and queried using the `read_parquet` function.

```sql
SELECT * FROM read_parquet('test.parquet');
```

See [here](../data/parquet) for a detailed description of Parquet loading.

### JSON Loading
JSON files can be efficiently loaded and queried using the `read_json_auto` function.

```sql
SELECT * from read_json_auto('test.json');
```

See [here](../data/json) for a detailed description of JSON loading.

### Appender (C++ and Java)

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

See [here](../data/appender) for a detailed description of the C++ appender.
