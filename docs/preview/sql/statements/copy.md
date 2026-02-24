---
layout: docu
railroad: statements/copy.js
title: COPY Statement
---

## Examples

Read a CSV file into the `lineitem` table, using auto-detected CSV options:

```sql
COPY lineitem FROM 'lineitem.csv';
```

Read a CSV file into the `lineitem` table, using manually specified CSV options:

```sql
COPY lineitem FROM 'lineitem.csv' (DELIMITER '|');
```

Read a Parquet file into the `lineitem` table:

```sql
COPY lineitem FROM 'lineitem.pq' (FORMAT parquet);
```

Read a JSON file into the `lineitem` table, using auto-detected options:

```sql
COPY lineitem FROM 'lineitem.json' (FORMAT json, AUTO_DETECT true);
```

Read a CSV file into the `lineitem` table, using double quotes:

```sql
COPY lineitem FROM "lineitem.csv";
```

Read a CSV file into the `lineitem` table, omitting quotes:

```sql
COPY lineitem FROM lineitem.csv;
```

Write a table to a CSV file:

```sql
COPY lineitem TO 'lineitem.csv' (FORMAT csv, DELIMITER '|', HEADER);
```

Write a table to a CSV file, using double quotes:

```sql
COPY lineitem TO "lineitem.csv";
```

Write a table to a CSV file, omitting quotes:

```sql
COPY lineitem TO lineitem.csv;
```

Write the result of a query to a Parquet file:

```sql
COPY (SELECT l_orderkey, l_partkey FROM lineitem) TO 'lineitem.parquet' (COMPRESSION zstd);
```

Copy the entire content of database `db1` to database `db2`:

```sql
COPY FROM DATABASE db1 TO db2;
```

Copy only the schema (catalog elements) but not any data:

```sql
COPY FROM DATABASE db1 TO db2 (SCHEMA);
```

## Overview

`COPY` moves data between DuckDB and external files. `COPY ... FROM` imports data into DuckDB from an external file. `COPY ... TO` writes data from DuckDB to an external file. The `COPY` command can be used for `CSV`, `PARQUET` and `JSON` files.

## `COPY ... FROM`

`COPY ... FROM` imports data from an external file into an existing table. The data is appended to whatever data is in the table already. The amount of columns inside the file must match the amount of columns in the table `tbl`, and the contents of the columns must be convertible to the column types of the table. In case this is not possible, an error will be thrown.

If a list of columns is specified, `COPY` will only copy the data in the specified columns from the file. If there are any columns in the table that are not in the column list, `COPY ... FROM` will insert the default values for those columns.

Copy the contents of a comma-separated file `test.csv` without a header into the table `test`:

```sql
COPY test FROM 'test.csv';
```

Copy the contents of a comma-separated file with a header into the `category` table:

```sql
COPY category FROM 'categories.csv' (HEADER);
```

Copy the contents of `lineitem.tbl` into the `lineitem` table, where the contents are delimited by a pipe character (`|`):

```sql
COPY lineitem FROM 'lineitem.tbl' (DELIMITER '|');
```

Copy the contents of `lineitem.tbl` into the `lineitem` table, where the delimiter, quote character, and presence of a header are automatically detected:

```sql
COPY lineitem FROM 'lineitem.tbl' (AUTO_DETECT true);
```

Read the contents of a comma-separated file `names.csv` into the `name` column of the `category` table. Any other columns of this table are filled with their default value:

```sql
COPY category(name) FROM 'names.csv';
```

Read the contents of a Parquet file `lineitem.parquet` into the `lineitem` table:

```sql
COPY lineitem FROM 'lineitem.parquet' (FORMAT parquet);
```

Read the contents of a newline-delimited JSON file `lineitem.ndjson` into the `lineitem` table:

```sql
COPY lineitem FROM 'lineitem.ndjson' (FORMAT json);
```

Read the contents of a JSON file `lineitem.json` into the `lineitem` table:

```sql
COPY lineitem FROM 'lineitem.json' (FORMAT json, ARRAY true);
```

An expression may be used as the source of a `COPY ... FROM` command if it is placed within parentheses. 

Read the contents of a file whose path is stored in a variable into the `lineitem` table:

```sql
SET VARIABLE source_file = 'lineitem.json';
COPY lineitem FROM (getvariable('source_file'));
```

Read the contents of a file provided as parameter of a prepared statement into the `lineitem` table:

```sql
PREPARE v1 AS COPY lineitem FROM ($1);
EXECUTE v1('lineitem.json');
```

