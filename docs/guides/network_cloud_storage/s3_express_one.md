---
layout: docu
title: S3 Express One
redirect_from:
  - /docs/guides/import/s3_express_one
---

In late 2023, AWS [announced](https://aws.amazon.com/about-aws/whats-new/2023/11/amazon-s3-express-one-zone-storage-class/) the [S3 Express One Zone](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-one-zone.html), a high-speed variant of traditional S3 buckets.
DuckDB can read S3 Express One buckets using the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}).

## Credentials and Configuration

The configuration of S3 Express One buckets is similar to [regular S3 buckets]({% link docs/guides/network_cloud_storage/s3_import.md %}) with one exception:
we have to specify the endpoint according to the following pattern:

```text
s3express-⟨availability zone⟩.⟨region⟩.amazonaws.com
```

where the `⟨availability zone⟩` (e.g., `use-az5`) can be obtained from the S3 Express One bucket's configuration page and the `⟨region⟩` is the AWS region (e.g., `us-east-1`).

For example, to allow DuckDB to use an S3 Express One bucket, configure the [Secrets manager]({% link docs/sql/statements/create_secret.md %}) as follows:

```sql
CREATE SECRET (
    TYPE S3,
    REGION 'us-east-1',
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    ENDPOINT 's3express-use1-az5.us-east-1.amazonaws.com'
);
```

## Instance Location

For best performance, make sure that the EC2 instance is in the same availability zone as the S3 Express One bucket you are querying. To determine the mapping between zone names and zone IDs, use the `aws ec2 describe-availability-zones` command.

* Zone name to zone ID mapping:

  ```bash
  aws ec2 describe-availability-zones --output json | \
      jq -r '.AvailabilityZones[] | select(.ZoneName == "us-east-1f") | .ZoneId'
  ```

  ```text
  use1-az5
  ```

* Zone ID to zone name mapping:

  ```bash
  aws ec2 describe-availability-zones --output json | \
      jq -r '.AvailabilityZones[] | select(.ZoneId == "use1-az5") | .ZoneName'
  ```

  ```text
  us-east-1f
  ```

## Querying

You can query the S3 Express One bucket as any other S3 bucket:

```sql
SELECT *
FROM 's3://express-bucket-name--use1-az5--x-s3/my-file.parquet';
```

## Performance

We ran two experiments on a `c7gd.12xlarge` instance using the [LDBC SF300 Comments `creationDate` Parquet file](https://blobs.duckdb.org/data/ldbc-sf300-comments-creationDate.parquet) file (also used in the [microbenchmarks of the performance guide]({% link docs/guides/performance/benchmarks.md %}#data-sets)).

<div class="narrow_table"></div>

| Experiment | File size | Runtime |
|:-----|--:|--:|
| Loading only from Parquet | 4.1 GB | 3.5s |
| Creating local table from Parquet | 4.1 GB | 5.1s |

The "loading only" variant is running the load as part of an [`EXPLAIN ANALYZE`]({% link docs/guides/meta/explain_analyze.md %}) statement to measure the runtime without account creating a local table, while the "creating local table" variant uses [`CREATE TABLE ... AS SELECT`]({% link docs/sql/statements/create_table.md %}#create-table--as-select-ctas) to create a persistent table on the local disk.
