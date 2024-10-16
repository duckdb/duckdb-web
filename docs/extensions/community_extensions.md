---
layout: docu
title: Community Extensions 
---

DuckDB recently launched a [Community Extensions repository](https://github.com/duckdb/community-extensions).
For details, see the [announcement blog post]({% post_url 2024-07-05-community-extensions %}).

## User Experience

We are going to use the [`h3` extension](https://github.com/isaacbrodsky/h3-duckdb) as our example.
This extension implements [hierarchical hexagonal indexing](https://github.com/uber/h3) for geospatial data.

Using the DuckDB Community Extensions repository, you can install and load the `h3` extension as follows:

```sql
INSTALL h3 FROM community;
LOAD h3;
```

Then, you can instantly start using it. Note that the sample data is 500 MB:

```sql
SELECT
    h3_latlng_to_cell(pickup_latitude, pickup_longitude, 9) AS cell_id,
    h3_cell_to_boundary_wkt(cell_id) AS boundary,
    count() AS cnt
FROM read_parquet('https://blobs.duckdb.org/data/yellow_tripdata_2010-01.parquet')
GROUP BY cell_id
HAVING cnt > 10;
```

On load, the extension’s signature is checked, both to ensure platform and versions are compatible, and to verify that the source of the binary is the community extensions repository. Extensions are built, signed and distributed for Linux, macOS, Windows, and WebAssembly. This allows extensions to be available to any DuckDB client using version 1.0.0 and upcoming versions.

For more details, see the [`h3` extension’s documentation](https://community-extensions.duckdb.org/extensions/h3.html).

## Developer Experience

From the developer’s perspective, the Community Extensions repository performs the steps required for publishing extensions, including building the extensions for all relevant [platforms]({% link docs/dev/building/platforms.md %}), signing the extension binaries and serving them from the repository.

For the [maintainer of `h3`](https://github.com/isaacbrodsky/), the publication process required performing the following steps:

1. Sending a PR with a metadata file `description.yml` contains the description of the extension:

   ```yaml
   extension:
     name: h3
     description: Hierarchical hexagonal indexing for geospatial data
     version: 1.0.0
     language: C++
     build: cmake
     license: Apache-2.0
     maintainers:
       - isaacbrodsky

   repo:
     github: isaacbrodsky/h3-duckdb
     ref: 3c8a5358e42ab8d11e0253c70f7cc7d37781b2ef
   ```

2. The CI will build and test the extension. The checks performed by the CI are aligned with the [`extension-template` repository](https://github.com/duckdb/extension-template), so iterations can be done independently.

3. Wait for approval from the DuckDB Community Extension repository’s maintainers and for the build process to complete.

## Security Considerations

See the [Securing Extensions page]({% link docs/operations_manual/securing_duckdb/securing_extensions.md %}) for details.

## List of Community Extensions

See the [DuckDB Community Extensions repository site](https://community-extensions.duckdb.org/).
