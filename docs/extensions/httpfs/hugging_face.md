---
layout: docu
title: Hugging Face Support
---

The `httpfs` extension introduces support for the `hf://` protocol to access data sets hosted in [Hugging Face](https://huggingface.co/) repositories.
See the [announcement blog post]({% link _posts/2024-05-29-access-150k-plus-datasets-from-hugging-face-with-duckdb.md %}) for details.

## Usage

Hugging Face repositories can be queried using the following URL pattern:

```text
hf://datasets/⟨my_username⟩/⟨my_dataset⟩/⟨path_to_file⟩
```

For example, to read a CSV file, you can use the following query:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

Where:

* `datasets-examples` is the name of the user/organization
* `doc-formats-csv-1` is the name of the dataset repository
* `data.csv` is the file path in the repository

The result of the query is:

|  kind   | sound |
|---------|-------|
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

To read a JSONL file, you can run:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-jsonl-1/data.jsonl';
```

Finally, for reading a Parquet file, use the following query:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet';
```

Each of these commands reads the data from the specified file format and displays it in a structured tabular format. Choose the appropriate command based on the file format you are working with.

## Creating a local table

To avoid accessing the remote endpoint for every query, you can save the data in a DuckDB table by running a [`CREATE TABLE ... AS` command]({% link docs/sql/statements/create_table.md %}#create-table--as-select-ctas). For example:

```sql
CREATE TABLE data AS
    SELECT *
    FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

Then, simply query the `data` table as follows:

```sql
SELECT *
FROM data;
```

## Multiple files

To query all files under a specific directory, you can use a [glob pattern]({% link docs/data/multiple_files/overview.md %}#multi-file-reads-and-globs). For example:

```sql
SELECT count(*) AS count
FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet';
```

| count |
|------:|
| 173   |

By using glob patterns, you can efficiently handle large datasets and perform comprehensive queries across multiple files, simplifying your data inspections and processing tasks.
Here, you can see how you can look for questions that contain the word “planet” in astronomy:

```sql
SELECT count(*) AS count
FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet'
WHERE question LIKE '%planet%';
```

| count |
|------:|
| 21    |

## Versioning and revisions

In Hugging Face repositories, dataset versions or revisions are different dataset updates. Each version is a snapshot at a specific time, allowing you to track changes and improvements. In git terms, it can be understood as a branch or specific commit.

You can query different dataset versions/revisions by using the following URL:

```text
hf://datasets/⟨my-username⟩/⟨my-dataset⟩@⟨my_branch⟩/⟨path_to_file⟩
```

For example:

```sql
SELECT *
FROM 'hf://datasets/datasets-examples/doc-formats-csv-1@~parquet/**/*.parquet';
```

|  kind   | sound |
|---------|-------|
| dog     | woof  |
| cat     | meow  |
| pokemon | pika  |
| human   | hello |

The previous query will read all parquet files under the `~parquet` revision. This is a special branch where Hugging Face automatically generates the Parquet files of every dataset to enable efficient scanning.

## Authentication

Configure your Hugging Face Token in the DuckDB Secrets Manager to access private or gated datasets.
First, visit [Hugging Face Settings – Tokens](https://huggingface.co/settings/tokens) to obtain your access token.
Second, set it in your DuckDB session using DuckDB’s [Secrets Manager]({% link docs/configuration/secrets_manager.md %}). DuckDB supports two providers for managing secrets:

### `CONFIG`

The user must pass all configuration information into the `CREATE SECRET` statement. To create a secret using the `CONFIG` provider, use the following command:

```sql
CREATE SECRET hf_token (
    TYPE HUGGINGFACE,
    TOKEN 'your_hf_token'
);
```

### `CREDENTIAL_CHAIN`

Automatically tries to fetch credentials. For the Hugging Face token, it will try to get it from `~/.cache/huggingface/token`. To create a secret using the `CREDENTIAL_CHAIN` provider, use the following command:

```sql
CREATE SECRET hf_token (
    TYPE HUGGINGFACE,
    PROVIDER CREDENTIAL_CHAIN
);
```