### Syntax

<div id="rrdiagram1"></div>

> To ensure compatibility with PostgreSQL, DuckDB accepts `COPY ... FROM` statements that do not fully comply with the railroad diagram shown here. For example, the following is a valid statement:
>
> ```sql
> COPY tbl FROM 'tbl.csv' WITH DELIMITER '|' CSV HEADER;
> ```

## `COPY ... TO`

`COPY ... TO` exports data from DuckDB to an external CSV, Parquet, JSON or BLOB file. It has mostly the same set of options as `COPY ... FROM`, however, in the case of `COPY ... TO` the options specify how the file should be written to disk. Any file created by `COPY ... TO` can be copied back into the database by using `COPY ... FROM` with a similar set of options.

The `COPY ... TO` function can be called specifying either a table name, or a query. When a table name is specified, the contents of the entire table will be written into the resulting file. When a query is specified, the query is executed and the result of the query is written to the resulting file.

Copy the contents of the `lineitem` table to a CSV file with a header:

```sql
COPY lineitem TO 'lineitem.csv';
```

Copy the contents of the `lineitem` table to the file `lineitem.tbl`, where the columns are delimited by a pipe character (`|`), including a header line:

```sql
COPY lineitem TO 'lineitem.tbl' (DELIMITER '|');
```

Use tab separators to create a TSV file without a header:

```sql
COPY lineitem TO 'lineitem.tsv' (DELIMITER '\t', HEADER false);
```

Copy the l_orderkey column of the `lineitem` table to the file `orderkey.tbl`:

```sql
COPY lineitem(l_orderkey) TO 'orderkey.tbl' (DELIMITER '|');
```

Copy the result of a query to the file `query.csv`, including a header with column names:

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.csv' (DELIMITER ',');
```

Copy the result of a query to the Parquet file `query.parquet`:

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.parquet' (FORMAT parquet);
```

