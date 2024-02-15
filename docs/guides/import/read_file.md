---
layout: docu
title: Directly Reading Files
---

DuckDB allows directly reading files via the [`read_text`](#read_text) and [`read_blob`](#read_blob) functions.
These functions accept a file name, a list of file names or a glob pattern, and output the content of each file as a `VARCHAR` or `BLOB`, respectively, as well as additional metadata such as the file size and last modified time.

## `read_text`

```sql
SELECT size, parse_path(filename), content
FROM read_text('test/sql/table_function/files/*.txt');
```

```text
┌───────┬───────────────────────────────────────────────┬──────────────┐
│ size  │             parse_path(filename)              │   content    │
│ int64 │                   varchar[]                   │   varchar    │
├───────┼───────────────────────────────────────────────┼──────────────┤
│    12 │ [test, sql, table_function, files, one.txt]   │ Hello World! │
│     2 │ [test, sql, table_function, files, three.txt] │ 42           │
│    10 │ [test, sql, table_function, files, two.txt]   │ Föö Bär      │
└───────┴───────────────────────────────────────────────┴──────────────┘
```

## `read_blob`

```sql
SELECT size, content, filename
FROM read_blob('test/sql/table_function/files/*');
```

```text
┌───────┬──────────────────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────┐
│ size  │                                             content                                              │                filename                 │
│ int64 │                                               blob                                               │                 varchar                 │
├───────┼──────────────────────────────────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────┤
│   178 │ PK\x03\x04\x0A\x00\x00\x00\x00\x00\xACi=X\x14t\xCE\xC7\x0A\x00\x00\x00\x0A\x00\x00\x00\x09\x00…  │ test/sql/table_function/files/four.blob │
│    12 │ Hello World!                                                                                     │ test/sql/table_function/files/one.txt   │
│     2 │ 42                                                                                               │ test/sql/table_function/files/three.txt │
│    10 │ F\xC3\xB6\xC3\xB6 B\xC3\xA4r                                                                     │ test/sql/table_function/files/two.txt   │
└───────┴──────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────┘
```

## Handling Missing Metadata

In cases where the underlying filesystem is unable to provide some of this data due (e.g. because HTTPFS can't always return a valid timestamp), the cell is set to `NULL` instead.

## Support for Projection Pushdown

The table functions also utilize projection pushdown to avoid computing properties unnecessarily. So you could e.g. use this to glob a directory full of huge files to get the file size in the size column, as long as you omit the content column the data wont be read into DuckDB.
