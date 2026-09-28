---
layout: post
title: "DuckDB and Hugging Face: Querying Datasets Directly"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/hugging-face.svg"
image: "/images/blog/thumbs/hugging-face.png"
excerpt: "Hugging Face hosts hundreds of thousands of datasets, and DuckDB can read them directly, exactly where they are and without downloading anything, over the DuckDB `hf://` protocol. This post looks at how the integration works and the scenarios where it works best."
tags: ["extensions"]
---

[Hugging Face](https://huggingface.co/) is where much of the machine learning community publishes and finds its datasets, while DuckDB is the in-process analytical database that queries files like CSV and Parquet directly, with no server or warehouse to install or run. 

Did you know that, since DuckDB [v0.10.3](https://github.com/duckdb/duckdb/releases/tag/v0.10.3) (released on May 22, 2024), you can point a `SELECT` at a dataset on the [Hugging Face Hub](https://huggingface.co/docs/hub), using the DuckDB `hf://` protocol, and query it, without downloading it first? This post covers how that integration works and the use cases it fits.

## Background

On the [Hugging Face Hub](https://huggingface.co/docs/hub), each dataset is a git repository holding its data as plain files, usually CSV, JSONL, or Parquet. The [`cais/mmlu`](https://huggingface.co/datasets/cais/mmlu) benchmark and the [`datasets-examples/doc-formats-csv-1`](https://huggingface.co/datasets/datasets-examples/doc-formats-csv-1) repository used later in this post are two such examples: you can browse their files and commit history in the browser, the same way you would any git repository. 

Before the Hugging Face integration, getting at that data from DuckDB meant downloading the files first, or loading them with the Hugging Face [`datasets`](https://huggingface.co/docs/datasets) library, before they could be read and analyzed. Either way, the data had to be copied out of the [Hugging Face Hub](https://huggingface.co/docs/hub) before you could query it.

DuckDB was already able to read remote files over HTTP through its [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}), so reading a URL directly was not new. Hugging Face datasets are also increasingly published as Parquet, the columnar format DuckDB reads natively and can scan without materializing everything in memory.

DuckDB and Hugging Face [worked together]({% post_url 2024-05-29-access-150k-plus-datasets-from-hugging-face-with-duckdb %}) to add the [`hf://` path scheme]({% link docs/lts/core_extensions/httpfs/hugging_face.md %}) on top of `httpfs`, [announced in May 2024]({% post_url 2024-05-29-access-150k-plus-datasets-from-hugging-face-with-duckdb %}) with DuckDB [v0.10.3](https://github.com/duckdb/duckdb/releases/tag/v0.10.3). As a result, DuckDB can resolve a dataset repository to the files inside it, so that a query can read and analyze them exactly where they are located, instead of via a downloaded copy.

## Reading Hugging Face Datasets Directly

The examples below cover the common cases. [DuckDB's Hugging Face docs]({% link docs/lts/core_extensions/httpfs/hugging_face.md %}) are the full reference. The scheme maps a Hugging Face dataset repository onto a path DuckDB can read:

```sql
hf://datasets/⟨my_username⟩/⟨my_dataset⟩/⟨path_to_file⟩
```

Reading a file is then just a query. This reads the CSV file from the [`datasets-examples/doc-formats-csv-1`](https://huggingface.co/datasets/datasets-examples/doc-formats-csv-1) repository:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

| kind    | sound |
| ------- | ----- |
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

Here `datasets-examples` is the user or organization, `doc-formats-csv-1` is the dataset repository, and `data.csv` is the file inside it. The same example data is published in the [`doc-formats-jsonl-1`](https://huggingface.co/datasets/datasets-examples/doc-formats-jsonl-1) and [`doc-formats-parquet-1`](https://huggingface.co/datasets/datasets-examples/doc-formats-parquet-1) repositories, so these queries return the same four rows:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-jsonl-1/data.jsonl';
```

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet';
```

DuckDB infers the format from the file and reads only the columns that the query actually needs. And, nothing is downloaded to a local copy first.

### Querying Many Files at Once

Datasets are often split across many files. A [glob pattern]({% link docs/current/data/multiple_files/overview.md %}#multi-file-reads-and-globs) lets you treat a whole directory as one table. The [`cais/mmlu`](https://huggingface.co/datasets/cais/mmlu) benchmark stores its `astronomy` task across three Parquet files (`dev`, `test`, and `validation`), and this counts the rows across all of them:

```sql
SELECT count(*) AS count
FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet';
```

| count |
| ----: |
|   173 |

Because DuckDB reads Parquet column by column, you can filter across all those files without pulling every row into memory:

```sql
SELECT count(*) AS count
FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet'
WHERE question LIKE '%planet%';
```

| count |
| ----: |
|    21 |

### Versions and the `~parquet` Branch

Each Hugging Face dataset is a git repository, so it has branches and revisions. You can pin a query to a specific one with an `@` suffix:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-csv-1@~parquet/**/*.parquet';
```

| kind    | sound |
| ------- | ----- |
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

Hugging Face automatically converts every dataset into Parquet on this special `~parquet` branch to make it efficient to scan. So even a dataset published as CSV or JSONL usually has a columnar version ready, which is what DuckDB reads fastest.

### Saving a Local Copy

If you are going to query the same data repeatedly, materialize it once so you are not hitting the remote endpoint each time:

```sql
CREATE TABLE data AS
    SELECT *
    FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

After that, the data lives in the local table and queries no longer touch the [Hugging Face Hub](https://huggingface.co/docs/hub):

```sql
SELECT *
FROM data;
```

| kind    | sound |
| ------- | ----- |
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

### Private and Gated Datasets

Public datasets need no setup. For private or gated ones, store a Hugging Face token in DuckDB's [Secrets Manager]({% link docs/current/configuration/secrets_manager.md %}). You can pass the token directly:

```sql
CREATE SECRET hf_token (
    TYPE huggingface,
    TOKEN 'your_hf_token'
);
```

Or let DuckDB pick it up from `~/.cache/huggingface/token`, where the Hugging Face tooling stores it:

```sql
CREATE SECRET hf_token (
    TYPE huggingface,
    PROVIDER credential_chain
);
```

## Typical Use Cases

The integration is a good fit whenever you want to look at data on the [Hugging Face Hub](https://huggingface.co/docs/hub) without committing to a download or a pipeline.

* **Exploring a dataset before you use it.** Before training or finetuning a dataset, you usually want to know what is in it: the row count, how many rows are unique, and what the columns look like. A single query against an `hf://` path answers that, reading only the columns you ask for:

  ```sql
  SELECT
      count(*) AS questions,
      count(DISTINCT question) AS distinct_questions,
      avg(len(choices)) AS avg_choices
  FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet';
  ```

  | questions | distinct_questions | avg_choices |
  | --------: | -----------------: | ----------: |
  |       173 |                166 |         4.0 |

* **Filtering and sampling for training.** Large datasets often need to be narrowed to a subset, say a single language or the rows above some quality threshold, before they are useful. Express that as a `WHERE` clause and write the result straight to a local Parquet file with `COPY`:

  ```sql
  COPY (
      SELECT question, choices, answer
      FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet'
      WHERE question LIKE '%planet%'
  ) TO 'astronomy_planets.parquet';
  ```

  This turns a remote dataset into a focused local file, here the 21 astronomy questions that mention a planet.

* **Working with benchmarks and evaluation sets.** Benchmarks like [MMLU](https://huggingface.co/datasets/cais/mmlu) ship as many small files grouped by task. You can read several tasks as one table and compute per-task statistics:

  ```sql
  SELECT subject, count(*) AS questions
  FROM read_parquet([
      'hf://datasets/cais/mmlu/astronomy/test-00000-of-00001.parquet',
      'hf://datasets/cais/mmlu/anatomy/test-00000-of-00001.parquet'
  ])
  GROUP BY subject
  ORDER BY subject;
  ```

  | subject   | questions |
  | --------- | --------: |
  | anatomy   |       135 |
  | astronomy |       152 |

* **Joining Hugging Face Hub data with your own.** Because an `hf://` path behaves like any other table source, you can join a public dataset against your own tables. Here a small lookup table maps each numeric answer to a choice letter:

  ```sql
  SELECT l.letter AS correct_choice, count(*) AS n
  FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet' AS m
  JOIN (VALUES (0, 'A'), (1, 'B'), (2, 'C'), (3, 'D')) AS l(idx, letter)
    ON m.answer = l.idx
  GROUP BY l.letter
  ORDER BY l.letter;
  ```

  | correct_choice |  n |
  | -------------- | -: |
  | A              | 35 |
  | B              | 32 |
  | C              | 48 |
  | D              | 58 |

* **Reproducible analysis.** Pinning a query to a specific commit means it reads the same data every time it runs, which matters for anything you need to reproduce later. Add the revision with an `@` suffix:

  ```sql
  SELECT count(*) AS count
  FROM 'hf://datasets/cais/mmlu@c30699e8356da336a370243923dbaf21066bb9fe/astronomy/*.parquet';
  ```

  | count |
  | ----: |
  |   173 |

## Conclusion

The [`hf://` protocol]({% link docs/lts/core_extensions/httpfs/hugging_face.md %}) lets you query a dataset on the [Hugging Face Hub](https://huggingface.co/docs/hub) by putting its path in a `SELECT`, with no download step and no server to run.

If you work with datasets on the [Hugging Face Hub](https://huggingface.co/docs/hub), that covers a lot of day-to-day tasks, from inspecting a new dataset to creating a training subset out of a larger one.

For further reading, see the original [announcement post]({% post_url 2024-05-29-access-150k-plus-datasets-from-hugging-face-with-duckdb %}), [DuckDB's Hugging Face docs]({% link docs/lts/core_extensions/httpfs/hugging_face.md %}), and Hugging Face's own [DuckDB guide](https://huggingface.co/docs/hub/datasets-duckdb).
