---
github_repository: https://github.com/duckdb/duckdb-aws-glue
layout: docu
redirect_from:
- /docs/current/core_extensions/glue
- /docs/preview/core_extensions/glue
- /docs/stable/core_extensions/glue
title: AWS Glue Extension
---

> Warning The `glue` extension is experimental. Its features, settings, and behavior may change in future releases. Use its DDL and DML statements in production at your own risk: there is no guarantee that all incompatibilities between DuckDB and other engines (e.g., Trino and Spark) writing to Hive tables in Glue have been discovered.

The `glue` extension attaches an [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) as a DuckDB database. You can list, read, create, and insert into its Hive tables (Glue's native tables) stored as Parquet, CSV, JSON, or Avro files on S3. The extension also supports Hive-style partition management and Glue views.

Tables of other formats that Glue registers (Iceberg, Delta Lake, Hudi, etc.) are listed with the columns Glue reports, but they cannot be read or written through the `glue` extension. To read and write Iceberg tables in Glue, use the [`iceberg` extension]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}#aws-glue-amazon-sagemaker-lakehouse).

> New The `glue` extension was introduced in DuckDB 2.0.

## Installing and Loading

The `glue` extension will be transparently [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD glue;
```

The extension loads the `parquet` extension itself. The [`avro` extension]({% link docs/2.0/core_extensions/avro.md %}) is loaded on demand when a query reads an Avro table.

## Usage

The `glue` extension uses an `s3` or `aws` [secret]({% link docs/2.0/configuration/secrets_manager.md %}) both to call the Glue API and to read and write the table files on S3. For example, to use the [`credential_chain` provider]({% link docs/2.0/core_extensions/aws.md %}#credential_chain-provider) of the `aws` extension, create a secret and attach the catalog:

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    REGION 'eu-central-1'
);
ATTACH '⟨account_id⟩' AS my_datalake (TYPE glue);
```

Then, query the catalog's tables:

```sql
SHOW ALL TABLES;
SELECT * FROM my_datalake.default.some_table;
```

Each Glue database is a schema of the attached catalog.

### Catalog Identifiers

The path passed to `ATTACH` identifies the Glue catalog. It uses the same formats as Glue's own catalog ID parameter:

| Path | Catalog |
| --- | --- |
| `:` | Default catalog of the current account |
| `⟨account_id⟩` | Default catalog of the account with the given 12-digit ID |
| `⟨account_id⟩:⟨catalog⟩` | Catalog `⟨catalog⟩` in the given account |
| `⟨catalog⟩/⟨subcatalog⟩` | Nested catalog in the current account |
| `⟨account_id⟩:⟨catalog⟩/⟨subcatalog⟩` | Nested catalog in the given account |

### Attach Options

When attaching a Glue catalog, you can pass the following options to [`ATTACH`]({% link docs/2.0/sql/statements/attach.md %}):

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `SECRET` | `VARCHAR` | default secret | Name of the `s3` or `aws` secret to take the credentials from. |
| `REGION` | `VARCHAR` | region of the secret | AWS region of the catalog. If neither the option nor the secret specifies a region, `ATTACH` fails. |
| `ENDPOINT` | `VARCHAR` | AWS | Glue endpoint override, e.g., `http://localhost:5000` for a local [moto](https://github.com/getmoto/moto) server. |
| `DEFAULT_LOCATION` | `VARCHAR` | | S3 prefix for new databases and for tables created without an explicit location. It takes precedence over the Glue database's `LocationUri`. |
| `DEFAULT_SCHEMA` | `VARCHAR` | | Glue database to use as the default schema. It must exist. |
| `READ_ONLY` | `BOOLEAN` | `false` | Refuse everything that changes the catalog: DML, DDL, and the mutating `glue_*` functions. |
| `ICEBERG_CATALOG` | `VARCHAR` | | Name of an attached Iceberg catalog over the same Glue catalog. Glue views read their Iceberg tables from it, see [Views](#views). |
| `VERIFY_CONNECTION` | `BOOLEAN` | `true` | Check during `ATTACH` that the catalog can be reached with the given credentials. |

## Reading Tables

### Table Formats

Each table's format is determined from its parameters (`table_type`, `spark.sql.sources.provider`, `metadata_location`) and otherwise from its `InputFormat`. The format is shown in the `tags` column of [`duckdb_tables()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_tables) as `tags['table_type']`, which is one of `HIVE`, `ICEBERG`, `DELTA`, `HUDI`, `SYMLINK`, or `UNKNOWN`. Only `HIVE` tables can be read and written.

Hudi tables (e.g., `HoodieParquetInputFormat`) and symlink manifest tables (`SymlinkTextInputFormat`, e.g., a Delta `_symlink_format_manifest`) register a Parquet or text SerDe, so only their `InputFormat` tells them apart from a Hive table. Like Iceberg and Delta tables, they are listed but cannot be read or written.

### SerDes

The SerDe of the Glue table determines the reader:

| SerDe | Reader | Columns matched |
| --- | --- | --- |
| `ParquetHiveSerDe` | [`read_parquet`]({% link docs/2.0/data/parquet/overview.md %}) | by name |
| `LazySimpleSerDe` | [`read_csv`]({% link docs/2.0/data/csv/overview.md %}) | by position |
| `OpenCSVSerde` | [`read_csv`]({% link docs/2.0/data/csv/overview.md %}) | by position |
| Hive `JsonSerDe` and OpenX `JsonSerDe` | [`read_json`]({% link docs/2.0/data/json/overview.md %}) (one object per line) | by name, ignoring case |
| `AvroSerDe` | [`read_avro`]({% link docs/2.0/core_extensions/avro.md %}) | by name |

Other SerDes (ORC, Ion, etc.) are not supported.

A Parquet `BYTE_ARRAY` column without a `STRING` annotation (as produced by Impala and older Hive writers) is read as UTF-8 text when Glue declares the column `string` (bytes that are not valid UTF-8 are an error), and as bytes when Glue declares it `binary`, regardless of the [`binary_as_string` setting]({% link docs/2.0/data/parquet/overview.md %}#parameters).

CSV and JSON files are decompressed based on their file name extension (`.gz`, `.zst`), regardless of the codec recorded in the table. Parquet and Avro files carry their codec themselves.

### Text Tables

Text tables are read following the semantics of their SerDe as closely as possible.

`LazySimpleSerDe`:

* The delimiter is `field.delim`, else `serialization.format`, else `\001`. A number from -128 to 127 is a byte code, e.g., `'1'` is `\001` and `'9'` is a tab.
* The `NULL` string is `serialization.null.format`, `\N` by default. Fields are not quoted.
* With a single-byte `escape.delim`, the escape character makes the next character part of the field, including the delimiter (`a\,b` is `a,b`, `\\` is `\`). `\N` is still `NULL`.
* The `timestamp.formats` property is treated as a list of hints: a `timestamp` field is tried with [`try_strptime`]({% link docs/2.0/sql/functions/dateformat.md %}) and each pattern that `strptime` can express (the first match wins), then as milliseconds since the epoch if `millis` is listed, and finally with a regular cast. Patterns with a time zone, a fraction other than `SSS`, or no year are ignored.

`OpenCSVSerde`:

* The table's `separatorChar` (default `,`), `quoteChar` (default `"`), and `escapeChar` (default `\`) are used.
* An empty field is an empty string: there is no `NULL`.
* A `boolean` field is `true` when it is `true` in any case, and `false` otherwise.
* A `timestamp` field is a number of milliseconds since the epoch (`1579059880000` is `2020-01-15 03:44:40`) and a `date` field is a number of days since the epoch (`18276` is `2020-01-15`). Text such as `2020-01-15` does not parse.
* Unlike Hive, which reads files line by line, DuckDB reads a quoted field across line breaks. A quoted line break fails a parallel scan; `SET hive_csv_parallel = false` reads each file with a single thread, which supports quoted line breaks.

Both SerDes:

* `skip.header.line.count` lines are skipped at the start of every file.
* Short rows are padded with `NULL` values and extra fields are ignored.
* Values that do not parse as their column type are `NULL`. In `OpenCSVSerde` tables, they fail the query unless the `use.null.for.invalid.data` property is `true`.
* Fields are converted with `TRY_CAST`, which differs from Hive in details: surrounding spaces are ignored, `'1.5'` in an `int` column is `2` (Hive: `1`), and blank lines are skipped (Hive: a row of `NULL` values).
* A line may be up to `hive_csv_max_line_size` bytes long (default: 8,000,000; Hive has no limit). A longer line fails the query.
* As in Hive, a table property overrides the SerDe property of the same name. Keys are case-sensitive.

The following features are not supported for reads and writes: footer lines (`skip.footer.line.count`), header lines in JSON tables, nested columns in text tables, multi-byte quote or escape characters, and, for `LazySimpleSerDe`, `serialization.escape.crlf`, `serialization.last.column.takes.rest`, non-UTF-8 `serialization.encoding`, and `NUL` or line-break delimiters.

### JSON Tables

* JSON keys are matched to columns ignoring (ASCII) case at every nesting level, as both JSON SerDes do. An OpenX table with `case.insensitive=false` matches them exactly.
* With `ignore.malformed.json` or `use.null.for.invalid.data` set to `true` in an OpenX table, a line that is not valid JSON is read as a row of `NULL` values and a value that does not fit its column is `NULL`.
* Other JSON SerDe properties that change how files are read (OpenX `mapping.*` and `dots.in.keys`, Hive `timestamp.formats`) are not applied. The read succeeds and a warning is logged.

### Partitions and Files

* The data files of a table are those below the location of every partition Glue lists, at any depth, or below the table location for an unpartitioned table. Partition locations do not need to follow the `⟨key⟩=⟨value⟩` layout. Files and directories whose names start with `_` or `.`, `*_$folder$` directory markers, and empty objects are skipped.
* Partition column values are the values Glue stores for the partition (not the directory names), typed as Glue's partition keys.
* Filters on partition columns, including those derived from the build side of a join, are applied to the partition values first, so only the partitions a query reads are listed on S3. [`EXPLAIN`]({% link docs/2.0/guides/meta/explain.md %}) shows the partitions kept.
* The schema of a table is Glue's: data columns first and partition keys last, in `PARTITIONED BY` order. Files are matched by column name: a column a file does not have reads as `NULL`, a column with a different type in the file is cast, and file columns that Glue does not list are ignored.
* A partition declares its own columns. A scan that reads a column that a partition declares with a type that cannot be read as the table's type fails with an error naming the partition and both types.
* A partition whose own `InputFormat`, SerDe, or SerDe properties differ from the table's (e.g., a CSV partition of a Parquet table) fails the scan with an error naming the partition.
* A table with [Athena partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html) (`projection.enabled = true`) is refused, as a scan would silently read nothing. To read it, set `projection.enabled` to `false` and register its partitions.
* A location shared by two or more partitions is refused when a query reads one of them and the location holds data files.
* `s3a://` and `s3n://` locations are read as `s3://`.

Besides the `filename` column, scans offer three virtual columns, modeled after Trino's Hive connector, which `SELECT *` leaves out: `"$path"` (the data file), `"$file_size"` (`BIGINT`), and `"$file_modified_time"` (`TIMESTAMP WITH TIME ZONE`).

```sql
SELECT "$path", "$file_size", count(*)
FROM my_datalake.default.some_table
GROUP BY ALL;
```

### Caching and Consistency

Within a DuckDB transaction, a table's definition and its list of partitions are fetched from Glue once and reused, while the files inside the partitions are listed at each scan. Therefore, a partition added outside the transaction becomes visible only after the transaction ends, while a file added to an existing partition is seen by the next query.

With `SET glue_metadata_cache_scope = 'connection'`, the metadata cache also serves the connection's later transactions. The cache is per connection, so another connection's writes stay unseen until something clears this connection's cache: a write through it, a rollback, or `DETACH`.

With `SET glue_cache_listings = true`, S3 listings are also kept for later statements of the connection, and are cleared like the metadata cache. Files added any other way (e.g., by another writer) appear only after the next clear, and files removed any other way (e.g., by compaction) make scans fail until then. This setting is suitable for hosts that run one query per connection.

## Writing Tables

Glue has no transactions: DDL takes effect immediately, files are visible as soon as they are written, and nothing is rolled back on failure. Therefore, DDL statements, `INSERT`, and the `glue_*` functions that change Glue are not allowed inside an explicit `BEGIN` transaction; run them as statements of their own. `DELETE`, `UPDATE`, and `MERGE INTO` are not supported.

### Creating Schemas

`CREATE SCHEMA` creates a Glue database:

```sql
CREATE SCHEMA my_datalake.sales
WITH (comment = 'Sales data', location = 's3://⟨bucket⟩/sales');
```

The `comment` option sets the database's description and `location` sets its `LocationUri` (default: `⟨DEFAULT_LOCATION⟩/⟨schema⟩`, or none if the catalog was attached without `DEFAULT_LOCATION`). Any other key is stored as a database parameter (Hive's `DBPROPERTIES`).

`ALTER SCHEMA ... SET (⟨key⟩ = '⟨value⟩', ...)` merges options into the Glue database and `ALTER SCHEMA ... RESET (⟨key⟩, ...)` removes them:

```sql
ALTER SCHEMA my_datalake.sales SET (owner = 'analytics');
ALTER SCHEMA my_datalake.sales RESET (owner);
```

### Creating Tables

`CREATE TABLE` creates a Hive table in Glue:

```sql
CREATE TABLE my_datalake.sales.orders (
    id BIGINT,
    amount DOUBLE,
    dt VARCHAR
)
PARTITIONED BY (dt)
WITH (format = 'parquet');
```

The `WITH` clause supports the following options:

* `format`: `'parquet'` (default), `'csv'` (`LazySimpleSerDe`, comma-delimited, no header), `'json'` (Hive `JsonSerDe`, one object per line), or `'avro'` (`AvroSerDe`).
* `location`: the S3 location of the table. Without it, the table is created at `⟨DEFAULT_LOCATION⟩/⟨database⟩/⟨table⟩`, else at `⟨database LocationUri⟩/⟨table⟩`. If neither is available, the statement fails.
* For CSV tables: `delimiter = '|'` sets the field delimiter (`field.delim`) and `header = true` makes every file start with a header line. `quote = '"'` and `escape = '\'` switch the table to `OpenCSVSerde`.
* Any other key is stored as a Glue table parameter (Hive's `TBLPROPERTIES`), e.g., `'parquet.compression' = 'ZSTD'`. Other engines' spellings of options that this extension spells differently (e.g., `partitioned_by`, `external_location`, and `field_delimiter`) are refused.

Partition keys must be plain column names. They become Glue partition keys and are listed last in the table's columns. Generated columns, column defaults, and collated columns are refused.

Column types are stored as Hive types. DuckDB types without a Hive type are refused, e.g., `UBIGINT`, `HUGEINT`, and `TIMESTAMP_NS` (Hive's `timestamp` corresponds to DuckDB's microsecond-precision `TIMESTAMP`).

Bucketed (clustered) tables can be created with the `BucketColumns`, `NumberOfBuckets`, and `SortColumns` options after setting `SET glue_create_bucketed_tables = true`. DuckDB reads such tables, but does not write to them.

### Inserting Data

`INSERT INTO` and `CREATE TABLE ... AS` write files in the table's format to the table location and register new partitions in Glue:

```sql
INSERT INTO my_datalake.sales.orders
    SELECT * FROM 'orders.csv';

CREATE TABLE my_datalake.sales.daily_totals
PARTITIONED BY (dt)
WITH (format = 'csv', delimiter = '|') AS
    SELECT dt, sum(amount) AS total
    FROM my_datalake.sales.orders
    GROUP BY dt;
```

* Each write produces one file per partition touched. Partition columns are not stored in the files.
* New partitions get `⟨key⟩=⟨value⟩` directories. Rows of an existing partition are written to its registered location, which may be any directory below the table location.
* Because partition keys are the last columns of a table, `INSERT ... VALUES` without a column list must list them last.
* The files of a statement are named `⟨write_id⟩_⟨file_id⟩.⟨extension⟩`, with a new write ID (UUIDv7) for each statement. If the statement fails, DuckDB deletes the files it wrote (and, for `CREATE TABLE ... AS`, the Glue table it created), so the statement can be run again. This is best effort: if the process dies, the files remain.
* Other queries can read the files of an insert before it finishes.
* Written files are compressed as the table specifies: Parquet with `parquet.compression`, CSV and JSON with the codec the table records (gzip or zstd), and Avro with `avro.output.codec`.

`CREATE TABLE ... AS` creates the Glue table when the statement starts executing. It is refused when the location already holds data files, e.g., those of a dropped table. `WITH (overwrite = true)` deletes these files before creating the table. It is refused when the location overlaps with the location of another table in the same Glue database.

Writes are refused to bucketed tables, to tables with the OpenX JSON SerDe, and to tables whose `InputFormat` is not one that Hive uses for its file formats.

With `SET glue_store_written_files = true`, every write adds the data files it wrote to the temporary table `temp.main.glue_written_files`, with one row per file containing the statement's `query_id`, the `table`, and the `file_path`:

```sql
SET glue_store_written_files = true;
INSERT INTO my_datalake.sales.orders
    SELECT * FROM 'orders.csv';
SELECT file_path
FROM temp.main.glue_written_files
WHERE query_id = (SELECT max(query_id) FROM temp.main.glue_written_files);
```

### Altering Tables

The following statements update the Glue table definition:

* `ALTER TABLE ... ADD COLUMN` appends a column (no defaults or collations).
* `ALTER TABLE ... DROP COLUMN` drops a column. The last data column, partition keys, and bucket or sort columns cannot be dropped.
* `ALTER TABLE ... ALTER COLUMN ... TYPE` changes a column's type. As existing data files keep their types, only widening changes are allowed: integer widening (e.g., `TINYINT` to `BIGINT`), `FLOAT` to `DOUBLE`, and any type to `VARCHAR`. Partition keys cannot be retyped and `USING` expressions are not supported.
* `ALTER TABLE ... RENAME COLUMN` is only supported for CSV tables, whose files are read by position. In other formats, a rename would make existing data read as `NULL`.
* `COMMENT ON COLUMN` sets the Glue column comment.
* `ALTER TABLE ... SET (⟨key⟩ = '⟨value⟩', ...)` adds or overwrites table parameters and `ALTER TABLE ... RESET (⟨key⟩, ...)` removes them. The parameters that determine the table format cannot be changed.

```sql
ALTER TABLE my_datalake.sales.orders ADD COLUMN customer VARCHAR;
COMMENT ON COLUMN my_datalake.sales.orders.amount IS 'order amount in USD';
ALTER TABLE my_datalake.sales.orders SET ('parquet.compression' = 'ZSTD');
```

The `glue_replace_columns` function is the equivalent of Hive's `ALTER TABLE ... REPLACE COLUMNS`: it replaces all data columns of a table at once, which can also rename and reorder them. Columns that stay (compared case-insensitively) may only be widened. As in Hive, comments are dropped unless given in `comments` or kept with `keep_comments := true`. The partition keys are kept and must not be listed. The data files are not rewritten.

```sql
CALL glue_replace_columns(
    'my_datalake.sales.orders',
    {id: 'BIGINT', amount: 'DOUBLE', customer_name: 'VARCHAR'},
    comments := {amount: 'order amount in USD'}
);
```

### Dropping Tables and Schemas

`DROP TABLE` and `DROP SCHEMA` delete the Glue entries but leave the data files on S3. As Glue deletes all tables of a database when the database is dropped, `DROP SCHEMA` refuses a database that still has tables or views unless `CASCADE` is given.

## Views

`CREATE [OR REPLACE] VIEW` creates a Glue view (a table of type `VIRTUAL_VIEW`) marked as written by DuckDB:

```sql
CREATE VIEW my_datalake.sales.large_orders AS
    SELECT * FROM orders WHERE amount > 1000;
```

* Unqualified table names in the view's query refer to the view's own database.
* `SHOW TABLES`, `duckdb_views()`, `information_schema.views`, and `duckdb_columns()` list every view of a database, including views written by other engines. Only views written by DuckDB can be queried, replaced, or dropped.
* Other engines do not query DuckDB views.
* `CREATE VIEW ... WITH (DEFER_BINDING)`, `ALTER VIEW ... RENAME`, and `COMMENT ON VIEW` are not supported.

A view can join Hive and Iceberg tables of the same Glue catalog. The Iceberg tables are read through an [Iceberg attachment]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}#aws-glue-amazon-sagemaker-lakehouse) of the same catalog, named by the `ICEBERG_CATALOG` attach option:

```sql
ATTACH '⟨account_id⟩' AS lake (TYPE glue, ICEBERG_CATALOG 'lake_ice');
ATTACH '⟨account_id⟩' AS lake_ice (TYPE iceberg, ENDPOINT_TYPE glue);
CREATE VIEW lake.sales.orders_by_customer AS
    SELECT c.name, o.amount
    FROM lake.sales.customers c
    JOIN lake_ice.sales.orders o ON c.id = o.id;
```

Configure both attachments for the same region and endpoint.

With `SET experimental_glue_view_external_catalog_types = ['duckdb', 'iceberg']`, views can also read tables of catalogs of the given types. Such tables are stored by catalog type and alias, and are read wherever a catalog of that type is attached under that alias. This setting is global and is empty by default.

## Partitions

DuckDB has no `ALTER TABLE ... PARTITION` syntax, so the Hive partition statements are available as table functions. The partition is given as a struct naming every partition key. The table name may be partially qualified (e.g., `'db.t'`, or `'t'` after `USE my_datalake.db`).

| Function | Hive statement |
| --- | --- |
| `glue_partitions('⟨table⟩')` | `SHOW PARTITIONS`: one row per registered partition with a typed column per partition key, `location`, and `partition_values` (the strings Glue stores) |
| `CALL glue_add_partition('⟨table⟩', ⟨partition⟩, location := '⟨location⟩', if_not_exists := false)` | `ALTER TABLE ADD [IF NOT EXISTS] PARTITION (...) [LOCATION ...]`. Without `location`, the partition is placed at `⟨table location⟩/⟨key⟩=⟨value⟩/...`. |
| `CALL glue_drop_partition('⟨table⟩', ⟨partition⟩, if_exists := false)` | `ALTER TABLE DROP [IF EXISTS] PARTITION (...)`. The data files stay on S3. |
| `CALL glue_rename_partition('⟨table⟩', ⟨partition⟩, ⟨new_partition⟩)` | `ALTER TABLE PARTITION (...) RENAME TO PARTITION (...)`. The location is kept. |
| `CALL glue_set_partition_location('⟨table⟩', ⟨partition⟩, '⟨location⟩')` | `ALTER TABLE PARTITION (...) SET LOCATION '...'` |
| `CALL glue_set_table_location('⟨table⟩', '⟨location⟩')` | `ALTER TABLE SET LOCATION '...'`. Existing partitions keep their locations. |
| `CALL glue_repair_table('⟨table⟩')` | `MSCK REPAIR TABLE`: registers the `⟨key⟩=⟨value⟩` partition directories under the table location that are not yet in Glue. Returns one row per added partition. It never removes partitions. |

For example:

```sql
CALL glue_add_partition(
    'my_datalake.sales.orders',
    {dt: '2026-11-01'},
    location := 's3://⟨bucket⟩/imports/2026-11-01/'
);
SELECT * FROM glue_partitions('my_datalake.sales.orders');
CALL glue_drop_partition('my_datalake.sales.orders', {dt: '2026-11-01'});
```

In `glue_partitions`, a typed partition key column is `NULL` both for the `NULL` partition (which Glue stores as `__HIVE_DEFAULT_PARTITION__`) and for a value that the key's type cannot hold, e.g., `abc` registered by another tool for an integer key. The latter fails every filtered read of the table. To find such partitions, compare the typed columns with `partition_values`:

```sql
SELECT location, partition_values
FROM glue_partitions('my_datalake.default.events')
WHERE (year IS NULL) <> (partition_values[1] = '__HIVE_DEFAULT_PARTITION__');
```

### Hive Partition Statements

The Hive partition statements are also available as SQL through the `glue_hive_ddl` grammar extension, which is enabled per connection:

```sql
SET active_grammar_extensions = ['glue_hive_ddl'];
ALTER TABLE my_datalake.sales.orders ADD IF NOT EXISTS
    PARTITION (dt = '2026-11-01')
    PARTITION (dt = '2026-11-02') LOCATION 's3://⟨bucket⟩/imports/2026-11-02/';
ALTER TABLE my_datalake.sales.orders DROP IF EXISTS
    PARTITION (dt = '2026-11-01'), PARTITION (dt = '2026-11-02');
ALTER TABLE my_datalake.sales.orders PARTITION (dt = '2026-11-03')
    RENAME TO PARTITION (dt = '2026-11-04');
ALTER TABLE my_datalake.sales.orders PARTITION (dt = '2026-11-04')
    SET LOCATION 's3://⟨bucket⟩/other/';
ALTER TABLE my_datalake.sales.orders SET LOCATION 's3://⟨bucket⟩/orders_v2/';
```

Actions can be chained in one statement. Every action is checked against Glue before any is applied, so a statement that fails changes nothing. Dropping partitions requires the `glue:BatchGetPartition` and `glue:BatchDeletePartition` permissions.

## Reading Hive Tables without a Catalog: `hive_scan`

The `hive_scan` table function reads Hive tables that are not (or not yet) registered in Glue. The schema and the partitions are given as arguments, and nothing is looked up in a catalog:

```sql
SELECT *
FROM hive_scan(
    's3://⟨bucket⟩/warehouse/orders',
    schema := {id: 'INTEGER', amount: 'DOUBLE', dt: 'VARCHAR', country: 'VARCHAR'},
    partitions := [
        {dt: '2016-05-14', country: 'IN', location: NULL},
        {dt: '2016-05-16', country: 'IN', location: 's3://⟨bucket⟩/imports/INDIA_16_May_2016'}
    ]
);
```

The function supports the following parameters:

| Parameter | Description |
| --- | --- |
| `schema` | Required. A struct of column names to DuckDB type names, including both data columns and partition columns. |
| `format` | `'parquet'` (default), `'csv'`, `'json'`, or `'avro'`. |
| `partitions` | A list with one struct per partition, with a value for every partition key and an optional `location`. Without a location, the partition is read from `⟨root⟩/⟨key⟩=⟨value⟩/...`. Without `partitions`, the table is unpartitioned and all files below the root are read. |
| `partition_keys` | The names of the partition keys. By default, the fields of the `partitions` structs other than `location`, in that order. |
| `header`, `delim`, `quote`, `escape`, `nullstr` | For CSV: describe the files, as in `read_csv`. |
| `ignore_errors` | For JSON: read a line that is not valid JSON as a row of `NULL` values. |

CSV columns are matched by position, JSON keys by name. A root or partition without data files scans as zero rows.

## Inspecting Glue Metadata

The full Glue definition of tables, partitions, and databases is available through table functions. Each returns one row with the most important properties as columns, plus the complete Glue object as a [`VARIANT`]({% link docs/2.0/sql/data_types/variant.md %}) in the `response` column:

```sql
SELECT * FROM glue_get_table_response('my_datalake.default.some_table');
SELECT response.StorageDescriptor.Location
FROM glue_get_table_response('my_datalake.default.some_table');

SELECT location, response.StorageDescriptor.InputFormat
FROM glue_get_partition_response('my_datalake.default.some_table', {dt: '2024-01-01'});

SELECT * FROM glue_get_database_response('my_datalake.default');
```

For a table that DuckDB cannot read (e.g., because of an unsupported column type), pass the fully qualified name to `glue_get_table_response`.

## Logging

The AWS SDK's Glue calls are routed through DuckDB's HTTP layer (`httpfs`), so they honor DuckDB's proxy and certificate settings and appear in the [HTTP log]({% link docs/2.0/operations_manual/logging/overview.md %}). The `glue_requests()` table macro lists the Glue requests in the HTTP log, including retries and pages, with their `operation` (e.g., `AWSGlue.GetPartitions`), `status`, `reason`, `start_time`, `duration_ms`, `connection_id`, `transaction_id`, and `query_id`.

The extension also registers two log types:

* `GlueScan` (`INFO` level): records what each scan of a Hive table does, with one entry per `event` (`partitions`, `plan`, `listing`, `sample`, `footers`), e.g., how many partitions were loaded and read, and how many files were listed.
* `GlueRetry` (`WARNING` level): records each retry of a Glue API call, with the `error` that caused it (e.g., `ThrottlingException`), its HTTP `status`, the `retry` number, and the `request_id` of the failed attempt.

```sql
CALL enable_logging(['HTTP', 'GlueScan', 'GlueRetry'], storage = 'memory');
-- run queries
SELECT operation, count(*), sum(duration_ms)
FROM glue_requests()
GROUP BY operation;
SELECT "table", scan_id, event, partitions, partitions_read, listings, files, duration_ms
FROM duckdb_logs_parsed('GlueScan');
SELECT error, status, count(*)
FROM duckdb_logs_parsed('GlueRetry')
GROUP BY ALL;
```

## Settings

| Setting | Default | Description |
| --- | --- | --- |
| `experimental_glue_view_external_catalog_types` | `[]` | Types of non-Glue catalogs (e.g., `['duckdb', 'iceberg']`) whose tables Glue views may read. Global only. |
| `glue_batch_table_lookup` | `true` | After the first table of a database is looked up, fetch one `GetTables` page of the database instead of a `GetTable` call per table. |
| `glue_cache_listings` | `false` | Keep the S3 listings of tables for later statements of the connection, see [Caching and Consistency](#caching-and-consistency). |
| `glue_create_bucketed_tables` | `false` | Allow `CREATE TABLE` to create bucketed (clustered) Hive tables. |
| `glue_enable_partition_key_statistics` | `false` | Give the optimizer the bounds and distinct count of partition keys, from the partitions a scan reads. |
| `glue_get_partitions_segments` | `0` | Number of `GetPartitions` requests to run concurrently when listing a table's partitions (at most 10). `0` uses 8 against AWS and 1 against a custom `ENDPOINT`. |
| `glue_max_retries` | `-1` | Retry limit for Glue API calls (at most 10). `-1` uses the AWS SDK's retry policy. |
| `glue_metadata_cache_scope` | `'transaction'` | How long Glue metadata is reused: `'transaction'` or `'connection'`, see [Caching and Consistency](#caching-and-consistency). |
| `glue_network_calls_via_duckdb` | `true` | Route Glue API calls through DuckDB's HTTP layer instead of the AWS SDK's own HTTP client. |
| `glue_store_written_files` | `false` | Record the files written by each write in `temp.main.glue_written_files`. |
| `hive_csv_max_line_size` | `8000000` | Maximum line length in bytes when reading CSV tables. |
| `hive_csv_parallel` | `true` | Read each file of a CSV table with multiple threads. Set to `false` to read files with quoted line breaks. |
| `hive_footer_statistics_max_files` | `16` | For unpartitioned Parquet tables with at most this many files, read the row count and column statistics from the footers of all files (at most 25). `0` disables it. |
| `hive_partition_listing_threshold` | `NULL` | When set, a scan reading at least this many partitions below the table location lists the location once instead of each partition. |

## Limitations

* Only Hive tables (Parquet, CSV, JSON, and Avro) can be read and written. Iceberg, Delta Lake, Hudi, and symlink manifest tables are listed but cannot be read.
* ORC and Ion SerDes are not supported.
* `DELETE`, `UPDATE`, and `MERGE INTO` are not supported.
* Glue has no transactions: DDL statements and writes cannot be part of an explicit transaction, and they are not rolled back on failure.
* Writes to bucketed tables and to OpenX JSON tables are not supported.
* Tables with Athena partition projection cannot be read.
