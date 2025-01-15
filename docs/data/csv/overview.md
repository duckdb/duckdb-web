---
layout: docu
title: CSV Import
redirect_from:
  - /docs/data/csv
---

## Examples

The following examples use the [`flights.csv`](/data/flights.csv) file.

Read a CSV file from disk, auto-infer options:

```sql
SELECT * FROM 'flights.csv';
```

Use the `read_csv` function with custom options:

```sql
SELECT *
FROM read_csv('flights.csv',
    delim = '|',
    header = true,
    columns = {
        'FlightDate': 'DATE',
        'UniqueCarrier': 'VARCHAR',
        'OriginCityName': 'VARCHAR',
        'DestCityName': 'VARCHAR'
    });
```

Read a CSV from stdin, auto-infer options:

```bash
cat flights.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"
```

Read a CSV file into a table:

```sql
CREATE TABLE ontime (
    FlightDate DATE,
    UniqueCarrier VARCHAR,
    OriginCityName VARCHAR,
    DestCityName VARCHAR
);
COPY ontime FROM 'flights.csv';
```

Alternatively, create a table without specifying the schema manually using a [`CREATE TABLE .. AS SELECT` statement]({% link docs/sql/statements/create_table.md %}#create-table--as-select-ctas):

```sql
CREATE TABLE ontime AS
    SELECT * FROM 'flights.csv';
```

We can use the [`FROM`-first syntax]({% link docs/sql/query_syntax/from.md %}#from-first-syntax) to omit `SELECT *`.

```sql
CREATE TABLE ontime AS
    FROM 'flights.csv';
```

Write the result of a query to a CSV file.

```sql
COPY (SELECT * FROM ontime) TO 'flights.csv' WITH (HEADER, DELIMITER '|');
```

If we serialize the entire table, we can simply refer to it with its name.

```sql
COPY ontime TO 'flights.csv' WITH (HEADER, DELIMITER '|');
```

## CSV Loading

CSV loading, i.e., importing CSV files to the database, is a very common, and yet surprisingly tricky, task. While CSVs seem simple on the surface, there are a lot of inconsistencies found within CSV files that can make loading them a challenge. CSV files come in many different varieties, are often corrupt, and do not have a schema. The CSV reader needs to cope with all of these different situations.

The DuckDB CSV reader can automatically infer which configuration flags to use by analyzing the CSV file using the [CSV sniffer]({% post_url 2023-10-27-csv-sniffer %}). This will work correctly in most situations, and should be the first option attempted. In rare situations where the CSV reader cannot figure out the correct configuration it is possible to manually configure the CSV reader to correctly parse the CSV file. See the [auto detection page]({% link docs/data/csv/auto_detection.md %}) for more information.

## Parameters

Below are parameters that can be passed to the CSV reader. These parameters are accepted by the [`read_csv` function](#csv-functions). But not all parameters are accepted by the [`COPY` statement]({% link docs/sql/statements/copy.md %}#copy-to).

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `all_varchar` | Option to skip type detection for CSV parsing and assume all columns to be of type `VARCHAR`. This option is only supported by the `read_csv` function. | `BOOL` | `false` |
| `allow_quoted_nulls` | Option to allow the conversion of quoted values to `NULL` values | `BOOL` | `true` |
| `auto_detect` | Enables [auto detection of CSV parameters]({% link docs/data/csv/auto_detection.md %}). | `BOOL` | `true` |
| `auto_type_candidates` | This option allows you to specify the types that the sniffer will use when detecting CSV column types. The `VARCHAR` type is always included in the detected types (as a fallback option). See [example](#auto_type_candidates-details). | `TYPE[]` | [default types](#auto_type_candidates-details) |
| `buffer_size` | This option allows you to specify the size of the buffers used to read the file. It is important to note that the buffer must be large enough to always accommodate at least four lines of the CSV file. Altering this option can significantly impact performance. | `BIGINT` | [`16 * max_line_size` |
| `columns` | A struct that specifies the column names and column types contained within the CSV file (e.g., `{'col1': 'INTEGER', 'col2': 'VARCHAR'}`). Using this option implies that auto detection is not used. | `STRUCT` | (empty) |
| `comment` | The character used to represent a comment in a CSV file. Comment characters can either cause an entire line to be ignored or appear anywhere within a line, causing the parser to ignore the rest of it. | `VARCHAR` | `` |
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `t.csv.gz` will use gzip, `t.csv` will use `none`). Options are `none`, `gzip`, `zstd`. | `VARCHAR` | `auto` |
| `dateformat` or `date_format` | Specifies the date format to use when parsing dates. See [Date Format]({% link docs/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |
| `decimal_separator` | The decimal separator of numbers. | `VARCHAR` | `.` |
| `delimiter` | Specifies the delimiter character that separates columns within each row (line) of the file. Alias for `sep`. This option is only available in the `COPY` statement. | `VARCHAR` | `,` |
| `delim` | Specifies the delimiter character that separates columns within each row (line) of the file. Alias for `sep`. | `VARCHAR` | `,` |
| `escape` | Specifies the string that should appear before a data character sequence that matches the `quote` value. | `VARCHAR` | `"` |
| `encoding` | Specifies the encoding used by the CSV file and ensures conversion from the source encoding to `UTF-8`.  | `VARCHAR` | `utf-8` |
| `filename` | Whether or not an extra `filename` column should be included in the result. | `BOOL` | `false` |
| `force_not_null` | Do not match the specified columns' values against the `NULL` string. In the default case where the `NULL` string is empty, this means that empty values will be read as zero-length strings rather than `NULL`s. | `VARCHAR[]` | `[]` |
| `header` | Specifies that the file contains a header line with the names of each column in the file. | `BOOL` | `false` |
| `hive_partitioning` | Whether or not to interpret the path as a [Hive partitioned path]({% link docs/data/partitioning/hive_partitioning.md %}). | `BOOL` | `false` |
| `ignore_errors` | Option to ignore any parsing errors encountered – and instead ignore rows with errors. | `BOOL` | `false` |
| `max_line_size` or `maximum_line_size` | The maximum line size in bytes. | `BIGINT` | 2000000 |
| `names` or `column_names` | The column names as a list, see [example]({% link docs/data/csv/tips.md %}#provide-names-if-the-file-does-not-contain-a-header). | `VARCHAR[]` | (empty) |
| `new_line` | Set the new line character(s) in the file. Options are `'\r'`,`'\n'`, or `'\r\n'`. Note that the CSV parser only distinguishes between single-character and double-character line delimiters. Therefore, it does not differentiate between `'\r'` and `'\n'`.| `VARCHAR` | (empty) |
| `normalize_names` | Boolean value that specifies whether or not column names should be normalized, removing any non-alphanumeric characters from them. | `BOOL` | `false` |
| `null_padding` | If this option is enabled, when a row lacks columns, it will pad the remaining columns on the right with `NULL` values. | `BOOL` | `false` |
| `nullstr` or `null` | Specifies the string that represents a `NULL` value or (since v0.10.2) a list of strings that represent a `NULL` value. | `VARCHAR` or `VARCHAR[]` | (empty) |
| `parallel` | Whether or not the parallel CSV reader is used. | `BOOL` | `true` |
| `quote` | Specifies the quoting string to be used when a data value is quoted. | `VARCHAR` | `"` |
| `rejects_scan` | Name of a temporary table where the information of the scan information of faulty CSV file are stored.  | `VARCHAR` | `reject_scans` |
| `rejects_table` | Name of a temporary table where the information of the faulty lines of a CSV file are stored  | `VARCHAR` | `reject_errors` |
| `rejects_limit` | Upper limit on the number of faulty records from a CSV file that will be recorded in the rejects table. 0 is used when no limit should be applied.  | `BIGINT` | `0` |
| `rfc_4180` | Specifies whether the parser should adhere to the RFC 4180 standard. Setting this to `false may` allow the parser to read structurally incorrect files. | `BOOL` | `false` |
| `sample_size` | The number of sample rows for [auto detection of parameters]({% link docs/data/csv/auto_detection.md %}). | `BIGINT` | 20480 |
| `sep` | Specifies the delimiter character that separates columns within each row (line) of the file. Alias for `delim`. | `VARCHAR` | `,` |
| `skip` | The number of lines at the top of the file to skip. | `BIGINT` | 0 |
| `store_rejects` | If set to true, any errors in the file will be skipped and stored in the default rejects temporary tables. | `BOOL` | `false` |
| `timestampformat` or `timestamp_format` | Specifies the date format to use when parsing timestamps. See [Date Format]({% link docs/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |
| `types` or `dtypes` or `column_types` | The column types as either a list (by position) or a struct (by name). [Example here]({% link docs/data/csv/tips.md %}#override-the-types-of-specific-columns). | `VARCHAR[]` or `STRUCT` | (empty) |
| `union_by_name` | Whether the columns of multiple schemas should be [unified by name]({% link docs/data/multiple_files/combining_schemas.md %}#union-by-name), rather than by position. Note that using this option increases memory consumption. | `BOOL` | `false` |

### `auto_type_candidates` Details

The `auto_type_candidates` option lets you specify the data types that should be considered by the CSV reader for [column data type detection]({% link docs/data/csv/auto_detection.md %}#type-detection).
Usage example:

```sql
SELECT * FROM read_csv('csv_file.csv', auto_type_candidates = ['BIGINT', 'DATE']);
```

The default value for the `auto_type_candidates` option is `['SQLNULL', 'BOOLEAN', 'BIGINT', 'DOUBLE', 'TIME', 'DATE', 'TIMESTAMP', 'VARCHAR']`.

## CSV Functions

The `read_csv` automatically attempts to figure out the correct configuration of the CSV reader using the [CSV sniffer]({% post_url 2023-10-27-csv-sniffer %}). It also automatically deduces types of columns. If the CSV file has a header, it will use the names found in that header to name the columns. Otherwise, the columns will be named `column0, column1, column2, ...`. An example with the [`flights.csv`](/data/flights.csv) file:

```sql
SELECT * FROM read_csv('flights.csv');
```

| FlightDate | UniqueCarrier | OriginCityName |  DestCityName   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

The path can either be a relative path (relative to the current working directory) or an absolute path.

We can use `read_csv` to create a persistent table as well:

```sql
CREATE TABLE ontime AS
    SELECT * FROM read_csv('flights.csv');
DESCRIBE ontime;
```

|  column_name   | column_type | null | key  | default | extra |
|----------------|-------------|------|------|---------|-------|
| FlightDate     | DATE        | YES  | NULL | NULL    | NULL  |
| UniqueCarrier  | VARCHAR     | YES  | NULL | NULL    | NULL  |
| OriginCityName | VARCHAR     | YES  | NULL | NULL    | NULL  |
| DestCityName   | VARCHAR     | YES  | NULL | NULL    | NULL  |

```sql
SELECT * FROM read_csv('flights.csv', sample_size = 20_000);
```

If we set `delim` / `sep`, `quote`, `escape`, or `header` explicitly, we can bypass the automatic detection of this particular parameter:

```sql
SELECT * FROM read_csv('flights.csv', header = true);
```

Multiple files can be read at once by providing a glob or a list of files. Refer to the [multiple files section]({% link docs/data/multiple_files/overview.md %}) for more information.

## Writing Using the `COPY` Statement

The [`COPY` statement]({% link docs/sql/statements/copy.md %}#copy-to) can be used to load data from a CSV file into a table. This statement has the same syntax as the one used in PostgreSQL. To load the data using the `COPY` statement, we must first create a table with the correct schema (which matches the order of the columns in the CSV file and uses types that fit the values in the CSV file). `COPY` detects the CSV's configuration options automatically.

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

| flightdate | uniquecarrier | origincityname |  destcityname   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

If we want to manually specify the CSV format, we can do so using the configuration options of `COPY`.

```sql
CREATE TABLE ontime (flightdate DATE, uniquecarrier VARCHAR, origincityname VARCHAR, destcityname VARCHAR);
COPY ontime FROM 'flights.csv' (DELIMITER '|', HEADER);
SELECT * FROM ontime;
```

## Reading Faulty CSV Files

DuckDB supports reading erroneous CSV files. For details, see the [Reading Faulty CSV Files page]({% link docs/data/csv/reading_faulty_csv_files.md %}).

## Limitations

The CSV reader only supports input files using UTF-8 character encoding. For CSV files using different encodings, use e.g., the [`iconv` command-line tool](https://linux.die.net/man/1/iconv) to convert them to UTF-8. For example:

```bash
iconv -f ISO-8859-2 -t UTF-8 input.csv > input-utf-8.csv
```

## Order Preservation

The CSV reader respects the `preserve_insertion_order` [configuration option]({% link docs/configuration/overview.md %}) to [preserve insertion order]({% link docs/sql/dialect/order_preservation.md %}).
When `true` (the default), the order of the rows in the resultset returned by the CSV reader is the same as the order of the corresponding lines read from the file(s).
When `false`, there is no guarantee that the order is preserved.
