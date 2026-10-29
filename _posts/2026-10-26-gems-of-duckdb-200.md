---
layout: post
title: "Gems of DuckDB 2.0.0"
authors:
  - Gábor Szárnyas
  - Geertjan Wielenga
thumb: "/images/blog/thumbs/gems-of-duckdb-2-0-0.svg"
image: "/images/blog/thumbs/gems-of-duckdb-2-0-0.png"
excerpt: "We released DuckDB 2.0.0 last week with an improved Quack protocol and `VARIANT` support, asynchronous I/O, and many other features. In this blog post, we highlight a few smaller features and improvements that did not make it into the release announcement."
tag: release
---

Last week we released [DuckDB 2.0.0 LTS]({% post_url 2026-10-21-announcing-duckdb-200 %}), our biggest feature release so far.
The announcement covered the headline items: the Quack protocol, asynchronous I/O, the first-class `VARIANT` type, agent mode, the PEG parser, and triggers.
DuckDB 2.0.0 is now available in [all primary clients]({% link docs/2.0/clients/overview.md %}) – check the [installation page]({% link install/index.html %}) for instructions on installing or upgrading.

A release of this size ships many smaller improvements that never make it into the original announcement.
In this post, we highlight a few of these gems.
To find the documentation for everything that is new in 2.0, see the [“What's New in the Docs for 2.0”]({% link docs/2.0/whats_new_in_the_docs.md %}) page.

## Python Appender

Inserting rows one at a time is inefficient, and building up a giant `INSERT` statement is awkward.
Therefore, the preferred solution for inserting large amounts of data has been the [appender]({% link docs/2.0/data/appender.md %}). However, it was only available in some clients (C/C++, Go, Java, etc.) and notably absent from the Python client.
DuckDB 2.0.0's Python client ships an [appender]({% link docs/2.0/clients/python/appender.md %}) that collects rows and writes them together in a single operation:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE duckdb_releases (version VARCHAR, codename VARCHAR);")

with con.appender("duckdb_releases") as appender:
    appender.append_row("1.4", "Andium")
    appender.append_rows([("1.5", "Variegata"), ("2.0", "Cyanoptera")])

print(con.execute("FROM duckdb_releases").fetchall())
```

```text
[('1.4', 'Andium'), ('1.5', 'Variegata'), ('2.0', 'Cyanoptera')]
```

The `with` block flushes the buffered rows when it exits.
For data that already lives in a DataFrame or Arrow table, `INSERT INTO ... SELECT` is still faster, but the appender is ideal for rows that your Python code produces on the fly.

## Usability Improvements in the CLI

### Pretty-Printed `.schema`

As of DuckDB 2.0, the [`.schema` dot command]({% link docs/2.0/clients/cli/dot_commands.md %}#querying-the-database-schema) pretty-prints and highlights its output by default, which makes reading the schema of a database much easier. If you prefer the earlier single-line form, for example, to copy a statement verbatim, use `--no-indent` (or its alias `--no-format`):

```batch
duckdb mydata.duckdb ".schema --no-indent"
```

### `.manual` Dot Command

DuckDB 2.0 introduces the [`.manual` dot command]({% link docs/2.0/clients/cli/dot_commands.md %}#displaying-function-documentation), which shows the signatures, description, and examples of a SQL function.
For example, to get the details of the `bar` function, run:

```sql
.manual bar
```

```text
  ────────────────────────────────────────────────────────────────────────────────────────────────
  system.main                                   bar                                scalar function

  SIGNATURE

        bar(x DOUBLE, min DOUBLE, max DOUBLE) -> VARCHAR

        bar(x DOUBLE, min DOUBLE, max DOUBLE, width DOUBLE) -> VARCHAR

  DESCRIPTION

        Draws a band whose width is proportional to (`x - min`) and equal to `width` characters
        when `x` = `max`. `width` defaults to 80.

  EXAMPLES

        bar(5, 0, 20, 10)
```

The same page is available from the command line via `duckdb -manual bar`, and the name may contain `LIKE` wildcards, e.g., `.manual list_%`.
In the coming releases, we will extend the manuals to cover more features such as SQL statements and clauses.

### Calculator

You can use the CLI as a calculator. Simply type the expression followed by a semicolon – no more typing into your browser's address bar!

```sql
6*7;
```

```text
┌─────────┐
│ (6 * 7) │
│  int32  │
├─────────┤
│      42 │
└─────────┘
```

### Command History

The CLI now exposes its command history in two ways. The [`.history` dot command]({% link docs/2.0/clients/cli/dot_commands.md %}#command-history) shows previously executed statements with syntax highlighting, optionally limited to the last `N` entries:

```sql
.history 10
```

The same information is available as a table through the `shell_history()` table function, so you can query your own history with SQL:

```sql
SELECT sql
FROM shell_history()
WHERE sql ILIKE '%copy%';
```

## Offline Documentation

As a reminder, both the DuckDB documentation and the DuckDB blog are available [for offline browsing]({% link docs/2.0/guides/offline-copy.md %}):

* [Documentation as a Markdown file](https://blobs.duckdb.org/docs/duckdb-docs.md) (approx. 5 MB)
* [Documentation as a PDF file](https://blobs.duckdb.org/docs/duckdb-docs.pdf) (approx. 10 MB)
* [Blog as a Markdown file](https://blobs.duckdb.org/docs/duckdb-blog.md) (approx. 3 MB)
* [Blog as a PDF file](https://blobs.duckdb.org/docs/duckdb-blog.pdf) (approx. 35 MB)

You can download them to your e-reader (we are not affiliated with any particular brand!) or read them on your laptop on the go.
You can also use them to supply context to LLMs and coding agents.
At approximately 5 MB, the documentation exceeds the context window of most LLMs, so instead of ingesting it in full, point them to specific sections or let them find the parts they need.

## Unsung SQL Features

### `SHOW` for Configuration Settings

The [`SHOW` statement]({% link docs/2.0/sql/statements/show.md %}#show-statement) can now print a [configuration setting]({% link docs/2.0/configuration/overview.md %}) by name, PostgreSQL-style, when the name does not refer to a table:

```sql
SET threads = 42;
SHOW threads;
```

| threads |
|---------|
| 42      |

This is much more succinct than the previous formulation that used the [`current_setting` function]({% link docs/2.0/sql/functions/utility.md %}#current_settingsetting_name) (e.g., `SELECT current_setting('threads') AS threads;`).

When a table and a setting share a name, DuckDB prioritizes the table by default. You can control this with the `show_behavior` setting, which takes `'auto'` (the default), `'table'`, or `'setting'`.

> Deprecated Using `SHOW` to describe a table, view, or query (e.g., `SHOW my_table`) is deprecated as of DuckDB 2.0 and prints a warning. Use [`DESCRIBE`]({% link docs/2.0/sql/statements/describe.md %}) instead.

### `CREATE SECURE VIEW` Statement

Regular views can leak information about their underlying tables through statistics and query plans, for example via the `stats()` function. The new [`SECURE VIEW`]({% link docs/2.0/sql/statements/create_view.md %}#examples) does not:

```sql
CREATE SECURE VIEW users AS
    SELECT username
    FROM all_users
    WHERE access_level = 'standard';
```

On a secure view, `stats()` returns only uninformative statistics and `EXPLAIN ANALYZE` shows a single `Secure View` node instead of the view's query plan, so neither can be used to reconstruct the rows that the view filters out.

### Options in `regexp_extract`

The [`regexp_extract` function]({% link docs/2.0/sql/functions/regular_expressions.md %}#using-regexp_extract) gained an overload that takes regular expression options as the third argument, with no capture group required. For example, you can now match case-insensitively in a single call:

```sql
SELECT regexp_extract('ABC', 'abc', 'i'); -- ABC
```

### Setting a Sequence Value

[Sequences]({% link docs/2.0/sql/statements/create_sequence.md %}) gained a PostgreSQL-style [`setval` function]({% link docs/2.0/sql/statements/create_sequence.md %}#setting-the-sequence-value) to reset a sequence to a given value, which is useful after a bulk load:

```sql
CREATE SEQUENCE serial START 1;
SELECT setval('serial', 42);
SELECT nextval('serial');
```

| nextval |
|--------:|
| 43      |

The next value after `setval` is `value + increment` by default. Pass `false` as the optional third argument (`is_called`) to make the next `nextval` return `value` itself.

### Session Variables as Default Parameter Values

[Prepared statements]({% link docs/2.0/sql/query_syntax/prepared_statements.md %}#session-variables-as-default-values) can now fall back to a [session variable]({% link docs/2.0/sql/statements/set_variable.md %}) of the same name when a named parameter is not supplied at execution time:

```sql
SET VARIABLE multiplier = 10;
SET VARIABLE x = 42;
PREPARE compute AS SELECT $multiplier * $x AS result;
EXECUTE compute;
```

| result |
|-------:|
| 420    |

An explicit argument always takes precedence over the variable, and because the fallback is resolved at execution time, changing a variable and re-executing the statement picks up the new value.

### Custom Partition Paths

When writing [partitioned data]({% link docs/2.0/data/partitioning/partitioned_writes.md %}), the `PARTITION_BY` clause writes each partition to a `col=value` subdirectory following the Hive convention. The new [`PARTITION_PATH` option]({% link docs/2.0/data/partitioning/partitioned_writes.md %}#custom-partition-paths) gives you full control over the subdirectory that each partition is written to, using an expression over the partitioning columns.
Let's suppose you have a table named `orders` that stores customer orders.

<details markdown='1'>
<summary markdown='span'>
Click here to see the code to create the `orders` table.
</summary>
```sql
CREATE TABLE orders AS
FROM (VALUES
    (1, 2018, 3, 120.00),
    (2, 2018, 11, 75.50),
    (3, 2019, 6, NULL),
    (4, 2019, 6, 310.25),
    (5, 2020, 9, 18.75),
    (6, 2021, 2, 42.00),
    (7, 2021, 2, 99.90),
    (8, 2023, 12, 260.00)
) t(order_id, year, month, amount);
```
</details>

Let's partition this table based on year:

```sql
COPY orders TO 'orders'
    (FORMAT parquet,
     PARTITION_BY (year),
     PARTITION_PATH CASE
         WHEN year < 2020 THEN 'archive/' || year
         ELSE 'recent/' || year
     END);
```

This will result in the following directory structure:

```batch
tree orders
```
```text
orders
├── archive
│   ├── 2018
│   │   └── data_0.parquet
│   └── 2019
│       └── data_0.parquet
└── recent
    ├── 2020
    │   └── data_0.parquet
    ├── 2021
    │   └── data_0.parquet
    └── 2023
        └── data_0.parquet
```

The expression is evaluated once per partition, and its result must be a relative path that does not contain `..` segments. Each partition must map to a distinct path. A companion [`ORDER_BY` copy option]({% link docs/2.0/data/partitioning/partitioned_writes.md %}#sorting-rows-within-partitions) sorts the rows before they are written. When combined with `PARTITION_BY`, the rows are sorted within each partition:

```sql
COPY orders TO 'orders_sorted'
    (FORMAT parquet,
     PARTITION_BY (year, month),
     ORDER_BY (amount DESC NULLS LAST));
```

### Writing GeoJSON

DuckDB can now write [GeoJSON]({% link docs/2.0/data/json/writing_json.md %}#geojson) directly with `COPY ... (FORMAT GEOJSON)`, which produces a `FeatureCollection`, or `FORMAT GEOJSONL` for newline-delimited features:

```sql
COPY (SELECT 'POINT(0 1)'::GEOMETRY AS geom, 10 AS my_field)
    TO 'test.json' (FORMAT GEOJSON);
```

The optional `ID_COLUMN` and `GEOMETRY_COLUMN` options pick which columns become the feature `id` and geometry. Reading GeoJSON is covered on the [Loading JSON]({% link docs/2.0/data/json/loading_json.md %}#geojson) page.

## Extensions

### Compatibility Matrix for Community Extensions

In the days following the release, once our CI pipelines got some breathing room, we built and deployed the [community extensions]({% link community_extensions/index.md %}) for DuckDB 2.0.0.

Not every extension is available for every DuckDB version and platform, so each extension's page now includes a compatibility matrix that shows which DuckDB version and platform combinations the extension was deployed for, covering recent DuckDB releases. For example, see the [compatibility matrix of the DuckPGQ extension]({% link community_extensions/extensions/duckpgq.md %}#compatibility-matrix):

<div class="extension_compatibility_table"></div>

| Platform | 1.4.4 | 1.4.5 | 1.5.5 | 1.5.6 | 2.0.0 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Linux AMD64 | ✅ | ❌ | ❌ | ✅ | ✅ |
| Linux ARM64 | ✅ | ❌ | ❌ | ✅ | ✅ |
| macOS AMD64 | ✅ | ❌ | ❌ | ✅ | ✅ |
| macOS ARM64 | ✅ | ❌ | ❌ | ✅ | ✅ |
| Windows AMD64 | ✅ | ❌ | ❌ | ✅ | ✅ |
| Windows ARM64 | ❌ | ❌ | ❌ | ❌ | ❌ |
| WebAssembly | ✅ | ❌ | ❌ | ✅ | ✅ |

### Window Function Extensions

Every aggregate function can be used as a window function, but not every windowed operation is an aggregate. In DuckDB 2.0, window functions became catalog entries, so [extensions can now define their own window functions]({% link docs/2.0/extensions/window_function_extensions.md %}) using the same C++ API as the built-in ones.

An extension derives from the `WindowFunction` class, registers it with the `ExtensionLoader`, and implements a blocking interface, which builds its data structures and evaluates the function in parallel. Optionally, it can also implement a streaming interface for windows without `PARTITION BY` and `ORDER BY` clauses. As a side effect, window functions are now listed in `duckdb_functions()` and can be looked up with the `.manual` dot command.

For more details, see [Richard Wesley's slides on window extensions](https://blobs.duckdb.org/events/duckdb-boston/meetup/richard-wesley-windowing.pdf) (presented in September at our [Boston meetup]({% link _events/2026-09-03-duckdb-boston-meetup.md %})).

## Summary and Looking Ahead

In this blog post, we listed a few of the smaller features in DuckDB 2.0.0. For everything else, see the [announcement blog post]({% post_url 2026-10-21-announcing-duckdb-200 %}) and the [release notes](https://github.com/duckdb/duckdb/releases/tag/v2.0.0). There are even more things in the release as part our [core extensions]({% link docs/2.0/core_extensions/overview.md %}) – we'll release more posts on these in the coming weeks.

The ecosystem around DuckDB keeps growing: many projects are built both with DuckDB and within it. The community-driven [`awesome-duckdb` repository](https://github.com/davidgasquez/awesome-duckdb), maintained by [David Gasquez](https://github.com/davidgasquez), collects extensions, integrations, and articles in one place and is a great starting point for exploring what people are building.

We are also in the process of updating our [roadmap]({% link roadmap.md %}) with upcoming features. We already picked the codename for DuckDB 2.1, coming in 2027: we will name it after [Barrow's goldeneye](https://en.wikipedia.org/wiki/Barrow%27s_goldeneye) _(Bucephala islandica),_ so:

```python
with con.appender("duckdb_releases") as appender:
    appender.append_row("2.1", "Islandica")
```

As always, we are grateful to the contributors who made this release possible.
Thank you!
