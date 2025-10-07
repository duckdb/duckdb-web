---
layout: post
title: "Announcing DuckDB 1.4.1 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-1-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-1-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.1, the first bugfix release of our LTS edition."
tags: ["release"]
---

In this blog post, we highlight a few important fixes and convenience improvements in DuckDB v1.4.1 LTS.
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.1).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Iceberg Improvements

The DuckDB [`iceberg` extension]({% link docs/stable/core_extensions/iceberg/overview.md %}) received a number of patches:

* You can now attach to an Iceberg REST Catalog and specify an access delegation mode. This fixes a bug when using catalogs that did not vend credentials. The `ATTACH` statement will now look like this:

    ```sql
    ATTACH '⟨warehouse_name⟩' AS my_datalake (
        TYPE iceberg,
        ENDPOINT '⟨endpoint⟩',
        ACCESS_DELEGATION_MODE '⟨delegation_mode_option⟩',
        SECRET '⟨my_secret⟩'
    );
    ```

    The current `ACCESS_DELEGATION_MODE` options are `vended_credentials` (default) and `none`.

* When attaching to AWS-managed REST Catalogs, the `http_timeout` setting is now respected.
* Attempting to rename or replace a table within a transaction now throws a clear error message.
* AWS Athena can now read Iceberg tables written by DuckDB.

## AWS Improvements

The `aws` extension received a number of changes, which make it easier to configure and troubleshoot.
See the [`aws` documentation page]({% link docs/stable/core_extensions/aws.md %}) for more details.

### Secret Validation

Since DuckDB v1.4.0, the AWS `credential_chain` provider looks for any required credentials during `CREATE SECRET` time, failing if absent/unavailable. Since v1.4.1 this behavior can also be configured via the `VALIDATION` option as follows:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    VALIDATION 'exists'
);
```

Two validation modes are supported:

* `exists` (default) requires present credentials.
* `none` allows `CREATE SECRET` to succeed for `credential_chains` with no available credentials.

### S3 Default Region

Previously, setting the S3 region incorrectly could result in difficult-to-debug situations (`Unknown error for HTTP HEAD to ...`).

DuckDB v1.4.1 [removes `us-east-1` as the default S3 region](https://github.com/duckdb/duckdb/pull/19087) and returns a 301 error code if an incorrect region is used.

## Fixes for Missing Data

Users reported two cases where DuckDB omitted some data:

* The Parquet reader had a [regression which caused it to omit some rows](https://github.com/duckdb/duckdb/issues/19131) when using predicate pushdown on certain string columns.
* In certain edge cases, DuckDB’s ART index could [omit rows](https://github.com/duckdb/duckdb/issues/19190) rows non-deterministically when running on multiple threads. Note that this index is only used when you manually specify an index with [`CREATE INDEX`]({% link docs/stable/sql/indexes.md %}).

DuckDB v1.4.1 fixes both of these issues.

## Autoloading

In DuckDB v1.4.0, the [`httpfs` extension]({% link docs/stable/core_extensions/httpfs/overview.md %}) was not always autoloaded. For example, running:

```sql
COPY (SELECT 42 AS answer) TO 's3://my_bucket/my_file.parquet';
```

without loading `httpfs` manually returned the following error:

```console
Cannot open file "s3://my_bucket/my_file.parquet": No such file or directory
```

With v1.4.1, autoloading works and DuckDB can write to the bucket right away.

## Docker Image

We now officially distribute a [Docker image](https://hub.docker.com/r/duckdb/duckdb/), making it easy to run DuckDB in a containerized environment:

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
