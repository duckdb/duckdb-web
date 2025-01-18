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
| `all_varchar` | Skip type detection and assume all columns are of type `VARCHAR`. This option is only supported by the `read_csv` function. | `BOOL` | `false` |
| `allow_quoted_nulls` | Allow the conversion of quoted values to `NULL` values | `BOOL` | `true` |
| `auto_detect` | [Auto detect CSV parameters]({% link docs/data/csv/auto_detection.md %}). | `BOOL` | `true` |
| `auto_type_candidates` | Types that the sniffer uses when detecting column types. The `VARCHAR` type is always included as a fallback option. See [example](#auto_type_candidates-details). | `TYPE[]` | [default types](#auto_type_candidates-details) |
| `buffer_size` | Size of the buffers used to read files. Must be large enough to accommodate at least four lines and can significantly impact performance. | `BIGINT` | [`16 * max_line_size` |
| `columns` | Column names and types, as a struct (e.g., `{'col1': 'INTEGER', 'col2': 'VARCHAR'}`). Using this option implies that auto detection is not used. | `STRUCT` | (empty) |
| `comment` | Character used to start comments, either at the start or within a line. | `VARCHAR` | `` |
| `compression` | Method used to compress the CSV file. By default this is detected automatically from the file extension (e.g., `t.csv.gz` will use gzip, `t.csv` will use `none`). Options are `none`, `gzip`, `zstd`. | `VARCHAR` | `auto` |
| `dateformat` or `date_format` | Date format used when parsing and writing dates. See [Date Format]({% link docs/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |
| `decimal_separator` | Decimal separator for numbers. | `VARCHAR` | `.` |
| `delimiter` | Delimiter character used to separate columns within each row. Alias for `sep`. This option is only available in the `COPY` statement. | `VARCHAR` | `,` |
| `delim` | Delimiter character used to separate columns within each row. Alias for `sep`. | `VARCHAR` | `,` |
| `escape` | String used to escape the `quote` character within quoted values. | `VARCHAR` | `"` |
| `encoding` | Encoding used by the CSV file.  | `VARCHAR` | `utf-8` |
| `filename` | Add path of the containing file to each row, as a string column named `filename`. Relative or absolute paths are returned depending on the path or glob pattern provided to `read_csv`, not just filenames. | `BOOL` | `false` |
| `force_not_null` | Do not match values in the the specified columns values against the `NULL` string. In the default case where the `NULL` string is empty, this means that empty values are read as zero-length strings instead of `NULL`s. | `VARCHAR[]` | `[]` |
| `header` | First line is a header with the column names. | `BOOL` | `false` |
| `hive_partitioning` | Interpret the path as a [Hive partitioned path]({% link docs/data/partitioning/hive_partitioning.md %}). | `BOOL` | `false` |
| `ignore_errors` | Ignore any parsing errors encountered. | `BOOL` | `false` |
| `max_line_size` or `maximum_line_size` | Maximum line size, in bytes. | `BIGINT` | 2000000 |
| `names` or `column_names` | Column names, as a list. See [example]({% link docs/data/csv/tips.md %}#provide-names-if-the-file-does-not-contain-a-header). | `VARCHAR[]` | (empty) |
| `new_line` | New line character(s). Options are `'\r'`,`'\n'`, or `'\r\n'`. The CSV parser only distinguishes between single-character and double-character line delimiters. Therefore, it does not differentiate between `'\r'` and `'\n'`.| `VARCHAR` | (empty) |
| `normalize_names` | Normalize column names, removing any non-alphanumeric characters from them. | `BOOL` | `false` |
| `null_padding` | Pad the remaining columns on the right with `NULL` values when a row lacks columns. | `BOOL` | `false` |
| `nullstr` or `null` | Specifies a list of strings that represent a `NULL` value. | `VARCHAR` or `VARCHAR[]` | (empty) |
| `parallel` | Use the parallel CSV reader. | `BOOL` | `true` |
| `quote` | String used to quote values. | `VARCHAR` | `"` |
| `rejects_scan` | Name of a temporary table where scan information for faulty CSV files is stored.  | `VARCHAR` | `reject_scans` |
| `rejects_table` | Name of a temporary table where information on faulty lines is stored.  | `VARCHAR` | `reject_errors` |
| `rejects_limit` | Upper limit on the number of faulty lines from a CSV file that are recorded in the rejects table. Setting this to `0` means that no limit is applied.  | `BIGINT` | `0` |
| `rfc_4180` | Adhere to the RFC 4180 standard. Setting this to `false` may allow the parser to read structurally incorrect files. | `BOOL` | `false` |
| `sample_size` | Number of sample rows for [auto detection of parameters]({% link docs/data/csv/auto_detection.md %}). | `BIGINT` | 20480 |
| `sep` | Delimiter character used to separate columns within each row. Alias for `delim`. | `VARCHAR` | `,` |
| `skip` | Number of lines to skip at at the top of each file. | `BIGINT` | 0 |
| `store_rejects` | Skip any lines with errors and store them in the rejects table. | `BOOL` | `false` |
| `timestampformat` or `timestamp_format` | Date format used when parsing and writing timestamps. See [Date Format]({% link docs/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |
| `types` or `dtypes` or `column_types` | Column types, as either a list (by position) or a struct (by name). [Example here]({% link docs/data/csv/tips.md %}#override-the-types-of-specific-columns). | `VARCHAR[]` or `STRUCT` | (empty) |
| `union_by_name` | Unify columns of multiple schemas [by name]({% link docs/data/multiple_files/combining_schemas.md %}#union-by-name) rather than by position. Using this option increases memory consumption. | `BOOL` | `false` |

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
