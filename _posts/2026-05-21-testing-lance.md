---
layout: post
title: "Test-Driving the Lance Lakehouse Format in DuckDB"
author: "LanceDB team and Guillermo Sanchez"
thumb: "/images/blog/thumbs/testing-lance.svg"
image: "/images/blog/thumbs/testing-lance.jpg"
excerpt: "Lance is an open lakehouse format with a design geared toward AI workloads. LanceDB and DuckDB Labs have partnered to bring you fast vector and hybrid search directly from DuckDB SQL, without leaving your analytical workflow. In this post, we explain what Lance is, how to use it in DuckDB, and, of course, show some benchmark results."
tags: ["extension"]
---

With the [`lance` extension]({% link docs/current/core_extensions/lance.md %}), DuckDB users can query Lance datasets with the same familiar SQL interface (via the CLI or SDKs), while adding capabilities for AI and retrieval workloads. This blog post highlights how Lance is a good option for workloads that need to support storage and querying of vectors, rich table operations, and AI-oriented access patterns, while also supporting scan-friendly analytical workloads at scale. And with DuckDB, it becomes trivial to query those kinds of datasets in SQL.

> In this blog, there will be some mentions of “retrieval workloads” and “AI data patterns” or “AI datasets”. By “retrieval workloads,” we mean queries that find rows by similarity or keyword relevance, such as vector search and full-text search, rather than by exact filters or aggregations. By “AI data patterns,” we mean datasets that mix embeddings, images, or audio alongside scalar metadata.

## What is Lance?

