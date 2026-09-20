---
layout: post
title: "DuckDB Now Ships Inside dbt v2"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-dbt.svg"
image: "/images/blog/thumbs/duckdb-dbt.png"
excerpt: "dbt v2, which runs on the new Rust-based Fusion engine, is the first dbt release that ships with a built-in DuckDB adapter. This post covers setup, DuckLake and Iceberg catalogs, querying dbt's Parquet metadata with DuckDB, plus other v2 features that matter to DuckDB users, including migrating to dbt v2."
tags: ["using DuckDB"]
---

[dbt](https://www.getdbt.com/) is the tool many data teams use to manage their SQL transformations: you write each model as a `SELECT` statement, and dbt works out the order to run them in and builds the resulting tables and views in your database. 

[dbt-duckdb](https://github.com/duckdb/dbt-duckdb/blob/master/README.md), the dbt adapter for DuckDB, received its [first pull request](https://github.com/duckdb/dbt-duckdb/pull/3) on August 27, 2021, and in the meantime [has 1.4k stars on GitHub](https://github.com/duckdb/dbt-duckdb). You install one Python package, point it at a file, and you have a working project, without having needed to sign up to (and pay for) servers or warehouses. 

When dbt Labs [announced the new Rust-based Fusion engine](https://www.getdbt.com/blog/dbt-launch-showcase-2025-recap) in May 2025, DuckDB initially wasn't supported out of the box. That has changed with dbt v2, which ships with a DuckDB adapter built in. Here is how to set it up and what else is new.

## Background

dbt Labs announced the new Rust-based Fusion engine on [May 28, 2025](https://www.getdbt.com/licenses-faq#may-28-2025). Two days later, a user, [ran-codes](https://github.com/ran-codes), opened a [GitHub issue](https://github.com/dbt-labs/dbt/issues/13193) asking for a DuckDB adapter:

<blockquote class="quote">
<p><b>"There is a huge community utilizing the DuckDB adaptor to run DBT. For me personally, I was able to learn and start using DBT just because of the light-weight setup for the dbt-duckdb workflow and it has allowed me to get over the learning curve to start using DBT."</b></p>
<p class="quote-author">— <a href="https://github.com/dbt-labs/dbt/issues/13193">ran-codes, on GitHub</a></p>
</blockquote>

At the time of this writing, the issue resulted in 146 ❤️ and 21 👍 reactions. The adapter is now built into dbt v2.

On June 1, 2026, dbt Labs released the [first alpha of dbt Core 2.0](https://docs.getdbt.com/blog/dbt-core-v2-is-here), built on the same foundations as Fusion, and open-sourced a large part of the Fusion code. That code moved into the dbt-core repository under Apache 2.0, and the dbt-fusion repository was archived. There are two distributions of v2, both free to install locally and both running on the same engine.

[dbt 2.0.0](https://github.com/dbt-labs/dbt/releases/tag/v2.0.0) was released on September 14, 2026. That release also renamed the CLI branding from Fusion and dbt-core to dbt (proprietary) and dbt-oss (open source). So “Fusion” is now mostly the name of the engine, and the thing you install is just called dbt.

## Setup

In dbt v1, an adapter was a standalone Python package. In v2, adapters live inside a Rust monorepo and connect through [ADBC drivers](https://docs.getdbt.com/docs/contribute-dbt-adapters-v2). 

The DuckDB adapter is now built into v2, so after you [install dbt](https://docs.getdbt.com/docs/local/install-dbt?version=2.0) there is nothing else to add. dbt also publishes a [DuckDB quickstart guide](https://docs.getdbt.com/guides/duckdb) for getting a project running locally. 

A basic profile looks the same as before:

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ./warehouse.duckdb
```

## DuckLake and Iceberg Catalogs

v2 adds [catalog support](https://docs.getdbt.com/docs/build/iceberg/adapters/duckdb-iceberg-support) that the Python adapter doesn't have. dbt's DuckDB docs flag it as "dbt v2 only"; the legacy Python adapter instead attached DuckLake through the profile's [`attach` block](https://docs.getdbt.com/reference/resource-configs/duckdb-configs). 

With `catalogs.yml` you can configure [DuckLake](https://ducklake.select/), Iceberg REST, and local filesystem catalogs, with [catalog-aware materializations](https://github.com/dbt-labs/dbt/releases/tag/v2.0.0-alpha.4). This requires the v2 engine with the `use_catalogs_v2` flag enabled and isn't available in the Python adapter. dbt [generates and runs the `ATTACH` statements](https://docs.getdbt.com/docs/build/iceberg/adapters/duckdb-iceberg-support) for you.

A DuckLake catalog is defined in `catalogs.yml`:

```yaml
catalogs:
  - name: local_lake
    type: ducklake
    table_format: default
    config:
      duckdb:
        metadata_path: metadata.ducklake
        data_path: s3://my-bucket/lake
```

Enable the flag in `dbt_project.yml`, then reference the catalog from a model:

```yaml
flags:
  use_catalogs_v2: true
```

```sql
{% raw %}{{ config(materialized = 'table', catalog_name = 'local_lake') }}{% endraw %}
select * from {% raw %}{{ ref('customers') }}{% endraw %}
```

The example above follows the DuckDB [catalog support documentation](https://docs.getdbt.com/docs/build/iceberg/adapters/duckdb-iceberg-support).

## dbt Metadata as Parquet

v2 also [writes its metadata as Parquet](https://docs.getdbt.com/docs/build/dbt-information-schema?version=2.0) as an alternative to the large JSON files, and these (as well as the large JSON files) can be queried directly with DuckDB. 

dbt calls this the Information Schema, a v2 feature that stores the manifest as Parquet instead of JSON. Running `dbt parse --generate-info-schema` writes a set of Parquet files to `target/info_schema/v1/`, so you can list your models without parsing `manifest.json`. 

These are the same artifacts dbt ships as test fixtures, so you can query one straight from the dbt repository using DuckDB without running dbt first:

```sql
SELECT name, materialized, schema_name
FROM 'https://raw.githubusercontent.com/dbt-labs/dbt/main/crates/dbt-docs-server/web/src/test/fixtures/parquet/dbt.models.parquet';
```

For the above, this lists the three models in the fixture, along with how each is materialized and the schema it lands in:

```text
┌─────────────────┬──────────────┬─────────────┐
│      name       │ materialized │ schema_name │
│     varchar     │   varchar    │   varchar   │
├─────────────────┼──────────────┼─────────────┤
│ my_second_model │ view         │ main        │
│ my_third_model  │ view         │ main        │
│ my_first_model  │ view         │ main        │
└─────────────────┴──────────────┴─────────────┘
```

Why would you do this? On a large project, the JSON [`manifest.json`](https://docs.getdbt.com/reference/artifacts/manifest-json) can grow to hundreds of megabytes, and reading it means loading and parsing the whole file just to answer a simple question. (Although, [DuckDB can do this too](https://duckdb.org/docs/lts/data/json/json_functions).) The Parquet files are columnar, so DuckDB reads only the columns you select and can filter them without materializing everything in memory. That makes it practical to ask questions about the project itself: which models are materialized as tables rather than views, which schema each one lands in, or which models are missing tests.

This is useful in a CI check or an audit script, where you want to enforce conventions across a project without standing up dbt or the warehouse. Because the files are located on disk after a `dbt parse`, you can point DuckDB at them directly and treat your project's metadata as just another dataset to query.

## SQL Comprehension and Column-Level Lineage

dbt models [combine SQL with Jinja templating](https://docs.getdbt.com/docs/build/jinja-macros), which earlier versions compiled into a query string [without inspecting the SQL itself](https://www.getdbt.com/blog/dbt-labs-acquires-sdf-labs). The v2 engine instead has a [native understanding of SQL across multiple engine dialects](https://docs.getdbt.com/docs/fusion/about-fusion). That means it can catch invalid column references and type mismatches [before a query reaches the warehouse](https://docs.getdbt.com/docs/fusion/about-fusion), rather than surfacing them only when the model runs against DuckDB.

That same analysis produces [column-level lineage](https://docs.getdbt.com/docs/collaborate/column-level-lineage) locally, without a dbt platform account. Running [`dbt compile`](https://docs.getdbt.com/reference/commands/compile) with `--generate-info-schema --static-analysis strict` writes a `dbt.column_lineage` file into the [Information Schema](https://docs.getdbt.com/docs/build/dbt-information-schema?version=2.0) Parquet directory covered above, so you can trace which upstream columns feed each model with a plain DuckDB query.

## Faster Local Development

v2 is distributed as a [compiled Rust binary](https://docs.getdbt.com/blog/dbt-core-v2-is-here) rather than a set of Python packages, so there is no Python dependency tree to resolve before a run. dbt describes the engine as the foundation for [fast builds](https://docs.getdbt.com/docs/fusion/about-fusion) on large projects, where parsing and compiling happen inside that single native executable.

The [dbt VS Code extension](https://docs.getdbt.com/docs/install-dbt-extension) builds on the same SQL comprehension. As you edit models, it gives you [autocomplete, hover information, and inline errors](https://docs.getdbt.com/docs/dbt-extension-features), so mistakes show up in the editor instead of after a round trip to the warehouse. The extension is [published on the VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=dbtLabsInc.dbt).

## Bundled DuckDB and Native Functions

v2 ships a [pinned DuckDB version](https://github.com/dbt-labs/dbt/releases/tag/v2.0.0-alpha.3), rather than relying on whatever version pip resolves for the [Python adapter](https://github.com/duckdb/dbt-duckdb/blob/master/README.md). Pinning the version is what enables the [read-write Iceberg REST catalog support](https://github.com/dbt-labs/dbt/releases/tag/v2.0.0-alpha.4) [described above](#ducklake-and-iceberg-catalogs), which depends on features from that specific DuckDB build.

Bundling DuckDB also lets dbt push work down into the database. Some adapter logic that used to be a SQL macro is now [implemented as a native DuckDB extension function](https://github.com/dbt-labs/dbt/releases/tag/v2.0.0-alpha.4), such as `array_except`, which is exposed as `sf_array_except`.

## Migrating

A low-risk first step is to test the v2 parser while still on dbt v1.12, which ships an [opt-in v2 parser](https://docs.getdbt.com/reference/global-configs/parsing#opt-in-v2-parser). dbt's docs describe this as a way to catch compatibility issues early before fully migrating. Run the following command to check whether your project parses:

```batch
dbt parse --use-v2-parser
```

If it does, follow the [install guide](https://docs.getdbt.com/docs/local/install-dbt?version=2.0) to switch. The [dbt-autofix](https://github.com/dbt-labs/dbt-autofix) package handles many of the required changes, and there is an [upgrade guide for v2](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-v2).

## Conclusion

The DuckDB adapter is now part of dbt v2 and needs no separate install, and the Python versions of dbt Core remain available if you'd rather not move or not move yet. Either way, running dbt on DuckDB means you develop, test, and publish your models on your own machine.

Beyond removing the separate install, v2 is where DuckDB picks up several new capabilities: catalog support for DuckLake and Iceberg, metadata written as queryable Parquet, native SQL comprehension with column-level lineage, and a pinned DuckDB build.

If you've already been using dbt-duckdb, upgrading to v2 means one less package to install and all of the above to build on. And if you haven't, a single dbt install and a few lines of profile are enough to start building models directly on your laptop, without servers or warehouses.
