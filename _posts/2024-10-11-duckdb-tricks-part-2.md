---
layout: post
title: "DuckDB Tricks – Part 2"
author: "Gabor Szarnyas"
thumb: "/images/blog/thumbs/duckdb-tricks.svg"
image: "/images/blog/thumbs/duckdb-tricks.png"
excerpt: "We continue our “DuckDB tricks” series, focusing on queries that clean, transform and summarize data."
tags: ["using DuckDB"]
---

## Overview

This post is the latest installment of the [DuckDB Tricks series]({% post_url 2024-08-19-duckdb-tricks-part-1 %}), where we show you nifty SQL tricks in DuckDB.
Here’s a summary of what we’re going to cover:

| Operation | SQL instructions |
|-----------|---------|
| [Fixing timestamps in CSV files](#fixing-timestamps-in-csv-files) | `regexp_replace()`{:.language-sql .highlight} and `strptime()`{:.language-sql .highlight} |
| [Filling in missing values](#filling-in-missing-values) | `CROSS JOIN`{:.language-sql .highlight}, `LEFT JOIN`{:.language-sql .highlight} and `coalesce()`{:.language-sql .highlight} |
| [Repeated transformation steps](#repeated-data-transformation-steps) | `CREATE OR REPLACE TABLE t AS ... FROM t ...`{:.language-sql .highlight} |
| [Computing checksums for columns](#computing-checksums-for-columns) | `bit_xor(md5_number(COLUMNS(*)::VARCHAR))`{:.language-sql .highlight} |
| [Creating a macro for checksum](#creating-a-macro-for-the-checksum-query) | `CREATE MACRO checksum(tbl) AS TABLE ...`{:.language-sql .highlight} |

## Dataset

For our example dataset, we’ll use `schedule.csv`, a hand-written CSV file that encodes a conference schedule. The schedule contains the timeslots, the locations and the events scheduled.

```csv
timeslot,location,event
2024-10-10 9am,room Mallard,Keynote
2024-10-10 10.30am,room Mallard,Customer stories
2024-10-10 10.30am,room Fusca,Deep dive 1
2024-10-10 12.30pm,main hall,Lunch
2024-10-10 2pm,room Fusca,Deep dive 2
```

## Fixing Timestamps in CSV Files

As usual in real use case, the input CSV is messy with irregular timestamps such as `2024-10-10 9am`.
Therefore, if we load the `schedule.csv` file using DuckDB’s CSV reader, the CSV sniffer will detect the first column as a `VARCHAR` field:

```sql
CREATE TABLE schedule_raw AS
    SELECT * FROM 'https://duckdb.org/data/schedule.csv';

SELECT * FROM schedule_raw;
```

```text
┌────────────────────┬──────────────┬──────────────────┐
│      timeslot      │   location   │      event       │
│      varchar       │   varchar    │     varchar      │
├────────────────────┼──────────────┼──────────────────┤
│ 2024-10-10 9am     │ room Mallard │ Keynote          │
│ 2024-10-10 10.30am │ room Mallard │ Customer stories │
│ 2024-10-10 10.30am │ room Fusca   │ Deep dive 1      │
│ 2024-10-10 12.30pm │ main hall    │ Lunch            │
│ 2024-10-10 2pm     │ room Fusca   │ Deep dive 2      │
└────────────────────┴──────────────┴──────────────────┘
```

Ideally, we would like the `timeslot` column to have the type `TIMESTAMP` so we can treat it as a timestamp in the queries later. To achieve this, we can use the table we just loaded and fix the problematic entities by using a regular expression-based search and replace operation, which unifies the format to `hours.minutes` followed by `am` or `pm`. Then, we convert the string to timestamps using [`strptime`]({% link docs/stable/sql/functions/dateformat.md %}#strptime-examples) with the `%p` format specifier capturing the `am`/`pm` part of the string.

```sql
CREATE TABLE schedule_cleaned AS
    SELECT
        timeslot
            .regexp_replace(' (\d+)(am|pm)$', ' \1.00\2')
            .strptime('%Y-%m-%d %H.%M%p') AS timeslot,
        location,
        event
    FROM schedule_raw;
```

Note that we use the [dot operator for function chaining]({% link docs/stable/sql/functions/overview.md %}#function-chaining-via-the-dot-operator) to improve readability. For example, `regexp_replace(string, pattern, replacement)` is formulated as `string.regexp_replace(pattern, replacement)`. The result is the following table:

```text
┌─────────────────────┬──────────────┬──────────────────┐
│      timeslot       │   location   │      event       │
│      timestamp      │   varchar    │     varchar      │
├─────────────────────┼──────────────┼──────────────────┤
│ 2024-10-10 09:00:00 │ room Mallard │ Keynote          │
│ 2024-10-10 10:30:00 │ room Mallard │ Customer stories │
│ 2024-10-10 10:30:00 │ room Fusca   │ Deep dive 1      │
│ 2024-10-10 12:30:00 │ main hall    │ Lunch            │
│ 2024-10-10 14:00:00 │ room Fusca   │ Deep dive 2      │
└─────────────────────┴──────────────┴──────────────────┘
```

## Filling in Missing Values

Next, we would like to derive a schedule that includes the full picture: *every timeslot* for *every location* should have its line in the table. For the timeslot-location combinations, where there is no event specified, we would like to explicitly add a string that says `<empty>`.

To achieve this, we first create a table `timeslot_location_combinations` containing all possible combinations using a `CROSS JOIN`. Then, we can connect the original table on the combinations using a `LEFT JOIN`. Finally, we replace `NULL` values with the `<empty>` string using the [`coalesce` function]({% link docs/stable/sql/functions/utility.md %}#coalesceexpr-).

> The `CROSS JOIN` clause is equivalent to simply listing the tables in the `FROM` clause without specifying join conditions. By explicitly spelling out `CROSS JOIN`, we communicate that we intend to compute a Cartesian product – which is an expensive operation on large tables and should be avoided in most use cases.

```sql
CREATE TABLE timeslot_location_combinations AS 
    SELECT timeslot, location
    FROM (SELECT DISTINCT timeslot FROM schedule_cleaned)
    CROSS JOIN (SELECT DISTINCT location FROM schedule_cleaned);

CREATE TABLE schedule_filled AS
    SELECT timeslot, location, coalesce(event, '<empty>') AS event
    FROM timeslot_location_combinations
    LEFT JOIN schedule_cleaned
        USING (timeslot, location)
    ORDER BY ALL;

SELECT * FROM schedule_filled;
```

```text
┌─────────────────────┬──────────────┬──────────────────┐
│      timeslot       │   location   │      event       │
│      timestamp      │   varchar    │     varchar      │
├─────────────────────┼──────────────┼──────────────────┤
│ 2024-10-10 09:00:00 │ main hall    │ <empty>          │
│ 2024-10-10 09:00:00 │ room Fusca   │ <empty>          │
│ 2024-10-10 09:00:00 │ room Mallard │ Keynote          │
│ 2024-10-10 10:30:00 │ main hall    │ <empty>          │
│ 2024-10-10 10:30:00 │ room Fusca   │ Deep dive 1      │
│ 2024-10-10 10:30:00 │ room Mallard │ Customer stories │
│ 2024-10-10 12:30:00 │ main hall    │ Lunch            │
│ 2024-10-10 12:30:00 │ room Fusca   │ <empty>          │
│ 2024-10-10 12:30:00 │ room Mallard │ <empty>          │
│ 2024-10-10 14:00:00 │ main hall    │ <empty>          │
│ 2024-10-10 14:00:00 │ room Fusca   │ Deep dive 2      │
│ 2024-10-10 14:00:00 │ room Mallard │ <empty>          │
├─────────────────────┴──────────────┴──────────────────┤
│ 12 rows                                     3 columns │
└───────────────────────────────────────────────────────┘
```

We can also put everything together in a single query using a [`WITH` clause]({% link docs/stable/sql/query_syntax/with.md %}):

```sql
WITH timeslot_location_combinations AS (
    SELECT timeslot, location
    FROM (SELECT DISTINCT timeslot FROM schedule_cleaned)
    CROSS JOIN (SELECT DISTINCT location FROM schedule_cleaned)
)
SELECT timeslot, location, coalesce(event, '<empty>') AS event
FROM timeslot_location_combinations
LEFT JOIN schedule_cleaned
    USING (timeslot, location)
ORDER BY ALL;
```

## Repeated Data Transformation Steps

Data cleaning and transformation usually happens as a sequence of transformations that shape the data into a form that’s best fitted to later analysis.
These transformations are often done by defining newer and newer tables using [`CREATE TABLE ... AS SELECT` statements]({% link docs/stable/sql/statements/create_table.md %}#create-table--as-select-ctas).

For example, in the sections above, we created `schedule_raw`, `schedule_cleaned`, and `schedule_filled`. If, for some reason, we want to skip the cleaning steps for the timestamps, we have to reformulate the query computing `schedule_filled` to use `schedule_raw` instead of `schedule_cleaned`. This can be tedious and error-prone, and it results in a lot of unused temporary data – data that may accidentally get picked up by queries that we forgot to update!

In interactive analysis, it’s often better to use the same table name by running [`CREATE OR REPLACE` statements]({% link docs/stable/sql/statements/create_table.md %}#create-or-replace):

```sql
CREATE OR REPLACE TABLE ⟨table_name⟩ AS
    ...
    FROM ⟨table_name⟩
    ...;
```

Using this trick, we can run our analysis as follows:

```sql
CREATE OR REPLACE TABLE schedule AS
    SELECT * FROM 'https://duckdb.org/data/schedule.csv';

CREATE OR REPLACE TABLE schedule AS
    SELECT
        timeslot
            .regexp_replace(' (\d+)(am|pm)$', ' \1.00\2')
            .strptime('%Y-%m-%d %H.%M%p') AS timeslot,
        location,
        event
    FROM schedule;

CREATE OR REPLACE TABLE schedule AS
    WITH timeslot_location_combinations AS (
        SELECT timeslot, location
        FROM (SELECT DISTINCT timeslot FROM schedule)
        CROSS JOIN (SELECT DISTINCT location FROM schedule)
    )
    SELECT timeslot, location, coalesce(event, '<empty>') AS event
    FROM timeslot_location_combinations
    LEFT JOIN schedule
        USING (timeslot, location)
    ORDER BY ALL;

SELECT * FROM schedule;
```

Using this approach, we can skip any step and continue the analysis without adjusting the next one.

What’s more, our script can now be re-run from the beginning without explicitly deleting any tables: the `CREATE OR REPLACE` statements will automatically replace any existing tables.

## Computing Checksums for Columns

It’s often beneficial to compute a checksum for each column in a table, e.g., to see whether a column’s content has changed between two operations.
We can compute a checksum for the `schedule` table as follows:

```sql
SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
FROM schedule;
```

What’s going on here?
We first list columns ([`COLUMNS(*)`]({% link docs/stable/sql/expressions/star.md %}#columns-expression)) and cast all of them to `VARCHAR` values.
Then, we compute the numeric MD5 hashes with the [`md5_number` function]({% link docs/stable/sql/functions/utility.md %}#md5_numberstring) and aggregate them using the [`bit_xor` aggregate function]({% link docs/stable/sql/functions/aggregates.md %}#bit_xorarg).
This produces a single `HUGEINT` (`INT128`) value per column that can be used to compare the content of tables.

If we run this query in the script above, we get the following results:

```text
┌──────────────────────────────────────────┬────────────────────────────────────────┬─────────────────────────────────────────┐
│                 timeslot                 │                location                │                  event                  │
│                  int128                  │                 int128                 │                 int128                  │
├──────────────────────────────────────────┼────────────────────────────────────────┼─────────────────────────────────────────┤
│ -134063647976146309049043791223896883700 │ 85181227364560750048971459330392988815 │ -65014404565339851967879683214612768044 │
└──────────────────────────────────────────┴────────────────────────────────────────┴─────────────────────────────────────────┘
```

```text
┌────────────────────────────────────────┬────────────────────────────────────────┬─────────────────────────────────────────┐
│                timeslot                │                location                │                  event                  │
│                 int128                 │                 int128                 │                 int128                  │
├────────────────────────────────────────┼────────────────────────────────────────┼─────────────────────────────────────────┤
│ 62901011016747318977469778517845645961 │ 85181227364560750048971459330392988815 │ -65014404565339851967879683214612768044 │
└────────────────────────────────────────┴────────────────────────────────────────┴─────────────────────────────────────────┘
```

```text
┌──────────────────────────────────────────┬──────────┬──────────────────────────────────────────┐
│                 timeslot                 │ location │                  event                   │
│                  int128                  │  int128  │                  int128                  │
├──────────────────────────────────────────┼──────────┼──────────────────────────────────────────┤
│ -162418013182718436871288818115274808663 │        0 │ -135609337521255080720676586176293337793 │
└──────────────────────────────────────────┴──────────┴──────────────────────────────────────────┘
```

## Creating a Macro for the Checksum Query

We can turn the [checksum query](#computing-checksums-for-columns) into a [table macro]({% link docs/stable/sql/statements/create_macro.md %}#table-macros) with the new [`query_table` function]({% link docs/stable/guides/sql_features/query_and_query_table_functions.md %}):

```sql
CREATE MACRO checksum(table_name) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(table_name);
```

This way, we can simply invoke it on the `schedule` table as follows (also leveraging DuckDB’s [`FROM`-first syntax]({% link docs/stable/sql/query_syntax/from.md %})):

```sql
FROM checksum('schedule');
```

```text
┌──────────────────────────────────────────┬────────────────────────────────────────┬─────────────────────────────────────────┐
│                 timeslot                 │                location                │                  event                  │
│                  int128                  │                 int128                 │                 int128                  │
├──────────────────────────────────────────┼────────────────────────────────────────┼─────────────────────────────────────────┤
│ -134063647976146309049043791223896883700 │ 85181227364560750048971459330392988815 │ -65014404565339851967879683214612768044 │
└──────────────────────────────────────────┴────────────────────────────────────────┴─────────────────────────────────────────┘
```

## Closing Thoughts

That’s it for today!
We’ll be back soon with more DuckDB tricks and case studies.
In the meantime, if you have a trick that would like to share, please share it with the DuckDB team on our social media sites, or submit it to the [DuckDB Snippets site](https://duckdbsnippets.com/) (maintained by our friends at MotherDuck).