Copy the result of a query to the newline-delimited JSON file `query.ndjson`:

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.ndjson' (FORMAT json);
```

Copy the result of a query to the JSON file `query.json`:

```sql
COPY (SELECT 42 AS a, 'hello' AS b) TO 'query.json' (FORMAT json, ARRAY true);
```

Return the files and their column statistics that were written as part of the `COPY` statement:

```sql
COPY (SELECT l_orderkey, l_comment FROM lineitem) TO 'lineitem_part.parquet' (RETURN_STATS);
```

|       filename        | count  | file_size_bytes | footer_size_bytes |                                                                                   column_statistics                                                                                    | partition_keys |
|-----------------------|-------:|----------------:|------------------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| lineitem_part.parquet | 600572 | 8579141         | 1445              | {'"l_comment"'={column_size_bytes=7642227, max=zzle. slyly, min=' Tiresias above the blit', null_count=0}, '"l_orderkey"'={column_size_bytes=935457, max=600000, min=1, null_count=0}} | NULL           |

Note: for nested columns (e.g., structs) the column statistics are defined for each part. For example, if we have a column `name STRUCT(field1 INTEGER, field2 INTEGER)` the column statistics will have stats for `name.field1` and `name.field2`.

An expression may be used as the target of a `COPY ... TO` command if it is placed within parentheses. 

Copy the result of a query to a file whose path is stored in a variable:

```sql
SET VARIABLE target_file = 'target_file.parquet';
COPY (SELECT 'hello world') TO (getvariable('target_file'));
```

Copy to a file provided as parameter of a prepared statement:

```sql
PREPARE v1 AS COPY (SELECT 42 AS i) to $1;
EXECUTE v1('file.csv');
```

Expressions may be used for options as well. Copy to a file using a format stored in a variable:

```sql
SET VARIABLE my_format = 'parquet';
COPY (SELECT 42 AS i) TO 'file' (FORMAT getvariable('my_format'));
```

### `COPY ... TO` Options

Zero or more copy options may be provided as a part of the copy operation. The `WITH` specifier is optional, but if any options are specified, the parentheses are required. Parameter values can be passed in with or without wrapping in single quotes. Arbitrary expressions may be used for parameter values.

Any option that is a Boolean can be enabled or disabled in multiple ways. You can write `true`, `ON`, or `1` to enable the option, and `false`, `OFF`, or `0` to disable it. The `BOOLEAN` value can also be omitted, e.g., by only passing `(HEADER)`, in which case `true` is assumed.

With few exceptions, the below options are applicable to all formats written with `COPY`.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `FORMAT` | Specifies the copy function to use. The default is selected from the file extension (e.g., `.parquet` results in a Parquet file being written/read). If the file extension is unknown `CSV` is selected. Vanilla DuckDB provides `CSV`, `PARQUET` and `JSON` but additional copy functions can be added by [`extensions`]({% link docs/preview/extensions/overview.md %}). | `VARCHAR` | `auto` |
| `USE_TMP_FILE` | Whether or not to write to a temporary file first if the original file exists (`target.csv.tmp`). This prevents overwriting an existing file with a broken file in case the writing is cancelled. | `BOOL` | `auto` |
| `OVERWRITE_OR_IGNORE` | Whether or not to allow overwriting files if they already exist. Only has an effect when used with `PARTITION_BY`. | `BOOL` | `false` |
| `OVERWRITE` | When `true`, all existing files inside targeted directories will be removed (not supported on remote filesystems). Only has an effect when used with `PARTITION_BY`. | `BOOL` | `false` |
| `APPEND` | When `true`, in the event a filename pattern is generated that already exists, the path will be regenerated to ensure no existing files are overwritten. Only has an effect when used with `PARTITION_BY`. | `BOOL` | `false` |
| `FILENAME_PATTERN` | Set a pattern to use for the filename, can optionally contain `{uuid}` / `{uuidv4}` or `{uuidv7}` to be filled in with a generated [UUID]({% link docs/preview/sql/data_types/numeric.md %}#universally-unique-identifiers-uuids) (v4 or v7, respectively), and `{i}`, which is replaced by an incrementing index. Only has an effect when used with `PARTITION_BY`. | `VARCHAR` | `auto` |
| `FILE_EXTENSION` | Set the file extension that should be assigned to the generated file(s). | `VARCHAR` | `auto` |
| `PER_THREAD_OUTPUT` | When `true`, the `COPY` command generates one file per thread, rather than one file in total. This allows for faster parallel writing. | `BOOL` | `false` |
| `FILE_SIZE_BYTES` | If this parameter is set, the `COPY` process creates a directory which will contain the exported files. If a file exceeds the set limit (specified as bytes such as `1000` or in human-readable format such as `1k`), the process creates a new file in the directory. This parameter works in combination with `PER_THREAD_OUTPUT`. Note that the size is used as an approximation, and files can be occasionally slightly over the limit. | `VARCHAR` or `BIGINT` | (empty) |
| `PARTITION_BY` | The columns to partition by using a Hive partitioning scheme, see the [partitioned writes section]({% link docs/preview/data/partitioning/partitioned_writes.md %}). | `VARCHAR[]` | (empty) |
| `PRESERVE_ORDER` | Whether or not to [preserve order]({% link docs/preview/sql/dialect/order_preservation.md %}) during the copy operation. Defaults to the value of the `preserve_insertion_order` [configuration option]({% link docs/preview/configuration/overview.md %}). | `BOOL`| (*) |
| `RETURN_FILES` | Whether or not to include the created filepath(s) (as a `files VARCHAR[]` column) in the query result. | `BOOL` | `false` |
| `RETURN_STATS` | Whether or not to return the files and their column statistics that were written as part of the `COPY` statement. | `BOOL`| `false` |
| `WRITE_PARTITION_COLUMNS` | Whether or not to write partition columns into files. Only has an effect when used with `PARTITION_BY`. | `BOOL` | `false` |

### Syntax

<div id="rrdiagram2"></div>

> To ensure compatibility with PostgreSQL, DuckDB accepts `COPY ... TO` statements that do not fully comply with the railroad diagram shown here. For example, the following is a valid statement:
>
> ```sql
> COPY (SELECT 42 AS x, 84 AS y) TO 'out.csv' WITH DELIMITER '|' CSV HEADER;
> ```

## `COPY FROM DATABASE ... TO`

The `COPY FROM DATABASE ... TO` statement copies the entire content from one attached database to another attached database. This includes the schema, including constraints, indexes, sequences, macros and the data itself.

```sql
ATTACH 'db1.db' AS db1;
CREATE TABLE db1.tbl AS SELECT 42 AS x, 3 AS y;
CREATE MACRO db1.two_x_plus_y(x, y) AS 2 * x + y;

