---
layout: post
title: "Flying Through Windows"
author: "Richard Wesley"
excerpt: "Dive into the details of recent DuckDB windowing performance improvements."
tags: ["deep dive"]
---

## Introduction

In the previous post I went into some new windowing functionality in DuckDB available through SQL.
But there are other changes that improve our use of resources (such as memory) without adding new functionality.
So let's get “under the feathers” and look at these changes.

## Segment Tree Vectorisation

One important improvement that was made in the summer of 2023 was converting the segment tree evaluation code
to vectorised evaluation from single-value evaluation.
You might wonder why it wasn't that way to begin with in a “vectorised relational database” (!),
but the answer is lost in the mists of time.
My best guess is either that the published algorithm was written for values
or that the aggregation API had not been nailed down yet (or both).

In the old version, we used the aggregate's `update` or `combine` APIs,
but with only the values and tree states for a single row.
To vectorise the segment tree aggregation, we accumulate _vectors_ of leaf values and tree states
and flush them into each output row's state when we reach the vector capacity of 2048 rows..
Some care needed to be taken to handle order-sensitive aggregates by accumulating values in the correct order.
`FILTER` and `EXCLUDE` clauses also provided some entertainment, but the segment trees are now fully vectorised.
The performance gains here were about
[a factor of four](https://github.com/duckdb/duckdb/issues/7809#issuecomment-1679387022)
(from “Baseline” to “Fan Out”).

Once segment trees were vectorised,
we could use the same approach when implementing `DISTINCT` aggregates with merge sort trees.
It may be worth updating the custom window API to handle vectorisation at some point,
because although most custom window aggregates are quite slow (e.g., `quantile`, `mad` and `mode`),
`count(*)` is also implemented as a custom aggregate and would likely benefit from a vectorised implementation.

## Constant Aggregation

A lot of window computations are aggregates over frames,
and a common analytic task with these results is to compare a partial aggregate
to the same aggregate over _the entire partition_.
Computing this value repeatedly is expensive and potentially wasteful of memory
(e.g, the old implementation would construct a segment tree even though only one value was needed.)

The previous performance workaround for this was
to compute the aggregate in a subquery and join it in on the partition keys, but that was, well, unfriendly.
Instead, we have added an optimisation that checks for _partition-wide aggregates_
and computes that value once per partition.
This not only reduces memory and compute time for the aggregate itself,
but we can often return a constant vector that shares the values across all rows in a chunk,
reducing copy costs and potentially even downstream evaluation costs.

Returning a constant vector can yield surprisingly large memory and performance benefits.
In the issue that drove this improvement, the user was constructing a constant 100K element list(!)
and then computing the median with a list aggregation lambda.
By returning a single constant list, we build and reduce that list only once
instead of once per row!

## Streaming Windows

Computing window functions is usually quite expensive!
The entire relation has to be materialised,
broken up into partitions, and each partition needs to be sorted.

But what if there is no partitioning or ordering?
This just means that the window function is computed over the entire relation, in the “natural order”,
using a frame that starts with the first row and continues to the current row.
Examples might be assigning row numbers or computing a running sum.
This is simple enough that we can _stream_ the evaluation of the function on a single thread.

First, let's step back a bit and talk about the window _operator_.
During parsing and optimisation of a query, all the window functions are attached to a single _logical_ window operator.
When it comes time to plan the query, we group the functions that have common partitions and “compatible” orderings
(see Cao et. al.,
[_Optimization of Analytic Window Functions_](https://www.vldb.org/pvldb/vol5/p1244_yucao_vldb2012.pdf)
for more information)
and hand each group off to a separate _physical_ window operator that handles that partitioning and ordering.
In order to use the “natural order” we have to group those functions that can be streamed and execute them first
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
* `LEAD` and `LAG` distances are restricted to a constant within ±2048 (one vector). This is not really a big deal because the distance is usually 1.

In the future we may be able to relax the end of the frame to a constant distance from the current row
that fits inside the buffer length (e.g., `BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`)
but that hasn't been investigated yet.

## Partition Major Evaluation

Window partitions are completely independent, so evaluating them separately is attractive.
Our first implementation took advantage of this and evaluated each partition on a separate thread.
This works well if you have more partitions than threads, and they are all roughly the same size,
but if the partition sizes are skewed or if there is only one partition (a common situation),
then most of the cores will be idle, reducing throughput.

<div align="center">
<img src="/images/blog/windowing/parallel-partitions.png" alt="Thread Partition Evaluation" title="Thread Partition Evaluation" style="max-width:50%;width:50%;height:auto"/>
</div>

To improve the CPU utilisation, we changed the execution model for v1.1 to evaluate partitions in parallel.
The partitions are evaluated from largest to smallest and
we then distribute each partition across as many cores as we can, while synchronising access to shared data structures.
This was a lot more challenging than independent single-threaded evaluation of partitions,
and we had some synchronisation issues (hopefully all sorted now!) that were dealt with in the v1.1.x releases.
But we now have much better core utilisation, especially for unpartitioned data.
As a side benefit, we were able to reduce the memory footprint because fewer partitions were in memory at a time.

<div align="center">
<img src="/images/blog/windowing/partition-major.png" alt="Partition Major Evaluation" title="Partition Major Evaluation" style="max-width:50%;width:50%;height:auto"/>
</div>

One remaining issue is the coarseness of the sub-partitions.
At the moment to avoid copying they use the blocks produced by the sorting code,
which are often larger than we would like.
Reducing the size of these chunks is future work, 
but hopefully we will get to it as part of some proposed changes to the sorting code.

## Out Of Memory Operation

Because windowing materialises the entire relation, it was very easy to blow out the memory budget of a query.
For v1.2 we have switched from materialising active partitions in memory to using a pageable collection.
So now not only do we have fewer active partitions (due to partition major evaluation above),
but those partitions themselves can now spool to disk.
This further reduces memory pressure during evaluation of large partitions.

Windowing is so complex, however, that there are still some remaining large data structures.
The [segment trees](https://www.vldb.org/pvldb/vol8/p1058-leis.pdf)
and [merge sort trees](https://dl.acm.org/doi/10.1145/3514221.3526184)
used for accelerating aggregation are still in memory,
especially the intermediate aggregate states in the middle of the trees.
Solving this completely, will require a general method of serialising aggregate states to disk,
which we do not yet have.
Still, most aggregates can be serialised as binary data without special handling,
so in the short term we can probably cover a lot of cases with the current aggregation infrastructure,
just as we do for `GROUP BY`.

## Shared Expressions

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
    AVG(x) OVER w AS avg_x,
    MAX(x) OVER w AS max_x,
FROM data
WINDOW w AS (
    PARTITION BY p
    ORDER BY s
    ROWS BETWEEN 1_000_000 PRECEDING and 1_000_000 FOLLOWING
)
```

Paging the data for `x` reduces the memory footprint, but the segment trees used to evaluate the three aggregates
will contain duplicate copies of `x` - along with the with operator itself (which has to return `x`).
With v1.2 we have added a mechanism for sharing evaluation of expressions like these between functions.
This not only reduces memory, but in this example we will also reduce disk paging
because all three functions will be accessing the same values.

There are a number of places where we are sharing expressions, including `ORDER BY` arguments,
`RANGE` expressions and “value” functions like `LEAD`, `LAG` and `NTH_VALUE`,
and we are always on the lookout for more (such as frame boundaries - or even segment trees).

## Future Work

While I have mentioned a number of things we would like to get to in the future,
one that doesn't fit nicely into any of the topics so far is query rewriting.
It turns out that some window functions can be evaluated using other techniques
such as [self-joins](https://www.vldb.org/pvldb/vol17/p2162-baca.pdf)
and some of our smarter aggregates (like `arg_max`).
Generating these alternate query plans can have large performance benefits
and we plan to investigate them.

## Conclusion

As you can see, windowing is a big hairy beast!
There is also not a lot of published research on effective algorithms (I've linked to pretty much all of it),
so we are often stuck making it up ourselves or falling back to extremely simple and slow approaches.
But I hope that many of you will find something new and exciting in what we have been up to for the past 2-3 years -
and I will try to be more timely in blogging about future window improvements.
