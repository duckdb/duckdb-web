---
layout: docu
title: Parquet
---
Parquet files are compressed columnar files that are efficient to load and process. DuckDB provides support for both reading and writing Parquet files in an efficient manner, as well as support for pushing filters and projections into the Parquet file scans.

### Examples
```sql
-- read a single parquet file
SELECT * FROM 'test.parquet';
-- figure out which columns/types are in a parquet file
DESCRIBE SELECT * FROM 'test.parquet';
-- create a table from a parquet file
CREATE TABLE test AS SELECT * FROM 'test.parquet';
-- if the file does not end in ".parquet", use the parquet_scan function
SELECT * FROM parquet_scan('test.parq');
-- use list parameter to read 3 parquet files and treat them as a single table
SELECT * FROM parquet_scan(['file1.parquet', 'file2.parquet', 'file3.parquet']);
-- read all files that match the glob pattern
SELECT * FROM 'test/*.parquet';
-- use a list of globs to read all parquet files from 2 specific folders
SELECT * FROM parquet_scan(['folder1/*.parquet','folder2/*.parquet']);
-- query the metadata of a parquet file
SELECT * FROM parquet_metadata('test.parquet');
-- query the schema of a parquet file
SELECT * FROM parquet_schema('test.parquet');
-- write the results of a query to a parquet file
COPY (SELECT * FROM tbl) TO 'result-snappy.parquet' (FORMAT 'parquet');
-- export the table contents of the entire database as parquet
EXPORT DATABASE 'target_directory' (FORMAT PARQUET);
```

### Single-File Reads
DuckDB includes an efficient Parquet reader in the form of the `parquet_scan` function.

```sql
SELECT * FROM parquet_scan('test.parquet');
```

If your file ends in `.parquet`, the parquet_scan syntax is optional. The system will automatically infer that you are reading a Parquet file.

```sql
SELECT * FROM 'test.parquet';
```

Unlike CSV files, parquet files are structured and as such are unambiguous to read. No parameters need to be passed to this function. The `parquet_scan` function will figure out the column names and column types present in the file and emit them.

### Multi-File Reads and Globs
DuckDB can also read a series of Parquet files and treat them as if they were a single table. Note that this only works if the Parquet files have the same schema. You can specify which Parquet files you want to read using a list parameter, glob pattern matching syntax, or a combination of both.

#### List Parameter
The parquet_scan function can accept a list of filenames as the input parameter. See the [nested types documentation](../sql/data_types/overview) for more details on lists.
```sql
-- read 3 parquet files and treat them as a single table
SELECT * FROM parquet_scan(['file1.parquet', 'file2.parquet', 'file3.parquet']);
```

#### Glob Syntax
Any file name input to the parquet_scan function can either be an exact filename, or use a glob syntax to read multple files that match a pattern.

|  Wildcard  |                        Description                        |
|------------|-----------------------------------------------------------|
| `*`        | matches any number of any characters (including none)     |
| `?`        | matches any single character                              |
| `[abc]`    | matches one character given in the bracket                |
| `[a-z]`    | matches one character from the range given in the bracket |

Here is an example that reads all the files that end with `.parquet` located in the `test` folder:

```sql
-- read all files that match the glob pattern
SELECT * FROM parquet_scan('test/*.parquet');
```

#### List of Globs
The glob syntax and the list input parameter can be combined to scan files that meet one of multiple patterns.

```sql
-- Read all parquet files from 2 specific folders
SELECT * FROM parquet_scan(['folder1/*.parquet','folder2/*.parquet']);
```

### Partial Reading
DuckDB supports projection pushdown into the Parquet file itself. That is to say, when querying a Parquet file, only the columns required for the query are read. This allows you to read only the part of the Parquet file that you are interested in. This will be done automatically by the system.

DuckDB also supports filter pushdown into the Parquet reader. When you apply a filter to a column that is scanned from a Parquet file, the filter will be pushed down into the scan, and can even be used to skip parts of the file using the built-in zonemaps. Note that this will depend on whether or not your Parquet file contains zonemaps.

