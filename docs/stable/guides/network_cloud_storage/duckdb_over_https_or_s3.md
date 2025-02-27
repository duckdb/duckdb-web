---
layout: docu
redirect_from:
- /docs/guides/network_cloud_storage/duckdb_over_https_or_s3
title: Attach to a DuckDB Database over HTTPS or S3
---

You can establish a read-only connection to a DuckDB instance via HTTPS or the S3 API.

## Prerequisites

This guide requires the [`httpfs` extension]({% link docs/stable/extensions/httpfs/overview.md %}), which can be installed using the `INSTALL httpfs` SQL command. This only needs to be run once.

## Attaching to a Database over HTTPS

To connect to a DuckDB database via HTTPS, use the [`ATTACH` statement]({% link docs/stable/sql/statements/attach.md %}) as follows:

```sql
ATTACH 'https://blobs.duckdb.org/databases/stations.duckdb' AS stations_db;
```

> Since DuckDB version 1.1, the `ATTACH` statement creates a read-only connection to HTTP endpoints.
> In prior versions, it is necessary to use the `READ_ONLY` flag.

Then, the database can be queried using:

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

## Attaching to a Database over the S3 API

To connect to a DuckDB database via the S3 API, [configure the authentication]({% link docs/stable/guides/network_cloud_storage/s3_import.md %}#credentials-and-configuration) for your bucket (if required).
Then, use the [`ATTACH` statement]({% link docs/stable/sql/statements/attach.md %}) as follows:

```sql
ATTACH 's3://duckdb-blobs/databases/stations.duckdb' AS stations_db;
```

> Since DuckDB version 1.1, the `ATTACH` statement creates a read-only connection to HTTP endpoints.
> In prior versions, it is necessary to use the `READ_ONLY` flag.

The database can be queried using:

```sql
SELECT count(*) AS num_stations
FROM stations_db.stations;
```

| num_stations |
|-------------:|
| 578          |

> Connecting to S3-compatible APIs such as the [Google Cloud Storage (`gs://`)]({% link docs/stable/guides/network_cloud_storage/gcs_import.md %}#attaching-to-a-database) is also supported.

## Limitations

* Only read-only connections are allowed, writing the database via the HTTPS protocol or the S3 API is not possible.