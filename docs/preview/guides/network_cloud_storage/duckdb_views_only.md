---
layout: docu
title: Share a DuckDB Database That Only Stores Views
---

A DuckDB database file does not have to contain any data: it can store only [view]({% link docs/preview/sql/statements/create_view.md %}) definitions that point at remote data such as Parquet files on object storage. The resulting file is only a few hundred kilobytes, yet it behaves like a shared catalog: anyone who attaches it sees a set of named, ready-to-query relations, while the underlying data stays in its original location and format.

This is useful for publishing a curated “semantic layer” over a data lake, where the view definitions encode the joins, filters, and column names that consumers should use, without copying or moving the data itself.

## Prerequisites

This guide requires the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}), which can be installed using the `INSTALL httpfs` SQL command. This only needs to be run once.

## Building the Catalog

Create a persistent database file and define views that reference the remote data. Use fully qualified locations (remote URLs or absolute paths) so that the views resolve regardless of the client's working directory:

```sql
ATTACH 'catalog.duckdb' AS catalog;
USE catalog;

CREATE VIEW services AS
    SELECT *
    FROM read_parquet('s3://my-bucket/rail/services/*.parquet');

CREATE VIEW stations AS
    SELECT *
    FROM read_parquet('s3://my-bucket/rail/stations.parquet');
```

Because the file stores only view definitions, it stays small no matter how large the referenced datasets are.

## Hosting the Catalog

Upload the `catalog.duckdb` file to any location that DuckDB can read over the network, for example an [`s3://`]({% link docs/preview/guides/network_cloud_storage/s3_import.md %}) bucket or an [`https://`]({% link docs/preview/guides/network_cloud_storage/http_import.md %}) endpoint.

## Querying the Catalog

Consumers attach the catalog [read-only]({% link docs/preview/guides/network_cloud_storage/duckdb_over_https_or_s3.md %}) and query the views as if they were local tables. Each query reads the current data from the referenced remote files:

```sql
ATTACH 'https://example.com/catalog.duckdb' AS catalog (READ_ONLY);

SELECT count(*) AS num_stations
FROM catalog.stations;
```

Consumers need the `httpfs` extension and, for `s3://` sources, [credentials]({% link docs/preview/guides/network_cloud_storage/s3_import.md %}#credentials-and-configuration) that grant access to the underlying data.

## Limitations

* Consumers must be able to access both the catalog file and every data source that its views reference.
* Connections over HTTPS and the S3 API are [read-only]({% link docs/preview/guides/network_cloud_storage/duckdb_over_https_or_s3.md %}#limitations), so the catalog cannot be modified in place.
* Query performance depends on the [network and the layout of the referenced files]({% link docs/preview/guides/performance/file_formats.md %}). The tips for [querying remote files]({% link docs/preview/guides/performance/how_to_tune_workloads.md %}#querying-remote-files) apply.