ATTACH 'db2.db' AS db2;
COPY FROM DATABASE db1 TO db2;
SELECT db2.two_x_plus_y(x, y) AS z FROM db2.tbl;
```

| z  |
|---:|
| 87 |

To only copy the **schema** of `db1` to `db2` but omit copying the data, add `SCHEMA` to the statement:

```sql
COPY FROM DATABASE db1 TO db2 (SCHEMA);
```

### Syntax

<div id="rrdiagram3"></div>

## Format-Specific Options

### CSV Options

The below options are applicable when writing CSV files.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `COMPRESSION` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `file.csv.gz` will use `gzip`, `file.csv.zst` will use `zstd`, and `file.csv` will use `none`). Options are `none`, `gzip`, `zstd`. | `VARCHAR` | `auto` |
| `DATEFORMAT` | Specifies the date format to use when writing dates. See [Date Format]({% link docs/preview/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |
| `DELIM` or `SEP` | The character that is written to separate columns within each row. | `VARCHAR` | `,` |
| `ESCAPE` | The character that should appear before a character that matches the `quote` value. | `VARCHAR` | `"` |
| `FORCE_QUOTE` | The list of columns to always add quotes to, even if not required. | `VARCHAR[]` | `[]` |
| `HEADER` | Whether or not to write a header for the CSV file. | `BOOL` | `true` |
| `NULLSTR` | The string that is written to represent a `NULL` value. | `VARCHAR` | (empty) |
| `PREFIX` | Prefixes the CSV file with a specified string. This option must be used in conjunction with `SUFFIX` and requires `HEADER` to be set to `false`.| `VARCHAR` | (empty) |
| `SUFFIX` | Appends a specified string as a suffix to the CSV file. This option must be used in conjunction with `PREFIX` and requires `HEADER` to be set to `false`.| `VARCHAR` | (empty) |
| `QUOTE` | The quoting character to be used when a data value is quoted. | `VARCHAR` | `"` |
| `TIMESTAMPFORMAT` | Specifies the date format to use when writing timestamps. See [Date Format]({% link docs/preview/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |

### Parquet Options

The below options are applicable when writing Parquet files.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `COMPRESSION` | The compression format to use (`uncompressed`, `snappy`, `gzip`, `zstd`, `brotli`, `lz4`, `lz4_raw`). | `VARCHAR` | `snappy` |
| `COMPRESSION_LEVEL` | Compression level, set between 1 (lowest compression, fastest) and 22 (highest compression, slowest). Only supported for zstd compression. | `BIGINT` | `3` |
| `FIELD_IDS` | The `field_id` for each column. Pass `auto` to attempt to infer automatically. | `STRUCT` | (empty) |
| `ROW_GROUP_SIZE_BYTES` | The target size of each row group. You can pass either a human-readable string, e.g., `2MB`, or an integer, i.e., the number of bytes. This option is only used when you have issued `SET preserve_insertion_order = false;`, otherwise, it is ignored. | `BIGINT` | `row_group_size * 1024` |
| `ROW_GROUP_SIZE` | The target size, i.e., number of rows, of each row group. | `BIGINT` | 122880 |
| `ROW_GROUPS_PER_FILE` | Create a new Parquet file if the current one has a specified number of row groups. If multiple threads are active, the number of row groups in a file may slightly exceed the specified number of row groups to limit the amount of locking – similarly to the behavior of `FILE_SIZE_BYTES`. However, if `per_thread_output` is set, only one thread writes to each file, and it becomes accurate again. | `BIGINT` |  (empty) |
| `PARQUET_VERSION` | The Parquet version to use (`V1`, `V2`). | `VARCHAR` | `V1` |

Some examples of `FIELD_IDS` are as follows.

Assign `field_ids` automatically:

```sql
COPY
    (SELECT 128 AS i)
    TO 'my.parquet'
    (FIELD_IDS 'auto');
```

Sets the `field_id` of column `i` to 42:

```sql
COPY
    (SELECT 128 AS i)
    TO 'my.parquet'
    (FIELD_IDS {i: 42});
```

Sets the `field_id` of column `i` to 42, and column `j` to 43:

```sql
COPY
    (SELECT 128 AS i, 256 AS j)
    TO 'my.parquet'
    (FIELD_IDS {i: 42, j: 43});
```

Sets the `field_id` of column `my_struct` to 42, and column `i` (nested inside `my_struct`) to 43:

```sql
COPY
    (SELECT {i: 128} AS my_struct)
    TO 'my.parquet'
    (FIELD_IDS {my_struct: {__duckdb_field_id: 42, i: 43}});
```

Sets the `field_id` of column `my_list` to 42, and column `element` (default name of list child) to 43:

```sql
COPY
    (SELECT [128, 256] AS my_list)
    TO 'my.parquet'
    (FIELD_IDS {my_list: {__duckdb_field_id: 42, element: 43}});
```

Sets the `field_id` of column `my_map` to 42, and columns `key` and `value` (default names of map children) to 43 and 44:

```sql
COPY
    (SELECT MAP {'key1' : 128, 'key2': 256} my_map)
    TO 'my.parquet'
    (FIELD_IDS {my_map: {__duckdb_field_id: 42, key: 43, value: 44}});
```

### JSON Options

The below options are applicable when writing `JSON` files.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `ARRAY` | Whether to write a JSON array. If `true`, a JSON array of records is written, if `false`, newline-delimited JSON is written | `BOOL` | `false` |
| `COMPRESSION` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `file.json.gz` will use `gzip`, `file.json.zst` will use `zstd`, and `file.json` will use `none`). Options are `none`, `gzip`, `zstd`. | `VARCHAR` | `auto` |
| `DATEFORMAT` | Specifies the date format to use when writing dates. See [Date Format]({% link docs/preview/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |
| `TIMESTAMPFORMAT` | Specifies the date format to use when writing timestamps. See [Date Format]({% link docs/preview/sql/functions/dateformat.md %}). | `VARCHAR` | (empty) |


Sets the value of column `hello` to `QUACK!` and outputs the results to `quack.json`:

```sql
COPY (SELECT 'QUACK!' AS hello) TO 'quack.json';
--RETURNS: {"hello":"QUACK!"}
```

Sets the value of column `num_list` to `[1,2,3]` and outputs the results to `numbers.json`:

```sql
COPY (SELECT [1, 2, 3] AS num_list) TO 'numbers.json';
--RETURNS: {"num_list":[1,2,3]}
```

Sets the value of column `compression_type` to `gzip_explicit` and outputs the results to `compression.json.gz` with explicit compression:

```sql
COPY (SELECT 'gzip_explicit' AS compression_type) TO 'explicit_compression.json' (FORMAT json, COMPRESSION 'GZIP');
-- RETURNS: {"compression_type":"gzip_explicit"}
```

Sets all values of single rows to be returned as nested arrays to `array_true.json`:

```sql
COPY (SELECT 1 AS id, 'Alice' AS name, [1, 2, 3] AS numbers
      UNION ALL
      SELECT 2, 'Bob', [4, 5, 6] AS numbers)
TO 'array_true.json' (FORMAT json, ARRAY true);

-- RETURNS: 
/*
[
	{"id":1,"name":"Alice","numbers":[1,2,3]},
	{"id":2,"name":"Bob","numbers":[1,2,3]}
]
*/
```

Sets all values of single rows to be returned as non-nested arrays to `array_false.json`:

```sql
COPY (SELECT 1 AS id, 'Alice' AS name, [1, 2, 3] AS numbers
      UNION ALL
      SELECT 2, 'Bob', [4, 5, 6] AS numbers)
TO 'array_false.json' (FORMAT json, ARRAY false);

-- RETURNS:
/*
{"id":1,"name":"Alice","numbers":[1,2,3]}
{"id":2,"name":"Bob","numbers":[4,5,6]}
*/
```

### BLOB Options

The `BLOB` format option allows you to select a single column of a DuckDB table into a `.blob` file.
The column must be cast to the `BLOB` data type. For details on typecasting, see the 
[Casting Operations Matrix]({% link docs/preview/sql/data_types/typecasting.md %}#Casting-Operations-Matrix).

The below options are applicable when writing `BLOB` files.

| Name | Description | Type | Default |
|:--|:-----|:-|:-|
| `COMPRESSION` | The compression type for the file. By default this will be detected automatically from the file extension (e.g., `file.blob.gz` will use `gzip`, `file.blob.zst` will use `zstd`, and `file.blob` will use `none`). Options are `none`, `gzip`, `zstd`. | `VARCHAR` | `auto` |

Type casts the string value `foo` to the `BLOB` data type and outputs the results to `blob_output.blob`:

```sql
COPY (select 'foo'::BLOB) TO 'blob_output.blob' (FORMAT BLOB);
```

Type casts the string value `foo` to the `BLOB` data type and outputs the results to `blob_output_gzip.blob.gz` with `gzip` compression:

```sql
COPY (select 'foo'::BLOB) TO 'blob_output_gzip.blob' (FORMAT BLOB, COMPRESSION 'GZIP');
```

## Limitations

`COPY` does not support copying between tables. To copy between tables, use an [`INSERT statement`]({% link docs/preview/sql/statements/insert.md %}):

```sql
INSERT INTO tbl2
    FROM tbl1;
```
