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

If we want to use the automatic format detection, we can set `FORMAT` to `CSV_AUTO` and omit the otherwise required configuration options.

```sql
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'test.csv' ( FORMAT CSV_AUTO );
SELECT * FROM ontime;
```

The detailed syntax description can be found [here](/docs/sql/statements/copy.html).

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
