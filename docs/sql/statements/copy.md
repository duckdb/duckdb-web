---
layout: docu
title: Copy
selected: Documentation/SQL/Copy
expanded: SQL
railroad: statements/copy.js
---

# Examples

```sql
-- read a CSV file into the lineitem table - using auto-detected options
COPY lineitem FROM 'lineitem.csv' (AUTO_DETECT TRUE);
-- read a parquet file into the lineitem table
COPY lineitem FROM `lineitem.pq` (FORMAT PARQUET);

-- write a table to a CSV file
COPY lineitem TO 'lineitem.csv' (FORMAT CSV, DELIMITER '|', HEADER);
-- write the result of a query to a Parquet file
COPY (SELECT l_orderkey, l_partkey FROM lineitem) TO 'lineitem.parquet' (COMPRESSION ZSTD);
```

#### Copy Statements

`COPY` moves data between DuckDB and external files. `COPY ... FROM` imports data into DuckDB from an external file. `COPY ... TO` writes data from DuckDB to an external file. The `COPY` command can be used for `CSV`, `PARQUET` and `JSON` files.


# Copy From
`COPY ... FROM` imports data into DuckDB from an external file into an existing table. The data is appended to whatever data is in the table already. The amount of columns inside the file must match the amount of columns in the table `table_name`, and the contents of the columns must be convertible to the column types of the table. In case this is not possible, an error will be thrown.

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



# Copy To
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

## Copy Options

Zero or more copy options may be provided as a part of the copy operation. The `WITH` specifier is optional, but if any options are specified, the parentheses are required. Parameter values can be passed in with or without wrapping in single quotes. See the above note about `boolean` options as well.

The below options are applicable to all formats written with `COPY`. 

| Name | Description | Type | Default |
|:---|:---|:----|:----|
| `allow_overwrite` | Whether or not to allow overwriting a directory if one already exists. Only has an effect when used with `partition_by`. | bool | false |
| `format` | Specifies the copy function to use. The default is selected from the file extension (e.g. `.parquet` results in a Parquet file being written/read). If the file extension is unknown `CSV` is selected. Available options are `CSV`, `PARQUET` and `JSON`. | varchar | auto |
| `partition_by` | The columns to partition by using a hive partitioning scheme, see the [partitioned writes section](../partitioning/partitioned_writes). | varchar[] | (empty) |
| `per_thread_output` | Generate one file per thread, rather than one file in total. This allows for faster parallel writing. | bool | false |
| `use_tmp_file` | Whether or not to write to a temporary file first if the original file exists (`target.csv.tmp`). This prevents overwriting an existing file with a broken file in case the writing is cancelled. | bool | auto |

## CSV Options

The below options are applicable when writing `CSV` files.

| Name | Description | Type | Default |
|:---|:---|:----|:----|
| `compression` | The compression type for the file. By default this will be detected automatically from the file extension (e.g. `file.csv.gz` will use gzip, `file.csv` will use `none`). Options are `none`, `gzip`, `zstd`. | varchar | auto |
| `force_quote` | The list of columns to always add quotes to, even if not required. | varchar[] | `[]` |
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../../sql/functions/dateformat) | varchar | `(empty)` |
| `delim` or `sep` | The character that is written to separate columns within each row (line) of the file. | varchar | `,` |
| `escape` | The character that should appear before a character that matches the `quote` value. | varchar | `"` |
| `header` | Whether or not to write a header for the CSV file. | bool | false |
| `nullstr` | The string that is written to represent a NULL value. | varchar | `(empty)` |
| `quote` | The quoting character to be used when a data value is quoted. | varchar | `"` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) | varchar | `(empty)` |


## Parquet Options

The below options are applicable when writing `Parquet` files.

| Name | Description | Type | Default |
|:---|:---|:----|:----|
| `compression` | The compression format to use (uncompressed, snappy, gzip or zstd). | varchar | snappy |
| `row_group_size` | The target size of each row-group. | bigint | 122880 |


## JSON Options

The below options are applicable when writing `JSON` files.

| Name | Description | Type | Default |
|:---|:---|:----|:----|
| `dateformat` | Specifies the date format to use when parsing dates. See [Date Format](../../sql/functions/dateformat) | varchar | `(empty)` |
| `timestampformat` | Specifies the date format to use when parsing timestamps. See [Date Format](../../sql/functions/dateformat) | varchar | `(empty)` |
