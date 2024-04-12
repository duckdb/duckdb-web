---
layout: post
title: "Vector Similarity Search in DuckDB"
author: Max Gabrielsson
excerpt: "DuckDB now supports creation of HNSW indexes to accelerate vector similarity search through the new \"vss\" extension."
---

In DuckDB v0.10.0 we introduced the "fixed size list" [`ARRAY` data type]({% link docs/sql/data_types/array.md %}) to complement the existing variable size [`LIST` data type]({% link docs/sql/data_types/list.md %}) in DuckDB. 

The initial motivation for adding this data type was to provide optimized operations for lists that can utilize the positional semantics of their child elements and avoid branching as all lists have the same length. Think e.g. the sort of array manipulations you'd do in NumPy: stacking, shifting, multiplying - you name it. Additionally, we wanted to improve our interoperability with Apache Arrow, as previously arrow fixed size lists would be converted to regular lists when ingested into DuckDB, losing some type information. 

However, as the hype for __vector embeddings__ and __semantic similarity search__ were growing, we also snuck in a couple of distance metric functions for this new `ARRAY` type: `array_distance`, `array_inner_product` and `array_cosine_distance`. 

This got the community really excited! While we initially went on record saying that we (DuckDB Labs) would not be adding a vector similarity search index to DuckDB as we deemed it to be too far out of scope, we were very interested in supporting custom indexes through extensions in general. Shoot, I've been _personally_ nagging on about wanting to plug-in a spatial index since the inception of DuckDBs [spatial extension]({% link docs/extensions/spatial.md %})! So when one of our client projects evolved into creating a proof-of-concept custom HNSW index extension we said that we would give it a shot. And... well, one thing led to another.

Fast forward to now and we're happy to announce the availability of the `vss` vector similarity search extension for DuckDB! While some may say we're late to the vector search party, we'd like to think DuckDB `vss` emerges right on time alongside the [plateu of productivity](https://en.wikipedia.org/wiki/Gartner_hype_cycle).

Alright, so what's in `vss`?

## The Vector Similarity Search (VSS) Extension

On the surface, `vss` seems like a comparatively small DuckDB extension. It does not provide any new data types, scalar functions or copy functions, but rather a single new index type: `HNSW`. 

```sql
-- Create a table with a fixed-size list column
CREATE TABLE embeddings (vec FLOAT[3]);

-- Create an HNSW index on the column
CREATE INDEX idx ON embeddings USING HNSW (vec);
```

This index type can't be used to enforce constraints or uniqueness like the built-in `ART` index, and can't be used to speed up joins or index regular columns either. Instead, the `HNSW` index is only applicable to columns of the fixed-size list type and will only be used to accelerate queries calculating the "distance" between a constant array and the arrays in the indexed column, ordered by the resulting distance and returning the top-n results. That is, queries on the form:

```sql
SELECT * 
FROM embeddings
ORDER BY array_distance(vec, [1,2,3]::FLOAT[3]) 
LIMIT 5;
```

...will have their logical plan optimized to instead become a projection over a new `HNSW` index scan operator, removing the limit and sort altogether. We can verify this by checking the `EXPLAIN` output!

```sql
EXPLAIN SELECT * FROM embeddings ORDER BY array_distance(vec, [1,2,3]::FLOAT[3]) LIMIT 3;

┌───────────────────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             #0            │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            vec            │
│array_distance(vec, [1.0, 2│
│         .0, 3.0])         │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│      HNSW_INDEX_SCAN      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│   t1 (HNSW INDEX SCAN :   │
│           my_idx)         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            vec            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 3           │
└───────────────────────────┘   
```

You can pass the `HNSW` index creation statement a `metric` parameter to decide what kind of distance metric to use. The supported metrics are `l2sq`, `cosine` and `inner_product`, matching the three built in distance functions: `array_distance`, `array_cosine_distance` and `array_inner_product`.
 The default is `l2sq` (`array_distance`)..

```sql
-- Create an HNSW index on the column using euclidean distance
CREATE INDEX l2sq_idx ON embeddings USING HNSW (vec) WITH (metric = 'l2sq');

-- Create an HNSW index on the column using cosine distance
CREATE INDEX cos_idx ON embeddings USING HNSW (vec) WITH (metric = 'cosine');

-- Create an HNSW index on the column using inner product
CREATE INDEX ip_idx ON embeddings USING HNSW (vec) WITH (metric = 'ip');
```

It is important to know that the `HNSW` index is a _approximate_ index, meaning that the results returned by the index may not be the _exact_ top-n results, but rather a set of results that are _close_ to the top-n results. The `HNSW` in `HNSW` index stands for Hierarchical Navigable Small World, which is a graph-based index structure that is particularly well suited for high-dimensional vector similarity search. 


While the `HNSW` index supports deletes and insertions to the base table after the index has been created, deletes are not immediately reflected internally in the index structure, but are instead marked as deleted, and will only be removed after a certain number of updates have been made. This is a trade-off to maintain the performance of updates, but will lead to the _quality_ of the index deteriorating over time, impacting both speed and accuracy of retrieval. To remedy this you can use the pragma `pragma_hnsw_compact_index('<index name>')` to trigger a recompaction, which will be faster than dropping and recreating the index. 

Additionally, it is generally recommended to create the index __after__ loading a table with data as the initial index creation step can utilize some degree of parallelism to speed up index creation on larger tables.


Like the `ART` the `HNSW` index must be able to fit into RAM in its entirety, but will also be persisted to disk as part of the DuckDB database file (if running DuckDB in disk-backed mode) during checkpointing. After restarting or loading a database file with a persisted `HNSW` index, the index will only be lazily loaded back into memory whenever the table the index is created on is first accessed.

## Future Work

The main limitations of the `HNSW` index so far is that it only supports the `FLOAT` type for the fixed-size list elements and only distance metrics corresponding to the three built in distance functions, `array_distance`, `array_inner_product` and `array_cosine_distance`. Additionally the memory allocated by the `HNSW` at runtime is allocated "outside" of the DuckDB memory management system, meaning that it wont respect DuckDB's  `memory_limit` configuration parameter.

However, we still think that the `HNSW` and `vss` extension is a useful addition to the DuckDB extension ecosystem and we're excited to see what the community will do with it. We're also interested in eventually addressing some of the limitations mentioned above and make it even easier to create custom indexes in DuckDB in the future.

## Conclusion

The `vss` extension for DuckDB is a new extension that adds support for creating HNSW indexes on fixed-size list columns in DuckDB, accelerating vector similarity search queries. The extension can currently be installed on the nightly builds of DuckDB by running `INSTALL vss` and will also be available in the upcoming release of DuckDB v0.10.2. The `vss` extension treads new ground for DuckDB extensions by providing a custom index type and we're excited to refine and expand on this functionality going forward. 

Check out the [vss extension documentation]({% link docs/extensions/vss.md %}) for more information as well as the [vss extension GitHub repository](https://github.com/duckdb/duckdb_vss) to keep up with the latest developments.