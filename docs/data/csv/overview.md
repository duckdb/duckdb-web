---
layout: docu
title: CSV Loading
redirect_from:
  - /docs/data/csv
---

## Examples

```sql
-- read a CSV file from disk, auto-infer options
SELECT * FROM 'flights.csv';
-- read_csv with custom options
SELECT * FROM read_csv('flights.csv', delim='|', header=true, columns={'FlightDate': 'DATE', 'UniqueCarrier': 'VARCHAR', 'OriginCityName': 'VARCHAR', 'DestCityName': 'VARCHAR'});
-- read a CSV from stdin, auto-infer options
cat data/csv/issue2471.csv | duckdb -c "SELECT * FROM read_csv_auto('/dev/stdin')"

-- read a CSV file into a table
CREATE TABLE ontime(FlightDate DATE, UniqueCarrier VARCHAR, OriginCityName VARCHAR, DestCityName VARCHAR);
COPY ontime FROM 'flights.csv' (AUTO_DETECT true);
-- alternatively, create a table without specifying the schema manually
CREATE TABLE ontime AS SELECT * FROM 'flights.csv';
-- we can use the FROM-first syntax to omit 'SELECT *'
CREATE TABLE ontime AS FROM 'flights.csv';

-- write the result of a query to a CSV file
COPY (SELECT * FROM ontime) TO 'flights.csv' WITH (HEADER 1, DELIMITER '|');
-- we can use the FROM-first syntax to omit 'SELECT *'
COPY (FROM ontime) TO 'flights.csv' WITH (HEADER 1, DELIMITER '|');
```

## CSV Reader

CSV loading is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a challenge. CSV files come in many different varieties, are often corrupt, and do not have a schema. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file. See the [auto detection page](auto_detection) for more information.

## Parameters

