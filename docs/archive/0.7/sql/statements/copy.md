---
layout: docu
title: Copy
selected: Documentation/SQL/Copy
expanded: SQL
railroad: statements/copy.js
---
`COPY` moves data between DuckDB tables and external Comma Separated Value (CSV) or Parquet files. The Parquet [extension](/docs/extensions/overview) must be installed in order to operate on Parquet files, although many clients bundle the Parquet extension by default (Ex: Python, the Command Line Interface/CLI etc.). For more Parquet examples, see the [Parquet Files page](/docs/data/parquet).

# CSV or Parquet Import
`COPY ... FROM` imports data into DuckDB from an external CSV or Parquet file into an existing table. The data is appended to whatever data is in the table already. The amount of columns inside the file must match the amount of columns in the table `table_name`, and the contents of the columns must be convertible to the column types of the table. In case this is not possible, an error will be thrown.

If a list of columns is specified, `COPY` will only copy the data in the specified columns from the file. If there are any columns in the table that are not in the column list, `COPY ... FROM` will insert the default values for those columns

```sql
-- Copy the contents of a comma-separated file 'test.csv' without a header into the table 'test'
COPY test FROM 'test.csv';
-- Copy the contents of a comma-separated file with a header into the 'category' table
COPY category FROM 'categories.csv' ( HEADER );
-- Copy the contents of 'lineitem.tbl' into the 'lineitem' table, where the contents are delimited by a pipe character ('|')
COPY lineitem FROM 'lineitem.tbl' ( DELIMITER '|' );
-- Copy the contents of 'lineitem.tbl' into the 'lineitem' table, where the delimiter, quote character, and presence of a header are automatically detected
COPY lineitem FROM 'lineitem.tbl' ( AUTO_DETECT TRUE );
-- Read the contents of a comma-separated file 'names.csv' into the 'name' column of the 'category' table. Any other columns of this table are filled with their default value.
COPY category(name) FROM 'names.csv';
-- Read the contents of a parquet file 'lineitem.parquet' into the lineitem table
COPY lineitem FROM 'lineitem.parquet' ( FORMAT PARQUET );
```

## Syntax
<div id="rrdiagram1"></div>

# CSV or Parquet Export
`COPY ... TO` exports data from DuckDB to an external CSV or Parquet file. It has mostly the same set of options as `COPY ... FROM`, however, in the case of `COPY ... TO` the options specify how the file should be written to disk. Any file created by `COPY ... TO` can be copied back into the database by using `COPY ... FROM` with a similar set of options.

The `COPY ... TO` function can be called specifying either a table name, or a query. When a table name is specified, the contents of the entire table will be written into the resulting file. When a query is specified, the query is executed and the result of the query is written to the resulting file.

```sql
-- Copy the contents of the 'lineitem' table to the file 'lineitem.tbl', where the columns are delimited by a pipe character ('|'), including a header line.
COPY lineitem TO 'lineitem.tbl' ( DELIMITER '|', HEADER );
-- Copy the l_orderkey column of the 'lineitem' table to the file 'orderkey.tbl'
COPY lineitem(l_orderkey) TO 'orderkey.tbl' ( DELIMITER '|' );
-- Copy the result of a query to the file 'query.csv', including a header with column names
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.csv' WITH (HEADER 1, DELIMITER ',');
-- Copy the result of a query to the Parquet file 'query.parquet'
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.parquet' (FORMAT PARQUET);
```

## Syntax
<div id="rrdiagram2"></div>

# Parameters

| Name | Description |
|:---|:---|
| `table_name` | The name (optionally schema-qualified) of an existing table. |
| `column_name` | An optional list of columns to be copied. If no column list is specified, all columns of the table will be copied. |
| `filename` | The path and name of the input or output file. |
| `boolean` | Specifies whether the selected option should be turned on or off. You can write `TRUE`, `ON`, or `1` to enable the option, and `FALSE`, `OFF`, or `0` to disable it. The `boolean` value can also be omitted, in which case `TRUE` is assumed. |

## Copy Options

Zero or more copy options may be provided as a part of the copy operation. The `WITH` specifier is optional, but if any options are specified, the parentheses are required. Parameter values can be passed in with or without wrapping in single quotes. See the above note about `boolean` options as well. 

