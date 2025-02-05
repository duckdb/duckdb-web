---
layout: post
title: "Announcing DuckDB 1.2.0"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-2-0.svg"
image: "/images/blog/thumbs/duckdb-release-1-2-0.png"
excerpt: "The DuckDB team is happy to announce that today we're releasing DuckDB version 1.2.0, codenamed “Histrionicus”."
---

To install the new version, please visit the [installation guide]({% link docs/installation/index.html %}).
For the release notes, see the [release page](https://github.com/duckdb/duckdb/releases/tag/v1.2.0).

> Some packages (R, Java) take a few extra days to release due to the reviews required in the release pipelines.

We are proud to release DuckDB 1.2.0. This release is codenamed “Histrionicus” after the good-looking [Harlequin duck (Histrionicus histrionicus)](https://en.wikipedia.org/wiki/Harlequin_duck), that inhabits "cold fast moving streams in North America, Greenland, Iceland and eastern Russia".

## What's New in 1.2.0

### Breaking Changes

[**The `random` function now uses a larger state.**](https://github.com/duckdb/duckdb/pull/13920)
This means that it's even more random™ now. Due to this change fixed seeds will now produce different values than the previous versions of DuckDB.

[**`map['entry']` now returns a value, instead of a *list* of entries.**](https://github.com/duckdb/duckdb/pull/14175)
For example, `map(['k'], ['v'])['k']` now returns `v`, while previously it returned `['v']`. We also introduced the `map_extract_value`, which is now the alias for the bracket operator `[]`.
Note that [`map_extract`]({% link docs/sql/functions/map.md %}#map_extractmap-key) still returns a list: `map(['k'], ['v']), 'k' = ['v']`.

[**The indexing of `list_reduce` was fixed.**](https://github.com/duckdb/duckdb/pull/15614)
The indexing starts from 1 now.

There have been far too many changes to discuss them each in detail, but we would like to highlight several particularly exciting features!
Below is a summary of those new features with examples.

### Explicit Storage Versions

DuckDB v1.2.0 ships new compression methods but *they are not yet enabled by default* to enable older DuckDB versions to read files.

In practice, this means the following: DuckDB v1.2.0 can read database files written by past stable DuckDB versions such as v1.1.3. When using DuckDB v1.2.0 with default settings, older versions can read files written by DuckDB v1.2.0.

Users can *opt-in to newer forwards incompatible features* using the following syntax:

```sql
ATTACH 'file.db' (STORAGE_VERSION 'v1.2.0');
```

This setting specifies the minimum DuckDB version that should be able to read the database file. When database files are written with this option, the resulting files cannot be opened by older DuckDB released versions than the specified version. They can be read by the specified version and all newer versions of DuckDB.

```sql
SELECT database_name, tags
FROM duckdb_databases();
```

This shows the storage versions:

```text
file1  │ {storage_version=v1.0.0 - v1.1.3}
file2  │ {storage_version=v1.2.0}
```

Meaning `file1` can be opened by past DuckDB versions while `file2` is compatible only with `v1.2.0` (or future versions).

To convert from the new format to the old format, use the following sequence in DuckDB v1.2.0:

```sql
ATTACH 'file1.db';
ATTACH 'file2.db' (STORAGE_VERSION 'v1.0.0');
COPY FROM DATABASE file1 TO file2;
```

### Indexing

[**`ALTER TABLE ... ADD PRIMARY KEY`.**] (https://github.com/duckdb/duckdb/pull/14419)
After a long while, DuckDB is finally able to add a primary key to an existing table 🎉. So it is now possible to run this:

```sql
CREATE TABLE tbl(id INTEGER);
INSERT INTO tbl VALUES (42);
ALTER TABLE tbl ADD PRIMARY KEY (id);
```

[**Over-eager constraint checking addressed.**](https://github.com/duckdb/duckdb/pull/15092)

We also resolved a long-standing issue with [over-eager unique constraint checking]({% link docs/archive/1.0/sql/indexes.md %}#over-eager-unique-constraint-checking). For example, the following sequence of commands used to throw an error but now works:

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR);
INSERT INTO students VALUES (1, 'John Doe');

BEGIN; -- start transaction
DELETE FROM students WHERE id = 1;
INSERT INTO students VALUES (1, 'Jane Doe');
```

### CSV Features

[**Latin-1 and UTF-16 encodings.**](https://github.com/duckdb/duckdb/pull/14560)
Previously, DuckDB's CSV reader was limited to UTF-8 files. It can now read Latin-1 and UTF-16 files. For example:

```sql
FROM read_csv('cities-latin-1.csv', encoding = 'latin-1');
```

[**Multi-byte delimiters.**](https://github.com/duckdb/duckdb/pull/14670)
DuckDB now supports delimiters of up to 4 bytes. This means that you can finally use the [duck emoji](https://emojipedia.org/duck) as a column delimiter. For example:

```text
a🦆b
hello🦆world
```

```plsql
FROM read_csv('example.dsv', sep = '🦆');
```
[**Strict CSV parsing.**](https://github.com/duckdb/duckdb/pull/14464)
[RFC 4180](https://www.ietf.org/rfc/rfc4180.txt) defines requirements for well-formed CSV files, e.g., having a single line delimiter.
DuckDB can parse CSVs in so-called strict mode, just set the `strict_mode` flag to `true`. For example, the following CSV file gets rejected because of mixed newline characters:

```bash
echo "a,b\r\nhello,42\nworld,84" > rfc_4180-defiant.csv
```

```sql
FROM read_csv('rfc_4180-defiant.csv', strict_mode = true);
```

```console
Invalid Input Error:
Error when sniffing file "rfc_4180-defiant.csv".
It was not possible to automatically detect the CSV Parsing dialect/types
```

But it's parsed with the more lenient option, which is also the default:

```sql
FROM read_csv('rfc_4180-defiant.csv');
-- or
FROM read_csv('rfc_4180-defiant.csv', strict_mode = false);
```

```text
┌─────────┬───────┐
│    a    │   b   │
│ varchar │ int64 │
├─────────┼───────┤
│ hello   │    42 │
│ world   │    84 │
└─────────┴───────┘
```

[**Performance improvements.**](https://github.com/duckdb/duckdb/pull/14260)
The CSV parser in the new release uses a new algorithm to find a new line on parallel execution. This leads to speedups of around 15%.

[**Unlimited row length.**](https://github.com/duckdb/duckdb/pull/14512)
Previously, DuckDB was limited to CSV files with rows of up to 8 MB. The new version lifts this restriction, and lines can be of arbitrary length.

### Parquet Features

[**Parquet dictionary and Bloom filter support.**](https://github.com/duckdb/duckdb/pull/14597)
DuckDB now supports writing many more types using dictionary encoding. This should reduce file size in some cases. DuckDB is now also able to read and write Parquet Bloom filters. Bloom filters are small indexing data structures that can be used to exclude row groups if a filter is set. This is particularly useful for often-repeated but unordered data (e.g., categorical values). A separate blog post will follow.

[**Delta binary packed compression for Parquet.**](https://github.com/duckdb/duckdb/pull/14257)
DuckDB now supports the `DELTA_BINARY_PACKED` compression as well as the `DELTA_LENGTH_BYTE_ARRAY` and `BYTE_STREAM_SPLIT` options. A few weeks ago, we elaborated on these in a [blog post]({% post_url 2025-01-22-parquet-encodings %}).

### CLI Improvements

[**Safe mode.**](https://github.com/duckdb/duckdb/pull/14509)
The CLI now supports *safe mode*, which can be activated with the `-safe` flag or the `.safe_mode` [dot command]({% link docs/api/cli/dot_commands.md %). In this mode, the CLI client is prevented from accessing external files other than the database file that it was initially connected to and prevented from interacting with the host file system. For more information, see the [Securing DuckDB page in the Operations Manual]({% link docs/operations_manual/securing_duckdb/overview.md %}.

[**Better autocomplete.**](https://github.com/duckdb/duckdb/pull/15003)
The autocomplete in CLI now uses a [Parsing Expression Grammar (PEG)]({% post_url 2024-11-22-runtime-extensible-parsers %}) for better autocomplete, as well as improved error messages and suggestions.

[**Pretty-printing large numbers.**](https://github.com/duckdb/duckdb/pull/15031)
The CLI provides a summary of the number printed if the client is only rendering only a single row.

```sql
SELECT 100_000_000 AS x, pi() * 1e9 AS y;
```

```text
┌──────────────────┬───────────────────┐
│        x         │         y         │
│      int32       │      double       │
├──────────────────┼───────────────────┤
│    100000000     │ 3141592653.589793 │
│ (100.00 million) │  (3.14 billion)   │
└──────────────────┴───────────────────┘
```

## Friendly SQL

[**Prefix aliases.**](https://github.com/duckdb/duckdb/pull/14436)
SQL Expression and table aliases can now be specified before the thing they are referring to (instead of using the well-known `AS`s syntax. This can improve readability in some cases, for example:

```sql
SELECT 
    e1: some_long_and_winding_expression,
    e2: t2.a_column_name 
FROM
    t1: long_schema.some_long_table_name,
    t2: short_s.tbl;
```

Credit for this idea goes to [Michael Toy](https://www.linkedin.com/in/michael-toy-27b3407/). A separate blog post will follow soon.
[**RENAME clause**.](https://github.com/duckdb/duckdb/pull/14650)
DuckDB now supports the `RENAME` clause in `SELECT`. This allows renaming fields emitted by the [`*` expression]({% link %}):

```sql
CREATE TABLE integers(col1 INT, col2 INT);
INSERT INTO integers VALUES (42, 84);
SELECT * RENAME (col1 AS new_col1) FROM integers;
```

[**STAR LIKE**.](https://github.com/duckdb/duckdb/pull/14662) The `LIKE` and `SIMILAR TO` clauses can now be used on `*` expressions as a short-hand for the `COLUMNS` syntax.

```sql
CREATE TABLE key_val(key VARCHAR, val1 INT, val2 INT);
INSERT INTO key_val VALUES ('v', 42, 84);
SELECT * LIKE 'val%' FROM key_val;
```

```text
┌───────┬───────┐
│ val1  │ val2  │
│ int32 │ int32 │
├───────┼───────┤
│  42   │  84   │
└───────┴───────┘
```

### Optimizations

We have spent
[a](https://github.com/duckdb/duckdb/pull/14864)
[lot](https://github.com/duckdb/duckdb/pull/14313)
[of](https://github.com/duckdb/duckdb/pull/14329)
[time](https://github.com/duckdb/duckdb/pull/14424)
[on](https://github.com/duckdb/duckdb/pull/15020)
[DuckDB's](https://github.com/duckdb/duckdb/pull/15692)
[optimizer](https://github.com/duckdb/duckdb/pull/14750).
It is hard to quantify optimizer improvements, but as a result of these optimizations, DuckDB for example achieves a **13% improvement** on the total runtime of TPC-H SF100 queries when run on a MacBook Pro over the previous release.

### C API for Extensions

Currently, DuckDB extensions use DuckDB’s internal C++ structures. This - along with some fun linking issues - requires a lock-step development of extensions with mainline DuckDB and constant updates. Starting with this release, we expose a new C-style API for extensions in [`duckdb_extension.h`](https://github.com/duckdb/duckdb/blob/v1.2.0/src/include/duckdb_extension.h). This API can be used to create for example scalar, aggregate or table functions in DuckDB. There are two main advantages of using this API: First, many programming languages (e.g. Go, Rust, even Java) have direct bindings to C APIs, making it rather easy to integrate. Secondly, the C Extension API is stable and backwards-compatible, meaning that extensions that target this API will keep working for new DuckDB versions. We will follow up with a new extension template.

### musl Extensions

[**Distributing extensions for musl.**](https://github.com/duckdb/duckdb/pull/15607)
The [`musl` C library](https://musl.libc.org/) is often used in lightweight setups such as Docker setups running Alpine Linux. Starting with this release, we officially support musl and we distribute extensions for the `linux_amd64_musl` platform (but not yet for `linux_arm64_musl`).

## Final Thoughts

These were a few highlights – but there are many more features and improvements in this release.  There have been **over 5 000 commits** by over 70 contributors since we released 1.1.3. The full - very long - release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.2.0).

We would like to thank again our amazing community for using DuckDB, building cool projects on DuckDB and improving DuckDB by providing us feedback. Your contributions truly mean a lot!
