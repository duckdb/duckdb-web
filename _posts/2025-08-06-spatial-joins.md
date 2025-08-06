---
layout: post
title: "Spatial Joins in DuckDB"
author: "Max Gabrielsson"
tags: ["deep dive"]
excerpt: "Despite being challenging to optimize, DuckDB v1.3.0 signifcantly improves the scalability of geospatial joins with a dedicated `SPATIAL_JOIN` operator"
---

## Introduction 

Spatial joins are join operations that match rows based on the (geo-)spatial relationship between column(s). In practice they are often used to answer questions like “which of these points are within which of these polygons?”, but at a high level, connecting two datasets based on the **physical location(s)** they model is an extremely powerful way to correlate and enrich otherwise disparate data sources, anchor insights to the real world, and more often than not tell a great story with your analysis.

Ever since its inception, DuckDB's `spatial` extension has provided a `GEOMETRY` column type to represent locations, regions and shapes, along with plenty of _spatial predicate_ functions to use when `JOIN`:ing. But it wasn't until recently, in DuckDB v1.3.0 that spatial joins really became _scalable_ thanks to the introduction of the dedicated `SPATIAL_JOIN` query **operator**. 

I managed to hastily sneak in some information about it towards [the end of the v1.3.0 release notes]({% post_url 2025-05-21-announcing-duckdb-130 %}#spatial-join-operator), but we figured there is enough say about it to justify a separate blog post. So in this post, we will take a closer look at some of the challenges of optimizing spatial joins in DuckDB and how the new `SPATIAL_JOIN` operator achieves new levels of efficency.

## What does spatial join look like again?

Spatial joins are incredibly important in geospatial analysis, and performing one in SQL is actually surprisingly easy. They don't require any special syntax or magic incantation, you just have to join two tables with a `GEOMETRY` column using some _spatial predicate_. Below is a simple query that joins two tables `a` and `b` on the condition that the geometries in `a.geom` and `b.geom` “intersect”, using the `ST_Intersects` spatial predicate function:

```sql
SELECT * FROM a JOIN b ON ST_Intersects(a.geom, b.geom)
```

Let's try to do something more advanced to demonstrate. We're going to analyze the [New York City Citi Bike Trip dataset](https://citibikenyc.com/system-data), which contains around 58 million rows representing rental bike trips in New York City, including the start and end locations of each trip. We want to find neighborhoods in NYC that have the most bike trips starting in them. To do this, we will join the bike trip data with a [dataset of NYC neighborhoods](https://www.nyc.gov/content/planning/pages/resources/datasets/neighborhood-tabulation), count and group the number of trips starting in each neighborhood, and finally sort a limit to return the top 3 groups. We've compiled these datasets and extracted the relevant columns for this example into two tables, `rides` and `hoods` in a [DuckDB database available to download here](https://duckdb-blobs.s3.us-east-1.amazonaws.com/biketrips.db)

The query looks like this:

```sql
LOAD spatial; -- Load the spatial extension

SELECT neighborhood, count(*) as num_rides 
FROM rides JOIN hoods on st_intersects(rides.start_geom, hoods.geom) 
GROUP BY neighborhood 
ORDER BY num_rides 
LIMIT 3;
```

```text
┌──────────────┬───────────┐
│ neighborhood │ num_rides │
│   varchar    │   int64   │
├──────────────┼───────────┤
│ Midtown      │   6253835 │
│ Chelsea      │   6238693 │
│ East Village │   4047396 │
└──────────────┴───────────┘
```

This query joins the 58,033,724 rides with the 310 neighborhood polygons and takes about **30s** to run on my laptop (MacBook M3 Pro, 36GB RAM). 

While this might not seem that impressive at first glance (a `HASH_JOIN` over similarly sized input would finish an order of magnitude faster), I'm actually somewhat pleased that DuckDB is able to execute a spatial join at this scale in a time frame somewhat acceptable for interactive exploratory analysis (on a laptop no less!). To understand why, we first need to take a closer look at how DuckDB used to do spatial joins, why spatial joins are so challenging to optimize, and how the new `SPATIAL_JOIN` operator changes the game.

## How DuckDB (used to) do spatial joins

The first thing to understand is that a _spatial predicate_ is really just a function that evaluates some spatial relation between two geometries and returns `true` or `false`, e.g. “does A _contain_ B” or “is A _within distance_ X of B”. In theory you could write your own spatial predicate function, but in practice, you will probably use one of the many that come with the `spatial` extension. The nuances of the different spatial predicates are beyond the scope of this post, but here is a quick overview of the most commonly used ones:

| Function                    | Description                                                                    |
| --------------------------- | ------------------------------------------------------------------------------ |
| `ST_Intersects(a, b)`       | Returns true if geometry A intersects geometry B                               |
| `ST_Contains(a, b)`         | Returns true if geometry A contains geometry B                                 |
| `ST_ContainsProperly(a, b)` | Returns true if geometry A contains geometry B without B touching A's boundary |
| `ST_Within(a, b)`           | Returns true if geometry A is within geometry B                                |
| `ST_Overlaps(a, b)`         | Returns true if geometry A overlaps geometry B                                 |
| `ST_Touches(a, b)`          | Returns true if geometry A touches geometry B                                  |
| `ST_Equals(a, b)`           | Returns true if geometry A is equal to geometry B                              |
| `ST_Crosses(a, b)`          | Returns true if geometry A crosses geometry B                                  |
| `ST_Covers(a, b)`           | Returns true if geometry A covers geometry B                                   |
| `ST_CoveredBy(a, b)`        | Returns true if geometry A is covered by geometry B                            |
| `ST_DWithin(a, b, x)`       | Returns true if geometry A is within distance X of geometry B                  |

Since all the above spatial predicates live in the `spatial` extension, DuckDB's query planner doesn't really know anything about them, except their names and that they are functions that take two `GEOMETRY` arguments and return a boolean value. This means that vanilla DuckDB on its own can't apply any special optimizations to them, and has to treat them like **any other function** in the database.

When DuckDB plans a join where the join condition is an arbitrary function, it normally can't use any of the advanced built-in join strategies like `HASH_JOIN` or `RANGE_JOIN` which are optimized for equality or range comparisons. Instead DuckDB has to fall back to the simplest join strategy, which is to perform a “Nested Loop Join” (NLJ) – i.e. to evaluate the join condition for every possible pair of rows in the two tables. This is the most general way to implement a join, but it is also the least efficient. Since the _complexity_ of the join is `O(n * m)`, where `n` and `m` are the number of rows in the two tables, the time it takes to perform the join grows quadratically with the size of the input.

Quadratic complexity quickly becomes infeasible for large joins, but DuckDB's raw execution power usually makes it bearable when joining small to medium sized tables. However, what makes the nested-loop-join strategy impractical for spatial joins in particular, even at small to medium scale is that spatial predicates can be _very_ computationally expensive to evaluate in the first place. This is mostly due to the sheer complexity of the algorithms involved, but also due to the denormalized nature of geometries, in which a single geometry can contain a very large number of points. Also, besides the inherent theoretical complexity, the reality in `spatial` is that most of the spatial predicates implemented with the help of third-party libraries require a deserialization step to convert the internal binary format of the `GEOMETRY` column to an executable data structure. This usually also requires allocating memory outside of DuckDBs own memory management system, which increases pressure and lock contention on the global memory allocator, limiting the effectiveness of additional parallelism.

To illustrate how this plays out in practice, lets take a look at the query plan for the example query above, but with the `SPATIAL_JOIN` optimization disabled to force DuckDB to use a nested-loop-join instead:

```sql
LOAD spatial; -- Load the spatial extension

-- Disable the spatial join optimizer!
SET disabled_optimizers='extension';

-- Print the new plan, using EXPLAIN to verify that we are using a nested-loop-join
EXPLAIN SELECT neighborhood, count(*) as num_rides 
FROM rides JOIN hoods on st_intersects(rides.start_geom, hoods.geom) 
GROUP BY neighborhood 
ORDER BY num_rides DESC 
LIMIT 3;
```

```text
┌───────────────────────────┐
│           TOP_N           │
│           Top: 3          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│            ...            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│            ...            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│     BLOCKWISE_NL_JOIN     │
│    ────────────────────   │
│      Join Type: INNER     │
│                           ├──────────────┐
│         Condition:        │              │
│ ST_Intersects(start_geom, │              │
│            geom)          │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         SEQ_SCAN          │
│    ────────────────────   ││    ────────────────────   │
│        Table: rides       ││        Table: hoods       │
│            ...            ││            ...            │
│       ~58033724 Rows      ││         ~310 Rows         │
└───────────────────────────┘└───────────────────────────┘
```

Executing this query, with the `BLOCKWISE_NL_JOIN` (blockwise nested-loop-join), now takes **30 minutes** on my laptop. I've also run the query with a limit on the number of rows in the `rides` table to see how the performance scales with the size of the input. The results are as follows:

| Number of rows in `rides` | Execution time        |
| ------------------------- | --------------------- |
| 1,000,000                 | 30.8s                 |
| 10,000,000                | 310.3s (~5m)          |
| 58,033,724                | 1799.6s (~30 minutes) |

Which is obviously not great. Running a 1/58th of the full dataset already takes longer than the original query with the spatial join optimization enabled. And processing the full dataset takes almost half an hour to run! This is a clear indication that the nested-loop-join strategy is not suitable for spatial joins at scale, and we really needed to do something about it.

### The IE-Join Optimization

In order to improve the situation, one of the first optimizations implemented in the early versions of the `spatial` extension was a re-write rule for the query planner. 

The goal was to try to reduce the number of pairs that need to be evaluated by the exact spatial predicate function, by first filtering out pairs that are guaranteed to not match using a more efficient but less accurate bounding box check. The key insight is that the common spatial predicates almost all _imply_ that the geometries involved have to also _intersect_. And if they intersect, they also have to have _bounding boxes_ that intersect. This means that we can use the bounding boxes of the geometries to quickly filter out pairs that are guaranteed to not match, before evaluating the more expensive spatial predicate function. 

Since checking if two bounding boxes intersect can be expressed as a set of simple less-than and greater-than comparisons, we can use DuckDB's existing [inequality join]({% post_url 2022-05-27-iejoin %}#inequality-join-iejoin) functionality to perform this join efficiently!

To implement this, we made the following changes to `spatial`:

* Cache an approximate bounding box for each geometry in the serialized binary representation of the `GEOMETRY` column
* Introduce a re-write rule to change any inner nested-loop-join operators with a spatial predicate into two new operators:
    * `PIECEWISE_MERGE_JOIN`, a “IE” (inequality) range-join operator joining on the intersection of the bounding boxes, written as a series of `BETWEEN` clauses on the min/max values of the bounding boxes
    * `FILTER` operator that filters the resulting rows on the actual spatial predicate function.

To show how this affects the query plan, we're going to go back in time and use DuckDB **v1.2.0** (which does contain the `PIECEWISE_MERGE_JOIN` optimization, but **not** the `SPATIAL_JOIN` operator) to re-run the query from above.

```sql
LOAD spatial; -- Load the spatial extension

-- Check that we are using DuckDB v1.2.0
PRAGMA version;
┌─────────────────┬────────────┐
│ library_version │ source_id  │
│     varchar     │  varchar   │
├─────────────────┼────────────┤
│ v1.2.0          │ 5f5512b827 │
└─────────────────┴────────────┘

-- Print the new query plan, using EXPLAIN
EXPLAIN SELECT neighborhood, count(*) as num_rides 
FROM rides JOIN hoods on st_intersects(rides.start_geom, hoods.geom) 
GROUP BY neighborhood 
ORDER BY num_rides DESC 
LIMIT 3;
```

```text
┌───────────────────────────┐
│           TOP_N           │
│    ────────────────────   │
│           Top: 3          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│            ...            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│            ...            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│           FILTER          │
│    ────────────────────   │
│ ST_Intersects(start_geom, │ -- Here we evaluate the actual
│            geom)          │ -- precise spatial predicate
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│    PIECEWISE_MERGE_JOIN   │ 
│    ────────────────────   │
│      Join Type: INNER     │
│                           │
│        Conditions:        │
│  ST_XMin(ST_Extent_Approx │ -- Very complex join condition,
│  (start_geom)) <= ST_XMax │ -- but its all just inequality checks!
│  (ST_Extent_Approx(geom)) │
│  ST_XMax(ST_Extent_Approx │
│  (start_geom)) >= ST_XMin ├──────────────┐
│  (ST_Extent_Approx(geom)) │              │
│  ST_YMin(ST_Extent_Approx │              │
│  (start_geom)) <= ST_YMax │              │
│  (ST_Extent_Approx(geom)) │              │
│  ST_YMax(ST_Extent_Approx │              │
│  (start_geom)) >= ST_YMin │              │
│  (ST_Extent_Approx(geom)) │              │
│                           │              │
│       ~58033724 Rows      │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         SEQ_SCAN          │
│    ────────────────────   ││    ────────────────────   │
│            ...            ││            ...            │
│       ~58033724 Rows      ││         ~310 Rows         │
└───────────────────────────┘└───────────────────────────┘
```

As you can see, the `PIECEWISE_MERGE_JOIN` operator has replaced the `BLOCKWISE_NL_JOIN` operator, and the join condition has been rewritten to use the approximate bounding boxes of the geometries (`ST_Extent_Approx`) instead of directly joining on the spatial predicate. The `FILTER` operator is added on top to only apply the spatial predicate functions on the rows that pass the initial bounding box check. 

This looks a lot more complicated than the original nested-loop-join, so how does it perform?

| Number of rows in `rides` | Execution time |
| ------------------------- | -------------- |
| 1,000,000                 | 2s             |
| 10,000,000                | 21s            |
| 58,033,724                | 108s           |

Much better, we managed to reduce the execution time from 30 minutes to just under 2 minutes for the full dataset! This was a huge improvement. Without requiring any custom operator code, we were able to leverage DuckDBs existing inequality join functionality to significantly speed up spatial joins as well.

However, this approach still has some drawbacks:

* This re-write is only possible to do for `INNER` joins
* We now have to store bounding boxes for each geometry, which increases the memory footprint of the `GEOMETRY` column, and we also have to recompute it whenever create or modify a `GEOMETRY`
* The `PIECEWISE_MERGE_JOIN` operator has to sort the two input tables, which requires a lot of memory and can be really slow for large tables once the data no longer fits in memory

DuckDB has since optimized sorting considerably, and `spatial` and its functions have also received various optimizations that improve performance slightly. Nonetheless this was always somewhat of a stop-gap solution to make spatial joins at least usable in the common case. How can we do better?

## The Spatial Join Operator

One of the goals when implementing the [`RTREE` index]({% link docs/stable/core_extensions/spatial/r-tree_indexes.md %}) last year was to eventually be able to replace the `spatial` extensions `PIECEWISE_MERGE_JOIN` optimization with an index-based join strategy. After implementing the `RTREE`, we realized that creating a r-tree based index on top of existing data is actually surprisingly fast. Instead of requiring the user to always have to load data into a table and then index it just to accelerate their spatial joins, what if we just create a temporary r-tree index on-the-fly when executing the join? Kind of like how we create a temporary hash-table when performing a `HASH_JOIN`?

This is exactly what the new `SPATIAL_JOIN` operator does. It takes two input tables, buffers all the input of the “right” table (i.e. table that the join-order-optimizer expects to be smaller), builds an r-tree index on top of the collected input, and then performs a join by looking up each row of the “left” table in the r-tree index as they arrive. The idea is exactly the same as with a `HASH_JOIN`, but instead of using a hash-table, we use an r-tree as our acceleration data structure to look up the matching rows.

While being a lot more complex to implement compared to the `PIECEWISE_MERGE_JOIN` based approach, this has several advantages:
* The query re-write rule is much simpler, we just have to detect a nested-loop-join with a spatial predicate and replace it with a `SPATIAL_JOIN` operator, no other modifications to the query plan are needed.
* Only the smaller side input needs to be materialized and (sorted to construct the r-tree). The left side can be streamed in parallel, and matching rows can be emitted immediately as they are found.
* The hierarchical structure of the r-tree allows us to prune more of the right side input more accurately
* Since all logic is in one operator, we don't need to rely on a separate `FILTER` operator and can therefore support `LEFT`, `RIGHT` and `FULL OUTER` joins as well as `INNER` joins.

Just to show what this plan looks like, this is what you get when you run the same query but on DuckDB v1.3.0 or later, with the `SPATIAL_JOIN` operator enabled:

```sql
LOAD spatial; -- Load the spatial extension

-- Print the new query plan, using EXPLAIN
EXPLAIN SELECT neighborhood, count(*) as num_rides 
FROM rides JOIN hoods on st_intersects(rides.start_geom, hoods.geom) 
GROUP BY neighborhood 
ORDER BY num_rides DESC 
LIMIT 3;
```

```text
┌───────────────────────────┐
│           TOP_N           │
│    ────────────────────   │
│           Top: 3          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│            ...            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│            ...            │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│        SPATIAL_JOIN       │
│    ────────────────────   │
│      Join Type: INNER     │
│                           │
│        Conditions:        ├──────────────┐
│ ST_Intersects(start_geom, │              │
│            geom)          │              │
│                           │              │
│       ~58033724 Rows      │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         SEQ_SCAN          │
│    ────────────────────   ││    ────────────────────   │
│            ...            ││            ...            │
│       ~58033724 Rows      ││         ~310 Rows         │
└───────────────────────────┘└───────────────────────────┘
```

Nice, we're back to a single join condition again. So how does this perform? We already saw in the first example that DuckDB v1.3.2 was able to execute the original query in about 30 seconds using the `SPATIAL_JOIN` operator, but here are the results for all the different sizes and join strategies for comparison. All queries were run on the same Apple MacBook M3 Pro with 36GB of memory and timings averaged over 3 runs:

| Number of rows in `rides` | Nested Loop Join | Piecewise Merge Join | Spatial Join |
| ------------------------- | ---------------- | -------------------- | ------------ |
| 1,000,000                 | 30.8s            | 2.3s                 | 0.5s         |
| 10,000,000                | 310.3.8s         | 21.2s                | 14.5s        |
| 58,033,724                | 1799.6           | 107.6s               | 28.7s        |

As you can see, the `SPATIAL_JOIN` operator is able to execute the full 58 million row dataset faster than the original naive nested-loop-join could execute the 1 million row dataset. That's a 58x improvement!
But more importantly it also _scales_ much better. Compared to the `PIECEWISE_MERGE_JOIN`, the execution time only doubles as the input size increases almost 6 times over, instead of being multiplied by a similar factor.

## Limitations and Future work

Even though we've made a lot of improvements, spatial joins in DuckDB are not quite perfect just yet. Like always, theres plenty more to do, and we have a few ideas for how to improve the `SPATIAL_JOIN` operator even further:

### Larger-than-memory build-sides: 

The current implementation of the `SPATIAL_JOIN` operator buffers the entire right side input in memory to build the r-tree index. This means that it can only handle right side inputs that fit in memory. We plan to add support for larger-than-memory r-trees by partitioning the right side into smaller separate r-trees, and then merging the results of the join from each partition, similar to how the `HASH_JOIN` operator handles larger-than-memory hash tables.

### Increased parallelism 

DuckDB's execution engine dynamically adjusts the number of threads used in a query based on the number of rows scanned, but since the spatial predicates are so expensive to evaluate, we could potentially benefit from more parallelism as the spatial joins are mostly CPU bound. In particular, we are considering buffering and partitioning the left side of the join as well, which would allow us to spawn our own worker tasks within the operator to evaluate the join condition across a number of threads decoupled from the cardinality of the input. This would increase memory usage and prevent the join from being streamed, but we've been able to employ a similar technique when constructing the [`HNSW` index over in the `vss`  extension]({% link docs/stable/core_extensions/vss.md %}) to great effect.

### Advanced join conditions

The `SPATIAL_JOIN` operator currently only supports the case where the join condition is a single spatial predicate function. We plan to add support for more complex join conditions that can include comparisons, arithmetic operations, and other functions in combination with the spatial predicates. This will allow users to express more complex spatial relationships in their joins, e.g. join `... ON ST_Intersects(a.geom, b.geom) AND a.id = b.id`.

### ANTI/SEMI joins

The `SPATIAL_JOIN` operator currently only supports `INNER`, `LEFT`, `RIGHT` and `FULL OUTER` joins. We plan to add support for `ANTI` and `SEMI` joins in the future.

## Conclusion

Spatial joins are a powerful way to connect and enrich datasets based on their geospatial relationship. DuckDB's `spatial` extension provides a wide assortment of spatial predicate functions that can be used to perform spatial joins in SQL. While the performance of spatial joins has been challenging to deal with in the past due to the complexity of the spatial predicates and the limitations of the join strategies, the new `SPATIAL_JOIN` operator introduced in DuckDB v1.3.0 significantly raises the efficiency and scalability of these workloads, making spatial joins a first-class citizen in DuckDB's execution engine.

