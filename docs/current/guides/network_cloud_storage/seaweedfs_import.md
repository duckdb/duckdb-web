---
layout: docu
title: SeaweedFS Import
---

## Prerequisites

For [SeaweedFS](https://github.com/seaweedfs/seaweedfs), the S3-compatible gateway allows you to use DuckDB's S3 support to read and write from SeaweedFS buckets.

This requires the [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}), which can be installed using the `INSTALL` SQL command. This only needs to be run once.

To try SeaweedFS locally, create a file `s3config.json` with the S3 credentials:

```json
{
  "identities": [
    {
      "name": "analyst",
      "credentials": [
        {
          "accessKey": "your_access_key_id",
          "secretKey": "your_secret_access_key"
        }
      ],
      "actions": ["Admin", "Read", "Write", "List", "Tagging"]
    }
  ]
}
```

Then start the whole SeaweedFS stack in one container and create a bucket:

```bash
docker run -d --name seaweedfs -p 8333:8333 \
    -v "$(pwd)/s3config.json:/etc/seaweedfs/s3config.json" \
    chrislusf/seaweedfs:latest \
    mini -dir=/data -s3.config=/etc/seaweedfs/s3config.json

echo "s3.bucket.create -name ⟨your-bucket⟩" | \
    docker exec -i seaweedfs weed shell -master=localhost:9333
```

The S3 endpoint listens on port 8333.

## Credentials and Configuration

Create an `S3` secret with the credentials from the SeaweedFS S3 configuration:

```sql
CREATE SECRET my_secret (
    TYPE s3,
    KEY_ID '⟨your_access_key_id⟩',
    SECRET '⟨your_secret_access_key⟩',
    ENDPOINT '⟨seaweedfs-host⟩:8333',
    URL_STYLE 'path',
    USE_SSL false
);
```

* SeaweedFS serves path-style requests, so set `URL_STYLE` to `path`. No wildcard DNS is needed.
* SeaweedFS does not require a region, so `REGION` can be omitted.
* Set `USE_SSL false` for a plain-HTTP endpoint such as the local setup above; omit it when the gateway runs behind TLS.

## Querying

After setting up the SeaweedFS credentials, you can query the data using DuckDB's built-in methods, such as `read_csv` or `read_parquet`:

```sql
SELECT * FROM 's3://⟨your-bucket⟩/⟨file⟩.csv';
SELECT * FROM read_parquet('s3://⟨your-bucket⟩/⟨file⟩.parquet');
```

Writing works the same way, including glob reads over the result:

```sql
COPY (SELECT 42 AS answer) TO 's3://⟨your-bucket⟩/sample/answer.parquet';
SELECT * FROM read_parquet('s3://⟨your-bucket⟩/sample/*.parquet');
```

SeaweedFS also supports Iceberg: table buckets store the table data as Parquet files, and the gateway's built-in Iceberg REST Catalog serves the table metadata. See the [SeaweedFS catalog example]({% link docs/current/core_extensions/iceberg/catalogs.md %}#seaweedfs) to query Iceberg tables through it.
