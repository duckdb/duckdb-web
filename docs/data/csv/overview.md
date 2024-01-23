---
layout: docu
title: CSV Import
redirect_from:
  - /docs/data/csv
---

## Examples

The following examples use the [`flights.csv`](/data/flights.csv) file.

```sql
-- read a CSV file from disk, auto-infer options
SELECT * FROM 'flights.csv';
-- read_csv with custom options
SELECT * FROM read_csv('flights.csv',
  delim = '|',
  header = true,
  columns = {
    'FlightDate': 'DATE',
    'UniqueCarrier': 'VARCHAR',
    'OriginCityName': 'VARCHAR',
    'DestCityName': 'VARCHAR'
  });
```
```bash
# read a CSV from stdin, auto-infer options
cat flights.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```
```sql
-- read a CSV file into a table
CREATE TABLE ontime (
    FlightDate DATE,
    UniqueCarrier VARCHAR,
    OriginCityName VARCHAR,
    DestCityName VARCHAR
);
COPY ontime FROM 'flights.csv';
```
```sql
-- alternatively, create a table without specifying the schema manually
CREATE TABLE ontime AS SELECT * FROM 'flights.csv';
-- we can use the FROM-first syntax to omit 'SELECT *'
CREATE TABLE ontime AS FROM 'flights.csv';
```
```sql
-- write the result of a query to a CSV file
COPY (SELECT * FROM ontime) TO 'flights.csv' WITH (HEADER true, DELIMITER '|');
-- if we serialize the entire table, we can simply refer to it with its name
COPY ontime TO 'flights.csv' WITH (HEADER true, DELIMITER '|');
```

## CSV Loading

CSV loading, i.e., importing CSV files to the database, is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a challenge. CSV files come in many different varieties, are often corrupt, and do not have a schema. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file using the [CSV sniffer](/2023/10/27/csv-sniffer). This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file. See the [auto detection page](auto_detection) for more information.

## Parameters

