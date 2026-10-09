---
layout: post
title: "A DuckDB Database with No Data in It"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/no-data.svg"
image: "/images/blog/thumbs/no-data.png"
excerpt: "A DuckDB database file does not have to hold any data. It can store nothing but view definitions that point at Parquet files on object storage, so a few hundred kilobytes behave like a shared catalog over a whole data lake. This post shows how to build one, host it, and attach it read-only."
tag: using-duckdb
---

A DuckDB database file does not have to contain any data. It can store nothing but [view]({% link docs/preview/sql/statements/create_view.md %}) definitions that point at files stored somewhere else, such as Parquet on object storage. The file stays a few hundred kilobytes no matter how large the data it describes, and anyone who attaches it sees a set of named relations that are ready to query.

Nikolas Goebel described this idea in [DuckDB doesn't need data](https://www.nikolasgoebel.com/2024/05/28/duckdb-doesnt-need-data), which argues that modern databases have separated where data is stored from how it is read, to the point that most databases no longer need to hold any data of their own. From that perspective, DuckDB becomes a browser for the data cloud, where you access a dataset through a URL rather than a copy on your own disk. 

In this blog post, we turn that idea into a small, shareable catalog.

## The Idea

A DuckDB table stores its rows inside the database file. A view stores only the text of a query. When you read the view, DuckDB runs that query and returns the current result. If the query reads a remote Parquet file, the data lives in object storage and the view holds only the instruction for how to read it.

A database file made entirely of such views contains no rows of its own. It is a catalog: a set of named, ready-to-query relations created over data that stays in its original location and format. You can publish that catalog as a curated semantic layer over a data lake, where the view definitions encode the joins, filters, and column names that consumers should use, without copying or moving the underlying data.

## Building a Catalog of Views

The examples use DuckDB's public train services dataset, which records one row for every stop a Dutch railway train makes. The data comes from the open datasets published by the [Rijden de Treinen *(Are the trains running?)* application](https://www.rijdendetreinen.nl/en/open-data/), and you can read it straight from its URL.

First, install the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) so that DuckDB can read over the network. This only needs to be run once.

```sql
INSTALL httpfs;
```

Now create a persistent database file and define a view over the remote data. Use a fully qualified location, a remote URL or an absolute path, so that the view resolves regardless of the client's working directory.

```sql
ATTACH 'rail_catalog.duckdb' AS rail;
USE rail;

CREATE VIEW services AS
    SELECT *
    FROM 'https://blobs.duckdb.org/train_services.parquet';
```

The catalog now exposes a `services` relation that reads from the remote file whenever it is queried.

```sql
SELECT departure_time, station_name, type
FROM rail.services
LIMIT 3;
```

| departure_time | station_name | type |
| --- | --- | --- |
| 2023-05-15 00:00:00 | Rotterdam Centraal | Intercity |
| 2023-05-15 00:13:00 | Delft | Intercity |
| 2023-05-15 00:29:00 | Den Haag HS | Intercity |

Because the file stores only the view definition, it stays small no matter how large the referenced dataset grows. The `train_services.parquet` file holds 380,959 rows, yet the catalog that reads it is a few hundred kilobytes.

## Hosting the Catalog

Upload `rail_catalog.duckdb` to any location that DuckDB can read over the network, for example an [`s3://`]({% link docs/preview/guides/network_cloud_storage/s3_import.md %}) bucket or an [`https://`]({% link docs/preview/guides/network_cloud_storage/http_import.md %}) endpoint. The same bucket that already holds the Parquet files is a convenient place to put it.

Sharing the catalog then means sharing one URL instead of a list of individual file paths. The recipient does not need to know how many files back each view or where they are stored, only the address of the catalog.

## Attaching the Catalog Read-Only

Consumers attach the catalog [read-only]({% link docs/preview/guides/network_cloud_storage/duckdb_over_https_or_s3.md %}) and query the views as if they were local tables. Each query reads the current data from the referenced files, so the result reflects whatever is in object storage at that moment.

```sql
ATTACH 'https://example.com/rail_catalog.duckdb' AS rail (READ_ONLY);

SELECT station_name, count(*) AS calls
FROM rail.services
GROUP BY station_name
ORDER BY calls DESC
LIMIT 3;
```

| station_name | calls |
| --- | --- |
| Utrecht Centraal | 7663 |
| Amsterdam Centraal | 7591 |
| Zwolle | 5013 |

Consumers need the `httpfs` extension and, for `s3://` sources, [credentials]({% link docs/preview/guides/network_cloud_storage/s3_import.md %}#credentials-and-configuration) that grant access to the underlying data. DuckDB reads only the columns and row groups a query needs, so a filtered or aggregated query over a large remote dataset does not download the whole thing.

## Surviving Changes to the Data Layout

Because a query reads the view rather than the files directly, the publisher can change the files without changing the query. The consumer runs the same query before and after.

Suppose the single Parquet file becomes too large and the publisher splits it into one file per year. Updating the view to read a directory of files is a one-line change in the catalog, and consumers notice nothing.

```sql
CREATE OR REPLACE VIEW services AS
    SELECT *
    FROM read_parquet('s3://my-bucket/rail/services/year=*/*.parquet');
```

A view can also keep the schema stable when the files change. If a later batch of files renames `station_name` to `station`, the view can map the new column back to the name consumers already use.

```sql
CREATE OR REPLACE VIEW services AS
    SELECT
        * EXCLUDE (station),
        station AS station_name
    FROM read_parquet('s3://my-bucket/rail/services/*.parquet');
```

If you repartition the files or move them to a new bucket, you only have to update the catalog. Anyone querying it keeps running the same queries as before.

## When to Use It

Use this pattern when you want to share a dataset without sending the recipient a long list of individual file paths, and when the data is already in a format DuckDB reads well, such as [Parquet]({% link docs/preview/data/parquet/overview.md %}). Readers get a set of named relations to query, and the publisher can change the file layout without breaking those queries.

Note the following limitations:

* Consumers must be able to access both the catalog file and every data source that its views reference.
* Connections over HTTPS and the S3 API are [read-only]({% link docs/preview/guides/network_cloud_storage/duckdb_over_https_or_s3.md %}#limitations), so the catalog cannot be modified in place. To change a view, edit a local copy and upload it again.
* Query performance depends on the [network and the layout of the referenced files]({% link docs/preview/guides/performance/file_formats.md %}). The tips for [querying remote files]({% link docs/preview/guides/performance/how_to_tune_workloads.md %}#querying-remote-files) apply.

## Conclusion

A DuckDB file that holds only views is a small catalog you can share as a single URL. The data stays in its original location, the publisher can change how it is stored, and the reader gets a stable set of relations to query.

For the full reference, see the [Share a DuckDB Database That Only Stores Views]({% link docs/preview/guides/network_cloud_storage/duckdb_views_only.md %}) guide.
