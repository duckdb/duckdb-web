---
layout: docu
redirect_from:
- /docs/archive/0.10/guides/import/read_file
title: Directly Reading Files
---

DuckDB allows directly reading files via the [`read_text`](#read_text) and [`read_blob`](#read_blob) functions.
These functions accept a filename, a list of filenames or a glob pattern, and output the content of each file as a `VARCHAR` or `BLOB`, respectively, as well as additional metadata such as the file size and last modified time.

## `read_text`

The `read_text` table function reads from the selected source(s) to a `VARCHAR`.

```sql
SELECT size, parse_path(filename), content
FROM read_text('test/sql/table_function/files/*.txt');
```

| size |             parse_path(filename)              |   content    |
|-----:|-----------------------------------------------|--------------|
| 12   | [test, sql, table_function, files, one.txt]   | Hello World! |
| 2    | [test, sql, table_function, files, three.txt] | 42           |
| 10   | [test, sql, table_function, files, two.txt]   | Föö Bär      |

The file content is first validated to be valid UTF-8. If `read_text` attempts to read a file with invalid UTF-8 an error is thrown suggesting to use [`read_blob`](#read_blob) instead.

## `read_blob`

The `read_blob` table function reads from the selected source(s) to a `BLOB`.

```sql
SELECT size, content, filename
FROM read_blob('test/sql/table_function/files/*');
```

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

|  column_name  | column_type | null | key  | default | extra |
|---------------|-------------|------|------|---------|-------|
| filename      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| content       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| size          | BIGINT      | YES  | NULL | NULL    | NULL  |
| last_modified | TIMESTAMP   | YES  | NULL | NULL    | NULL  |

## Handling Missing Metadata

In cases where the underlying filesystem is unable to provide some of this data due (e.g., because HTTPFS can't always return a valid timestamp), the cell is set to `NULL` instead.

## Support for Projection Pushdown

The table functions also utilize projection pushdown to avoid computing properties unnecessarily. So you could e.g., use this to glob a directory full of huge files to get the file size in the size column, as long as you omit the content column the data wont be read into DuckDB.