Filter and projection pushdown provide significant performance benefits. See [our blog post on this](https://duckdb.org/2021/06/25/querying-parquet.html) for more information.

### Inserts and Views
You can also insert the data into a table or create a table from the parquet file directly. This will load the data from the parquet file and insert it into the database.

```sql
-- insert the data from the parquet file in the table
INSERT INTO people SELECT * FROM parquet_scan('test.parquet');
-- create a table directly from a parquet file
CREATE TABLE people AS SELECT * FROM parquet_scan('test.parquet');
```

If you wish to keep the data stored inside the parquet file, but want to query the parquet file directly, you can create a view over the `parquet_scan` function. You can then query the parquet file as if it were a built-in table.

```sql
-- create a view over the parquet file
CREATE VIEW people AS SELECT * FROM parquet_scan('test.parquet');
-- query the parquet file
SELECT * FROM people;
```

### Parquet Metadata
The `parquet_metadata` function can be used to query the metadata contained within a Parquet file, which reveals various internal details of the Parquet file such as the statistics of the different columns. This can be useful for figuring out what kind of skipping is possible in Parquet files, or even to obtain a quick overview of what the different columns contain.

```sql
SELECT * FROM parquet_metadata('test.parquet');
```

Below is a table of the columns returned by `parquet_metadata`.

|          Field          |  Type   |
|-------------------------|---------|
| file_name               | VARCHAR |
| row_group_id            | BIGINT  |
| row_group_num_rows      | BIGINT  |
| row_group_num_columns   | BIGINT  |
| row_group_bytes         | BIGINT  |
| column_id               | BIGINT  |
| file_offset             | BIGINT  |
| num_values              | BIGINT  |
| path_in_schema          | VARCHAR |
| type                    | VARCHAR |
| stats_min               | VARCHAR |
| stats_max               | VARCHAR |
| stats_null_count        | BIGINT  |
| stats_distinct_count    | BIGINT  |
| stats_min_value         | VARCHAR |
| stats_max_value         | VARCHAR |
| compression             | VARCHAR |
| encodings               | VARCHAR |
| index_page_offset       | BIGINT  |
| dictionary_page_offset  | BIGINT  |
| data_page_offset        | BIGINT  |
| total_compressed_size   | BIGINT  |
| total_uncompressed_size | BIGINT  |


### Parquet Schema
The `parquet_schema` function can be used to query the internal schema contained within a Parquet file. Note that this is the schema as it is contained within the metadata of the Parquet file. If you want to figure out the column names and types contained within a Parquet file it is easier to use `DESCRIBE`.

```sql
-- fetch the column names and column types
DESCRIBE SELECT * FROM 'test.parquet';
-- fetch the internal schema of a parquet file
SELECT * FROM parquet_schema('test.parquet');
```

Below is a table of the columns returned by `parquet_schema`.

|      Field      |  Type   |
|-----------------|---------|
| file_name       | VARCHAR |
| name            | VARCHAR |
| type            | VARCHAR |
| type_length     | VARCHAR |
| repetition_type | VARCHAR |
| num_children    | BIGINT  |
| converted_type  | VARCHAR |
| scale           | BIGINT  |
| precision       | BIGINT  |
| field_id        | BIGINT  |
| logical_type    | VARCHAR |

### Writing to Parquet Files
DuckDB also has support for writing to Parquet files using the `COPY` statement syntax. You can specify which compression format should be used using the `CODEC` parameter (options: `UNCOMPRESSED`, `SNAPPY` (default), `ZSTD`, `GZIP`).

```sql
-- write a query to a snappy compressed parquet file
COPY (SELECT * FROM tbl) TO 'result-snappy.parquet' (FORMAT 'parquet')
-- write "tbl" to a zstd compressed parquet file
COPY tbl TO 'result-zstd.parquet' (FORMAT 'PARQUET', CODEC 'ZSTD')
-- write a csv file to an uncompressed parquet file
COPY 'test.csv' TO 'result-uncompressed.parquet' (FORMAT 'PARQUET', CODEC 'UNCOMPRESSED')
```

DuckDB's `EXPORT` command can be used to export an entire database to a series of Parquet files. See the [Export statement documentation](../sql/statements/export) for more details.
```sql
-- export the table contents of the entire database as parquet
EXPORT DATABASE 'target_directory' (FORMAT PARQUET);
```
