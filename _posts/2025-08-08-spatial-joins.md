---
layout: post
title: "Spatial Joins in DuckDB"
author: "Max Gabrielsson"
tags: ["deep dive"]
thumb: "/images/blog/thumbs/spatial-joins.svg"
image: "/images/blog/thumbs/spatial-joins.png"
excerpt: "DuckDB v1.3.0 significantly improved the scalability of geospatial joins with a dedicated `SPATIAL_JOIN` operator."
---

## Introduction

Spatial joins are join operations that match rows based on the (geo-)spatial relationship between column(s). In practice they are often used to answer questions like “which of these points are within which of these polygons?”. Being able to connect datasets based on the **physical location(s)** they model is fundamental to the whole field of geospatial data science, but at a high level, also an extremely powerful way to correlate and enrich otherwise disparate data sources, anchor insights to the real world, and more often than not tell a great story with your analysis.

Ever since its inception, DuckDB's `spatial` extension has provided a `GEOMETRY` column type to represent locations, regions and shapes, along with plenty of _spatial predicate_ functions to use when `JOIN`ing. However, it wasn't until recently in [DuckDB v1.3.0]({% post_url 2025-05-21-announcing-duckdb-130 %}) that spatial joins really became _scalable_ thanks to the introduction of the dedicated `SPATIAL_JOIN` query **operator**.

