---
layout: post
title: "Catching up with Windowing"
author: "Richard Wesley"
excerpt: "DuckDB implements a number of modern window features, some of which are extensions to the SQL standard."
tags: ["using DuckDB"]
---

## Background

In the beginning, the relational data processing model was all about sets.
This was [Codd's great insight](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf)
and for many years, relational processing took little notice of data ordering.

But it turns out that there are a lot of analytic operations that are related to ordering.
For example, smoothing out noise in time series is very difficult to do in traditional SQL queries
(it involves self-joins with inequality conditions!)
So in the late 1990s database vendors started adding _windowing_ operations.
By making the user's intent clear, the operations could be implemented much more efficiently,
and these operations were eventually
[added to the SQL:2003 standard](https://en.wikipedia.org/wiki/Window_function_(SQL)).

DuckDB has had support for window functions since the early days,
but if they are new to you, you might want to start with my earlier blog posts
on [Windowing in DuckDB](2021/10/13/windowing.html)
and [Fast Moving Holistic Aggregates](2021/11/12/moving-holistic.html),
or just [the window function documentation](docs/sql/functions/window_functions).
In this post, I will start by introducing the more recent functionality additions,
and then spelunk into the internals to talk about some performance and scaling improvements.

For the examples in this post, I will mostly stick to using a table of athletic results:

| Field | Type | Description |
| ----- | ---- | ----------- |
| event | VARCHAR | The name of the event (e.g., 200 meter butterfly)
| athlete | VARCHAR | The name of the competitor (e.g., Michael Phelps)
| date | TIMESTAMP | The start of the event. |
| time | DECIMAL(18, 3) | The athlete's time in that event (in seconds). |

## Functionality

> Several of the outfits, Ignatius noticed, were new enough and expensive enough to be properly considered
> offenses against taste and decency.
>   -- John Kennedy O'Tools, _A Confederacy of Dunces_

### Frame Exclusion

In our original implementation, there was a piece of the 2003 specification that had not been implemented:
the `EXCLUDE` clause.
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
    AVG(time) OVER w AS recent,
FROM results
WINDOW w AS (PARTITION BY event ORDER BY date RANGE BETWEEN 10 DAYS PRECEDING AND 10 DAYS FOLLOWING EXCLUDE CURRENT ROW)
ORDER BY event, date, athlete;
```

There are four options for `EXCLUDE` that specify how to treat the current row:

* `CURRENT ROW` - exclude just the current row
* `GROUP` - exclude the current row and all its "peers" (rows that have the same `ORDER BY` value)
* `TIES` - exclude all peer rows, but _not_ the current row (this makes a hole on either side)
* `NO OTHERS` - don't exclude anything (the default)

Exclusion is implemented for both windowed aggregates and for the `FIRST/LAST/NTH_VALUE` functions.

### Aggregate Modifiers

There are several modifiers for ordinary aggregate functions (`FILTER`, `DISTINCT` and `ORDER BY` as an argument)
that are not part of the SQL:2003 standard for windowing, but which are also useful in a windowing context.
`FILTER` is pretty straightforward (and DuckDB has supported it for a while)
but the others are not easy to implement efficiently.

They can of course be implemented naïvely (academic-speak for "slow"!) by just computing each row independently:

* re-read all the values,
* filtering out the ones we don't want,
* sticking them into a hash table to remove duplicates,
* sort the results,
* send them off to the aggregate function to get the result

We have an implementation that does this (which you can access by turning off the optimiser)
and we use it to check fancier implementations, but it is horribly slow.

Fortunately, these last two modifiers have been the subject of
[research](https://www.vldb.org/pvldb/vol9/p1221-wesley.pdf)
[published](https://dl.acm.org/doi/10.1145/3514221.3526184)
in the last 10 years,
and we have now added those algorithms to the windowing aggregates.
We can then use the `DISTINCT` modifier to exclude duplicates in the frame:

```sql
-- Count the number of distinct athletes at a given point in time
SELECT COUNT(DISTINCT athlete) OVER (ORDER BY date) FROM results;
-- Concatenate those distinct athletes into a list
SELECT LIST(DISTINCT athlete) OVER (ORDER BY date) FROM results;
```

We can also use the `ORDER BY` modifier with order-sensitive aggregates to get sorted results:

```sql
-- Return an alphabetised list of athletes who made or beat a time
SELECT LIST(althete ORDER BY athlete) OVER (PARTITION by event, date ORDER BY time DESC)
FROM results
```

I should mention that the research on these extensions is ongoing,
and combining them will often force us to use the naïve implementation.
So for example, if we wished to exclude the athlete who made the time in the previous example:

```sql
-- Return an alphabetised list athletes who beat the each time
SELECT LIST(althete ORDER BY athlete) OVER (PARTITION by event, date ORDER BY time DESC EXCLUDE CURRENT ROW)
FROM results
```

DuckDB will still compute this for you, but it may be horribly slow.

### Function Modifiers

The `ORDER BY` modifier also makes sense for some non-aggregate window functions,
especially if we let them use framing:

```sql
-- Compute the current world record holder over time for each event
SELECT
    event,
    date,
    FIRST_VALUE(time ORDER BY time DESC) OVER w AS record_time,
    FIRST_VALUE(athlete ORDER BY time DESC) OVER w AS record_holder,
FROM results
WINDOW w AS (
    PARTITION BY event
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
ORDER BY event, date
```

All of the non-aggregate window functions (except `DENSE_RANK`) now support ordering arguments
and will use the frame instead of the entire partition when an ordering argument is supplied.

> Tip If you wish to use the entire frame with an ordering argument, then you will need to be explicit and use `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

## Performance

Now that we have covered several years of new functionality,
lets get "under the feathers" and look at some performance improvements that are not part of SQL.

### Constant Aggregation

A lot of window computations are aggregates over frames,
and a common analytic task with these results is to compare a partial aggregate
to the same aggregate over _the entire partition_.
Computing this value repeatedly is expensive and potentially wasteful of memory
(the old implementation would construct a segment tree even though only one value was needed.)

The previous workaround for this was to compute the aggregate in a subquery and join it in on the partition keys,
but that was, well, unfriendly.
Instead, we added an optimisation that checks for partition-wide aggregates
and computes it once per partition.
This not only reduces memory and compute time for the aggregate itself,
but we can often return a constant vector that shares the values across all rows in a chunk,
reducing copy costs and potentially even downstream evaluation costs.

### Streaming Windows

Computing window functions is usually quite expensive!
The entire relation has to be materialised,
broken up into partitions, and each partition needs to be sorted.

But what if there is no partitioning or ordering?
This just means that the window function is computed over the entire relation, in the "natural order",
using a frame that starts with the first row and continues to the current row.
Examples might be assigning row numbers or computing a running sum.
This is simple enough that we can _stream_ the evaluation of the function on a single thread.

First, let's step back a bit and talk about the window _operator_.
During parsing and optimisation of a query, all the window functions are attached to a single _logical_ window operator.
When it comes time to plan the query, we group the functions that have common partitions and "compatible" orderings
(see Cao et. al., (Optimization of Analytic Window Functions)[https://www.vldb.org/pvldb/vol5/p1244_yucao_vldb2012.pdf]
for more information)
and hand each group off to a separate physical window operator that handles that partitioning and ordering.
In order to use the "natural order" we have to group those functions that can be streamed and execute them first
(or the order will have been destroyed!) and hand them off to the _streaming_ physical window operator.

So what functions can we stream? It turns out there are quite a few:

* Aggregates `BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (we just update the aggregate)
* `FIRST_VALUE` - it's always the same
* `PERCENT RANK` - it's always 0
* `RANK` - it's always 0
* `DENSE_RANK` - it's always 0
* `ROW_NUMBER` - we just count the rows
* `LEAD` and `LAG` - we just keep a buffer

There are a few more restrictions:

* `IGNORE NULLS`, `EXCLUDE` and `ORDER BY` arguments are not allowed
* `LEAD` and `LAG` distances are restricted to a constant within ±2048 (one vector)

(The `LEAD` and `LAG` restriction is actually not a big one because usually the distance is 1.)

In the future we may be able to relax the end of the frame to a constant distance from the current row
that fits inside the buffer length (e.g., `BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`)
but that hasn't been investigated yet.

### Partition Major Evaluation

Window partitions are completely independent, so evaluating them separately is attractive.
Our first implementation took advantage of this and evaluated each partition on a separate thread.
This works well if you have more partitions than threads, and they are all roughly the same size,
but if the partition sizes are skewed or if there is only one partitions (a common situation),
then most of the cores will be idle, reducing throughput.

To improve the CPU utilisation, we changed the execution model for v1.1 to evaluate partitions in parallel.
The partitions are evaluated from largest to smallest and
we then distribute each partition across as many cores as we can and synchronise access to shared data structures.
This was a lot more challenging than independent single-threaded evaluation of partitions,
and we had some synchronisation issues (hopefully all sorted now!) that were dealt with in the v1.1.x releases.
But we now have much better core utilisation, especially for unpartitioned data.
As a side benefit, we were able to reduce the memory footprint because fewer partitions were in memory at a time.

One remaining issue is the coarseness of the sub-partitions.
At the moment to avoid copying they use the blocks produced by the sorting code,
which are often larger than we would like.
Reducing the size of these chunks is future work, but hopefully we will get to it in the near future.

### Out Of Memory Operations

Because windowing materialises the entire relation, it was very easy to blow out the memory budget of a query.
For v1.2 we have switched from materialising active partitions in memory to using a pageable collection.
So now not only do we have fewer active partitions (due to partition major evaluation above),
but those partitions themselves can now spool to disk.
This further reduces memory pressure during evaluation of large partitions.

Windowing is so complex, however, that there are still some remaining large data structures.
The [segment trees](https://www.vldb.org/pvldb/vol8/p1058-leis.pdf)
and merge sort trees used for accelerating aggregation are still in memory,
especially the intermediate aggregate states in the middle of the trees.
Solving this completely, will require a general method of serialising aggregate states to disk,
which we do not yet have.
Still, most aggregates can be serialised as binary data without special handling,
so in the short term we can probably cover a lot of cases with the current aggregation infrastructure,
just as we do for `GROUP BY`.

### Shared Expressions

Window expressions are evaluated independently, but they often share expressions.
Some of those expressions can be expensive to evaluate and others need to be materialised
over the entire partition.
As an example of the latter, aggregate functions can reference values anywhere in the partition.
This could result in computing and materialising the same values multiple times:

```sql
-- Compute the moving average and range of x over a large window
SELECT
    x,
    MIN(x) OVER w AS min_x,
    AVG(x) OVER w AS min_x,
    MAX(x) OVER w AS max_x,
FROM data
WINDOW w AS (PARTITION BY p ORDER BY s ROWS BETWEEN 1_000_000 PRECEDING and 1_000_000 FOLLOWING)
```

Paging the data for `x` reduces the memory footprint, but the segment trees used to evaluate the three aggregates
will contain duplicate copies of `x` - along with the with operator itself (which has to return `x`).
With v1.2 we have added a mechanism for sharing evaluation of expressions like these between functions.
This not only reduces memory, but in this example we will also reduce disk paging
because all three functions will be accessing the same values.

There are a number of places where we are sharing expressions, including `ORDER BY` arguments,
`RANGE` expressions and "value" functions like `LEAD`, `LAG` and `NTH_VALUE`,
and we are always on the lookout for more (such as frame boundaries).

### Future Work

While I have mentioned a number of things we would like to get to in the future,
one that doesn't fit nicely into any of the topics so far is query rewriting.
It turns out that some window functions can be evaluated using other techniques
such as [self-joins](https://www.vldb.org/pvldb/vol17/p2162-baca.pdf)
and some of our smarter aggregates (like `arg_max`).
Generating these alternate query plans can have large performance benefits
and we will be investigating them in the future.

## Conclusion

As you can see, windowing is a big hairy beast!
There is also not a lot of published research on effective algorithms (I've linked to pretty much all of it),
so we are often stuck making it up ourselves or falling back to extremely simple and slow approaches.
But I hope that many of you will find something new and exciting in what we have been up to for the past 2-3 years -
and I will try to be more timely in blogging about future window improvements.