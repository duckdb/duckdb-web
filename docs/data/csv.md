---
layout: docu
title: CSV Loading
---
CSV loading is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a pain. CSV files exist with different delimiters, they can contain quoted values, have an optional header row (or even multiple!) or even be completely deformed. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file.

We use the following CSV file in our examples:

**test.csv**
```
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-01|AA|New York, NY|Los Angeles, CA
1988-01-02|AA|New York, NY|Los Angeles, CA
1988-01-03|AA|New York, NY|Los Angeles, CA
```

# read_csv_auto function
The `read_csv_auto` is the simplest method of loading CSV files: it automatically attempts to figure out the correct configuration of the CSV reader. It also automatically deduces types of columns. If the CSV file has a header, it will use the names found in that header to name the columns. Otherwise, the columns will be named `column0, column1, column2, ...`

```sql
SELECT * FROM read_csv_auto('test.csv');
```

|FlightDate|UniqueCarrier| OriginCityName  | DestCityName  |
|---------:|------------:|----------------:|--------------:|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

The path can either be a relative path (relative to the current working directory) or an absolute path.

We can use read_csv_auto to create a persistent table as well:

```sql
CREATE TABLE ontime AS SELECT * FROM read_csv_auto('test.csv');
DESCRIBE ontime;
```

|Field         |Type   |Null|Key |Default|Extra|
|-------------:|------:|---:|---:|------:|----:|
|FlightDate    |DATE   |YES |NULL|NULL   |NULL |
|UniqueCarrier |VARCHAR|YES |NULL|NULL   |NULL |
|OriginCityName|VARCHAR|YES |NULL|NULL   |NULL |
|DestCityName  |VARCHAR|YES |NULL|NULL   |NULL |

| `SAMPLE_SIZE` | Option to define number of sample rows for automatic CSV type detection. Chunks of sample rows will be drawn from different locations of the input file. Set to `-1` to scan the entire input file. Note: Only the first max. 1024 rows will be used for dialect detection. |
| `ALL_VARCHAR` | Option to skip type detection for CSV parsing and assume all columns to be of type VARCHAR. |

```sql
SELECT * FROM read_csv_auto('test.csv', SAMPLE_SIZE=20000);
```

If we set `DELIM`/`SEP`, `QUOTE`, `ESCAPE`, or `HEADER` explicitly, we can bypass the automatic detection of this particular parameter:

```sql
SELECT * FROM read_csv_auto('test.csv', HEADER=TRUE);
```

Note:
`read_csv_auto()` is an alias for `read_csv(AUTO_DETECT=TRUE)`.


## COPY Statement
The `COPY` statement can be used to load data from a CSV file into a table. This statement has the same syntax as the `COPY` statement supported by PostgreSQL. For the `COPY` statement, we must first create a table with the correct schema to load the data into. We then specify the CSV file to load from plus any configuration options separately.

```sql
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'test.csv' ( DELIMITER '|', HEADER );
SELECT * FROM ontime;
```

|flightdate|uniquecarrier| origincityname  | destcityname  |
|---------:|------------:|----------------:|--------------:|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

If we want to use the automatic format detection, we can set `AUTO_DETECT` to `TRUE` and omit the otherwise required configuration options.

```sql
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'test.csv' ( AUTO_DETECT TRUE );
SELECT * FROM ontime;
```

More on the copy statement can be found [here](/docs/sql/statements/copy.html).

## Shell Import
The DuckDB shell also offers a way of importing CSV files. This method is the same syntax as would be used in the SQLite shell. For this method we need to first create a table, then specify the parameters and then use the `.import` statement.

```sql
.sep |
.headers on
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
.import test.csv ontime
SELECT * FROM ontime;
```

|flightdate|uniquecarrier| origincityname  | destcityname  |
|---------:|------------:|----------------:|--------------:|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|
