---
layout: docu
title: Copy
selected: Documentation/SQL/Copy
expanded: SQL
railroad: statements/copy.js
---
`COPY` moves data between DuckDB tables and external Comma Separated Value (CSV) files.

# CSV Import
`COPY ... FROM` imports data into DuckDB from an external CSV file into an existing table. The data is appended to whatever data is in the table already. The amount of columns inside the file must match the amount of columns in the table `table_name`, and the contents of the columns must be convertible to the column types of the table. In case this is not possible, an error will be thrown.

If a list of columns is specified, `COPY` will only copy the data in the specified columns from the file. If there are any columns in the table that are not in the column list, `COPY ... FROM` will insert the default values for those columns

```sql
-- Copy the contents of a comma-separated file 'test.csv' without a header into the table 'test'
COPY test FROM 'test.csv';
-- Copy the contents of a comma-separated file with a header into the 'category' table
COPY category FROM 'categories.csv' ( HEADER );
-- Copy the contents of 'lineitem.tbl' into the 'lineitem' table, where the contents are delimited by a pipe character ('|')
COPY lineitem FROM 'lineitem.tbl' ( DELIMITER '|' );
-- Copy the contents of 'lineitem.tbl' into the 'lineitem' table, where the delimiter, quote character, and presence of a header are automatically detected
COPY lineitem FROM 'lineitem.tbl' ( FORMAT CSV_AUTO );
-- Read the contents of a comma-separated file 'names.csv' into the 'name' column of the 'category' table. Any other columns of this table are filled with their default value.
COPY category(name) FROM 'names.csv';
```

## Syntax
<div id="rrdiagram1"></div>

# CSV Export
`COPY ... TO` exports data from DuckDB to an external CSV file. It has mostly the same set of options as `COPY ... FROM`, however, in the case of `COPY ... TO` the options specify how the CSV file should be written to disk. Any CSV file created by `COPY ... TO` can be copied back into the database by using `COPY ... FROM` with the same set of options.

The `COPY ... TO` function can be called specifying either a table name, or a query. When a table name is specified, the contents of the entire table will be written into the resulting CSV file. When a query is specified, the query is executed and the result of the query is written to the resulting file.

```sql
-- Copy the contents of the 'lineitem' table to the file 'lineitem.tbl', where the columns are delimited by a pipe character ('|'), including a header line.
COPY lineitem TO 'lineitem.tbl' ( DELIMITER '|', HEADER );
-- Copy the l_orderkey column of the 'lineitem' table to the file 'orderkey.tbl'
COPY lineitem(l_orderkey) TO 'orderkey.tbl' ( DELIMITER '|' );
-- Copy the result of a query to the file 'query.csv', including a header with column names
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.csv' WITH (HEADER 1, DELIMITER ',');
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
| `FORMAT` | If this option is used, its value must be `CSV`. With any other format an error will be thrown. |
| `DELIMITER` | Specifies the string that separates columns within each row (line) of the file. The default value is a comma (`,`). |
| `NULL` | Specifies the string that represents a null value. The default is an empty string. Please note that in `COPY ... FROM` both an unquoted empty string and a quoted empty string represent a null value. If any other null string is specified, again both its quoted and its unquoted appearance represent a null value. `COPY ... TO` does not quote null values on output, even if `FORCE_QUOTE` is true. |
| `HEADER` | Specifies that the file contains a header line with the names of each column in the file. Thus, `COPY ... FROM` ignores the first line when importing data, whereas on output (`COPY ... TO`) the first line of the file contains the column names of the exported columns. |
| `QUOTE` | Specifies the quoting string to be used when a data value is quoted. The default is double-quote (`"`). |
| `ESCAPE` | Specifies the string that should appear before a data character sequence that matches the `QUOTE` value. The default is the same as the `QUOTE` value (so that the quoting string is doubled if it appears in the data). |
| `FORCE_QUOTE` | Forces quoting to be used for all non-NULL values in each specified column. `NULL` output is never quoted. If `*` is specified, non-`NULL` values will be quoted in all columns. This option is allowed only in `COPY ... TO`. |
| `FORCE_NOT_NULL` | Do not match the specified columns' values against the null string. In the default case where the null string is empty, this means that empty values will be read as zero-length strings rather than nulls. This option is allowed only in `COPY ... FROM`. |
| `ENCODING` | If this option is used, its value must be `UTF8`. With any other encoding an error will be thrown. |


> It is recommended that the file name used in COPY always be specified as an absolute path.
>
> The values in each record are separated by the `DELIMITER` string. If the value contains the `DELIMITER` string, the `QUOTE` string, the `NULL` string, a carriage return, or line feed character, then the whole value is prefixed and suffixed by the `QUOTE` string, and any occurrence within the value of a `QUOTE` string or the `ESCAPE` string is preceded by the `ESCAPE` string. You can also use `FORCE_QUOTE` to force quotes when outputting non-`NULL` values in specific columns.
>
> The CSV format has no standard way to distinguish a NULL value from an empty string. You can use `FORCE_NOT_NULL` to prevent `NULL` input comparisons for specific columns.
>
> In CSV format, all characters are significant. A quoted value surrounded by white space, or any characters other than `DELIMITER`, will include those characters. This can cause errors if you import data from a system that pads CSV lines with white space out to some fixed width. If such a situation arises you might need to preprocess the CSV file to remove the trailing white space, before importing the data into DuckDB.
