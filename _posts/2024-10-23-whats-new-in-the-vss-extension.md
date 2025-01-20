---
layout: post
title: "What's New in the Vector Similarity Search Extension?"
author: "Max Gabrielsson"
thumb: "/images/blog/thumbs/vss.svg"
image: "/images/blog/thumbs/vss.png"
excerpt: "DuckDB is another step closer to becoming a vector database! In this post, we show the new performance optimizations implemented in the vector search extension."
tags: ["extensions"]
---

In the [previous blog post]({% post_url 2024-05-03-vector-similarity-search-vss %}), we introduced the DuckDB [Vector Similarity Search (VSS) extension]({% link docs/extensions/vss.md %}). While the extension is still quite experimental, we figured it would be interesting to dive into the details of some of the new features and improvements that we've been working on since the initial release.

## Indexing Speed Improvements

As previously documented, creating an HNSW (Hierarchical Navigable Small Worlds) index over an already populated table is much more efficient than first creating the index and then inserting into the table. This is because it is much easier to predict how large the index will be if the total amount of rows are known up-front, which makes its possible to divide the work into chunks large enough to distribute over multiple threads. However, in the initial release this work distribution was a bit too coarse-grained as we would only schedule an additional worker thread for each [_row-group_]({% link docs/internals/storage.md %}#row-groups) (about 120,000 rows by default) in the table.

We've now introduced an extra buffer step in the index creation pipeline which enables more fine-grained work distribution, smarter memory allocation and less contention between worker threads. This results in much higher CPU saturation and a significant speedup when building HNSW indexes in environments with many threads available, regardless of how big or small the underlying table is.

Another bonus of this change is that we can now emit a progress bar when building the index, which is a nice touch when you still need to wait a while for the index creation to finish (despite the now much better use of system resources!).

## New Distance Functions

In the initial release of VSS we supported three different distance functions:
[`array_distance`]({% link docs/sql/functions/array.md %}#array_distancearray1-array2),
[`array_cosine_similarity`]({% link docs/sql/functions/array.md %}#array_cosine_similarityarray1-array2) and
[`array_inner_product`]({% link docs/sql/functions/array.md %}#array_inner_productarray1-array2). However, only the `array_distance` function is actually a _distance_ function in that it returns results closer to 0 when the vectors are similar, and close to 1 when they are dissimilar, in contrast to, e.g., `array_cosine_similarity` that returns 1 when the vectors are identical. Oops!

To remedy this we've introduced two new distances:

* `array_cosine_distance`, equivalent to `1 - array_cosine_simililarity`
* `array_negative_inner_product`equivalent to `-array_inner_product`

These will now be accelerated with the use of the HNSW index instead, making the query patterns and ordering consistent for all supported metrics regardless if you make use of the HNSW index or not. Additionally, if you have an HNSW using, e.g., the `cosine` metric and write a top-k style query using `1 - array_cosine_similarity` as the ranking criterium, the optimizer should be able to normalize the expression to `array_cosine_distance` and use the index for this function as well.

For completeness we've also added the equivalent distance functions for the dynamically-sized [`LIST` datatype]({% link docs/sql/data_types/list.md %}) (prefixed with `list_` instead of `array_`) and changed the `<=>` binary operator to now be an alias of `array_cosine_distance`, matching the semantics of the [`pgvector` extension](https://github.com/pgvector/pgvector) for PostgreSQL.

## Index Accelerated "Top-K" Aggregates

Another cool thing that's happened in core DuckDB since last time is that DuckDB now has extra overloads for the [`min_by`]({% link docs/sql/functions/aggregates.md %}#min_byarg-val-n) and [`max_by`]({% link docs/sql/functions/aggregates.md %}#max_byarg-val-n) aggregate functions (and their aliases `arg_min` and `arg_max`)
These new overloads take an optional third `n` argument that specifies the number of top-k (or top-`n`) elements to keep and outputs them into a sorted `LIST` value. Here's an example:

```sql
-- Create a table with some example data
CREATE OR REPLACE TABLE vecs AS 
    SELECT
        row_number() OVER () AS id, 
        [a, b, c]::FLOAT[3] AS vec 
    FROM
        range(1,4) AS x(a), range(1,4) AS y(b), range(1,4) AS z(c);

-- Find the top 3 rows with the vector closest to [2, 2, 2]
SELECT
    arg_min(vecs, array_distance(vec, [2, 2, 2]::FLOAT[3]), 3)
FROM
    vecs;
```

```text
[{'id': 14, 'vec': [2.0, 2.0, 2.0]}, {'id': 13, 'vec': [2.0, 1.0, 2.0]}, {'id': 11, 'vec': [1.0, 2.0, 2.0]}]
```

Of course, the VSS extension now includes optimizer rules to use to the HNSW index to accelerate these top-k aggregates when the ordering input is a distance function that references an indexed vector column, similarly to the `SELECT a FROM b ORDER BY array_distance(a.vec, query_vec) LIMIT k` query pattern that we discussed in the previous blog post. These new overloads allow you to express the same query in a more concise and readable way, while still avoiding the need for a full scan and sort of the underlying table (as long as the table has a matching HNSW index).

## Index Accelerated `LATERAL` Joins

After running some benchmarking on the initial version of VSS, we realized that even though index-lookups on our HNSW index is really fast (thanks to the [USearch](https://github.com/unum-cloud/usearch) library that it is based on!), using DuckDB to search for individual vectors at a time has a lot of latency compared to other solutions. The reasons for this are many and nuanced, but we want to be clear that our choice of HNSW implementation, USearch, is not the bottleneck here as profiling revelead only about 2% of the runtime is actually spent inside of usearch.

Instead, most of the per-query overhead comes from the fact that DuckDB is just not optimized for _point queries,_ i.e., queries that only really fetch and process a single row. Because DuckDB is based on a vectorized execution engine, the smallest unit of work is not 1 row but 2,048, and because we expect to crunch through a ton of data, we generally favor spending a lot of time up front to optimize the query plan and pre-allocate large buffers and caches so that everything is as efficient as possible once we start executing. But a lot of this work becomes unneccessary when the actual working set is so small. For example, is it really worthwile to inspect and hash every single element of a constant 768-long query vector to attempt to look for common subexpressions if you know there is only going to be a handful of rows in the result?

While we have some ideas on how to improve this scenario in the future, we decided to take another approach for now and instead try focus not on our weaknesses, but on our strengths. That is, crunching through a ton of data! So instead of trying to optimize the “1:N”, i.e., “given this one embedding, give me the closes N embeddings” query, what if we instead focused on the “N:M”, “given all these N embeddings, pair them up with the closest M embeddings each”. What would that look like? Well, that would be a [`LATERAL` join]({% link docs/sql/query_syntax/from.md %}#lateral-joins) of course!

Basically, we are now able to make use of HNSW indexes to accelerate `LATERAL` joins where the “inner” query looks just like the top-k style queries we normally target, for example:

```sql
SELECT a
FROM b
ORDER BY array_distance(a.vec, query_vec)
LIMIT k;
```

But where the `query_vec` array is now a reference to an “outer” join table. The only requirement is for the inner table to have an HNSW index on the vector column matching the distance function. Here's an example:

```sql
-- Set the random seed for reproducibility
SELECT setseed(0.42);

-- Create some example tables
CREATE TABLE queries AS
    SELECT
        i AS id,
        [random(), random(), random()]::FLOAT[3] AS embedding 
    FROM generate_series(1, 10_000) r(i);

CREATE TABLE items AS
    SELECT
        i AS id,
        [random(), random(), random()]::FLOAT[3] AS embedding
FROM generate_series(1, 10_000) r(i);

-- Collect the 5 closest items to each query embedding
SELECT queries.id AS id, list(inner_id) AS matches 
    FROM queries, LATERAL (
        SELECT
            items.id AS inner_id,
            array_distance(queries.embedding, items.embedding) AS dist
        FROM items 
        ORDER BY dist 
        LIMIT 5
    )
GROUP BY queries.id;
```

Executing this on my Apple M3 Pro-equipped MacBook with 36 GB memory takes about 10 seconds.

If we `EXPLAIN` this query plan, we'll see a lot of advanced operators:

```sql
PRAGMA explain_output = 'optimized_only';
EXPLAIN ...
```

<details markdown='1'>
<summary markdown='span'>
Vanilla query plan (operators and expected cardinalities)
</summary>

```text
┌───────────────────────────┐
│         PROJECTION        │
│    ────────────────────   │
│       ~5000000 Rows       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│       ~5000000 Rows       │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│       ~10000000 Rows      │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│       ~10000000 Rows      │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      RIGHT_DELIM_JOIN     │
│    ────────────────────   │
│       ~10000000 Rows      ├──────────────┐
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││         HASH_JOIN         │
│    ────────────────────   ││    ────────────────────   │
│        ~10000 Rows        ││       ~10000000 Rows      ├──────────────┐
└───────────────────────────┘└─────────────┬─────────────┘              │
                             ┌─────────────┴─────────────┐┌─────────────┴─────────────┐
                             │         PROJECTION        ││         DUMMY_SCAN        │
                             │    ────────────────────   ││                           │
                             │       ~10000000 Rows      ││                           │
                             └─────────────┬─────────────┘└───────────────────────────┘
                             ┌─────────────┴─────────────┐
                             │           FILTER          │
                             │    ────────────────────   │
                             │       ~10000000 Rows      │
                             └─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │         PROJECTION        │
                             │    ────────────────────   │
                             │       ~50000000 Rows      │
                             └─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │           WINDOW          │
                             └─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │         PROJECTION        │
                             │    ────────────────────   │
                             │       ~50000000 Rows      │
                             └─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │       CROSS_PRODUCT       ├──────────────┐
                             └─────────────┬─────────────┘              │
                             ┌─────────────┴─────────────┐┌─────────────┴─────────────┐
                             │         SEQ_SCAN          ││         DELIM_SCAN        │
                             │    ────────────────────   ││    ────────────────────   │
                             │        ~10000 Rows        ││         ~5000 Rows        │
                             └───────────────────────────┘└───────────────────────────┘
```
</details>

While this plan looks very complicated, the most worrysome among these operators is the `CROSS_PRODUCT` towards the bottom of the plan, which blows up the expected cardinality and is a sign that we are doing a lot of work that we probably don't want to do. However, if we create an HNSW index on the `items` table using

```sql
CREATE INDEX my_hnsw_idx ON items USING HNSW(embedding);
```

and re-run `EXPLAIN`, we get this plan instead:

<details markdown='1'>
<summary markdown='span'>
Query plan with HNSW index (operators and expected cardinalities)
</summary>

```text
┌───────────────────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        ~50000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│       HASH_GROUP_BY       │
│    ────────────────────   │
│        ~50000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        ~50000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        ~50000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│    ────────────────────   │
│        ~50000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│      HNSW_INDEX_JOIN      │
│    ────────────────────   │
│        ~50000 Rows        │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         SEQ_SCAN          │
│    ────────────────────   │
│        ~10000 Rows        │
└───────────────────────────┘
```
</details>

We can see that this plan is drastically simplified, but most importantly, the new `HNSW_INDEX_JOIN` operator replaces the `CROSS_PRODUCT` node that was there before and the estimated cardinality went from 5,000,000 to 50,000! Executing this query now takes about 0.15 seconds. That's an almost 66× speedup!

This optimization was just recently added to the VSS extension, so if you've already installed `vss` for DuckDB v1.1.2, run the following command to get the latest version:

```sql
UPDATE EXTENSIONS (vss);
```

## Conclusion

That's all for this time folks! We hope you've enjoyed this update on the DuckDB Vector Similarity Search extension. While this update has focused a lot on new features and improvements such as faster indexing, additional distance functions and more optimizer rules, we're still working on improving some of the limitations mentioned in the previous blog post. We hope to have more to share related to custom indexes and index-based optimizations soon! If you have any questions or feedback, feel free to reach out to us on the [`duckdb-vss` GitHub repository](https://github.com/duckdb/duckdb-vss) or on the [DuckDB Discord](https://discord.duckdb.org/). Hope to see you around!