| Name | To / From | Description |
|:---|:---|:---|
| `FORMAT` | To & From | Specifies the copy function to use. This defaults to `CSV`, but other options can be available (e.g. `PARQUET`, `JSON`). |
| `DELIMITER` | To & From | Specifies the string that separates columns within each row (line) of the file. The default value is a comma (`,`). |
| `NULL` | To & From | Specifies the string that represents a NULL value. The default is an empty string. Please note that in `COPY ... FROM` both an unquoted empty string and a quoted empty string represent a NULL value. If any other NULL string is specified, again both its quoted and its unquoted appearance represent a NULL value. `COPY ... TO` does not quote NULL values on output, even if `FORCE_QUOTE` is true. |
| `HEADER` | To & From | Specifies that the file contains a header line with the names of each column in the file. Thus, `COPY ... FROM` ignores the first line when importing data, whereas on output (`COPY ... TO`) the first line of the file contains the column names of the exported columns. |
| `QUOTE` | To & From | Specifies the quoting string to be used when a data value is quoted. The default is double-quote (`"`). |
| `ESCAPE` | To & From | Specifies the string that should appear before a data character sequence that matches the `QUOTE` value. The default is the same as the `QUOTE` value (so that the quoting string is doubled if it appears in the data). |
| `DATEFORMAT` | To & From | Specifies the date format to use when parsing dates. See [Date Format](../../sql/functions/dateformat) |
| `TIMESTAMPFORMAT` | To & From | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) |
| `FORCE_QUOTE` | To | Forces quoting to be used for all non-NULL values in each specified column. `NULL` output is never quoted. If `*` is specified, non-NULL values will be quoted in all columns. |
| `FORCE_NOT_NULL` | From | Do not match the specified columns' values against the NULL string. In the default case where the NULL string is empty, this means that empty values will be read as zero-length strings rather than NULLs. |
| `ENCODING` | To & From | If this option is used, its value must be `UTF8`. With any other encoding an error will be thrown. |
| `AUTO_DETECT` | From | Option for CSV parsing. If `TRUE`, the parser will attempt to detect the input format and data types automatically. `DELIM`/`SEP`, `QUOTE`, `ESCAPE`, and `HEADER` parameters become optional. |
| `SAMPLE_SIZE` | From | Option to define number of sample rows for automatic CSV type detection. Chunks of sample rows will be drawn from different locations of the input file. Set to `-1` to scan the entire input file. Only the first max. 1024 rows will be used for dialect detection. |
| `ALL_VARCHAR` | From | Option to skip type detection for CSV parsing and assume all columns to be of type VARCHAR. |
| `COMPRESSION` | To & From | Option to compress the file. Value can be `UNCOMPRESSED`, `GZIP`, `SNAPPY`, or `ZSTD`. |
| `CODEC` | To & From | Alias for compression, but only valid for Parquet files. Option to compress the file. Value can be `UNCOMPRESSED`, `GZIP`, `SNAPPY`, or `ZSTD`. |
| `ROW_GROUP_SIZE` | To | Option for Parquet writing. Specifies the minimum number of rows in a parquet row group, with a minimum value equal to DuckDB’s vector size (currently 2048, but adjustable when compiling DuckDB). A parquet row group is a partition of rows, consisting of a column chunk for each column in the dataset. |

> It is recommended that the file name used in `COPY` always be specified as an absolute path.
>
> The values in each record are separated by the `DELIMITER` string. If the value contains the `DELIMITER` string, the `QUOTE` string, the `NULL` string, a carriage return, or line feed character, then the whole value is prefixed and suffixed by the `QUOTE` string, and any occurrence within the value of a `QUOTE` string or the `ESCAPE` string is preceded by the `ESCAPE` string. You can also use `FORCE_QUOTE` to force quotes when outputting non-NULL values in specific columns.
>
> The CSV format has no standard way to distinguish a NULL value from an empty string. You can use `FORCE_NOT_NULL` to prevent `NULL` input comparisons for specific columns.
>
> In CSV format, all characters are significant. A quoted value surrounded by white space, or any characters other than `DELIMITER`, will include those characters. This can cause errors if you import data from a system that pads CSV lines with white space out to some fixed width. If such a situation arises you might need to preprocess the CSV file to remove the trailing white space, before importing the data into DuckDB.
