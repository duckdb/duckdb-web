---
layout: post
title: "DuckDB Tricks – Part 1"
author: "Gabor Szarnyas"
thumb: "/images/blog/thumbs/duckdb-tricks.svg"
image: "/images/blog/thumbs/duckdb-tricks.png"
excerpt: "We use a simple example data set to present a few tricks that are useful when using DuckDB."
tags: ["using DuckDB"]
---

In this blog post, we present five simple DuckDB operations that we found particularly useful for interactive use cases.
The operations are summarized in the following table:

| Operation | Snippet |
|---|---|
| [Pretty-printing floats](#pretty-printing-floating-point-numbers) | `SELECT (10 / 9)::DECIMAL(15, 3);` |
| [Copying the schema](#copying-the-schema-of-a-table) | `CREATE TABLE tbl AS FROM example LIMIT 0;` |
| [Shuffling data](#shuffling-data) | `FROM example ORDER BY hash(rowid + 42);` |
| [Specifying types when reading CSVs](#specifying-types-in-the-csv-loader) | `FROM read_csv('example.csv', types = {'x': 'DECIMAL(15, 3)'});` |
| [Updating CSV files in-place](#updating-csv-files-in-place) | `COPY (SELECT s FROM 'example.csv') TO 'example.csv';` |

## Creating the Example Data Set

We start by creating a data set that we'll use in the rest of the blog post. To this end, we define a table, populate it with some data and export it to a CSV file.

```sql
CREATE TABLE example (s STRING, x DOUBLE);
INSERT INTO example VALUES ('foo', 10/9), ('bar', 50/7), ('qux', 9/4);
COPY example TO 'example.csv';
```

Wait a bit, that’s way too verbose! DuckDB’s syntax has several SQL shorthands including the [“friendly SQL” clauses]({% link docs/sql/dialect/friendly_sql.md %}).
Here, we combine the [`VALUES` clause]({% link docs/sql/query_syntax/values.md %}) with the [`FROM`-first syntax]({% link docs/sql/query_syntax/from.md %}#from-first-syntax), which makes the `SELECT` clause optional.
With these, we can compress the data creation script to ~60% of its original size.
The new formulation omits the schema definition and creates the CSV with a single command:

```sql
COPY (FROM VALUES ('foo', 10/9), ('bar', 50/7), ('qux', 9/4) t(s, x))
TO 'example.csv';
```

Regardless of which script we run, the resulting CSV file will look like this:

```csv
s,x
foo,1.1111111111111112
bar,7.142857142857143
qux,2.25
```

Let’s continue with the code snippets and their explanations.

## Pretty-Printing Floating-Point Numbers

When printing a floating-point number to the output, the fractional parts can be difficult to read and compare. For example, the following query returns three numbers between 1 and 8 but their printed widths are very different due to their fractional parts.

```sql
SELECT x
FROM 'example.csv';
```

```text
┌────────────────────┐
│         x          │
│       double       │
├────────────────────┤
│ 1.1111111111111112 │
│  7.142857142857143 │
│               2.25 │
└────────────────────┘
```

By casting a column to a `DECIMAL` with a fixed number of digits after the decimal point, we can pretty-print it as follows:

```sql
SELECT x::DECIMAL(15, 3) AS x
FROM 'example.csv';
```

```text
┌───────────────┐
│       x       │
│ decimal(15,3) │
├───────────────┤
│         1.111 │
│         7.143 │
│         2.250 │
└───────────────┘
```

A typical alternative solution is to use the [`printf`]({% link docs/sql/functions/char.md %}#printf-syntax) or [`format`]({% link docs/sql/functions/char.md %}#fmt-syntax) functions, e.g.:

```sql
SELECT printf('%.3f', x)
FROM 'example.csv';
```

However, these approaches require us to specify a formatting string that's easy to forget.
What's worse, the statement above returns string values, which makes subsequent operations (e.g., sorting) more difficult.
Therefore, unless keeping the full precision of the floating-point numbers is a concern, casting to `DECIMAL` values should be the preferred solution for most use cases.

## Copying the Schema of a Table

To copy the schema from a table without copying its data, we can use `LIMIT 0`.

```sql
CREATE TABLE example AS
    FROM 'example.csv';
CREATE TABLE tbl AS
    FROM example
    LIMIT 0;
```

This will result in an empty table with the same schema as the source table:

```sql
DESCRIBE tbl;
```

```text
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ s           │ VARCHAR     │ YES     │         │         │         │
│ x           │ DOUBLE      │ YES     │         │         │         │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
```

Alternatively, in the CLI client, we can run the `.schema` [dot command]({% link docs/clients/cli/dot_commands.md %}):

```plsql
.schema
```

This will return the schema of the table.

```sql
CREATE TABLE example (s VARCHAR, x DOUBLE);
```

After editing the table’s name (e.g., `example` to `tbl`), this query can be used to create a new table with the same schema.

## Shuffling Data

Sometimes, we need to introduce some entropy into the ordering of the data by shuffling it.
To shuffle _non-deterministically_, we can simply sort on a random value provided the [`random()` function]({% link docs/sql/functions/numeric.md %}#random):

```sql
FROM 'example.csv' ORDER BY random();
```

Shuffling _deterministically_ is a bit more tricky. To achieve this, we can order on the [hash]({% link docs/sql/functions/utility.md %}#hashvalue), of the [`rowid` pseudocolumn]({% link docs/sql/statements/select.md %}#row-ids). Note that this column is only available in physical tables, so we first have to load the CSV in a table, then perform the shuffle operation as follows:

```sql
CREATE OR REPLACE TABLE example AS FROM 'example.csv';
FROM example ORDER BY hash(rowid + 42);
```

The result of this shuffle operation is deterministic – if we run the script repeatedly, it will always return the following table:

```text
┌─────────┬────────────────────┐
│    s    │         x          │
│ varchar │       double       │
├─────────┼────────────────────┤
│ bar     │  7.142857142857143 │
│ qux     │               2.25 │
│ foo     │ 1.1111111111111112 │
└─────────┴────────────────────┘
```

Note that the `+ 42` is only necessary to nudge the first row from its position – as `hash(0)` returns `0`, the smallest possible value, using it for ordering leaves the first row in its place.

## Specifying Types in the CSV Loader

DuckDB’s CSV loader auto-detects types from a [short list]({% link docs/data/csv/auto_detection.md %}#type-detection) of `BOOLEAN`, `BIGINT`, `DOUBLE`, `TIME`, `DATE`, `TIMESTAMP` and `VARCHAR`.
In some cases, it’s desirable to override the detected type of a given column with a type outside of this list.
For example, we may want to treat column `x` as a `DECIMAL` value from the get-go.
We can do this on a per-column basis with the `types` argument of the `read_csv` function:

```sql
CREATE OR REPLACE TABLE example AS
    FROM read_csv('example.csv', types = {'x': 'DECIMAL(15, 3)'});
```

Then, we can simply query the table to see the result:

```sql
FROM example;
```

```text
┌─────────┬───────────────┐
│    s    │       x       │
│ varchar │ decimal(15,3) │
├─────────┼───────────────┤
│ foo     │         1.111 │
│ bar     │         7.143 │
│ qux     │         2.250 │
└─────────┴───────────────┘
```

## Updating CSV Files In-Place

In DuckDB, it is possible to read, process and write CSV files in-place. For example, to project the column `s` into the same file, we can simply run:

```sql
COPY (SELECT s FROM 'example.csv') TO 'example.csv';
```

The resulting `example.csv` file will have the following content:

```csv
s
foo
bar
qux
```

Note that this trick is not possible in Unix shells without a workaround.
One might be tempted to run the following command on the `example.csv` file and expect the same result:

```bash
cut -d, -f1 example.csv > example.csv
```

However, due to the intricacies of Unix pipelines, executing this command leaves us with an empty `example.csv` file.
The solution is to use different file names, then perform a rename operation:

```bash
cut -d, -f1 example.csv > tmp.csv && mv tmp.csv example.csv
```

## Closing Thoughts

That’s it for today. The tricks shown in this post are available on [duckdbsnippets.com](https://duckdbsnippets.com/page/1/most-recent). If you have a trick that would like to share, please submit it there, or send it to us via social media or [Discord](https://discord.duckdb.org/). Happy hacking!