We managed to hastily sneak in some information about this new operator towards [the end of the v1.3.0 release notes]({% post_url 2025-05-21-announcing-duckdb-130 %}#spatial-join-operator), but we figured we got enough to talk about to justify a separate blog post. So in this post, we will take a closer look at some of the challenges involved in optimizing spatial joins, and how the new `SPATIAL_JOIN` operator addresses them to achieve new levels of efficiency.

## What Does a Spatial Join Look Like Again?

Performing a spatial join in SQL is actually very straightforward. There is no special syntax or magic incantation required. Like you probably could've guessed, you just have to `JOIN` two tables with a `GEOMETRY` column using some _spatial predicate_. Below is a simple example that joins two tables `some_table` and `another_table` on the condition that the geometries in `some_table.geom` and `another_table.geom` “intersect”, using the `ST_Intersects` spatial predicate function:

```sql
SELECT *
FROM some_table
JOIN another_table
  ON ST_Intersects(some_table.geom, another_table.geom);
```

Let's try to do something more advanced. We're going to analyze the [NYC _Citi Bike Trip_ dataset](https://citibikenyc.com/system-data), which contains around 58 million rows representing rental bike trips in New York City, including the start and end locations of each trip. We want to find neighborhoods in NYC that have the most bike trips starting in them. Therefore, we join the bike trip data with a [dataset of NYC neighborhood polygons](https://www.nyc.gov/content/planning/pages/resources/datasets/neighborhood-tabulation). We then count and group the number of trips starting in each neighborhood, and finally sort and limit the results to return the top-3 neighborhoods in which most trips originate. We've compiled the datasets and extracted the relevant columns for this example into two tables, `rides` and `hoods`, into a [218 MB DuckDB database file](https://blobs.duckdb.org/data/biketrips.duckdb).

Let's make sure the `spatial` extension is installed and loaded:

```sql
INSTALL spatial; -- Install the spatial extension
LOAD spatial;    -- Load the spatial extension
```

Our query looks like this:

```sql
SELECT neighborhood, count(*) AS num_rides
FROM rides
JOIN hoods ON ST_Intersects(rides.start_geom, hoods.geom)
GROUP BY neighborhood
ORDER BY num_rides DESC
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

This query joins the 58,033,724 rides with the 310 neighborhood polygons and takes about **30 seconds** to run on my laptop (MacBook with an M3 Pro CPU and 36 GB RAM).

While 30 seconds might not seem that impressive at first glance (a `HASH_JOIN` over similarly sized input would finish an order of magnitude faster), I'm actually pleased DuckDB is able to execute a spatial join at this scale in a time frame that is, if not great, still acceptable for exploratory analysis (on a laptop no less!). To understand the difference in execution time, compared to, e.g., a `HASH_JOIN`, we first need to take a closer look at how DuckDB used to do spatial joins and why spatial joins are so challenging to optimize. Then, we'll dive into how the new `SPATIAL_JOIN` operator changes the game.

## How DuckDB (Used to) Do Spatial Joins

### Spatial Predicates

The first thing to understand is that a _spatial predicate_ is really just a function that evaluates some spatial relation between two geometries and returns `true` or `false`, e.g., “does `a` _contain_ `b`” or “is `a` _within distance_ `x` of `b`”. In theory you could write your own spatial predicate function, but in practice, you will probably use one of the many that come with the `spatial` extension. The nuances of the different spatial predicates are beyond the scope of this post, but here is a quick overview of the most commonly used ones, taking two geometries `a` and `b`:

| Function                                               | Description                                                  |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| `ST_Intersects(a, b)`{:.language-sql .highlight}       | Whether `a` intersects `b`                                   |
| `ST_Contains(a, b)`{:.language-sql .highlight}         | Whether `a` contains `b`                                     |
| `ST_ContainsProperly(a, b)`{:.language-sql .highlight} | Whether `a` contains `b` without `b` touching `a`'s boundary |
| `ST_Within(a, b)`{:.language-sql .highlight}           | Whether `a` is within `b`                                    |
| `ST_Overlaps(a, b)`{:.language-sql .highlight}         | Whether `a` overlaps `b`                                     |
| `ST_Touches(a, b)`{:.language-sql .highlight}          | Whether `a` touches `b`                                      |
| `ST_Equals(a, b)`{:.language-sql .highlight}           | Whether `a` is equal to `b`                                  |
| `ST_Crosses(a, b)`{:.language-sql .highlight}          | Whether `a` crosses `b`                                      |
| `ST_Covers(a, b)`{:.language-sql .highlight}           | Whether `a` covers `b`                                       |
| `ST_CoveredBy(a, b)`{:.language-sql .highlight}        | Whether `a` is covered by `b`                                |
| `ST_DWithin(a, b, x)`{:.language-sql .highlight}       | Whether `a` is within distance `x` of `b`                    |

> We use `ST_Intersects` in the example query above to keep it simple, even if `ST_Contains` or `ST_ContainsProperly` might be more appropriate for point-in-polygon joins.

Since all the above spatial predicates live in the `spatial` extension, DuckDB's query planner doesn't really know anything about them, except their names and that they are functions that take two `GEOMETRY` arguments and return a boolean value. This means that vanilla DuckDB on its own can't apply any special optimizations to them, and has to treat them like **any other function** in the database.

### Optimization Challenges

When DuckDB plans a join where the join condition is an arbitrary function, it normally can't use any of the advanced built-in join strategies like `HASH_JOIN` or `RANGE_JOIN` which are optimized for equality or range comparisons. Instead DuckDB has to fall back to the simplest join strategy, which is to perform a **nested loop join** (NLJ), i.e., to evaluate the join condition for every possible pair of rows in the two tables. In pseudo-code, a nested loop join would look something like this:

```python
for row_a in table_a:
    for row_b in table_b:
        if join_condition(row_a, row_b):
            emit(row_a, row_b)
```

This is the most general way to implement a join, but it is also the least efficient. Since the _complexity_ of the join is `O(nm)`, where `n` and `m` are the number of rows in the two tables, the time it takes to perform the join grows quadratically with the size of the input.

### Complexity Challenges

Obviously, quadratic complexity quickly becomes infeasible for large joins, but DuckDB's raw execution power usually makes it bearable when joining small- to medium-sized tables.

However, what makes the nested loop join strategy impractical for spatial joins in particular, even at small- to medium-scale is that spatial predicates can be _very_ computationally expensive to evaluate in the first place. This is mostly due to the sheer complexity of the algorithms involved, but also due to the denormalized nature of geometries, in which a single geometry can contain a very large number of points. Also, besides the inherent theoretical complexity, the reality in `spatial` is that most of the spatial predicates implemented with the help of third-party libraries require a deserialization step to convert the internal binary format of the `GEOMETRY` column to an executable data structure. This usually also requires allocating memory outside of DuckDB's own memory management system, which increases pressure and lock contention on the global memory allocator, limiting the effectiveness of additional parallelism.

To illustrate how this plays out in practice, let's take a look at the query plan for the example query above, but with the `SPATIAL_JOIN` optimization disabled to force DuckDB to use a nested loop join instead:

### Experiment

```sql
LOAD spatial; -- Load the spatial extension

-- Disable the spatial join optimizer
SET disabled_optimizers = 'extension';

-- Print the new plan, using EXPLAIN to verify
-- that we are using a nested loop join
EXPLAIN SELECT neighborhood, count(*) AS num_rides
FROM rides
JOIN hoods ON ST_Intersects(rides.start_geom, hoods.geom)
GROUP BY neighborhood
ORDER BY num_rides DESC
LIMIT 3;
```

<details markdown='1'>
<summary markdown='span'>
Result of EXPLAIN
</summary>

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

</details>

Executing this query, with the `BLOCKWISE_NL_JOIN` (blockwise nested loop join), now takes **30 minutes** on my laptop. I've also run the query with a subset of number of rows in the `rides` table to see how the performance scales with the size of the input. The results are as follows:

| Number of rows in `rides` | Execution time (s) | Execution time (min) |
| ------------------------: | -----------------: | -------------------: |
|                 1,000,000 |             30.8 s |              0.5 min |
|                10,000,000 |            310.3 s |              5.2 min |
|                58,033,724 |           1799.6 s |             30.0 min |

This is obviously not great. Running a 1/58th of the full dataset already takes longer than the original query with the spatial join optimization enabled. And processing the full dataset takes almost half an hour to run! This is a clear indication that the nested loop join strategy is not suitable for spatial joins at scale, and we really needed to do something about it.

### The IE-Join Optimization

In order to improve the situation, one of the first optimizations implemented in the early versions of the `spatial` extension was a re-write rule for the query planner.

Since evaluating the spatial predicate function itself is so expensive, its a good idea to try to do some *cheap* filtering of potential join matches first in order to reduce the number of pairs that actually need to go through the precise spatial relationship check. Luckily for us, it is relatively easy to do this for most spatial predicates since they all have a common property. Almost all spatial predicates _imply_ _intersection_ in some way, and **if two geometries intersect, their bounding boxes must also intersect**.

The *bounding box*, sometimes called *minimum bounding rectangle* (MBR) of a geometry is the smallest rectangle that fully contains the geometry. Because bounding boxes basically represent the minimum and maximum x and y coordinates of all vertices in the geometry, they are relatively efficient to compute by just scanning over the geometry a single pass. Additionally, checking if two bounding boxes intersect is also very cheap, as it can be done in constant time with a few simple less-than and greater-than comparisons.

Since bounding box intersection can be expressed as a series of inequality checks, we can make use of DuckDB's existing **inequality join** functionality to perform a bounding-box join! Explaining the inner workings of inequality joins is beyond the scope of this post because Richard have already done a great job of that in his [blog post on range joins]({% post_url 2022-05-27-iejoin %}#inequality-join-iejoin), but the gist is that it is a join type that can efficiently join two tables using a series of inequality operators like `<`, `>`, `<=`, `>=`, etc.

To leverage this, we made the following changes to `spatial`:

* Cache an approximate bounding box for each geometry in the serialized binary representation of the `GEOMETRY` column so that we don't have to recompute it every time we need to evaluate a spatial predicate.
* Introduce a re-write rule to change any inner nested loop join operators with a spatial predicate into two new operators:
    * `PIECEWISE_MERGE_JOIN`, a “IE” (inequality) range-join operator joining on the intersection of the bounding boxes, written as a series of `BETWEEN` clauses on the min/max values of the bounding boxes
    * `FILTER` operator that filters the resulting rows on the actual spatial predicate function.

To show how this affects the query plan, we're going to go [back in time]({% link release_calendar.md %}#past-releases) and use DuckDB **v1.2.0** (which does contain the `PIECEWISE_MERGE_JOIN` optimization, but **not** the `SPATIAL_JOIN` operator) to re-run the query from above.

```sql
LOAD spatial; -- Load the spatial extension

-- Check that we are using DuckDB v1.2.0
PRAGMA version;
```

```text
┌─────────────────┬────────────┐
│ library_version │ source_id  │
│     varchar     │  varchar   │
├─────────────────┼────────────┤
│ v1.2.0          │ 5f5512b827 │
└─────────────────┴────────────┘
```

```sql
-- Print the new query plan, using EXPLAIN
EXPLAIN SELECT neighborhood, count(*) AS num_rides
FROM rides
JOIN hoods ON ST_Intersects(rides.start_geom, hoods.geom)
GROUP BY neighborhood
ORDER BY num_rides DESC
LIMIT 3;
```


<details markdown='1'>
<summary markdown='span'>
Result of EXPLAIN
</summary>

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

</details>

As you can see, the `PIECEWISE_MERGE_JOIN` operator has replaced the `BLOCKWISE_NL_JOIN` operator, and the join condition has been rewritten to use the approximate bounding boxes of the geometries (`ST_Extent_Approx`) instead of directly joining on the spatial predicate. The `FILTER` operator is added on top to only apply the spatial predicate functions on the rows that pass the initial bounding box check.

This looks a lot more complicated than the original nested loop join, so how does it perform?

| Number of rows in `rides` | Execution time |
| ------------------------: | -------------: |
|                 1,000,000 |          2.3 s |
|                10,000,000 |         19.6 s |
|                58,033,724 |        107.6 s |

Much better, we managed to reduce the execution time from 30 minutes to **just under 2 minutes** for the full dataset! This was a huge improvement. Without requiring any custom operator code, we were able to leverage DuckDB's existing inequality join functionality to significantly speed up spatial joins as well.

However, this approach still has some drawbacks:

* This re-write is only possible to do for `INNER` joins.
* We now have to store bounding boxes for each geometry, which increases the memory footprint of the `GEOMETRY` column, and we also have to recompute it whenever create or modify a `GEOMETRY`.
* The `PIECEWISE_MERGE_JOIN` operator has to sort the two input tables, which requires a lot of memory and can be really slow for large tables once the data no longer fits in memory.

DuckDB has since optimized sorting considerably, and `spatial` and its functions have also received various optimizations that improve performance slightly. Nonetheless this was always somewhat of a stop-gap solution to make spatial joins at least usable in the common case. How can we do better?

## The Spatial Join Operator

### R-Tree Indexing

To quickly recap how an [r-tree](https://en.wikipedia.org/wiki/R-tree) works, it is a balanced tree data structure where internal nodes contain bounding boxes that cover the bounding boxes of their child nodes, and leaf nodes contain a bounding box for the geometry and a pointer to the row in the table they correspond to. This makes it possible to quickly look up all geometries that intersect a given bounding box by traversing the tree from the top down, only following branches that intersect the search box.

One of the motivations for implementing the [`RTREE` index]({% link docs/stable/core_extensions/spatial/r-tree_indexes.md %}) in the `spatial` extension last year, was to eventually be able to replace `PIECEWISE_MERGE_JOIN` optimization with an index-based join strategy. However, after implementing the `RTREE`, we realized that creating an R-tree based index on top of existing data is actually surprisingly fast. Instead of requiring the user to always have to load data into a table and then index it just to accelerate their spatial joins, what if we just create a temporary R-tree index on-the-fly when executing the join? Kind of like how we create a temporary hash table when performing a `HASH_JOIN`.

### Joining with R-Trees

This is exactly what the new `SPATIAL_JOIN` operator does. It takes two input tables, buffers all the input of the “right” table (i.e., table that the join-order-optimizer expects to be smaller), builds an R-tree index on top of the collected input, and then performs a join by looking up each row of the “left” table in the R-tree index as they arrive. The idea is exactly the same as with a `HASH_JOIN`, but instead of using a hash table, we use an R-tree as our acceleration data structure to look up the matching rows.

While being a lot more complex to implement compared to the `PIECEWISE_MERGE_JOIN`-based approach, this has several advantages:

* The query re-write rule is much simpler, we just have to detect a nested loop join with a spatial predicate and replace it with a `SPATIAL_JOIN` operator. No other modifications to the query plan are needed.
* Only the smaller side input needs to be materialized and (sorted to construct the R-tree). The left side can be streamed in parallel, and matching rows can be emitted immediately as they are found.
* The hierarchical structure of the R-tree allows us to prune more of the right side input more accurately
* Since all logic is in one operator, we don't need to rely on a separate `FILTER` operator and can therefore support `LEFT`, `RIGHT` and `FULL OUTER` joins as well as `INNER` joins.

### Experiment

Just to show what this plan looks like, this is what you get when you run the same query but on DuckDB v1.3.0 or later with the `SPATIAL_JOIN` operator enabled:

```sql
LOAD spatial; -- Load the spatial extension

-- Print the new query plan, using EXPLAIN
EXPLAIN SELECT neighborhood, count(*) AS num_rides
FROM rides
JOIN hoods ON ST_Intersects(rides.start_geom, hoods.geom)
GROUP BY neighborhood
ORDER BY num_rides DESC
LIMIT 3;
```


<details markdown='1'>
<summary markdown='span'>
Result of EXPLAIN
</summary>

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

</details>

Nice, we're back to a single join condition again. So how does this perform? We already saw in the first example that DuckDB v1.3.2 was able to execute the original query in about 30 seconds using the `SPATIAL_JOIN` operator, but here are the precise results for all the different sizes and join strategies for comparison. All queries were run on the same Apple MacBook M3 Pro with 36 GB of memory and timings averaged over 3 runs:

| Number of rows in `rides` | Nested loop join | Piecewise merge join | Spatial join |
| ------------------------: | ---------------: | -------------------: | -----------: |
|                 1,000,000 |           30.8 s |                2.3 s |        0.5 s |
|                10,000,000 |          310.3 s |              19.6s s |        4.8 s |
|                58,033,724 |         1799.6 s |              107.6 s |       28.7 s |

The `SPATIAL_JOIN` operator is able to execute the full 58 million row dataset faster than the original naive nested loop join could execute the 1 million row dataset. That's a 58× improvement!

## Limitations and Future work

Even though we've made a lot of improvements, spatial joins in DuckDB are not quite perfect just yet. Like always, there's plenty more to do, and we have a few ideas for how to improve the `SPATIAL_JOIN` operator even further.

### Larger-Than-Memory Build Sides

The current implementation of the `SPATIAL_JOIN` operator buffers the entire right side input in memory to build the R-tree index. This means that it can only handle right side inputs that fit in memory. We plan to add support for larger-than-memory R-trees by partitioning the right side into smaller separate R-trees, and then merging the results of the join from each partition, similar to how the `HASH_JOIN` operator handles larger-than-memory hash tables.

### Increased Parallelism

DuckDB's execution engine dynamically adjusts the number of threads used in a query based on the number of rows scanned, but since the spatial predicates are so expensive to evaluate, we could potentially benefit from more parallelism as the spatial joins are mostly CPU bound. In particular, we are considering buffering and partitioning the left side of the join as well, which would allow us to spawn our own worker tasks within the operator to evaluate the join condition across a number of threads decoupled from the cardinality of the input. This would increase memory usage and prevent the join from being streamed, but we've been able to employ a similar technique when constructing the [`HNSW` (Hierarchical Navigable Small Worlds) index over in the `vss` extension]({% link docs/stable/core_extensions/vss.md %}) to great effect.

### Faster Predicate Functions

Most predicate functions in the `spatial` extension are implemented using third-party libraries which carry some overhead as we are unable to integrate them as tightly with DuckDB's execution engine and memory management, often requiring some sort of deserialization or conversion step. This can be quite expensive, especially for large geometries. To demonstrate impact of this in practice, we can compare the performance of joining on `ST_Intersects(x, y)` with the somewhat equivalent `ST_DWithin(x, y, 0)`, by comparing the previous results with the timings of the following query:

```sql
SELECT neighborhood, count(*) AS num_rides
FROM rides
JOIN hoods ON ST_DWithin(rides.start_geom, hoods.geom, 0)
GROUP BY neighborhood
ORDER BY num_rides DESC
LIMIT 3;
```

| Number of rows in `rides` | Spatial join (`Intersects`) | Spatial join (`DWithin`) |
| ------------------------: | --------------------------: | -----------------------: |
|                 1,000,000 |                       0.5 s |                    0.1 s |
|                10,000,000 |                       4.8 s |                    0.7 s |
|                58,033,724 |                      28.7 s |                    4.3 s |

Now, `ST_DWithin` is not the strictly the same as `ST_Intersects`, so this is not an apples-to-apples comparison. Even if they produce the same output in this example, you should not rush to replace all instances of `ST_Intersects` with `ST_DWithin` in your code just to squeeze out some extra performance. In fact, `ST_DWithin` is technically doing _more_ work as the algorithm is more complex. The reason why it is still faster in this case, and the reason why we're bringing it up, is because its implementation in the `spatial` extension was recently changed to our own highly optimized native implementation. This implementation goes the extra mile in avoiding memory allocation and copying, and the results speak for themselves. This goes to show how optimizing the spatial predicate functions themselves can significantly improve the performance of spatial joins. We are actively working on adding optimized versions of the rest of the commonly used spatial predicates (like `ST_Intersects`, `ST_Contains`, `ST_Within`, etc.) to the `spatial` extension and expect to see similar performance improvements across the board. So stick with `ST_Intersects` when appropriate, and look forward to more performance gains in the future!

### Advanced Join Conditions

The `SPATIAL_JOIN` operator currently only supports the case where the join condition is a single spatial predicate function. We plan to add support for more complex join conditions that can include comparisons, arithmetic operations, and other functions in combination with the spatial predicates. This will allow users to express more complex spatial relationships in their joins, e.g., `JOIN ... ON ST_Intersects(a.geom, b.geom) AND a.id = b.id`{:.language-sql .highlight}.

### `ANTI` / `SEMI` Joins

The `SPATIAL_JOIN` operator currently only supports `INNER`, `LEFT`, `RIGHT` and `FULL OUTER` joins. We plan to add support for `ANTI` and `SEMI` joins in the future.

## Conclusion

Spatial joins are a powerful way to connect and enrich datasets based on their geospatial relationship. DuckDB's `spatial` extension provides a wide assortment of spatial predicate functions that can be used to perform spatial joins in SQL. While the performance of spatial joins has been challenging to deal with in the past due to the complexity of the spatial predicates and the limitations of the join strategies, the new `SPATIAL_JOIN` operator introduced in DuckDB v1.3.0 significantly raises the efficiency and scalability of these workloads, making spatial joins a first-class citizen in DuckDB's execution engine.

