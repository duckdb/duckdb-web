---
layout: post
title: "DuckDB Tricks"
author: "Gabor Szarnyas"
#thumb: "/images/blog/thumbs/design-patterns.svg"
excerpt: "We use a simple example data set to present a few tricks that are useful when using DuckDB for data science."
---

In this blog post, we present five simple DuckDB operations that are particularly useful for interactive data analysis.
The operations are summarized in the following table:

| Operation | Snippet |
|---|---|
| [Pretty-printing floats](#pretty-printing-floating-point-numbers) | `SELECT (10/9)::DECIMAL(15, 2);` |
| [Copying the schema](#copying-the-schema-of-a-table) | `CREATE TABLE tbl AS FROM example LIMIT 0;` |
| [Shuffling data](#shuffling-data) | `FROM example ORDER BY hash(rowid + 42);` |
| [Specifying types when reading CSVs](#specifying-types-in-the-csv-loader) | `FROM read_csv('example.csv', types = {'x': 'DECIMAL(15, 2)'});` |
| [Updating CSV files in-place](#updating-csv-files-in-place) | `COPY (SELECT s FROM 'example.csv') TO 'example.csv';` |

## Creating an example data set

We start by creating a data set that we'll use in the rest of the blog post. To this end, we define a table, populate it with some data and export it to a CSV.

```sql
CREATE TABLE example (s STRING, x DOUBLE);
INSERT INTO example VALUES ('foo', 10/9), ('bar', 50/7), ('qux', 9/4);
COPY example TO 'example.csv';
```

Wait a bit, that’s way too verbose! DuckDB’s syntax has [several “friendly SQL” shorthands]({% link docs/sql/dialect/friendly_sql.md %}), including the [`FROM`-first syntax]({% link docs/sql/query_syntax/from.md %}#from-first-syntax), which makes the `SELECT` clause optional.
Combining a few shorthands allow us to compress the data creation script to about ~60% of its original size. The new formulation omits the schema definition and creates the CSV with a single command:

```sql
COPY (FROM VALUES ('foo', 10/9), ('bar', 50/7), ('qux', 9/4) t(s, x))
TO 'example.csv';
```

Regardless of which syntax we choose, the resulting CSV file looks like this:

```csv
s,x
foo,1.1111111111111112
bar,7.142857142857143
qux,2.25
```

Let’s continue with the code snippets and their explanations.

## Pretty-printing floating-point numbers

When printing a floating-point number to the output, the fractional parts can be difficult to read and compare. For example:

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

By casting the result to a `DECIMAL` with a fixed number of digits after the decimal point, we can pretty-print the results quickly:

```sql
SELECT x::DECIMAL(15, 2) AS x
FROM 'example.csv';
```

```text
┌───────────────┐
│       x       │
│ decimal(15,2) │
├───────────────┤
│          1.11 │
│          7.14 │
│          2.25 │
└───────────────┘
```

A typical alternative solution is to use the [`printf`]({% link docs/sql/functions/char.md %}#printf-syntax) or [`format`]({% link docs/sql/functions/char.md %}#fmt-syntax) functions, e.g.:

```sql
SELECT printf('%.2f', x)
FROM 'example.csv';
```

However, this has more complicated syntax and returns string values, which make subsequent operations (e.g. sorting) more difficult.
Therefore, unless keeping the precision is a concern, casting to `DECIMAL` values is the preferred solution for most use cases.

## Copying the schema of a table

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

Alternatively, in the CLI client, we can run the `.schema` [dot command]({% link docs/api/cli/dot_commands.md %}):

```plsql
.schema
```

This will return the schema of the table.

```sql
CREATE TABLE example(s VARCHAR, x DOUBLE);
```

After editing the table’s name (e.g., `example` to `tbl`), this query can be used to create a new table with the same schema.

## Shuffling data

Sometimes, we need to introduce some entropy into the ordering of the data by shuffling it.
To shuffle _non-deterministically_, we can simply sort on a random value provided the [`random` function]({% link docs/sql/functions/numeric.md %}#random):

```sql
FROM 'example.csv' ORDER BY random();
```

Shuffling _deterministically_ is a bit more tricky. To achieve this, we can order on a hash function (e.g., [`hash`]({% link docs/sql/functions/utility.md %}#hashvalue)), which takes the [`rowid` pseudocolumn]({% link docs/sql/statements/select.md %}#row-ids) as its input. Note that this column is only available in physical tables, so we first have to load the CSV in a table, then perform the shuffle operation as follows:

```sql
CREATE OR REPLACE TABLE example AS FROM 'example.csv';
SELECT * FROM example ORDER BY hash(rowid + 42);
```

The result of this shuffle operation is deterministic. If you run the script repeatedly, it will always return the following table:

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

Note that the `+ 42` is only necessary to nudge the first row from its position – as `hash(0)` returns the smallest possible value, `0`, it would leave the first row in its place.

## Specifying types in the CSV loader

DuckDB’s CSV loader auto-detects types from a [short list]({% link docs/data/csv/auto_detection.md %}#type-detection) (`BOOLEAN`, `BIGINT`, `DOUBLE`, `TIME`, `DATE`, `TIMESTAMP`, `VARCHAR`).
In some cases, it’s desirable to override the detected type of a given column with a different type.
For example, we may want to treat column `x` as a `DECIMAL` value from the get-go.
We can do this on a per-column basis with the `types` argument of the `read_csv` function:

```sql
CREATE OR REPLACE TABLE example AS
    FROM read_csv('example.csv', types = {'x': 'DECIMAL(15, 2)'});
```

Then, we can simply query the table to see the result:

```sql
FROM example;
```

```text
┌─────────┬───────────────┐
│    s    │       x       │
│ varchar │ decimal(15,2) │
├─────────┼───────────────┤
│ foo     │          1.11 │
│ bar     │          7.14 │
│ qux     │          2.25 │
└─────────┴───────────────┘
```

## Updating CSV files in-place

In DuckDB, it is possible to read, process and write CSV files in-place. To project the column `s`, we can simply run:

```sql
COPY (SELECT s FROM 'example.csv') TO 'example.csv';
```

The resulting `example.csv` file contains the following:

```csv
s
foo
bar
qux
```

Note that this trick is not possible in Unix shells without a workaround. One might be tempted to run the following command to project the first column of the `example.csv` file:

```bash
cut -d, -f1 example.csv > example.csv
```

However, due to the intricacies of Unix pipelines, executing this command leaves us with an empty `example.csv` file. The solution in the shell is to use different file names, then perform a rename operation:

```bash
cut -d, -f1 example.csv > tmp.csv && mv tmp.csv example.csv
```

## Closing thoughts

That’s it for today. If you tried out the examples in your shell, there is a good chance the content of your `example.csv` file is changed or completely destroyed.
In the spirit of the [Choose Your Own Adventure](https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure) books, you may go back to the [data generation step](#creating-an-example-data-set) and continue your experiments.
Happy hacking!
