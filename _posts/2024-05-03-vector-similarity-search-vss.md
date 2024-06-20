---
layout: post
title: "Vector Similarity Search in DuckDB"
author: Max Gabrielsson
excerpt: "This blog post shows a preview of DuckDB's new [`vss` extension](/docs/extensions/vss), which introduces support for HNSW (Hierarchical Navigable Small Worlds) indexes to accelerate vector similarity search."
---

In DuckDB v0.10.0, we introduced the [`ARRAY` data type]({% link docs/sql/data_types/array.md %}), which stores fixed-sized lists, to complement the existing variable-size [`LIST` data type]({% link docs/sql/data_types/list.md %}).

The initial motivation for adding this data type was to provide optimized operations for lists that can utilize the positional semantics of their child elements and avoid branching as all lists have the same length. Think e.g., the sort of array manipulations you'd do in NumPy: stacking, shifting, multiplying – you name it. Additionally, we wanted to improve our interoperability with Apache Arrow, as previously Arrow's fixed-size list types would be converted to regular variable-size lists when ingested into DuckDB, losing some type information.

However, as the hype for __vector embeddings__ and __semantic similarity search__ was growing, we also snuck in a couple of distance metric functions for this new `ARRAY` type:
[`array_distance`]({% link docs/sql/functions/array.md %}#array_distancearray1-array2),
[`array_inner_product`]({% link docs/sql/functions/array.md %}#array_inner_productarray1-array2) and
[`array_cosine_similarity`]({% link docs/sql/functions/array.md %}#array_cosine_similarityarray1-array2)

> If you're one of today's [lucky 10,000](https://xkcd.com/1053/) and haven't heard of word embeddings or vector search, the short version is that it's a technique used to represent documents, images, entities – _data_ as high-dimensional _vectors_ and then search for _similar_ vectors in a vector space, using some sort of mathematical "distance" expression to measure similarity. This is used in a wide range of applications, from natural language processing to recommendation systems and image recognition, and has recently seen a surge in popularity due to the advent of generative AI and availability of pre-trained models.

This got the community really excited! While we (DuckDB Labs) initially went on record saying that we would not be adding a vector similarity search index to DuckDB as we deemed it to be too far out of scope, we were very interested in supporting custom indexes through extensions in general. Shoot, I've been _personally_ nagging on about wanting to plug-in an "R-Tree" index since the inception of DuckDBs [spatial extension]({% link docs/extensions/spatial.md %})! So when one of our client projects evolved into creating a proof-of-concept custom "HNSW" index extension, we said that we'd give it a shot. And... well, one thing led to another.

Fast forward to now and we're happy to announce the availability of the `vss` vector similarity search extension for DuckDB! While some may say we're late to the vector search party, [we'd like to think the party is just getting started!](https://www.gartner.com/en/newsroom/press-releases/2023-10-11-gartner-says-more-than-80-percent-of-enterprises-will-have-used-generative-ai-apis-or-deployed-generative-ai-enabled-applications-by-2026)

Alright, so what's in `vss`?

## The Vector Similarity Search (VSS) Extension

On the surface, `vss` seems like a comparatively small DuckDB extension. It does not provide any new data types, scalar functions or copy functions, but rather a single new index type: `HNSW` ([Hierarchical Navigable Small Worlds](https://en.wikipedia.org/wiki/Hierarchical_Navigable_Small_World_graphs)), which is a graph-based index structure that is particularly well-suited for high-dimensional vector similarity search.

```sql
-- Create a table with an array column
CREATE TABLE embeddings (vec FLOAT[3]);

-- Create an HNSW index on the column
CREATE INDEX idx ON embeddings USING HNSW (vec);
```

This index type can't be used to enforce constraints or uniqueness like the built-in [`ART` index]({% link docs/sql/indexes.md %}), and can't be used to speed up joins or index regular columns either. Instead, the `HNSW` index is only applicable to columns of the `ARRAY` type containing `FLOAT` elements and will only be used to accelerate queries calculating the "distance" between a constant `FLOAT` `ARRAY` and the `FLOAT` `ARRAY`'s in the indexed column, ordered by the resulting distance and returning the top-n results. That is, queries of the form:

```sql
SELECT *
FROM embeddings
ORDER BY array_distance(vec, [1, 2, 3]::FLOAT[3])
LIMIT 3;
```

will have their logical plan optimized to become a projection over a new `HNSW` index scan operator, removing the limit and sort altogether. We can verify this by checking the `EXPLAIN` output:

```sql
EXPLAIN
SELECT *
FROM embeddings
ORDER BY array_distance(vec, [1, 2, 3]::FLOAT[3])
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

You can pass the `HNSW` index creation statement a `metric` parameter to decide what kind of distance metric to use. The supported metrics are `l2sq`, `cosine` and `inner_product`, matching the three built-in distance functions: `array_distance`, `array_cosine_similarity` and `array_inner_product`.
The default is `l2sq`, which uses Euclidean distance (`array_distance`):

```sql
CREATE INDEX l2sq_idx ON embeddings USING HNSW (vec)
WITH (metric = 'l2sq');
```

To use cosine distance (`array_cosine_similarity`):

```sql
CREATE INDEX cos_idx ON embeddings USING HNSW (vec)
WITH (metric = 'cosine');
```

To use inner product (`array_inner_product`):

```sql
CREATE INDEX ip_idx ON embeddings USING HNSW (vec)
WITH (metric = 'ip');
```

## Implementation

The `vss` extension is based on the [`usearch`](https://github.com/unum-cloud/usearch) library, which provides a flexible C++ implementation of the HNSW index data structure boasting very impressive performance benchmarks. While we currently only use a subset of all the functionality and tuning options provided by `usearch`, we're excited to explore how we can leverage more of its features in the future. So far we're mostly happy that it aligns so nicely with DuckDB's development ethos. Much like DuckDB itself, `usearch` is written in portable C++11 with no external dependencies and released under a permissive license, making it super smooth to integrate into our extension build and distribution pipeline.

## Limitations

The big limitation as of now is that the `HNSW` index can only be created in in-memory databases, unless the `SET hnsw_enable_experimental_persistence = ⟨bool⟩` configuration parameter is set to `true`. If this parameter is not set, any attempt to create an `HNSW` index in a disk-backed database will result in an error message, but if the parameter is set, the index will not only be created in memory, but also persisted to disk as part of the DuckDB database file during checkpointing. After restarting or loading a database file with a persisted `HNSW` index, the index will be lazily loaded back into memory whenever the associated table is first accessed, which is significantly faster than having to re-create the index from scratch.

The reasoning for locking this feature behind an experimental flag is that we still have some known issues related to persistence of custom indexes that we want to address before enabling it by default. In particular, WAL recovery is not yet properly implemented for custom indexes, meaning that if a crash occurs or the database is shut down unexpectedly while there are uncommited changes to a `HNSW`-indexed table, you can end up with data loss or corruption of the index. While it is technically possible to recover from a unexpected shutdown manually by first starting DuckDB separately, loading the `vss` extension and then `ATTACH`ing the database file, which ensures that the `HNSW` index functionality is available during WAL-playback, you should not rely on this for production workloads.

We're actively working on addressing this and other issues related to index persistence, which will hopefully make it into [DuckDB v0.10.3]({% link docs/dev/release_calendar.md %}#upcoming-releases), but for now we recommend using the `HNSW` index in in-memory databases only.

At runtime however, much like the `ART` the `HNSW` index must be able to fit into RAM in its entirety, and the memory allocated by the `HNSW` at runtime is allocated "outside" of the DuckDB memory management system, meaning that it wont respect DuckDB's `memory_limit` configuration parameter.

Another current limitation with the `HNSW` index so far are that it only supports the `FLOAT` (a 32-bit, single-precision floating point) type for the array elements and only distance metrics corresponding to the three built in distance functions, `array_distance`, `array_inner_product` and `array_cosine_similarity`. But this is also something we're looking to expand upon in the near future as it is much less of a technical limitation and more of a "we haven't gotten around to it yet" limitation.

## Conclusion

The `vss` extension for DuckDB is a new extension that adds support for creating HNSW indexes on fixed-size list columns in DuckDB, accelerating vector similarity search queries. The extension can currently be installed on DuckDB v0.10.2 on all supported platforms (including WASM!) by running `INSTALL vss; LOAD vss`. The `vss` extension treads new ground for DuckDB extensions by providing a custom index type and we're excited to refine and expand on this functionality going forward.

While we're still working on addressing some of the limitations above, particularly those related to persistence (and performance), we still really want to share this early version the `vss` extension as we believe this will open up a lot of cool opportunities for the community. So make sure to check out the [`vss` extension documentation]({% link docs/extensions/vss.md %}) for more information on how to work with this extension!

This work was made possible by the sponsorship of a DuckDB Labs customer! If you are interested in similar work for specific capabilities, please reach out to [DuckDB Labs](https://duckdblabs.com/). Alternatively, we're happy to welcome contributors! Please reach out to the DuckDB Labs team over on Discord or on the [`vss` extension GitHub repository](https://github.com/duckdb/duckdb_vss) to keep up with the latest developments.
