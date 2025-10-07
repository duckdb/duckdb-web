---
layout: post
title: "Announcing DuckDB 1.4.1 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-1-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-1-lts.png"
excerpt: "We are shipping DuckDB 1.4.1 LTS!"
tags: ["release"]
---

Today we are releasing DuckDB 1.4.1 LTS, the first bugfix release for a Long-Term Support (LTS) edition of DuckDB.
In this blog post, we highlight a few important fixes and improvements.
For the complete release notes, see the [release page on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.0).

> To install the new version, please visit the [installation page]({% link install/index.html %}). Note that it can take a few days to release some client libraries (e.g., R) due to the extra changes and review rounds required.

## AWS Improvements

The AWS extension received a number of improvements and bugfixes.
See the [AWS documentation page]({% link docs/stable/core_extensions/aws.md %}) for more details.

### Secret Validation

Since DuckDB v1.4.0, the AWS `credential_chain` provider looks for and require credentials during `CREATE SECRET` time, failing if absent/unavailable. Since, v1.4.1 this behavior can also be configured via the `VALIDATION` option as follows:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    VALIDATION 'exists'
);
```

Two validation modes are supported:

* `exists` (default) requires present credentials.
* `none` allows `CREATE SECRET` to succeed for credential_chains with no available credentials.

### S3 Default Region

Previously, setting the S3 region incorrectly could result in difficult-to-debug situations (`Unknown error for HTTP HEAD to ...`).

DuckDB v1.4.1 [removes `us-east-1` as the default S3 region](https://github.com/duckdb/duckdb/pull/19087) and returns a 301 error code if an incorrect region is used.

## Missing Data

Users reported two cases where DuckDB omitted some data:

* The Parquet reader had a [regression which caused it to omit some rows](https://github.com/duckdb/duckdb/issues/19131) when using predicate pushdown.
* In some cornercases, DuckDB's ART index, used for `CREATE INDEX`, [omitted some rows](https://github.com/duckdb/duckdb/issues/19190) in a non-deterministic fashion when running on multiple threads.

This release fixes these issues.

## Autoloading

In DuckDB v1.4.0, the [httpfs extension]({% link docs/stable/core_extensions/httpfs/overview.md %}) was not always autoloaded. For example, running:

```sql
COPY (SELECT 42 AS answer) TO 's3://my_bucket/my_file.parquet';
```

without loading httpfs manually returned the following error:

```console
Cannot open file "s3://my_bucket/my_file.parquet": No such file or directory
```

With v1.4.1, the autoloading works and DuckDB can read from the bucket right away.

## Docker Image

We now officially distribute a [Docker image](https://github.com/duckdb/duckdb-docker), so you can run DuckDB in a containerized environment:

```batch
docker run --rm -it -v "$(pwd):/workspace" -w /workspace duckdb/duckdb
```

```text
DuckDB v1.4.1 (Andium) b390a7c376
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D
```

For more details including operational considerations and using the UI, read the [Docker image page]({% link docs/stable/operations_manual/duckdb_docker.md %}).
