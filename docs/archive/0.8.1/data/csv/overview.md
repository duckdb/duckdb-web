---
layout: docu
title: CSV Loading
redirect_from:
  - /docs/archive/0.8.1/data/csv
---

### Examples

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

### CSV Loading
CSV loading is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a challenge. CSV files come in many different varieties, are often corrupt, and do not have a schema. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file. See the [auto detection page](auto_detection) for more information.

Below are parameters that can be passed in to the CSV reader. 

# Parameters

| Name | Description | Type | Default |
|:---|:---|:----|:----|
| `all_varchar` | Option to skip type detection for CSV parsing and assume all columns to be of type VARCHAR. | bool | false |
| `auto_detect` | Enables [auto detection of parameters](auto_detection) | bool | true |
| `columns` | A struct that specifies the column names and column types contained within the CSV file (e.g. `{'col1': 'INTEGER', 'col2': 'VARCHAR'}`). | `struct` | `(empty)` |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g. `t.csv.gz` will use gzip, `t.csv` will use `none`). Options are `none`, `gzip`, `zstd`. | varchar | auto |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../../sql/functions/dateformat) | varchar | `(empty)` |
| `decimal_separator` | The decimal separator of numbers | varchar | `.` |
| `delim` or `sep` | Specifies the string that separates columns within each row (line) of the file. | varchar | `,` |
| `escape` | Specifies the string that should appear before a data character sequence that matches the `quote` value. | varchar | `"` |
| `filename` | Whether or not an extra `filename` column should be included in the result. | bool | false |
| `force_not_null` | Do not match the specified columns' values against the NULL string. In the default case where the NULL string is empty, this means that empty values will be read as zero-length strings rather than NULLs. | varchar[] | [] |
| `header` | Specifies that the file contains a header line with the names of each column in the file. | bool | false |
| `hive_partitioning` | Whether or not to interpret the path as a [hive partitioned path](../partitioning/hive_partitioning). | bool | false |
| `ignore_errors` | Option to ignore any parsing errors encountered - and instead ignore rows with errors. | bool | false |
| `max_line_size` | The maximum line size in bytes | bigint | 2097152 |
| `names` | The column names as a list. [Example here](tips#provide-names-if-the-file-does-not-contain-a-header). | varchar[] | `(empty)` |
| `new_line` | Set the new line character(s) in the file. Options are `'\r'`,`'\n'`, or `'\r\n'`. | varchar | `(empty)` |
| `normalize_names` | Boolean value that specifies whether or not column names should be normalized, removing any non-alphanumeric characters from them. | bool | false |
| `nullstr` | Specifies the string that represents a NULL value. | varchar | `(empty)` |
| `parallel` | Whether or not the experimental parallel CSV reader is used. | bool | false |
| `quote` | Specifies the quoting string to be used when a data value is quoted. | varchar | `"` |
| `sample_size` | The number of sample rows for [auto detection of parameters](auto_detection). | bigint | 20480 |
| `skip` | The number of lines at the top of the file to skip. | bigint | 0 |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) | varchar | `(empty)` |
| `types` or `dtypes` | The column types as either a list (by position) or a struct (by name). [Example here](tips#override-the-types-of-specific-columns). | varchar[] or struct | `(empty)` |
| `union_by_name` | Whether the columns of multiple schemas should be [unified by name](../multiple_files/combining_schemas), rather than by position. | bool | false |

### Writing

The contents of tables or the result of queries can be written directly to a CSV file using the `COPY` statement. See the [COPY documentation](../../sql/statements/copy#copy-to) for more information.

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

Multiple files can be read at once by providing a glob or a list of files. Refer to the [multiple files section](../multiple_files/overview) for more information.


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

More on the copy statement can be found [here](/docs/sql/statements/copy.html).
