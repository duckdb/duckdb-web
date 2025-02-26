---
layout: post
title: "Catching up with Windowing"
author: "Richard Wesley"
thumb: "/images/blog/thumbs/window-functions-1.svg"
image: "/images/blog/thumbs/window-functions-1.png"
excerpt: "DuckDB implements a number of modern windowing features, some of which are extensions to the SQL standard. This posts presents a few of these features, including GROUPS framing, QUALIFY and aggregate/function modifiers."
tags: ["using DuckDB"]
---

## Background

In the beginning, the relational data processing model was all about sets.
This was [Codd's great insight](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)
and for many years, relational processing took little notice of data ordering.

But it turns out that there are a lot of analytic operations that are related to ordering.
For example, smoothing out noise in time series is very difficult to do in traditional SQL queries
– it involves self-joins with inequality conditions!
So in the late 1990s database vendors started adding _windowing_ operations.
By making the user's intent clear, the operations could be implemented much more efficiently,
and these operations were eventually
[added to the SQL:2003 standard](https://en.wikipedia.org/wiki/Window_function_(SQL)).

DuckDB has had support for window functions since the early days,
but if they are new to you, you might want to start with my earlier blog posts
on [Windowing in DuckDB]({% post_url 2021-10-13-windowing %})
and [Fast Moving Holistic Aggregates]({% post_url 2021-11-12-moving-holistic %}),
or just the [window function documentation]({% link docs/sql/functions/window_functions.md %}).
In this post, I will start by introducing the more recent functionality additions.
In a follow-up post, I will spelunk into the internals to talk about some performance and scaling improvements.

For the examples in this post, I will mostly stick to using a table of athletic `results`:

| Field     | Type             | Description                                        |
| --------- | ---------------- | -------------------------------------------------- |
| `event`   | `VARCHAR`        | The name of the event (e.g., 200 meter butterfly). |
| `athlete` | `VARCHAR`        | The name of the competitor (e.g., Michael Phelps). |
| `date`    | `TIMESTAMP`      | The start time of the event.                       |
| `time`    | `DECIMAL(18, 3)` | The athlete's time in that event (in seconds).     |

## `GROUPS` Framing

In addition to the `ROWS` and `RANGE` frame boundary types (which we have supported for a while now),
the standard also defines `GROUPS` as a boundary type.
`ROWS` is pretty simple: it just counts the number of rows.
`RANGE` is trickier: it treats its counts as distances from
the value of the `ORDER BY` expression at the current row.
This means that there can only be one such expression
and you have to be able to do arithmetic on it.

`GROUPS` is somewhere in between.
A “group” in the standard's language is all the “peers” of a row,
which are all the rows with the same
value of the `ORDER BY` expression at the current row.
In the original windowing code, this was not easy to implement,
but after several years of work, the infrastructure has evolved,
and as of v1.2.0 we now support this last type of framing.

## Frame Exclusion

Another missing piece of the 2003 specification was the `EXCLUDE` clause.
Thanks to work by a community member, we have supported this since v0.10.0,
but we somehow never got around to mentioning it in a blog post!

`EXCLUDE` is an optional modifier to the frame clause for excluding rows around the `CURRENT ROW`.
This is useful when you want to compute some aggregate value of nearby rows
to see how the current row compares to it.
In this example, we want to know how an athlete's time in an event compares to
the average of all the times recorded for their event within ±10 days:

```sql
SELECT
    event,
    date,
    athlete,
    avg(time) OVER w AS recent,
FROM results
WINDOW w AS (
    PARTITION BY event
    ORDER BY date
    RANGE BETWEEN INTERVAL 10 DAYS PRECEDING AND INTERVAL 10 DAYS FOLLOWING
        EXCLUDE CURRENT ROW
)
ORDER BY event, date, athlete;
```

There are four options for `EXCLUDE` that specify how to treat the current row:

* `CURRENT ROW` – exclude just the current row
* `GROUP` – exclude the current row and all its “peers” (rows that have the same `ORDER BY` value)
* `TIES` – exclude all peer rows, but _not_ the current row (this makes a hole on either side)
* `NO OTHERS` – don't exclude anything (the default)

Exclusion is implemented for both windowed aggregates and for the `first`, `last` and `nth_value` functions.

## `QUALIFY` Clause

It may not be immediately obvious, but the SQL language
has rules for the order in which various expressions are computed.
For example, aggregates (like `sum`) are computed after row-level expressions (like `+`).
This is why SQL has two filtering clauses: `WHERE` and `HAVING`:
`WHERE` is for row-level computations and `HAVING` is applied after `GROUP BY`.

When windowing was introduced, it added another layer of computation:
window functions are computed _after_ aggregates.
That is great, but then how do you filter the results of an `OVER` function?
Originally, you had to put the query in a Common Table Expression (or CTE)
which is defined by a `WITH` clause:

```sql
-- Find the third fastest times in each event
WITH windowed AS (
    SELECT
        event,
        athlete,
        time,
        row_number() OVER w AS r
    FROM results
    WINDOW w AS (
        PARTITION BY event
        ORDER BY time
    )
)
SELECT event, athlete, time
FROM windowed
WHERE r = 3;
```

This was kind of clunky, so eventually the `QUALIFY` clause was proposed for filtering window functions.
DuckDB supports this, making it easier to filter the results of window functions:

```sql
-- Find the third fastest times in each event
SELECT event, athlete, time
FROM results
WINDOW w AS (
    PARTITION BY event
    ORDER BY time
)
QUALIFY row_number() OVER w = 3;
```

## Aggregate Modifiers

There are several modifiers for ordinary aggregate functions (`FILTER`, `DISTINCT` and `ORDER BY` as an argument)
that are not part of the SQL:2003 standard for windowing, but which are also useful in a windowing context.
`FILTER` is pretty straightforward (and DuckDB has supported it for a while)
but the others are not easy to implement efficiently.

They can of course be implemented naïvely (academic-speak for “slow”!) by just computing each row independently:

* re-read all the values,
* filter out the ones we don't want,
* stick them into a hash table to remove duplicates,
* sort the results,
* send them off to the aggregate function to get the result.

We have an implementation that does this (which you can access by turning off the optimizer)
and we use it to check fancier implementations, but it is horribly slow.

Fortunately, these last two modifiers have been the subject of
[research](https://www.vldb.org/pvldb/vol9/p1221-wesley.pdf)
[published](https://dl.acm.org/doi/10.1145/3514221.3526184)
in the last 10 years,
and we have now added those algorithms to the windowing aggregates.
We can then use the `DISTINCT` modifier to exclude duplicates in the frame:

```sql
-- Count the number of distinct athletes at a given point in time
SELECT count(DISTINCT athlete) OVER (ORDER BY date) FROM results;
-- Concatenate those distinct athletes into a list
SELECT list(DISTINCT athlete) OVER (ORDER BY date) FROM results;
```

We can also use the `ORDER BY` modifier with order-sensitive aggregates to get sorted results:

```sql
-- Return an alphabetized list of athletes who made or beat a time
SELECT list(athlete ORDER BY athlete) OVER (
    PARTITION BY event, date
    ORDER BY time DESC
)
FROM results;
```

I should mention that the research on these extensions is ongoing,
and combining them will often force us to use the naïve implementation.
So for example, if we wished to exclude the athlete who made the time in the previous example:

```sql
-- Return an alphabetized list athletes who beat the each time
SELECT list(athlete ORDER BY athlete) OVER (
    PARTITION BY event, date
    ORDER BY time DESC
    EXCLUDE CURRENT ROW
)
FROM results;
```

DuckDB will still compute this for you, but it may be very slow.

## Function Modifiers

The `ORDER BY` modifier also makes sense for some non-aggregate window functions,
especially if we let them use framing with it:

```sql
-- Compute the current world record holder over time for each event
SELECT
    event,
    date,
    first_value(time ORDER BY time DESC) OVER w AS record_time,
    first_value(athlete ORDER BY time DESC) OVER w AS record_holder,
FROM results
WINDOW w AS (
    PARTITION BY event
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
ORDER BY event, date;
```

All of the non-aggregate window functions (except `dense_rank`) now support ordering arguments
and will use the frame instead of the entire partition when an ordering argument is supplied.

> Tip If you wish to use the entire frame with an ordering argument, then you will need to be explicit and use `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

> Note If you wish to use the frame ordering _and_ the frame boundaries with a non-aggregate function, you will need to specify the `ORDER BY` _twice_ (once in the frame specification and once in the argument list). This has not yet been optimized, but it will be in the v1.3.0 release.

## Conclusion

Windowing is a very natural way to think about order-dependent analysis,
but it is at odds with traditional unordered query processing.
Nevertheless, since 2003 the SQL language has provided syntax for expressing a wide range of such queries.
In recent years, the community has also considered further extensions to the language
(such as `QUALIFY` and argument modifiers like `DISTINCT` and `ORDER BY`) to improve expressivity.
Here at DuckDB we love providing this kind of expressiveness as part of our [“friendly SQL”]({% link docs/sql/dialect/friendly_sql.md %}) work.
What may  be less obvious is that when we enable users to express their problem more naturally,
it helps us provide more performant solutions!
In my next post, I will go deeper into recent improvements in windowing's performance and resource utilization.
