---
layout: docu
title: Importing Data
---
<!-- not sure if this section should be abstracted into its own page, or where it would be best placed, feel free to move -->
### Create a Connection (in-memory or persistant file)
To use DuckDB, you must first create a connection to a database. The connection typically takes as parameter the database file to read and write from. If the database file does not exist, it will be created (the file extension may be `.db`, `.duckdb`, or anything else). The special value `:memory:` (the default) can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the process). See [API docs](docs/api/overview) for client-specfic usage. 

Once connected to a database system, you can access its data or insert data into that system. DuckDB provides several data ingestion methods that allow you to easily and efficiently fill up the database. In this section, we provide an overview of these methods so you can select which one is correct for you.

### Insert Statements
Insert statements are the standard way of loading data into a database system. They are suitable for quick prototyping, but should be avoided for bulk loading as they have significant per-row overhead.

```sql
INSERT INTO people VALUES (1, 'Mark');
```

See [here](/docs/data/insert) for a more detailed description of insert statements.

### CSV Loading
Data can be efficiently loaded from CSV files using the `read_csv_auto` function or the `COPY` statement.

```sql
SELECT * FROM read_csv_auto('test.csv');
```

You can also load data from **compressed** (e.g. compressed with [gzip](https://www.gzip.org/)) CSV files, for example:

```sql
SELECT * FROM read_csv_auto('test.csv.gz');
```

See [here](/docs/data/csv) for a detailed description of CSV loading.

### Parquet Loading
Parquet files can be efficiently loaded and queried using the `read_parquet` function.

```sql
SELECT * FROM read_parquet('test.parquet');
```

See [here](/docs/data/parquet) for a detailed description of Parquet loading.

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

See [here](/docs/data/appender) for a detailed description of the C++ appender.
