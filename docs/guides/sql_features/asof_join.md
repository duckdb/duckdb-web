---
layout: docu
title: AsOf Join
---

## What is an AsOf Join?

Time series data is not always perfectly aligned.
Clocks may be slightly off, or there may be a delay between cause and effect.
This can make connecting two sets of ordered data challenging.
AsOf joins are a tool for solving this and other similar problems.

One of the problems that AsOf joins are used to solve is
finding the value of a varying property at a specific point in time.
This use case is so common that it is where the name came from:  
_Give me the value of the property **as of this time**_.

More generally, however, AsOf joins embody some common temporal analytic semantics,
which can be cumbersome and slow to implement in standard SQL.

## Portfolio Example Data Set

Let's start with a concrete example.
Suppose we have a table of stock [`prices`](/data/prices.csv) with timestamps:

<div class="narrow_table"></div>

| ticker | when | price |
| :----- | :--- | ----: |
| APPL   | 2001-01-01 00:00:00 | 1 |
| APPL   | 2001-01-01 00:01:00 | 2 |
| APPL   | 2001-01-01 00:02:00 | 3 |
| MSFT   | 2001-01-01 00:00:00 | 1 |
| MSFT   | 2001-01-01 00:01:00 | 2 |
| MSFT   | 2001-01-01 00:02:00 | 3 |
| GOOG   | 2001-01-01 00:00:00 | 1 |
| GOOG   | 2001-01-01 00:01:00 | 2 |
| GOOG   | 2001-01-01 00:02:00 | 3 |

We have another table containing portfolio [`holdings`](/data/holdings.csv) at various points in time:

<div class="narrow_table"></div>

| ticker | when | shares |
| :----- | :--- | -----: |
| APPL   | 2000-12-31 23:59:30 | 5.16   |
| APPL   | 2001-01-01 00:00:30 | 2.94   |
| APPL   | 2001-01-01 00:01:30 | 24.13  |
| GOOG   | 2000-12-31 23:59:30 | 9.33   |
| GOOG   | 2001-01-01 00:00:30 | 23.45  |
| GOOG   | 2001-01-01 00:01:30 | 10.58  |
| DATA   | 2000-12-31 23:59:30 | 6.65   |
| DATA   | 2001-01-01 00:00:30 | 17.95  |
| DATA   | 2001-01-01 00:01:30 | 18.37  |

To load these tables to DuckDB, run:

```sql
CREATE TABLE prices AS FROM 'https://duckdb.org/data/prices.csv';
CREATE TABLE holdings AS FROM 'https://duckdb.org/data/holdings.csv';
```

## Inner AsOf Joins

We can compute the value of each holding at that point in time by finding
the most recent price before the holding's timestamp by using an AsOf Join:

```sql
SELECT h.ticker, h.when, price * shares AS value
FROM holdings h
ASOF JOIN prices p
       ON h.ticker = p.ticker
      AND h.when >= p.when;
```

This attaches the value of the holding at that time to each row:

<div class="narrow_table"></div>

| ticker | when | value |
| :----- | :--- | ----: |
| APPL   | 2001-01-01 00:00:30 | 2.94  |
| APPL   | 2001-01-01 00:01:30 | 48.26 |
| GOOG   | 2001-01-01 00:00:30 | 23.45 |
| GOOG   | 2001-01-01 00:01:30 | 21.16 |

It essentially executes a function defined by looking up nearby values in the `prices` table. 
Note also that missing `ticker` values do not have a match and don't appear in the output.

## Outer AsOf Joins

Because AsOf produces at most one match from the right hand side, 
the left side table will not grow as a result of the join,
but it could shrink if there are missing times on the right.
To handle this situation, you can use an *outer* AsOf Join:

```sql
SELECT h.ticker, h.when, price * shares AS value
FROM holdings h
ASOF LEFT JOIN prices p
            ON h.ticker = p.ticker
           AND h.when >= p.when
ORDER BY ALL;
```

As you might expect, this will produce `NULL` prices and values instead of dropping left side rows
when there is no ticker or the time is before the prices begin.

<div class="narrow_table"></div>

| ticker | when | value |
| :----- | :--- | ----: |
| APPL   | 2000-12-31 23:59:30 |       |
| APPL   | 2001-01-01 00:00:30 | 2.94  |
| APPL   | 2001-01-01 00:01:30 | 48.26 |
| GOOG   | 2000-12-31 23:59:30 |       |
| GOOG   | 2001-01-01 00:00:30 | 23.45 |
| GOOG   | 2001-01-01 00:01:30 | 21.16 |
| DATA   | 2000-12-31 23:59:30 |       |
| DATA   | 2001-01-01 00:00:30 |       |
| DATA   | 2001-01-01 00:01:30 |       |

## AsOf Joins with the `USING` Keyword

So far we have been explicit about specifying the conditions for AsOf,
but SQL also has a simplified join condition syntax 
for the common case where the column names are the same in both tables.
This syntax uses the `USING` keyword to list the fields that should be compared for equality.
AsOf also supports this syntax, but with two restrictions:

* The last field is the inequality
* The inequality is `>=` (the most common case)

Our first query can then be written as:

```sql
SELECT ticker, h.when, price * shares AS value
FROM holdings h
ASOF JOIN prices p USING (ticker, when);
```

Be aware that if you don't explicitly list the columns in the `SELECT`,
the ordering field value will be the probe value, not the build value.
For a natural join, this is not an issue because all the conditions are equalities,
but for AsOf, one side has to be chosen.
Since AsOf can be viewed as a lookup function,
it is more natural to return the "function arguments" than the function internals.

## See Also

For implementation details, see the [blog post "DuckDB's AsOf joins: Fuzzy Temporal Lookups"](/2023/09/15/asof-joins-fuzzy-temporal-lookups).
