---
layout: docu
title: CSV Loading
---

CSV loading is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a challenge. CSV files exist with different delimiters, they can contain quoted values, have an optional header row (or even multiple!) or even be completely deformed. In addition, CSV files have no set schema - they are stored only as plaintext. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file. See the [auto detection page](auto_detection) for more information.

### Examples

**flights.csv**
```
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-01|AA|New York, NY|Los Angeles, CA
1988-01-02|AA|New York, NY|Los Angeles, CA
1988-01-03|AA|New York, NY|Los Angeles, CA
```

```sql
-- read a CSV file from disk, auto-infer options
SELECT * FROM 'flights.csv';
-- read_csv with custom options
SELECT * FROM read_csv('flights.csv', delim='|', header=True, columns={'FlightDate': 'DATE', 'UniqueCarrier': 'VARCHAR', 'OriginCityName': 'VARCHAR', 'DestCityName': 'VARCHAR'});
-- read a CSV from stdin, auto-infer options
cat data/csv/issue2471.csv | duckdb -c "select * from read_csv_auto('/dev/stdin')"

-- read a CSV file into a table
CREATE TABLE ontime(FlightDate DATE, UniqueCarrier VARCHAR, OriginCityName VARCHAR, DestCityName VARCHAR);
COPY ontime FROM 'flights.csv' (AUTO_DETECT TRUE);
-- alternatively, create a table without specifying the schema manually
CREATE TABLE ontime AS SELECT * FROM 'flights.csv';

-- write the result of a query to a CSV file
COPY (SELECT * FROM ontime) TO 'flights.csv' WITH (HEADER 1, DELIMITER '|');
```

# Parameters

| Name | Description |
|:---|:---|
| `AUTO_DETECT` | Option for CSV parsing. If `TRUE`, the parser will attempt to detect the input format and data types automatically. `DELIM`/`SEP`, `QUOTE`, `ESCAPE`, and `HEADER` parameters become optional. `read_csv_auto` defaults to true for this parameter, `read_csv` defaults to false. |
| `COLUMNS` | A struct that specifies the column names and column types contained within the CSV file (e.g. `{'col1': 'INTEGER', 'col2': 'VARCHAR'}`). If `auto_detect` is enabled these will be inferred. |
| `SEP` or `DELIM` | Specifies the string that separates columns within each row (line) of the file. The default value is a comma (`,`). |
| `NULLSTR` | Specifies the string that represents a NULL value. The default is an empty string. |
| `HEADER` | Specifies that the file contains a header line with the names of each column in the file. |
| `QUOTE` | Specifies the quoting string to be used when a data value is quoted. The default is double-quote (`"`). |
| `ESCAPE` | Specifies the string that should appear before a data character sequence that matches the `QUOTE` value. The default is the same as the `QUOTE` value (so that the quoting string is doubled if it appears in the data). |
| `DATEFORMAT` | Specifies the date format to use when parsing dates. See [Date Format](../../sql/functions/dateformat) |
| `TIMESTAMPFORMAT` | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) |
| `SAMPLE_SIZE` | Option to define number of sample rows for automatic CSV type detection. Chunks of sample rows will be drawn from different locations of the input file. Set to `-1` to scan the entire input file. Note: Only the first max. 1024 rows will be used for dialect detection. |
| `ALL_VARCHAR` | Option to skip type detection for CSV parsing and assume all columns to be of type VARCHAR. |
| `NORMALIZE_NAMES` | Boolean value that specifies whether or not column names should be normalized, removing any non-alphanumeric characters from them. |
| `COMPRESSION` | The compression type for the file. By default this will be detected automatically from the file extension (e.g. `t.csv.gz` will use gzip, `t.csv` will use `none`). Options are `none`, `gzip`, `zstd`. |
| `FILENAME` | Boolean value that specifies whether or not an extra `FILENAME` column should be included in the result. |
| `SKIP` | The number of lines at the top of the file to skip. |

# read_csv_auto function
The `read_csv_auto` is the simplest method of loading CSV files: it automatically attempts to figure out the correct configuration of the CSV reader. It also automatically deduces types of columns. If the CSV file has a header, it will use the names found in that header to name the columns. Otherwise, the columns will be named `column0, column1, column2, ...`

```sql
SELECT * FROM read_csv_auto('flights.csv');
```

|FlightDate|UniqueCarrier| OriginCityName  | DestCityName  |
|---------:|------------:|----------------:|--------------:|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

The path can either be a relative path (relative to the current working directory) or an absolute path.

We can use read_csv_auto to create a persistent table as well:

```sql
CREATE TABLE ontime AS SELECT * FROM read_csv_auto('flights.csv');
DESCRIBE ontime;
```

|Field         |Type   |Null|Key |Default|Extra|
|-------------:|------:|---:|---:|------:|----:|
|FlightDate    |DATE   |YES |NULL|NULL   |NULL |
|UniqueCarrier |VARCHAR|YES |NULL|NULL   |NULL |
|OriginCityName|VARCHAR|YES |NULL|NULL   |NULL |
|DestCityName  |VARCHAR|YES |NULL|NULL   |NULL |

```sql
SELECT * FROM read_csv_auto('flights.csv', SAMPLE_SIZE=20000);
```

If we set `DELIM`/`SEP`, `QUOTE`, `ESCAPE`, or `HEADER` explicitly, we can bypass the automatic detection of this particular parameter:

```sql
SELECT * FROM read_csv_auto('flights.csv', HEADER=TRUE);
```

Note:
`read_csv_auto()` is an alias for `read_csv(AUTO_DETECT=TRUE)`.


## COPY Statement
The `COPY` statement can be used to load data from a CSV file into a table. This statement has the same syntax as the `COPY` statement supported by PostgreSQL. For the `COPY` statement, we must first create a table with the correct schema to load the data into. We then specify the CSV file to load from plus any configuration options separately.

```sql
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'flights.csv' ( DELIMITER '|', HEADER );
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
COPY ontime FROM 'flights.csv' ( AUTO_DETECT TRUE );
SELECT * FROM ontime;
```

More on the copy statement can be found [here](../../sql/statements/copy.html).