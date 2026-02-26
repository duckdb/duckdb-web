---
layout: docu
redirect_from:
- /docs/guides/import/read_file
- /docs/guides/file_formats/read_file
title: Directly Reading Files
---

DuckDB allows directly reading files via the [`read_text`](#read_text) and [`read_blob`](#read_blob) functions.
These functions accept a filename, a list of filenames, or a glob pattern. They output the content of each file as a `VARCHAR` or `BLOB`, respectively, along with metadata such as the file size and last modified time.

## `read_text`

The `read_text` table function reads from the selected source(s) to a `VARCHAR`. Each file results in a single row with the `content` field holding the entire content of the respective file.

```sql
SELECT size, parse_path(filename), content
FROM read_text('test/sql/table_function/files/*.txt');
```

<div class="monospace_table"></div>

| size |             parse_path(filename)              |      content     |
|-----:|-----------------------------------------------|------------------|
| 12   | [test, sql, table_function, files, one.txt]   | Hello World!     |
| 2    | [test, sql, table_function, files, three.txt] | 42               |
| 10   | [test, sql, table_function, files, two.txt]   | Foo Bar\nFöö Bär |

DuckDB first validates the file content as valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8, DuckDB throws an error suggesting to use [`read_blob`](#read_blob) instead.

## `read_blob`

The `read_blob` table function reads from the selected source(s) to a `BLOB`:

```sql
SELECT size, content, filename
FROM read_blob('test/sql/table_function/files/*');
```

<div class="monospace_table"></div>

| size |                              content                         |                filename                 |
|-----:|--------------------------------------------------------------|-----------------------------------------|
| 178  |  PK\x03\x04\x0A\x00\x00\x00\x00\x00\xACi=X\x14t\xCE\xC7\x0A… | test/sql/table_function/files/four.blob |
| 12   | Hello World!                                                 | test/sql/table_function/files/one.txt   |
| 2    | 42                                                           | test/sql/table_function/files/three.txt |
| 10   | F\xC3\xB6\xC3\xB6 B\xC3\xA4r                                 | test/sql/table_function/files/two.txt   |

## Schema

The schemas of the tables returned by `read_text` and `read_blob` are identical:

```sql
DESCRIBE FROM read_text('README.md');
```

<div class="monospace_table"></div>

|  column_name  | column_type | null | key  | default | extra |
|---------------|-------------|------|------|---------|-------|
| filename      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| content       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| size          | BIGINT      | YES  | NULL | NULL    | NULL  |
| last_modified | TIMESTAMP   | YES  | NULL | NULL    | NULL  |

## Hive Partitioning

Data can be read from [Hive partitioned]({% link docs/stable/data/partitioning/hive_partitioning.md %}) datasets.

```sql
SELECT *
FROM read_blob('data/parquet-testing/hive-partitioning/simple/**/*.parquet')
WHERE part IN ('a', 'b') AND date >= '2012-01-01';
```

<div class="monospace_table"></div>

|             filename                  |           content             | size |      last_modified     |    date    |  part   |
|---------------------------------------|-------------------------------|------|------------------------|------------|---------|
| …/part=a/date=2012-01-01/test.parquet | PAR1\x15\x00\x15\x14\x15\x18… | 266  | 2024-11-12 02:23:20+00 | 2012-01-01 | a       |
| …/part=b/date=2013-01-01/test.parquet | PAR1\x15\x00\x15\x14\x15\x18… | 266  | 2024-11-12 02:23:20+00 | 2013-01-01 | b       |


## Handling Missing Metadata

When the underlying filesystem cannot provide this data (e.g., HTTPFS may not always return a valid timestamp), the cell is set to `NULL` instead.

## Support for Projection Pushdown

These table functions also use projection pushdown to avoid computing properties unnecessarily. For example, you can glob a directory of large files to get file sizes in the `size` column. As long as you omit the `content` column, DuckDB won't read the file data.