[Lance](https://lance.org/) is an open lakehouse format designed for modern ML and AI workloads. Unlike Parquet, Lance is a file format, a table format, and a lightweight catalog spec all at once. At the table format level, Lance supports versioning, schema evolution, indexes, and transactional updates through MVCC and ACID-style semantics. In practice, this means Lance is built for datasets that change over time and need more than read-only scans.

This matters because many AI datasets are no longer just rows of scalar values. They often contain embeddings, long-form text, images, audio, metadata for filtering, and indexes used for retrieval. A format that works well for these workloads needs to do more than store and scan columns efficiently. It also needs to support search, updates, and lifecycle operations without forcing users into managing multiple different systems.

The mental model is still familiar to users coming from Parquet: columnar data in an open format, queried with standard analytical tools. Lance's fragment-based layout stores data in small columnar chunks. This design enables efficient random access without trade-offs in scan performance or memory utilization, something that has historically been difficult to achieve in columnar formats, and that the Lance team examines in [this 2025 paper on adaptive structural encodings](https://arxiv.org/abs/2504.15247).

On the data evolution side, adding columns or backfilling existing rows with new data only writes new files without touching existing ones. That makes schema changes lightweight in practice, which is useful for workflows where columns are added incrementally, such as appending derived features or embeddings to an existing dataset.

## The Lance DuckDB Extension

The [`lance` extension]({% link docs/current/core_extensions/lance.md %}) brings Lance into DuckDB as part of the SQL-based workflow. You can read Lance datasets directly, write to them via `COPY`, attach them as table namespaces, build indexes, and query them with regular DuckDB SQL. On top of that, the extension exposes Lance-native search functionality through SQL table functions.

This fits naturally with how DuckDB is already used: as a single, embedded SQL query engine that operates on many different data sources and file formats. With the Lance extension, DuckDB remains the familiar query engine, while Lance provides the storage, indexing, and search capabilities underneath, which is especially beneficial when your data is multimodal and includes embeddings.

### Example Usage

Installing and using the extension is straightforward:

```sql
INSTALL lance;
LOAD lance;

SELECT *
FROM 'path/to/dataset.lance'
LIMIT 10;
```

DuckDB can also write Lance datasets directly:

```sql
COPY (
    SELECT *
    FROM (
        VALUES
            (1::BIGINT, 'duck', [0.9, 0.7, 0.1]::FLOAT[3]),
            (2::BIGINT, 'horse', [0.3, 0.1, 0.5]::FLOAT[3]),
            (3::BIGINT, 'dragon', [0.5, 0.2, 0.7]::FLOAT[3])
        ) AS t(id, animal, vec)
) TO 'path/to/out.lance' (FORMAT lance, mode 'overwrite');
```

Once the data is in Lance, DuckDB can query it with Lance-native search operators. For example, hybrid search combines vector similarity and keyword relevance in one SQL query:

```sql
SELECT id, text, _hybrid_score, _distance, _score
FROM lance_hybrid_search(
    'path/to/dataset.lance',
    'vec',
    [0.1, 0.2, 0.3, 0.4]::FLOAT[4],
    'text',
    'puppy',
    k = 10,
    prefilter = false,
    alpha = 0.5,
    oversample_factor = 4
)
ORDER BY _hybrid_score DESC;
```

The extension also exposes `lance_vector_search(...)` for vector similarity search and `lance_fts(...)` for full-text search, so users can choose the retrieval mode that fits their workload.

If you want table-style access instead of path-based access, you can attach a directory as a Lance namespace:

```sql
ATTACH 'path/to/dir' AS ns (TYPE lance);

SELECT count(*)
FROM ns.main.my_table;
```

Index creation also happens through SQL. For example, a vector index can be created directly on a Lance dataset:

```sql
CREATE INDEX vec_idx ON 'path/to/dataset.lance' (vec)
USING IVF_FLAT WITH (num_partitions = 1, metric_type = 'l2');
```

The extension surface goes well beyond read-only scans. In the current implementation, DuckDB can:

- Read Lance datasets with direct path scans  
- Write and append Lance datasets with `COPY ... TO ... (FORMAT lance)`  
- Run vector, full-text, and hybrid search with SQL functions  
- Attach local directories or custom catalogs via REST namespaces  
- Create, update, delete, merge, and alter tables in attached namespaces  
- Create and manage vector, scalar, and full-text indexes  
- Run maintenance operations such as compaction, cleanup, and index optimization

Note that this extension is not just a file reader, but it also gives DuckDB users a way to work with Lance as an operational table format from inside SQL.

## Why Lance and DuckDB?

The combination of Lance and DuckDB is compelling for three reasons.

First, it gives users one SQL surface for analytics plus retrieval. The same DuckDB workflow can scan a dataset, filter it, join it with other tables, compute aggregates, and then run vector search or hybrid search over the result set. That is a good fit for AI applications where retrieval is only one step in a larger analytical pipeline.

Second, Lance is a table format for more than traditional analytics. Many AI pipelines need versioned datasets, updates, deletes, `MERGE`-style changes, index management, and schema evolution. The DuckDB extension exposes these capabilities through SQL, which means users do not need to leave the DuckDB environment just because their dataset is doing more than serving analytical reads.

Third, the workflow scales from local files to remote storage without changing the mental model. You can start with a local `lance` dataset, then [move to object storage]({% link docs/current/core_extensions/lance.md %}#query-a-lance-dataset).

The extension also supports REST namespaces, so DuckDB can connect to a remote Lance catalog (including [LanceDB Enterprise](https://docs.lancedb.com/enterprise/index)) and treat it like an attached database. That makes the local-to-remote storage progression feel incremental rather than disruptive.

To sum up, DuckDB remains the familiar SQL engine, while Lance adds storage and indexing features that are especially useful when the same dataset powers both analytics and retrieval.

## Performance Experiment

[LAION](https://laion.ai/) is an open dataset of image/caption pairs scraped from the public web, originally released to support research on models like [CLIP](https://openai.com/index/clip/), which learn a shared embedding space for images and text. The full release spans billions of pairs. For this experiment, we used the `lance-format/laion-1m` subset on Hugging Face Hub, which is easy to reproduce locally.

Each row carries a caption, a 768-dimensional CLIP image embedding, the raw image bytes, and scalar metadata like width, height, and NSFW flags. This mix of scalar, text, vector, and blob data in a single table makes it a useful workload for comparing formats, and it is structurally different from the wide-but-flat schemas like TPC-H or ClickBench that are traditionally used for analytical benchmarks.

The public Hugging Face export used by the benchmark currently materializes 69,632 rows locally, not the full million-row source dataset. The runner first downloads the public Parquet shards, then builds all local artifacts from that same baseline: an LZ4-compressed Parquet file, an indexed DuckDB database, and a Lance dataset. Generated files are reused across runs, so the initial download is the only networked step.

> The experiments were run on an Apple MacBook Pro with a 10-core M1 Max CPU and 32 GB of RAM, running DuckDB 1.5.2.

The benchmark was run using DuckDB as the query engine for the following three storage formats:

* **Parquet**: DuckDB scanning the LZ4-compressed Parquet baseline directly, with no auxiliary indexes.  
* **DuckDB indexed**: the same baseline loaded into a DuckDB table, with DuckDB's `vss` (HNSW) and `fts` extensions layered on top, plus scalar indexes on filter columns. This is the typical “build it yourself in DuckDB” stack.  
* **Lance native**: the same baseline written to a Lance dataset with a vector index, a full-text index, and native blob storage, queried through the DuckDB lance extension.

The workloads are aligned by task across the three paths, even though the exact SQL differs by storage/indexing backend:

* `fts`: find rows by keyword search over the caption text.  
* `vector_exact`: run nearest-neighbor search over the CLIP embedding column without using an approximate vector index.  
* `vector_indexed`: run nearest-neighbor search over the same embedding column using the available vector index.  
* `hybrid`: combine text search and vector search into one retrieval query, returning the best-ranked matches from both signals.  
* `blob_read`: fetch image bytes for selected rows, which exercises random access to large binary values rather than just scalar or vector columns.

Each workload is run five times by default, and the tables below report the average. The full scripts and SQL queries are in the `laion_1m` benchmark directory.

### Cold Results

The table below runs each workload cold, in a fresh DuckDB process, so it captures process startup, file open, and first-query cost. It's closest to what a one-off script or a cron job would see.

| Workload         | Parquet | DuckDB indexed | Lance native |
| :--------------- | ------: | -------------: | -----------: |
| `fts`            |   12 ms |          11 ms |        21 ms |
| `vector_exact`   |  695 ms |          61 ms |        89 ms |
| `vector_indexed` |  761 ms |         104 ms |        12 ms |
| `hybrid`         |  465 ms |          80 ms |        17 ms |
| `blob_read`      | 1559 ms |         271 ms |       278 ms |

In the cold run, Lance stands out in the `vector_indexed` and `hybrid` workloads. DuckDB’s own format does well in `vector_exact` and `fts`, while the `blob_read` workload is pretty much on par. Parquet is not well optimized for vector searches or blob reads, but does well on a simple text search powered by regex.

### Warm Results

The warm results are from running all workloads in a single DuckDB session after a silent warmup pass, so caches, memory-mapped pages, and loaded indexes are already primed.

| Workload         | Parquet | DuckDB indexed | Lance native |
| :--------------- | ------: | -------------: | -----------: |
| `fts`            |   12 ms |          10 ms |         7 ms |
| `vector_exact`   |  703 ms |          30 ms |        50 ms |
| `vector_indexed` |  755 ms |           2 ms |         5 ms |
| `hybrid`         |  471 ms |          11 ms |         8 ms |
| `blob_read`      | 1484 ms |         266 ms |       276 ms |

When caches and indexes are already warm, both DuckDB and Lance are significantly faster than using Parquet on retrieval workloads.

## Conclusion

Lance is a relatively new addition to the world of open lakehouse formats. It is designed for datasets that change over time, contain more than scalar values, and need to support both search and retrieval alongside traditional scan workloads. From DuckDB, the extension makes these capabilities available through SQL, while preserving the familiar embedded workflow. The benchmark results reflect, particularly in cold runs, how Lance is a good alternative to DuckDB’s own format for vector and hybrid search.

