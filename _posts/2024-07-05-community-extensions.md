---
layout: post
title: "DuckDB Community Extensions"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/community-extensions.svg"
image: "/images/blog/thumbs/community-extensions.png"
excerpt: "DuckDB extensions can now be published via the [DuckDB Community Extensions repository](https://github.com/duckdb/community-extensions). The repository makes it easier for users to install extensions using the `INSTALL ⟨extension name⟩ FROM community` syntax. Extension developers avoid the burdens of compilation and distribution."
tags: ["extensions"]
---

## DuckDB Extensions

### Design Philosophy

One of the main design goals of DuckDB is *simplicity*, which – to us – implies that the system should be rather nimble, very light on dependencies, and generally small enough to run on constrained platforms like [WebAssembly]({% link docs/api/wasm/overview.md %}). This goal is in direct conflict with very reasonable user requests to support advanced features like spatial data analysis, vector indexes, connectivity to various other databases, support for data formats, etc. Baking all those features into a monolithic binary is certainly possible and the route some systems take. But we want to preserve DuckDB’s simplicity. Also, shipping all possible features would be quite excessive for most users because no use cases require *all* extensions at the same time (the “Microsoft Word paradox”, where even power users only use a few features of the system, but the exact set of features vary between users).

To achieve this, DuckDB has a powerful extension mechanism, which allows users to add new functionalities to DuckDB. This mechanism allows for registering new functions, supporting new file formats and compression methods, handling new network protocols, etc. In fact, many of DuckDB’s popular features are implemented as extensions: the [Parquet reader]({% link docs/data/parquet/overview.md %}), the [JSON reader]({% link docs/data/json/overview.md %}), and the [HTTPS/S3 connector]({% link docs/extensions/httpfs/overview.md %}) all use the extension mechanism.

### Using Extensions

Since [version 0.3.2](https://github.com/duckdb/duckdb/releases/tag/v0.3.2), we have already greatly simplified the discovery and installation by hosting them on a centralized extension repository. So, for example, to install the [spatial extension]({% link docs/extensions/spatial/overview.md %}), one can just run the following commands using DuckDB’s SQL interface:

```sql
INSTALL spatial; -- once
LOAD    spatial; -- on each use
```

What happens behind the scenes is that DuckDB downloads an extension binary suitable to the current operating system and processor architecture (e.g., macOS on ARM64) and stores it in the `~/.duckdb` folder. On each `LOAD`, this file is loaded into the running DuckDB instance, and things happily continue from there. Of course, for this to work, we compile, sign and host the extensions for a rather large and growing list of processor architecture – operating system combinations. This mechanism is already heavily used, currently, we see around six million extension downloads *each week* with a corresponding data transfer volume of around 40 terabytes!

Until now, publishing third-party extensions has been a *difficult process* which required the extension developer to build the extensions in their repositories for a host of platforms. Moreover, they were unable to sign the extensions using official keys, forcing users to use the `allow_unsigned_extensions` option that disables signature checks which is problematic in itself.

## DuckDB Community Extensions

Distributing software in a safe way has never been easier, allowing us to reach a wide base of users across pip, conda, cran, npm, brew, etc. We want to provide a similar experience both to users who can easily grab the extension they will want to use, and developers who should not be burdened with distribution details. We are also interested in lowering the bar to package utilities and scripts as a DuckDB extension, empowering users to package useful functionality connected to their area of expertise (or pain points).

We believe that fostering a community extension ecosystem is the next logical step for DuckDB. That’s why we’re very excited about launching our [Community Extension repository](https://github.com/duckdb/community-extensions/) which was [announced at the Data + AI Summit](https://youtu.be/wuP6iEYH11E?t=275).

For users, this repository allows for easy discovery, installation and maintenance of community extensions directly from the DuckDB SQL prompt. For developers, it greatly streamlines the publication process of extensions. In the following, we’ll discuss how the new extension repository enhances the experiences of these groups.

### User Experience

We are going to use the [`h3` extension](https://github.com/isaacbrodsky/h3-duckdb) as our example. This extension implements [hierarchical hexagonal indexing](https://github.com/uber/h3) for geospatial data.

Using the DuckDB Community Extensions repository, you can now install and load the `h3` extension as follows:

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

The `h3` extension’s documentation is available at <https://duckdb.org/community_extensions/extensions/h3>.

### Developer Experience

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

## Published Extensions

To show that it’s feasible to publish extensions, we reached out to a few developers of key extensions. At the time of the publication of this blog post, the DuckDB Community Extensions repository already contains the following extensions.

<div class="narrow_table"></div>

| Name | Description |
|----|------------|
| [crypto](https://github.com/rustyconover/duckdb-crypto-extension) | Adds cryptographic hash functions and [HMAC](https://en.wikipedia.org/wiki/HMAC). |
| [h3](https://github.com/isaacbrodsky/h3-duckdb) | Implements hierarchical hexagonal indexing for geospatial data. |
| [lindel](https://github.com/rustyconover/duckdb-lindel-extension) | Implements linearization/delinearization, Z-Order, Hilbert and Morton curves. |
| [prql](https://github.com/ywelsch/duckdb-prql) | Allows running [PRQL](https://prql-lang.org/) commands directly within DuckDB. |
| [scrooge](https://github.com/pdet/Scrooge-McDuck) | Supports a set of aggregation functions and data scanners for financial data. |
| [shellfs](https://github.com/rustyconover/duckdb-shellfs-extension) | Allows shell commands to be used for input and output. |

DuckDB Labs and the DuckDB Foundation do not vet the code within community extensions and, therefore, cannot guarantee that DuckDB community extensions are safe to use. The loading of community extensions can be explicitly disabled with the following one-way configuration option:

```sql
SET allow_community_extensions = false;
```

For more details, see the documentation’s [Securing DuckDB page]({% link docs/operations_manual/securing_duckdb/securing_extensions.md %}#community-extension).

## Summary and Looking Ahead

In this blog post, we introduced the DuckDB Community Extensions repository, which allows easy installation of third-party DuckDB extensions.

We are looking forward to continuously extending this repository. If you have an idea for creating an extension, take a look at the already published extension source codes, which provide good examples of how to package community extensions, and join the `#extensions` channel on our [Discord](https://discord.duckdb.org/).
Once you have an extension, please contribute it via a [pull request](https://github.com/duckdb/community-extensions/pulls).

Finally, we would like to thank the early adopters of DuckDB’s extension mechanism and Community Extension repository. Thanks for iterating with us and providing feedback to us.
