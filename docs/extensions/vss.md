---
layout: docu
title: Vector Similarity Search Extension
github_repository: https://github.com/duckdb/duckdb-vss
---

The `vss` extension is an experimental extension for DuckDB that adds indexing support to accelerate vector similarity search queries using DuckDB's new fixed-size `ARRAY` type.

See the [announcement blog post]({% post_url 2024-05-03-vector-similarity-search-vss %}) and the [“What's New in the Vector Similarity Search Extension?” post]({% post_url 2024-10-23-whats-new-in-the-vss-extension %}).

## Usage

To create a new HNSW (Hierarchical Navigable Small Worlds) index on a table with an `ARRAY` column, use the `CREATE INDEX` statement with the `USING HNSW` clause. For example:

```sql
INSTALL vss;
LOAD vss;

CREATE TABLE my_vector_table (vec FLOAT[3]);
INSERT INTO my_vector_table
    SELECT array_value(a, b, c)
    FROM range(1, 10) ra(a), range(1, 10) rb(b), range(1, 10) rc(c);
CREATE INDEX my_hnsw_index ON my_vector_table USING HNSW (vec);
```

The index will then be used to accelerate queries that use a `ORDER BY` clause evaluating one of the supported distance metric functions against the indexed columns and a constant vector, followed by a `LIMIT` clause. For example:

```sql
SELECT *
FROM my_vector_table
ORDER BY array_distance(vec, [1, 2, 3]::FLOAT[3])
LIMIT 3;
```

Additionally, the overloaded `min_by(col, arg, n)` can also be accelerated with the `HNSW` index if the `arg` argument is a matching distance metric function. This can be used to do quick one-shot nearest neighbor searches. For example, to get the top 3 rows with the closest vectors to `[1, 2, 3]`:

```sql
SELECT min_by(my_vector_table, array_distance(vec, [1, 2, 3]::FLOAT[3]), 3) AS result
FROM my_vector_table;
---- [{'vec': [1.0, 2.0, 3.0]}, {'vec': [1.0, 2.0, 4.0]}, {'vec': [2.0, 2.0, 3.0]}]
```

Note how we pass the table name as the first argument to `min_by` to return a struct containing the entire matched row.

We can verify that the index is being used by checking the `EXPLAIN` output and looking for the `HNSW_INDEX_SCAN` node in the plan:

```sql
EXPLAIN
SELECT *
FROM my_vector_table
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
│           my_idx)         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            vec            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 3           │
└───────────────────────────┘
```

By default the HNSW index will be created using the euclidean distance `l2sq` (L2-norm squared) metric, matching DuckDBs `array_distance` function, but other distance metrics can be used by specifying the `metric` option during index creation. For example:

```sql
CREATE INDEX my_hnsw_cosine_index
ON my_vector_table
USING HNSW (vec)
WITH (metric = 'cosine');
```

The following table shows the supported distance metrics and their corresponding DuckDB functions

| Metric   | Function                       | Description                |
|----------|--------------------------------|----------------------------|
| `l2sq`   | `array_distance`               | Euclidean distance         |
| `cosine` | `array_cosine_distance`        | Cosine similarity distance |
| `ip`     | `array_negative_inner_product` | Negative inner product     |

Note that while each `HNSW` index only applies to a single column you can create multiple `HNSW` indexes on the same table each individually indexing a different column. Additionally, you can also create multiple `HNSW` indexes to the same column, each supporting a different distance metric.

## Index Options

Besides the `metric` option, the `HNSW` index creation statement also supports the following options to control the hyperparameters of the index construction and search process:

| Option | Default | Description |
|-------|--:|----------------------------|
| `ef_construction` | 128     | The number of candidate vertices to consider during the construction of the index. A higher value will result in a more accurate index, but will also increase the time it takes to build the index.                           |
| `ef_search`       | 64      | The number of candidate vertices to consider during the search phase of the index. A higher value will result in a more accurate index, but will also increase the time it takes to perform a search.                          |
| `M`               | 16      | The maximum number of neighbors to keep for each vertex in the graph. A higher value will result in a more accurate index, but will also increase the time it takes to build the index.                                        |
| `M0`              | 2 * `M` | The base connectivity, or the number of neighbors to keep for each vertex in the zero-th level of the graph. A higher value will result in a more accurate index, but will also increase the time it takes to build the index. |

Additionally, you can also override the `ef_search` parameter set at index construction time by setting the `SET hnsw_ef_search = ⟨int⟩` configuration option at runtime. This can be useful if you want to trade search performance for accuracy or vice-versa on a per-connection basis. You can also unset the override by calling `RESET hnsw_ef_search`.

## Persistence

Due to some known issues related to peristence of custom extension indexes, the `HNSW` index can only be created on tables in in-memory databases by default, unless the `SET hnsw_enable_experimental_persistence = ⟨bool⟩` configuration option is set to `true`.

The reasoning for locking this feature behind an experimental flag is that “WAL” recovery is not yet properly implemented for custom indexes, meaning that if a crash occurs or the database is shut down unexpectedly while there are uncommitted changes to a `HNSW`-indexed table, you can end up with **data loss or corruption of the index**.

If you enable this option and experience an unexpected shutdown, you can try to recover the index by first starting DuckDB separately, loading the `vss` extension and then `ATTACH`ing the database file, which ensures that the `HNSW` index functionality is available during WAL-playback, allowing DuckDB's recovery process to proceed without issues. But we still recommend that you do not use this feature in production environments.

With the `hnsw_enable_experimental_persistence` option enabled, the index will be persisted into the DuckDB database file (if you run DuckDB with a disk-backed database file), which means that after a database restart, the index can be loaded back into memory from disk instead of having to be re-created. With that in mind, there are no incremental updates to persistent index storage, so every time DuckDB performs a checkpoint the entire index will be serialized to disk and overwrite itself. Similarly, after a restart of the database, the index will be deserialized back into main memory in its entirety. Although this will be deferred until you first access the table associated with the index. Depending on how large the index is, the deserialization process may take some time, but it should still be faster than simply dropping and re-creating the index.

## Inserts, Updates, Deletes and Re-Compaction

The HNSW index does support inserting, updating and deleting rows from the table after index creation. However, there are two things to keep in mind:

* It's faster to create the index after the table has been populated with data as the initial bulk load can make better use of parallelism on large tables.
* Deletes are not immediately reflected in the index, but are instead “marked” as deleted, which can cause the index to grow stale over time and negatively impact query quality and performance.

To remedy the last point, you can call the `PRAGMA hnsw_compact_index('⟨index name⟩')` pragma function to trigger a re-compaction of the index pruning deleted items, or re-create the index after a significant number of updates.

## Bonus: Vector Similarity Search Joins

The `vss` extension also provides a couple of table macros to simplify matching multiple vectors against eachother, so called "fuzzy joins". These are:

* `vss_join(left_table, right_table, left_col, right_col, k, metric := 'l2sq')`
* `vss_match(right_table", left_col, right_col, k, metric := 'l2sq')`

These **do not** currently make use of the `HNSW` index but are provided as convenience utility functions for users who are ok with performing brute-force vector similarity searches without having to write out the join logic themselves. In the future these might become targets for index-based optimizations as well.

These functions can be used as follows:

```sql
CREATE TABLE haystack (id int, vec FLOAT[3]);
CREATE TABLE needle (search_vec FLOAT[3]);

INSERT INTO haystack
    SELECT row_number() OVER (), array_value(a,b,c)
    FROM range(1, 10) ra(a), range(1, 10) rb(b), range(1, 10) rc(c);

INSERT INTO needle
    VALUES ([5, 5, 5]), ([1, 1, 1]);

SELECT *
FROM vss_join(needle, haystack, search_vec, vec, 3) res;
```

```text
┌───────┬─────────────────────────────────┬─────────────────────────────────────┐
│ score │            left_tbl             │              right_tbl              │
│ float │   struct(search_vec float[3])   │  struct(id integer, vec float[3])   │
├───────┼─────────────────────────────────┼─────────────────────────────────────┤
│   0.0 │ {'search_vec': [5.0, 5.0, 5.0]} │ {'id': 365, 'vec': [5.0, 5.0, 5.0]} │
│   1.0 │ {'search_vec': [5.0, 5.0, 5.0]} │ {'id': 364, 'vec': [5.0, 4.0, 5.0]} │
│   1.0 │ {'search_vec': [5.0, 5.0, 5.0]} │ {'id': 356, 'vec': [4.0, 5.0, 5.0]} │
│   0.0 │ {'search_vec': [1.0, 1.0, 1.0]} │ {'id': 1, 'vec': [1.0, 1.0, 1.0]}   │
│   1.0 │ {'search_vec': [1.0, 1.0, 1.0]} │ {'id': 10, 'vec': [2.0, 1.0, 1.0]}  │
│   1.0 │ {'search_vec': [1.0, 1.0, 1.0]} │ {'id': 2, 'vec': [1.0, 2.0, 1.0]}   │
└───────┴─────────────────────────────────┴─────────────────────────────────────┘
```

```sql
-- Alternatively, we can use the vss_match macro as a "lateral join"
-- to get the matches already grouped by the left table.
-- Note that this requires us to specify the left table first, and then
-- the vss_match macro which references the search column from the left
-- table (in this case, `search_vec`).
SELECT *
FROM needle, vss_match(haystack, search_vec, vec, 3) res;
```

```text
┌─────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   search_vec    │                                                                                       matches                                                                                        │
│    float[3]     │                                                            struct(score float, "row" struct(id integer, vec float[3]))[]                                                             │
├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [5.0, 5.0, 5.0] │ [{'score': 0.0, 'row': {'id': 365, 'vec': [5.0, 5.0, 5.0]}}, {'score': 1.0, 'row': {'id': 364, 'vec': [5.0, 4.0, 5.0]}}, {'score': 1.0, 'row': {'id': 356, 'vec': [4.0, 5.0, 5.0]}}] │
│ [1.0, 1.0, 1.0] │ [{'score': 0.0, 'row': {'id': 1, 'vec': [1.0, 1.0, 1.0]}}, {'score': 1.0, 'row': {'id': 10, 'vec': [2.0, 1.0, 1.0]}}, {'score': 1.0, 'row': {'id': 2, 'vec': [1.0, 2.0, 1.0]}}]      │
└─────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Limitations

* Only vectors consisting of `FLOAT`s (32-bit, single precision) are supported at the moment.
* The index itself is not buffer managed and must be able to fit into RAM memory.
* The size of the index in memory does not count towards DuckDB's `memory_limit` configuration parameter.
* `HNSW` indexes can only be created on tables in in-memory databases, unless the `SET hnsw_enable_experimental_persistence = ⟨bool⟩` configuration option is set to `true`, see [Persistence](#persistence) for more information.
* The vector join table macros (`vss_join` and `vss_match`) do not require or make use of the `HNSW` index.
