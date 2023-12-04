---
layout: docu
title: CSV Import
redirect_from:
  - /docs/data/csv
---

## Examples

```sql
-- read a CSV file from disk, auto-infer options
SELECT * FROM 'flights.csv';
-- read_csv with custom options
SELECT * FROM read_csv('flights.csv', delim = '|', header = true, columns = {'FlightDate': 'DATE', 'UniqueCarrier': 'VARCHAR', 'OriginCityName': 'VARCHAR', 'DestCityName': 'VARCHAR'});
-- read a CSV from stdin, auto-infer options
cat data/csv/issue2471.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"

-- read a CSV file into a table
CREATE TABLE ontime (FlightDate DATE, UniqueCarrier VARCHAR, OriginCityName VARCHAR, DestCityName VARCHAR);
COPY ontime FROM 'flights.csv';
-- alternatively, create a table without specifying the schema manually
CREATE TABLE ontime AS SELECT * FROM 'flights.csv';
-- we can use the FROM-first syntax to omit 'SELECT *'
CREATE TABLE ontime AS FROM 'flights.csv';

-- write the result of a query to a CSV file
COPY (SELECT * FROM ontime) TO 'flights.csv' WITH (HEADER 1, DELIMITER '|');
-- we can use the FROM-first syntax to omit 'SELECT *'
COPY (FROM ontime) TO 'flights.csv' WITH (HEADER 1, DELIMITER '|');
```

## CSV Loading

CSV loading, i.e., importing CSV files to the database, is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a challenge. CSV files come in many different varieties, are often corrupt, and do not have a schema. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file using the [CSV sniffer](/2023/10/27/csv-sniffer). This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file. See the [auto detection page](auto_detection) for more information.

## Parameters

Below are parameters that can be passed to the CSV reader. These parameters are accepted by both the [`COPY` statement](../../sql/statements/copy#copy-to) and the [`read_csv` function](#read_csv-function).

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `all_varchar` | Option to skip type detection for CSV parsing and assume all columns to be of type `VARCHAR`. | `BOOL` | `false` |
| `auto_detect` | Enables [auto detection of CSV parameters](auto_detection). | `BOOL` | `true` |
| `auto_type_candidates` | This option allows you to specify the types that the sniffer will use when detecting CSV column types, e.g., `SELECT * FROM read_csv('csv_file.csv', auto_type_candidates=['BIGINT', 'DATE'])`. The `VARCHAR` type is always included in the detected types (as a fallback option). | `TYPE[]` | `['SQLNULL', 'BOOLEAN', 'BIGINT', 'DOUBLE', 'TIME', 'DATE', 'TIMESTAMP', 'VARCHAR']` |
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

The `read_csv` automatically attempts to figure out the correct configuration of the CSV reader using the [CSV sniffer](/2023/10/27/csv-sniffer)). It also automatically deduces types of columns. If the CSV file has a header, it will use the names found in that header to name the columns. Otherwise, the columns will be named `column0, column1, column2, ...`. An example with the [`flights.csv`](/data/flights.csv) file:

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
CREATE TABLE ontime (flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
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
Reading faulty CSV files is possible by utilizing the `ignore_errors` option. With that option set, rows containing data that would otherwise cause the CSV Parser to generate an error will be ignored.

 For example, consider the following CSV file:

```csv
Pedro,31
Oogie Boogie, three
```

If you read the CSV file, specifying that the first column is a varchar and the second column is an integer, the file would fail, as the string `three` cannot be converted to an integer.
For example:
```sql
from read_csv('data.csv', columns={'name':'varchar', 'age':'integer'})
```
Will throw a casting error.


However, with `ignore_errors` set, the second row of the file is skipped, outputting only the complete first row. For example:
```sql
from read_csv('data.csv', columns={'name':'varchar', 'age':'integer'}, ignore_errors = true)
```
Outputs:

| name | age |
|------|-----|
|Pedro | 31  |


One should note that the CSV Parser is affected by the projection pushdown optimization. Hence, if we were to select only the name column, both rows would be considered valid, as the casting error on the age would never occur. For example:

```sql
select name from read_csv('data.csv', columns={'name':'varchar', 'age':'integer'})
```
Outputs:

|     name     |
|--------------|
|     Pedro    |
| Oogie Boogie | 

## Retrieving Faulty CSV Lines
Being able to read faulty CSV files is important, but for many data cleaning operations, it is also necessary to know exactly which lines are corrupted and what errors the parser discovered on them. For scenarios like these, it is possible to use DuckDB's CSV Rejects Tables. It is important to note that the rejects tables can only be used when `ignore_errors` is set, and currently, only stores casting errors.

The CSV Rejects Tables returns the following information:
| Column Name | Description | Type |
|:--|:-----|:-|
| `file` | File path.| `VARCHAR` |
| `line` | Line number, from the CSV File, where the error occured.| `INTEGER` |
| `column` | Column number, from the CSV File, where the error occured.| `INTEGER` |
| `column_name` | Column name, from the CSV File, where the error occured.| `VARCHAR` |
| `parsed_value` | The value, where the casting error happened, in a string format.| `VARCHAR` |
| `recovery_columns` | An optional primary key of the CSV File.| `STRUCT{NAME:VALUE}` |
| `error` | Exact error encountered by the parser. | `VARCHAR` |

### Parameters

The parameters listed below are used in the `read_csv` function to configure the CSV Rejects Tables.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `rejects_table` | Name of a temporary table where the information of the faulty lines of a csv file are stored.| `VARCHAR` | (empty) |
| `rejects_limit` | Upper limit on the number of faulty records from a CSV file that will be recorded in the rejects table. 0 is used when no limit should be applied.| `BIGINT` | 0 |
| `rejects_recovery_columns` | Column values that serve as a primary key to the csv file. The are stored in the CSV Rejects Table to help identify the faulty tuples.| `VARCHAR[]` | (empty) |

To store the information of the faulty csv lines in a rejects table, the user must simply provide the rejects table name in the`rejects_table` option. For example:
```sql
from read_csv('data.csv', columns={'name':'varchar', 'age':'integer'}, rejects_table='rejects_table', ignore_errors = true);
```

You can then query the `rejects_table` table, to retrieve information about the rejected tuples. For example:
```sql
select * from rejects_table;
```
Outputs:

|   file   | line | column | column_name | parsed_value |                     error                      |
|----------|------|--------|-------------|--------------|------------------------------------------------|
| data.csv |  2   |    1   |     age     |     three    | Could not convert string ' three' to 'INTEGER' |


Aditionally, the `name` column could also be provided as a primary key via the `rejects_recovery_columns` option to provide more information over the faulty lines. For example:
```sql
from read_csv('data.csv', columns={'name':'varchar', 'age':'integer'}, rejects_table='rejects_table', rejects_recovery_columns = '[name]', ignore_errors = true);
```

Reading from the `rejects_table` will return:

|   file   | line | column | column_name | parsed_value |     recovery_columns     |                     error                      |
|----------|------|--------|-------------|--------------|--------------------------|------------------------------------------------|
| data.csv |  2   |    1   |     age     |     three    | {'name': 'Oogie Boogie'} | Could not convert string ' three' to 'INTEGER' |

## Pages in This Section
