---
github_repository: https://github.com/lance-format/lance-duckdb
layout: docu
title: Lance Extension
---

The `lance` extension adds support for reading and writing Lance tables. [Lance](https://github.com/lance-format/lance/) is a modern lakehouse format optimized for ML/AI workloads, with native cloud storage support.

## Installing and Loading

You can install the `lance` extension from DuckDB's core extensions repository and load it using the following commands:

```sql
INSTALL lance;
LOAD lance;
```

## Usage

- [Full SQL reference](https://github.com/lance-format/lance-duckdb/blob/main/docs/sql.md)
- [Cloud storage reference](https://github.com/lance-format/lance-duckdb/blob/main/docs/cloud.md)

### Query a Lance Dataset

Local file:

```sql
SELECT *
FROM 'path/to/dataset.lance'
LIMIT 10;
```

S3:

```sql
SELECT *
FROM 's3://bucket/path/to/dataset.lance'
LIMIT 10;
```

To access object store URIs (e.g., `s3://...`), configure a `TYPE lance` secret using the [Secrets Manager]({% link docs/lts/sql/statements/create_secret.md %}):

```sql
CREATE SECRET (
    TYPE lance,
    PROVIDER credential_chain,
    SCOPE 's3://bucket/'
);

SELECT *
FROM 's3://bucket/path/to/dataset.lance'
LIMIT 10;
```

### Write a Lance Dataset

Use the [`COPY ... TO ...` statement]({% link docs/lts/sql/statements/copy.md %}#copy--to) to materialize query results as a Lance dataset.

```sql
-- Create/overwrite a Lance dataset from a query
COPY (
    SELECT 1::BIGINT AS id, 'a'::VARCHAR AS s
    UNION ALL
    SELECT 2::BIGINT AS id, 'b'::VARCHAR AS s
) TO 'path/to/out.lance' (
    FORMAT lance,
    MODE 'overwrite'
);

-- Read it back via the replacement scan
SELECT count(*) FROM 'path/to/out.lance';

-- Append more rows to an existing dataset
COPY (
    SELECT 3::BIGINT AS id, 'c'::VARCHAR AS s
) TO 'path/to/out.lance' (
    FORMAT lance,
    MODE 'append'
);

-- Optionally create an empty dataset (schema only)
COPY (
    SELECT 1::BIGINT AS id, 'x'::VARCHAR AS s
    WITH NO DATA
) TO 'path/to/empty.lance' (
    FORMAT lance,
    MODE 'overwrite',
    WRITE_EMPTY_FILE true
);
```

To write to `s3://...` paths, configure a `TYPE lance` secret for that scope using the [Secrets Manager]({% link docs/lts/sql/statements/create_secret.md %}):

```sql
CREATE SECRET (
    TYPE lance,
    PROVIDER credential_chain,
    SCOPE 's3://⟨bucket⟩/'
);

COPY (SELECT 1 AS id)
TO 's3://⟨bucket/path/to/out.lance⟩'
(FORMAT lance, MODE 'overwrite');
```

### Create a Lance Dataset via `CREATE TABLE` (Directory Namespace)

When you `ATTACH` a directory as a Lance namespace, you can create new datasets using `CREATE TABLE` (schema-only)
or `CREATE TABLE AS SELECT` (CTAS). The dataset is written to `⟨namespace_root⟩/⟨table_name⟩.lance`{:.language-sql .highlight}.

```sql
ATTACH 'path/to/dir' AS lance_ns (TYPE lance);

-- Schema-only (creates an empty dataset)
CREATE TABLE lance_ns.main.my_empty (id BIGINT, s VARCHAR);

-- CTAS (writes query results)
CREATE TABLE lance_ns.main.my_dataset AS
    SELECT 1::BIGINT AS id, 'a'::VARCHAR AS s
    UNION ALL
    SELECT 2::BIGINT AS id, 'b'::VARCHAR AS s;

SELECT count(*) FROM lance_ns.main.my_dataset;
```

### Vector Search

```sql
-- Search a vector column, returning distances in `_distance` (smaller is closer)
SELECT id, label, _distance
FROM lance_vector_search(
    'path/to/dataset.lance', 'vec',
    [0.1, 0.2, 0.3, 0.4]::FLOAT[4],
    k = 5,
    prefilter = true
)
ORDER BY _distance ASC;
```

See the [SQL reference for full parameter documentation](https://github.com/lance-format/lance-duckdb/blob/main/docs/sql.md#search).

### Full-Text Search (FTS)

```sql
-- Search a text column, returning BM25-like scores in `_score`
SELECT id, text, _score
FROM lance_fts(
    'path/to/dataset.lance',
    'text',
    'puppy',
    k = 10,
    prefilter = true
)
ORDER BY _score DESC;
```

See the [SQL reference for full parameter documentation](https://github.com/lance-format/lance-duckdb/blob/main/docs/sql.md#search).

### Hybrid Search (Vector + FTS)

```sql
-- Combine vector and text scores, returning `_hybrid_score` in addition to `_distance` / `_score`
SELECT id, _hybrid_score, _distance, _score
FROM lance_hybrid_search('path/to/dataset.lance',
                         'vec', [0.1, 0.2, 0.3, 0.4]::FLOAT[4],
                         'text', 'puppy',
                         k = 10, prefilter = false,
                         alpha = 0.5, oversample_factor = 4)
ORDER BY _hybrid_score DESC;
```

## Limitations

The `lance` extension is currently available for the following [platforms]({% link docs/lts/dev/building/overview.md %}#supported-platforms):

- `linux_amd64`
- `linux_arm64`
- `osx_arm64`
- `windows_amd64`
