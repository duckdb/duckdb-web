---
layout: docu
title: Loading Duckbox Tables
---

> The scripts provided in this page work on Linux, macOS, and WSL.

By default, the DuckDB [CLI client]({% link docs/clients/cli/overview.md %}) renders query results in the [duckbox format]({% link docs/clients/cli/output_formats.md %}),
which uses rich, ASCII-art inspired tables to show data.
These tables are often shared verbatim in other documents.
For example, take the table used to demonstrate [new CSV features in the DuckDB v1.2.0 release blog post]({% post_url 2025-02-05-announcing-duckdb-120 %}#csv-features.md):

```text
┌─────────┬───────┐
│    a    │   b   │
│ varchar │ int64 │
├─────────┼───────┤
│ hello   │    42 │
│ world   │    84 │
└─────────┴───────┘
```

What if we would like to load this data back to DuckDB?
This is not supported by default but it can be achieved by some scripting:
we can turn the table into a `│`-separated file and read it with DuckDB's [CSV reader]({% link docs/data/csv/overview.md %}).
Note that the separator is not the pipe character `|`, instead it is the [“Box Drawings Light Vertical” character](https://www.compart.com/en/unicode/U+2502) `│`.

## Loading Duckbox Tables to DuckDB

First, we save the table above as `duckbox.csv`.
Then, we clean it using `sed`:

```batch
echo -n > duckbox-cleaned.csv
sed -n "2s/^│ *//;s/ *│$//;s/ *│ */│/p;2q" duckbox.csv >> duckbox-cleaned.csv
sed "1,4d;\$d;s/^│ *//;s/ *│$//;s/ *│ */│/g" duckbox.csv >> duckbox-cleaned.csv
```

The `duckbox-cleaned.csv` file looks as follows:

```text
a│b
hello│42
world│84
```

We can then simply load this to DuckDB via:

```sql
FROM read_csv('duckbox-cleaned.csv', delim = '│');
```

And export it to a CSV:

```sql
COPY (FROM read_csv('duckbox-cleaned.csv', delim = '│')) TO 'out.csv';
```

```text
a,b
hello,42
world,84
```

## Using `shellfs`

To implement this in a single `read_csv` without any temporary files, we can use the [`shellfs` Community Extension]({% link community_extensions/extensions/shellfs.md %}):

```sql
INSTALL shellfs FROM community;
LOAD shellfs;
FROM read_csv(
    '(sed -n "2s/^│ *//;s/ *│$//;s/ *│ */│/p;2q" duckbox.csv; ' ||
    'sed "1,4d;\$d;s/^│ *//;s/ *│$//;s/ *│ */│/g" duckbox.csv) |',
    delim = '│');
```

We can also create a [table macro]({% link docs/sql/statements/create_macro.md %}#table-macros):

```sql
CREATE MACRO read_duckbox(path) AS TABLE
    FROM read_csv(
        printf('(sed -n "2s/^│ *//;s/ *│$//;s/ *│ */│/p;2q" %s; ' ||
               'sed "1,4d;\$d;s/^│ *//;s/ *│$//;s/ *│ */│/g" %s) |',
               path, path),
        delim = '│');
```

Then, reading a duckbox table is as simple as:

```sql
FROM read_duckbox('duckbox.csv');
```

## Notes

Please consider the following points when running this script:

* This approach only works if the table does not have long pipe `│` characters.
  It also trims spaces from the table cell values.
  Make sure to factor in these assumptions when running the script.

* The script is compatible with both BSD `sed` (which is the default on macOS) and GNU `sed` (which is the default on Linux and available on macOS as `gsed`).
