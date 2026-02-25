---
layout: post
title: "Announcing DuckDB 1.3.0"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-3-0.svg"
image: "/images/blog/thumbs/duckdb-release-1-3-0.png"
excerpt: "The DuckDB team is happy to announce that today we're releasing DuckDB version 1.3.0, codenamed “Ossivalis”."
tags: ["release"]
---

> To install the new version, please visit the [installation guide]({% link install/index.html %}). Note that it can take a few hours to days to release some client libraries (e.g., Go, R, Java) and extensions (e.g., the UI) due to the extra changes and review rounds required.

We are proud to release DuckDB 1.3.0. This release of DuckDB is named “Ossivalis” after Bucephala Ossivalis, an ancestor of the [Goldeneye duck](https://en.wikipedia.org/wiki/Common_goldeneye) that lived millions of years ago.

In this blog post, we cover the most important features of the new release. DuckDB is moving rather quickly, and we could cover only a small fraction of the changes in this release. For the complete release notes, see the [release page on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.3.0).

## Breaking Changes and Deprecations

### Old Linux glibc Deprecation

Now that all mainstream Linux distributions use [glibc 2.28](https://lists.gnu.org/archive/html/info-gnu/2018-08/msg00000.html) or newer, DuckDB's official Linux binaries require at least glibc 2.28 or newer. The release is [built using the `manylinux_2_28` image from Python](https://github.com/duckdb/duckdb/pull/16956), which combines an older glibc with a newer compiler. This change also implies that extensions are no longer distributed for the `linux_amd64_gcc4` platform.

We highly value [portability]({% link why_duckdb.md %}#portable), so it is of course still possible to [build DuckDB from source]({% link docs/stable/dev/building/overview.md %}) for older versions of glibc.

### Lambda Function Syntax

Previously, lambda functions in DuckDB could be specified using the single arrow syntax: `x -> x + 1`.
The single arrow operator is also used by the JSON extension to express [JSON extraction]({% link docs/stable/data/json/json_functions.md %}#json-extraction-functions) using the syntax `->'field'`.
The two meanings of the single arrow operator are treated the same by the binder, thus they share the same (low) precedence, necessitating extra parentheses in JSON expression with equality checks:

```sql
SELECT (JSON '{"field": 42}')->'field' = 42;
-- throws a Binder Error:
-- No function matches the given name and argument types 'json_extract(JSON, BOOLEAN)

SELECT ((JSON '{"field": 42}')->'field') = 42;
-- return true
```

This often caused confusion among users, therefore, the new release deprecates the old arrow lambda syntax and replaces it with Python-style lambda syntax:

```sql
SELECT list_transform([1, 2, 3], lambda x: x + 1);
```

To make the transition smoother, the deprecation will happen in several steps over the next year.
First, DuckDB 1.3.0 [introduces a new setting to configure the lambda syntax](https://github.com/duckdb/duckdb/pull/17235):

```sql
SET lambda_syntax = 'DEFAULT';
SET lambda_syntax = 'ENABLE_SINGLE_ARROW';
SET lambda_syntax = 'DISABLE_SINGLE_ARROW';
```

Currently, `DEFAULT` enables both syntax styles, i.e., the old single arrow syntax and the Python-style syntax. DuckDB 1.4.0 will be the last release supporting the single arrow syntax without explicitly enabling it. DuckDB 1.5.0 will disable the single arrow syntax by default. DuckDB 1.6.0 will remove the `lambda_syntax` flag and fully deprecate the single arrow syntax,
so the old behavior will no longer be accessible.

### Serializing Strings in List with Escapes

Starting with the new version, DuckDB escapes characters such as `'` in strings serialized in nested data structures to allow round-tripping between the serialized string and the nested representation.
For example:

```sql
SELECT ['hello ''my'' world'] AS s;
```

DuckDB version 1.2.2 returns `[hello 'my' world]` while DuckDB 1.3.0 returns `['hello \'my\' world']`.

To serialize a list of strings with the old behavior, use the [`array_to_string` function]({% link docs/stable/sql/functions/list.md %}#array_to_string):

```sql
SELECT printf('[%s]', array_to_string(
        ['hello ''my'' world', 'hello ''cruel'' world'], ', '
    )) AS s;
```
```text
┌─────────────────────────────────────────┐
│                    s                    │
│                 varchar                 │
├─────────────────────────────────────────┤
│ [hello 'my' world, hello 'cruel' world] │
└─────────────────────────────────────────┘
```

### Minor SQL Parser Changes

* The term `AT` now needs quotes to be used as an identifier as it is used for [time travel in Iceberg](https://github.com/duckdb/duckdb-iceberg/pull/225).
* `LAMBDA` is now a reserved keyword due to the change in lambda syntax.
* `GRANT` is no longer a reserved keyword.

## New Features

The new DuckDB release again contains a lot of exciting new features:

### External File Cache

DuckDB is used a lot to read from remote files, e.g., Parquet files stored on HTTP servers or blob storage. Previous versions would always fully re-read file data. With this release, we [added a cache for data from external files](https://github.com/duckdb/duckdb/pull/16463). This cache is subject to the overall DuckDB memory limit. If space is available, it will be used to dynamically cache data from external files. This should greatly improve re-running queries on remote data. For example:

```sql
.timer on
.mode trash -- do not show query result
FROM 'https://blobs.duckdb.org/data/shakespeare.parquet';
Run Time (s): real ⟨1.456⟩ user 0.037920 sys 0.028510
FROM 'https://blobs.duckdb.org/data/shakespeare.parquet';
Run Time (s): real ⟨0.360⟩ user 0.029188 sys 0.007620
```

We can see that the query is much faster the second time around due to the cache. In previous versions, the runtime would have been the same.

The cache contents can be queried using the `duckdb_external_file_cache()` table function like so:

```sql
.mode duckbox -- re-enable output
FROM duckdb_external_file_cache();
```

```text
┌───────────────────────────────────────────────────┬──────────┬──────────┬─────────┐
│                        path                       │ nr_bytes │ location │ loaded  │
│                      varchar                      │  int64   │  int64   │ boolean │
├───────────────────────────────────────────────────┼──────────┼──────────┼─────────┤
│ https://blobs.duckdb.org/data/shakespeare.parquet │  1697483 │        4 │ true    │
│ https://blobs.duckdb.org/data/shakespeare.parquet │    16384 │  1681808 │ true    │
└───────────────────────────────────────────────────┴──────────┴──────────┴─────────┘
```

The cache is enabled by default but can be disabled with:

```sql
SET enable_external_file_cache = false;
```

### Directly Query Data Files with the CLI

DuckDB's command line interface (CLI) gained the capability to [directly query Parquet, CSV or JSON files](https://github.com/duckdb/duckdb/pull/17415). This works by just using e.g. a Parquet file instead of the database file. This will expose a view that can be queried. For example, say we have a Parquet file called `region.parquet`, this will work:

```batch
duckdb region.parquet -c 'FROM region;'
```

```text
┌─────────────┐
│   r_name    │
│   varchar   │
├─────────────┤
│ AFRICA      │
│ AMERICA     │
│ ASIA        │
│ EUROPE      │
│ MIDDLE EAST │
└─────────────┘
```

When using the CLI like this, what actually happens is that we launch a temporary in-memory DuckDB database, and create two views over the given file:

* `file` – this view is always named the same, regardless of the name of the file.
* `[base_file_name]` – this view depends on the name of the file, e.g., for `region.parquet` this is `region`.

Both views can be queried and will give the same result.

The main advantage of this feature is usability: we can use the regular shell to navigate to a file, and then use DuckDB to open that file without having to refer to the path of the file at the SQL level.

### `TRY` Expression

DuckDB already supported [`TRY_CAST`]({% link docs/stable/sql/expressions/cast.md %}#TRY_CAST), which was trying to cast a value but did not fail the query if this was not possible. For example:

```sql
SELECT TRY_CAST('asdf' AS INTEGER);
```

returns `NULL`. This release [generalizes this functionality](https://github.com/duckdb/duckdb/pull/15939) beyond casting to arbitrary expressions that can error using `TRY`. For example, the logarithm of 0 [is undefined](https://www.quora.com/What-is-log-0), and `log(0)` will throw an exception and tell you that it “cannot take logarithm of zero”. With the new `TRY`, this will return `NULL` instead, e.g.:

```sql
SELECT TRY(log(0));
```

```text
NULL
```

Again, this will work for arbitrary expressions. We recommend to use `TRY` sparingly however if an error is expected often because there is going to be a performance impact. If any *batch* of rows causes an error, we switch to row-by-row execution of the expression to figure out exactly which row had an error and which did not. This is slower.

### Updatings Structs

Starting with the new release, [it's possible to update the sub-schema of structs using the `ALTER TABLE` clause](https://github.com/duckdb/duckdb/pull/17003). You can add, drop, and rename fields:

```sql
CREATE TABLE test (s STRUCT(i INTEGER, j INTEGER));
INSERT INTO test VALUES (ROW(1, 1)), (ROW(2, 2));
ALTER TABLE test DROP COLUMN s.i;
ALTER TABLE test ADD COLUMN s.k INTEGER;
ALTER TABLE test RENAME COLUMN s.j TO l;
```

```text
┌──────────────────────────────┐
│              s               │
│ struct(l integer, k integer) │
├──────────────────────────────┤
│ {'l': 1, 'k': NULL}          │
│ {'l': 2, 'k': NULL}          │
└──────────────────────────────┘
```

Altering structs is also supported [inside `LIST` and `MAP` columns](https://github.com/duckdb/duckdb/pull/17462).

### Swapping in New Databases

The [`ATTACH OR REPLACE` clause](https://github.com/duckdb/duckdb/pull/15355) allows you to replace a database,
so you can swap a database on the fly.
For example:

```sql
ATTACH 'taxi_v1.duckdb' AS taxi;
USE taxi;
ATTACH OR REPLACE 'taxi_v2.duckdb' AS taxi;
```

This feature was implemented by external contributor [`xevix`](https://github.com/xevix).

### UUID v7 Support

> Warning **Update (2025-05-23).**
> The [UUID v7 implementation in DuckDB v1.3.0 is not consistent with the UUID standard](https://github.com/duckdb/duckdb/issues/17611), causing the timestamp values to be off.
> This means that the timestamps in the generated UUID v7 values will only be correct if they are used exclusively within DuckDB.
> Importing or exporting UUID v7 values from/to systems will yield incorrect timestamps.
> We [patched this bug](https://github.com/duckdb/duckdb/pull/17612) and the fix will soon be available in the preview builds and the [upcoming 1.3.1 patch release]({% link release_calendar.md %}#upcoming-releases).

DuckDB now [supports](https://github.com/duckdb/duckdb/pull/15819) [UUID v7](https://uuid7.com/), which is a newer version of UUIDs. `UUIDv7` combines a Unix timestamp in milliseconds and random bits, offering both uniqueness and sortability. This is useful to e.g. order UUIDs by age or to combine the ubiquitous `ID` and `TIMESTAMP` columns in many tables into a single `UUIDv7` column.

New UUIDs can be created using the `uuidv7()` scalar function. For example:

```sql
SELECT uuidv7();
```

```text
┌──────────────────────────────────────┐
│               uuidv7()               │
│                 uuid                 │
├──────────────────────────────────────┤
│ 8196f1f6-e3cf-7a74-bc0e-c89ac1ea1e19 │
└──────────────────────────────────────┘
```

There are also additional functions to determine the UUID version (`uuid_extract_version()`) and to extract the internal timestamp (`uuid_extract_timestamp()`), for example:

```sql
SELECT uuid_extract_version(uuidv7());
```

```text
┌────────────────────────────────┐
│ uuid_extract_version(uuidv7()) │
│             uint32             │
├────────────────────────────────┤
│               7                │
└────────────────────────────────┘
```

```sql
SELECT uuid_extract_timestamp(uuidv7());
```

```text
┌──────────────────────────────────┐
│ uuid_extract_timestamp(uuidv7()) │
│     timestamp with time zone     │
├──────────────────────────────────┤
│ 2025-05-21 08:32:14.61+00        │
└──────────────────────────────────┘
```

This feature was implemented by external contributor [`dentiny`](https://github.com/dentiny).

### Expression Support in `CREATE SECRET`

DuckDB has an internal “secret” management facility for things like S3 credentials. With this release, it is [possible to use scalar expressions](https://github.com/duckdb/duckdb/pull/15801) in the creation of the secret. This allows for secret contents to not be specified in query text, which makes them easier to keep out of log files, etc. For example:

```sql
SET VARIABLE my_bearer_token = 'hocus pocus this token is bogus';
CREATE SECRET http (
    TYPE http,
    BEARER_TOKEN getvariable('my_bearer_token')
);
```

You can see that the `BEARER_TOKEN` field in the secret is set from the `getvariable` function in `CREATE SECRET`. In the CLI, this is also possible through *environment variables* using `getenv()`. For example, this is now possible:

```batch
MY_SECRET=asdf duckdb -c \
    "CREATE SECRET http (TYPE http, BEARER_TOKEN getenv('MY_SECRET'))"
```

### Unpacking Columns

DuckDB v1.3.0 brings a further boost to the popular [`COLUMNS(*)` expression]({% link docs/stable/sql/expressions/star.md %}#columns-expression).
Previously, _unpacking_ the entities into a list was possible by adding a leading `*` character:

```sql
CREATE TABLE tbl AS SELECT 21 AS a, 1.234 AS b;
SELECT [*COLUMNS(*)] AS col_exp FROM tbl;
```

```text
┌─────────────────┐
│     col_exp     │
│ decimal(13,3)[] │
├─────────────────┤
│ [21.000, 1.234] │
└─────────────────┘
```

However, this syntax could not be used in tandem with other expressions such as casting:

```sql
SELECT [*COLUMNS(*)::VARCHAR] AS col_exp FROM tbl;
```

```console
Binder Error:
*COLUMNS() can not be used in this place
```

The new `UNPACK` keyword removes this limitation. The following expression

```sql
SELECT [UNPACK(COLUMNS(*)::VARCHAR)] AS col_exp FROM tbl;
```

is equivalent to:

```sql
SELECT [a::VARCHAR, b::VARCHAR] AS col_exp FROM tbl;
```

```text
┌─────────────┐
│   col_exp   │
│  varchar[]  │
├─────────────┤
│ [21, 1.234] │
└─────────────┘
```

### Spatial `JOIN` Operator

We added a new specialized join operator as part of the [`spatial` extension]({% link docs/stable/core_extensions/spatial/overview.md %}), which greatly improves the efficiency of _spatial joins_, that is, queries that `JOIN` two geometry columns using specific spatial predicate functions, such as `ST_Intersects` and `ST_Contains`.

Similarly to a `HASH_JOIN`, the `SPATIAL_JOIN` builds a temporary lookup data-structure for the smaller side of the join, except it's an R-Tree, instead of a hash table. What this means for you is that you don't need to create an index first, or do any other pre-processing to optimize your spatial joins. It's all handled by the join operator internally.

While the query optimizer will try to instantiate this new operator for `LEFT`, `OUTER`, `INNER` and `RIGHT` spatial joins, one limitation currently is that the join can only contain a single join condition, or the optimizer will fall back to use a less efficient join strategy.

The following example illustrates how the `SPATIAL_JOIN` operator becomes part of the query plan. It's a relatively small query, but on my machine it executes almost 100× faster than it used to do in DuckDB v1.2.2!

```sql
LOAD spatial;

-- generate random points
CREATE TABLE points AS
  SELECT
      ST_Point(x, y) AS geom,
      (y * 50) + x // 10 AS id
  FROM
      generate_series(0, 1000, 5) r1(x),
      generate_series(0, 1000, 5) r2(y);

-- generate random polygons
CREATE TABLE polygons AS
  SELECT
      ST_Buffer(ST_Point(x, y), 5) AS geom,
      (y * 50) + x // 10 AS id
  FROM
      generate_series(0, 500, 10) r1(x),
      generate_series(0, 500, 10) r2(y);

-- inspect the join plan
EXPLAIN
    SELECT *
    FROM polygons
    JOIN points ON ST_Intersects(points.geom, polygons.geom);
```

```text
             ...
┌─────────────┴─────────────┐
│        SPATIAL_JOIN       │
│    ────────────────────   │
│      Join Type: INNER     │
│        Conditions:        ├──────────────┐
│ ST_Intersects(geom, geom) │              │
│        ~40401 Rows        │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         SEQ_SCAN          │
│    ────────────────────   ││    ────────────────────   │
│       Table: points       ││      Table: polygons      │
│   Type: Sequential Scan   ││   Type: Sequential Scan   │
│        ~40401 Rows        ││         ~2601 Rows        │
└───────────────────────────┘└───────────────────────────┘
```

For the curious, there are more details [in the PR](https://github.com/duckdb/duckdb-spatial/pull/545).

## Internal Changes

For this release there have also been a large number of internal changes.

We have completed an [almost complete re-implementation](https://github.com/duckdb/duckdb/pulls?q=is%3Apr+is%3Aclosed+closed%3A%3E2025-02-05+parquet) of DuckDB's *Parquet reader and writer*. This should greatly improve Parquet performance and reliability, and also expanded [Parquet feature support](https://parquet.apache.org/docs/file-format/implementationstatus/) for obscure logical types like `UNKNOWN` and `FLOAT16`.

We have also done a large amount of internal changes around the [reading of multiple files](https://github.com/duckdb/duckdb/pulls?q=is%3Apr+is%3Aclosed+closed%3A%3E2025-02-05+multifilereader+) (e.g., a folder of Parquet files) in an API called the `MultiFileReader`. We have unified the handling of multiple files across many of our file readers, e.g., Parquet, CSV, JSON, Avro, etc. This allows DuckDB to handle e.g. schema differences between multiple files in a unified way.

We have also added a new string compression method, `DICT_FSST`. Before, DuckDB supported *either* [dictionary encoding](https://en.wikipedia.org/wiki/Dictionary_coder) *or* [FSST compression](https://github.com/cwida/fsst) (“Fast Static Symbol Table”) for strings. Those compression methods could not be mixed within a storage block (265 kB by default). However, we observed a lot of real-world data where part of the block would benefit from dictionary encoding, and another part would benefit from FSST. FSST does not by default duplicate-eliminate strings. This release [combines both methods](https://github.com/duckdb/duckdb/pull/15637) into a new compression method, `DICT_FFST`. This *first* runs dictionary encoding and *then* compresses the dictionary using FSST. Dictionary encoding and FSST-only encoding are also still available. We have also [optimized storing validity masks](https://github.com/duckdb/duckdb/pull/15591) (“which rows are NULL?”) in this release, some compression methods (like the new `DICT_FSST`) can handle NULLs internally and this obviates the need for a separate validity mask. Combined, those new features should greatly reduce the storage space required especially for strings. Note that the compression method is automatically picked by DuckDB based on actually observed compression ratios so users will not have to explicitly set this.

## Final Thoughts

These were a few highlights – but there are many more features and improvements in this release. There have been over 3,000 commits by over 75 contributors since we released v1.2.2. The full release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.3.0). We would like to thank our community for providing detailed issue reports and feedback. And our special thanks goes to external contributors, who directly landed features in this release!
