---
layout: post
title: "Vector Similarity Search in DuckDB"
author: Max Gabrielsson
excerpt: "DuckDB now supports the creation of HNSW indexes to accelerate vector similarity search through the new `vss` extension."
---

In DuckDB v0.10.0, we introduced the "fixed-size list" [`ARRAY` data type](/docs/sql/data_types/array) to complement the existing variable-size [`LIST` data type](/docs/sql/data_types/list).

The initial motivation for adding this data type was to provide optimized operations for lists that can utilize the positional semantics of their child elements and avoid branching as all lists have the same length. Think e.g. the sort of array manipulations you'd do in NumPy: stacking, shifting, multiplying – you name it. Additionally, we wanted to improve our interoperability with Apache Arrow, as previously Arrow's fixed-size list types would be converted to regular variable-size lists when ingested into DuckDB, losing some type information.

However, as the hype for __vector embeddings__ and __semantic similarity search__ was growing, we also snuck in a couple of distance metric functions for this new `ARRAY` type:
`array_distance`
`array_inner_product` and
`array_cosine_distance`.

This got the community really excited! While we (DuckDB Labs) initially went on record saying that we would not be adding a vector similarity search index to DuckDB as we deemed it to be too far out of scope, we were very interested in supporting custom indexes through extensions in general. Shoot, I've been _personally_ nagging on about wanting to plug-in an "R-Tree" index since the inception of DuckDBs [spatial extension](/docs/extensions/spatial)! So when one of our client projects evolved into creating a proof-of-concept custom "HNSW" index extension, we said that we'd give it a shot. And... well, one thing led to another.

Fast forward to now and we're happy to announce the availability of the `vss` vector similarity search extension for DuckDB! While some may say we're late to the vector search party, we'd like to think DuckDB `vss` emerges right on time for the [plateau of productivity](https://en.wikipedia.org/wiki/Gartner_hype_cycle).

Alright, so what's in `vss`?

## The Vector Similarity Search (VSS) Extension