Below are parameters that can be passed to the CSV reader. These parameters are accepted by both the [`COPY` statement](../../sql/statements/copy#copy-to) and the CSV reader functions ([`read_csv`](#read_csv-function) and [`read_csv_auto`](#read_csv_auto-function)).

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `all_varchar` | Option to skip type detection for CSV parsing and assume all columns to be of type `VARCHAR`. | `BOOL` | `false` |
| `auto_detect` | Enables [auto detection of parameters](auto_detection). | `BOOL` | `true` |
| `buffer_size` | The buffer size used by the CSV reader, specified in bytes. By default, it is set to 32MB or the size of the CSV file (if smaller). The buffer size must be at least as large as the longest line in the CSV file. Note: this is an advanced option that has a significant impact on performance and memory usage. | `BIGINT` | min(32000000, CSV file size) |
| `columns` | A struct that specifies the column names and column types contained within the CSV file (e.g., `{'col1': 'INTEGER', 'col2': 'VARCHAR'}`). Using this option implies that auto detection is not used. | `STRUCT` | (empty) |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `t.csv.gz` will use gzip, `t.csv` will use `none`). Options are `none`, `gzip`, `zstd`. | `VARCHAR` | `auto` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../../sql/functions/dateformat). | `VARCHAR` | (empty) |
| `decimal_separator` | The decimal separator of numbers. | `VARCHAR` | `.` |
| `delim` or `sep` | Specifies the string that separates columns within each row (line) of the file. | `VARCHAR` | `,` |
| `escape` | Specifies the string that should appear before a data character sequence that matches the `quote` value. | `VARCHAR` | `"` |
| `filename` | Whether or not an extra `filename` column should be included in the result. | `BOOL` | `false` |
| `force_not_null` | Do not match the specified columns' values against the NULL string. In the default case where the `NULL` string is empty, this means that empty values will be read as zero-length strings rather than `NULL`s. | `VARCHAR[]` | `[]` |
| `header` | Specifies that the file contains a header line with the names of each column in the file. | `BOOL` | `false` |
| `hive_partitioning` | Whether or not to interpret the path as a [hive partitioned path](../partitioning/hive_partitioning). | `BOOL` | `false` |
| `ignore_errors` | Option to ignore any parsing errors encountered - and instead ignore rows with errors. | `BOOL` | `false` |
| `max_line_size` | The maximum line size in bytes. | `BIGINT` | 2097152 |
| `names` | The column names as a list, see [example](tips#provide-names-if-the-file-does-not-contain-a-header). | `VARCHAR[]` | (empty) |
| `new_line` | Set the new line character(s) in the file. Options are `'\r'`,`'\n'`, or `'\r\n'`. | `VARCHAR` | (empty) |
| `normalize_names` | Boolean value that specifies whether or not column names should be normalized, removing any non-alphanumeric characters from them. | `BOOL` | `false` |
| `nullstr` | Specifies the string that represents a NULL value. | `VARCHAR` | (empty) |
| `parallel` | Whether or not the parallel CSV reader is used. | `BOOL` | `true` |
| `quote` | Specifies the quoting string to be used when a data value is quoted. | `VARCHAR` | `"` |
| `sample_size` | The number of sample rows for [auto detection of parameters](auto_detection). | `BIGINT` | 20480 |
| `skip` | The number of lines at the top of the file to skip. | `BIGINT` | 0 |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) | `VARCHAR` | (empty) |
| `types` or `dtypes` | The column types as either a list (by position) or a struct (by name). [Example here](tips#override-the-types-of-specific-columns). | `VARCHAR[]` or `STRUCT` | (empty) |
| `union_by_name` | Whether the columns of multiple schemas should be [unified by name](../multiple_files/combining_schemas), rather than by position. | `BOOL` | `false` |

## read_csv_auto Function

The `read_csv_auto` is the simplest method of loading CSV files: it automatically attempts to figure out the correct configuration of the CSV reader. It also automatically deduces types of columns. If the CSV file has a header, it will use the names found in that header to name the columns. Otherwise, the columns will be named `column0, column1, column2, ...`. An example with the [`flights.csv`](/data/flights.csv) file:

```sql
SELECT * FROM read_csv_auto('flights.csv');
```

|FlightDate|UniqueCarrier| OriginCityName  | DestCityName  |
|----------|-------------|-----------------|---------------|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

The path can either be a relative path (relative to the current working directory) or an absolute path.

We can use `read_csv_auto` to create a persistent table as well:

```sql
CREATE TABLE ontime AS SELECT * FROM read_csv_auto('flights.csv');
DESCRIBE ontime;
```

|Field         |Type   |Null|Key |Default|Extra|
|--------------|-------|----|----|-------|-----|
|FlightDate    |DATE   |YES |NULL|NULL   |NULL |
|UniqueCarrier |VARCHAR|YES |NULL|NULL   |NULL |
|OriginCityName|VARCHAR|YES |NULL|NULL   |NULL |
|DestCityName  |VARCHAR|YES |NULL|NULL   |NULL |

```sql
SELECT * FROM read_csv_auto('flights.csv', SAMPLE_SIZE=20000);
```

If we set `DELIM`/`SEP`, `QUOTE`, `ESCAPE`, or `HEADER` explicitly, we can bypass the automatic detection of this particular parameter:

```sql
SELECT * FROM read_csv_auto('flights.csv', HEADER=true);
```

Multiple files can be read at once by providing a glob or a list of files. Refer to the [multiple files section](../multiple_files/overview) for more information.

## read_csv Function

The `read_csv` function accepts the same parameters that `read_csv_auto` does but does not assume `AUTO_DETECT=true`.

## Writing Using the COPY Statement

The [`COPY` statement](../../sql/statements/copy#copy-to) can be used to load data from a CSV file into a table. This statement has the same syntax as the one used in PostgreSQL. To load the data using the `COPY` statement, we must first create a table with the correct schema (which matches the order of the columns in the CSV file and uses types that fit the values in the CSV file). We then specify the CSV file to load from plus any configuration options separately.

```sql
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'flights.csv' (DELIMITER '|', HEADER);
SELECT * FROM ontime;
```

|flightdate|uniquecarrier| origincityname  | destcityname  |
|----------|-------------|-----------------|---------------|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

If we want to use the automatic format detection, we can set `AUTO_DETECT` to `true` and omit the otherwise required configuration options.

```sql
CREATE TABLE ontime(flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'flights.csv' (AUTO_DETECT true);
SELECT * FROM ontime;
```

## Pages in This Section