Below are parameters that can be passed to the CSV reader. These parameters are accepted by both the [`COPY` statement](../../sql/statements/copy#copy-to) and the [`read_csv` function](#read_csv-function).

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `all_varchar` | Option to skip type detection for CSV parsing and assume all columns to be of type `VARCHAR`. | `BOOL` | `false` |
| `allow_quoted_nulls` | Option to allow the conversion of quoted values to `NULL` values | `BOOL` | `true` |
| `auto_detect` | Enables [auto detection of CSV parameters](auto_detection). | `BOOL` | `true` |
| `auto_type_candidates` | This option allows you to specify the types that the sniffer will use when detecting CSV column types, e.g., `SELECT * FROM read_csv('csv_file.csv', auto_type_candidates=['BIGINT', 'DATE'])`. The `VARCHAR` type is always included in the detected types (as a fallback option). | `TYPE[]` | `['SQLNULL', 'BOOLEAN', 'BIGINT', 'DOUBLE', 'TIME', 'DATE', 'TIMESTAMP', 'VARCHAR']` |
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
| `null_padding` | If this option is enabled, when a row lacks columns, it will pad the remaining columns on the right with null values.| `BOOL` | `false` |
| `nullstr` | Specifies the string that represents a NULL value. | `VARCHAR` | (empty) |
| `parallel` | Whether or not the parallel CSV reader is used. | `BOOL` | `true` |
| `quote` | Specifies the quoting string to be used when a data value is quoted. | `VARCHAR` | `"` |
| `sample_size` | The number of sample rows for [auto detection of parameters](auto_detection). | `BIGINT` | 20480 |
| `skip` | The number of lines at the top of the file to skip. | `BIGINT` | 0 |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) | `VARCHAR` | (empty) |
| `types` or `dtypes` | The column types as either a list (by position) or a struct (by name). [Example here](tips#override-the-types-of-specific-columns). | `VARCHAR[]` or `STRUCT` | (empty) |
| `union_by_name` | Whether the columns of multiple schemas should be [unified by name](../multiple_files/combining_schemas), rather than by position. | `BOOL` | `false` |

## CSV Functions

> DuckDB 0.9.3-dev and the upcoming v0.10.0 versions introduce breaking changes to the `read_csv` function.
> Namely, The `read_csv` function now attempts auto-detecting the CSV parameters, making its behavior identical to the [old `read_csv_auto` function](../../../docs/archive/0.9.2/data/csv/overview#read_csv_auto-function).
> If you would like to use `read_csv` with its old behavior, turn off the auto-detection manually by using `read_csv(..., auto_detect = false)`.

The `read_csv` automatically attempts to figure out the correct configuration of the CSV reader using the [CSV sniffer](/2023/10/27/csv-sniffer). It also automatically deduces types of columns. If the CSV file has a header, it will use the names found in that header to name the columns. Otherwise, the columns will be named `column0, column1, column2, ...`. An example with the [`flights.csv`](/data/flights.csv) file:

```sql
SELECT * FROM read_csv('flights.csv');
```

<div class="narrow_table"></div>

|FlightDate|UniqueCarrier| OriginCityName  | DestCityName  |
|----------|-------------|-----------------|---------------|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

The path can either be a relative path (relative to the current working directory) or an absolute path.

We can use `read_csv` to create a persistent table as well:

```sql
CREATE TABLE ontime AS SELECT * FROM read_csv('flights.csv');
DESCRIBE ontime;
```

<div class="narrow_table"></div>

|Field         |Type   |Null|Key |Default|Extra|
|--------------|-------|----|----|-------|-----|
|FlightDate    |DATE   |YES |NULL|NULL   |NULL |
|UniqueCarrier |VARCHAR|YES |NULL|NULL   |NULL |
|OriginCityName|VARCHAR|YES |NULL|NULL   |NULL |
|DestCityName  |VARCHAR|YES |NULL|NULL   |NULL |

```sql
SELECT * FROM read_csv('flights.csv', sample_size = 20000);
```

If we set `delim`/`sep`, `quote`, `escape`, or `header` explicitly, we can bypass the automatic detection of this particular parameter:

```sql
SELECT * FROM read_csv('flights.csv', header = true);
```

Multiple files can be read at once by providing a glob or a list of files. Refer to the [multiple files section](../multiple_files/overview) for more information.

## Writing Using the `COPY` Statement

The [`COPY` statement](../../sql/statements/copy#copy-to) can be used to load data from a CSV file into a table. This statement has the same syntax as the one used in PostgreSQL. To load the data using the `COPY` statement, we must first create a table with the correct schema (which matches the order of the columns in the CSV file and uses types that fit the values in the CSV file). `COPY` detects the CSV's configuration options automatically.

```sql
CREATE TABLE ontime (
    flightdate DATE,
    uniquecarrier VARCHAR,
    origincityname VARCHAR,
    destcityname VARCHAR
);
COPY ontime FROM 'flights.csv';
SELECT * FROM ontime;
```

<div class="narrow_table"></div>

|flightdate|uniquecarrier| origincityname  | destcityname  |
|----------|-------------|-----------------|---------------|
|1988-01-01|AA           |New York, NY     |Los Angeles, CA|
|1988-01-02|AA           |New York, NY     |Los Angeles, CA|
|1988-01-03|AA           |New York, NY     |Los Angeles, CA|

If we want to manually specify the CSV format, we can do so using the configuration options of `COPY`.

```sql
CREATE TABLE ontime (flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'flights.csv' (DELIMITER '|', HEADER);
SELECT * FROM ontime;
```

## Reading Faulty CSV Files

DuckDB supports reading erroneous CSV files. For details, see the [Reading Faulty CSV Files page](reading_faulty_csv_files).

## Limitations

The CSV reader only supports input files using UTF-8 character encoding. For CSV files using different encodings, use e.g. the [`iconv` command-line tool](https://linux.die.net/man/1/iconv) to convert them to UTF-8.

## Pages in This Section
