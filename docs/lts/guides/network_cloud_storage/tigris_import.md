---
layout: docu
title: Tigris Import
---

## Prerequisites

For [Tigris](https://www.tigrisdata.com/), the [S3-compatible API](https://www.tigrisdata.com/docs/api/s3/) allows you to use DuckDB's S3 support to read and write from Tigris buckets.

This requires the [`httpfs` extension]({% link docs/lts/core_extensions/httpfs/overview.md %}), which can be installed using the `INSTALL` SQL command. This only needs to be run once.

## Credentials and Configuration

You will need to [generate an access key pair](https://www.tigrisdata.com/docs/iam/) and create an `S3` secret in DuckDB:

```sql
CREATE SECRET my_secret (
    TYPE s3,
    KEY_ID '⟨tid_xxxxxxxxxxxx⟩',
    SECRET '⟨tsec_xxxxxxxxxxxxxxxxxxxxxxxx⟩',
    REGION 'auto',
    ENDPOINT 'fly.storage.tigris.dev'
);
```

* A single endpoint (`fly.storage.tigris.dev`) serves all regions; requests are routed to the Tigris region nearest the caller. `REGION` is required for request signing but is not used for routing — set it to `auto`.
* `URL_STYLE` does not need to be set. Tigris uses virtual-hosted-style URLs, which is DuckDB's default for `TYPE s3`.

> Tip When DuckDB runs on a [Fly.io](https://fly.io/) Machine, requests to `fly.storage.tigris.dev` stay on Fly's internal network and are served from the same region as the Machine when possible.

## Querying

After setting up the Tigris credentials, you can query the data using DuckDB's built-in methods, such as `read_csv` or `read_parquet`:

```sql
SELECT * FROM 's3://⟨tigris-bucket-name⟩/⟨file⟩.csv';
SELECT * FROM read_parquet('s3://⟨tigris-bucket-name⟩/⟨file⟩.parquet');
```