On the surface, `vss` seems like a comparatively small DuckDB extension. It does not provide any new data types, scalar functions or copy functions, but rather a single new index type: `HNSW` ([Hierarchical Navigable Small Worlds](https://en.wikipedia.org/wiki/Hierarchical_Navigable_Small_World_graphs)), which is a graph-based index structure that is particularly well-suited for high-dimensional vector similarity search.


```sql
-- Create a table with an array column
CREATE TABLE embeddings (vec FLOAT[3]);

-- Create an HNSW index on the column
CREATE INDEX idx
ON embeddings
USING HNSW (vec);
```

This index type can't be used to enforce constraints or uniqueness like the built-in [`ART` index](/docs/sql/indexes), and can't be used to speed up joins or index regular columns either. Instead, the `HNSW` index is only applicable to columns of the `ARRAY` type containing `FLOAT` elements and will only be used to accelerate queries calculating the "distance" between a constant `FLOAT` `ARRAY` and the `FLOAT` `ARRAY`'s in the indexed column, ordered by the resulting distance and returning the top-n results. That is, queries of the form:

```sql
SELECT *
FROM embeddings
ORDER BY array_distance(vec, [1,2,3]::FLOAT[3])
LIMIT 3;
```

will have their logical plan optimized to become a projection over a new `HNSW` index scan operator, removing the limit and sort altogether. We can verify this by checking the `EXPLAIN` output:

```sql
EXPLAIN
SELECT *
FROM embeddings
ORDER BY array_distance(vec, [1,2,3]::FLOAT[3])
LIMIT 3;
```

```text
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
│            idx)           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            vec            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 3           │
└───────────────────────────┘
```

You can pass the `HNSW` index creation statement a `metric` parameter to decide what kind of distance metric to use. The supported metrics are `l2sq`, `cosine` and `inner_product`, matching the three built-in distance functions: `array_distance`, `array_cosine_distance` and `array_inner_product`.
The default is `l2sq`, which uses Euclidean distance (`array_distance`):

```sql
CREATE INDEX l2sq_idx
ON embeddings
USING HNSW (vec)
WITH (metric = 'l2sq');
```

To use cosine distance (`array_cosine_distance`):

```sql
CREATE INDEX cos_idx
ON embeddings
USING HNSW (vec)
WITH (metric = 'cosine');
```

To use inner product (`array_inner_product`):

```sql
CREATE INDEX ip_idx
ON embeddings
USING HNSW (vec)
WITH (metric = 'ip');
```

## Implementation

The `vss` extension is based on the [usearch](https://github.com/unum-cloud/usearch) library, which provides a flexible C++ implementation of the HNSW index data structure boasting very impressive performance benchmarks. While we currently only use a subset of all the functionality and tuning options provided by usearch, we're excited to explore how we can leverage more of its features in the future. So far we're mostly happy that it aligns so nicely with DuckDB's development ethos. Much like DuckDB itself, usearch is written in portable C++11 with no external dependencies and released under a permissive license, making it super smooth to integrate into our extension build and distribution pipeline.

## Limitations

### Persistence

The big limitation as of now is that the `HNSW` index can only be created in in-memory databases, unless the `SET hnsw_enable_experimental_persistence = <bool>` configuration parameter is set to `true`. If this parameter is not set, any attempt to create an `HNSW` index in a disk-backed database will result in an error message, but if the parameter is set, the index will not only be created in memory, but also persisted to disk as part of the DuckDB database file during checkpointing. After restarting or loading a database file with a persisted `HNSW` index, the index will be lazily loaded back into memory whenever the associated table is first accessed, which is significantly faster than having to re-create the index from scratch.

The reasoning for locking this feature behind an experimental flag is that we still have some known issues related to persistence of custom indexes that we want to address before enabling it by default. In particular, WAL recovery is not yet properly implemented for custom indexes, meaning that if a crash occurs or the database is shut down unexpectedly while there are uncommited changes to a `HNSW`-indexed table, you can end up with data loss or corruption of the index. While it is technically possible to recover from a unexpected shutdown manually by first starting DuckDB separately, loading the `vss` extension and then `ATTACH`:ing the database file, which ensures that the `HNSW` index functionality is available during WAL-playback, you should not rely on this for production workloads. 

We're actively working on addressing this and other issues related to index persistence, which will hopefully make it into DuckDB v0.10.3, but for now we recommend using the `HNSW` index in in-memory databases only.

### Other Limitations

Like the `ART` the `HNSW` index must be able to fit into RAM in its entirety, and the memory allocated by the `HNSW` at runtime is allocated "outside" of the DuckDB memory management system, meaning that it wont respect DuckDB's `memory_limit` configuration parameter.

Another limitation of the `HNSW` index so far are that it only supports the `FLOAT` (a 32-bit, single-precision floating point) type for the fixed-size list elements and only distance metrics corresponding to the three built in distance functions, `array_distance`, `array_inner_product` and `array_cosine_distance`. 

While the `HNSW` index supports insertions and deletes to the base table after the index has been created, deletes are not immediately reflected internally in the index structure, but are instead only marked as deleted, and will only be removed after a certain number of updates have been made. This is a trade-off to maintain the performance of updates, but will lead to the _quality_ of the index deteriorating over time, impacting both speed and accuracy of retrieval. To remedy this you can use the pragma `PRAGMA hnsw_compact_index('<index name>')` to trigger a recompaction, which will be faster than dropping and recreating the index.

It is important to know that the `HNSW` index is an _approximate_ index, meaning that the results returned by the index may not be the _exact_ top-n results, but rather a set of results that are _close_ to the top-n results. 

Additionally, it is generally recommended to create the index __after__ loading a table with data as the initial index creation step can utilize some degree of parallelism to speed up index creation on larger tables.

## Conclusion

The `vss` extension for DuckDB is a new extension that adds support for creating HNSW indexes on fixed-size list columns in DuckDB, accelerating vector similarity search queries. The extension can currently be installed by running `INSTALL vss`. The `vss` extension treads new ground for DuckDB extensions by providing a custom index type and we're excited to refine and expand on this functionality going forward.

While we're still working on addressing some of the limitations above, particularly those related to persistence, we believe that the `vss` extension and the `HNSW` index in their present form are already useful additions to the DuckDB extension ecosystem. We're really excited to see the opportunities this opens up for the community, so make sure to check out the [`vss` extension documentation](/docs/extensions/vss) for more information on how to install and use the extension. 

This work was made possible by the sponsorship of a DuckDB Labs customer! If you are interested in similar work for specific capabilities, please reach out to DuckDB Labs. Alternatively, we're happy to welcome contributors! Please reach out to the DuckDB Labs team over on Discord or on the [`vss` extension GitHub repository](https://github.com/duckdb/duckdb_vss) to keep up with the latest developments.

