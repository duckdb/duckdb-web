---
layout: post
title: "DuckDB 1.5.3: Not an Ordinary Patch Release"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-3.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-3.png"
excerpt: "We are releasing DuckDB version v1.5.3 with Quack as a core extension, support for Quack in DuckLake, several new features for Iceberg, AWS and HTTPS, as well as many other fixes."
tags: ["release"]
---

In this blog post, we highlight a few important features shipped in DuckDB v1.5.3, the third patch release in [DuckDB's v1.5 line]({% post_url 2026-03-09-announcing-duckdb-150 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.3).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## What's New

### Quack

On May 12, we introduced Quack, our new remote protocol that turns DuckDB into a client-server database.
If you are new to Quack and don't know where to start, check out the following resources:

* For a high-level overview, see the [Quack explainer page]({% link quack/index.html %}).
* For the rationale and history behind Quack, along with an introduction of the protocol and its features, see the [announcement blog post]({% post_url 2026-05-12-quack-remote-protocol %}).
* For the reference manual and setup guide, check out the [Quack documentation]({% link docs/current/quack/overview.md %}).

Starting from DuckDB v1.5.3, we ship Quack as a [core extension]({% link docs/current/core_extensions/quack.md %}). This means that you can now start using Quack right away from any client running DuckDB:
it will be transparently autoinstalled and [autoloaded]({% link docs/current/extensions/overview.md %}#autoloading-extension) on first use.

<!-- markdownlint-disable MD001 -->

<div class="duck-diagram" markdown="1">

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB #1

```sql
CALL quack_serve(
    'quack:localhost',
    token = 'super_secret'
);

CREATE TABLE hello AS
    FROM VALUES ('world') v(s);
```

</div>

<div class="duck-diagram-arrow">quack:</div>

<div class="duck-diagram-box" markdown="1">

#### <svg class="icon"><use href="#database-01"></use></svg> DuckDB #2

```sql
CREATE SECRET (
    TYPE quack,
    TOKEN 'super_secret'
);

ATTACH 'quack:localhost' AS remote;
FROM remote.hello;
```

</div>

</div>

<!-- markdownlint-enable MD001 -->

Please note that Quack is still in beta state and breaking changes may happen in the protocol, in function names, etc.
We plan to release the production-ready version of Quack together with [DuckDB v2.0]({% link release_calendar.md %}) in fall 2026.

### DuckLake with Quack

DuckLake now supports DuckDB with Quack as its catalog database ([ducklake#1151](https://github.com/duckdb/ducklake/pull/1151)).

TODO

### AWS

The [AWS extension]({% link docs/current/core_extensions/aws.md %}) now supports the [`web_identity` chain type for IAM Roles for Service Accounts (IRSA) support](https://github.com/duckdb/duckdb-aws/pull/136).
This was made possible through a contribution by community member [Marcel Steinbach (@mst)](https://github.com/mst).

[RDS IAM](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html) support (ongoing)

### `HTTP_PROXY` Variable for the HTTPS Extension

Setting the `HTTP_PROXY` environment variable now sets the `http_proxy` DuckDB configuration option ([duckdb#22541](https://github.com/duckdb/duckdb/pull/22541)).
This option makes sure that extensions installs are also passing through the proxy, which may come in handy in e.g. environments that use firewalls.

Note that since the [introduction of `curl` into DuckDB's network stack]({% post_url 2026-03-09-announcing-duckdb-150 %}#network-stack), `curl` automatically uses `HTTP_PROXY` and `HTTPS_PROXY`, so now implicitly also DuckDB handles those parameters when the `httpfs` extension is loaded with the default `curl` backend.

### Iceberg

The DuckDB-Iceberg extension has shipped a number of features between DuckDB v1.5.2 and v1.5.3. Most notably:

* `MERGE INTO` is now supported for Iceberg tables ([duckdb-iceberg#788](https://github.com/duckdb/duckdb-iceberg/pull/788))
* The `INSERT` and `UPDATE` statements are now supported on partitioned Iceberg tables with a `truncate` or `bucket` transform ([duckdb-iceberg#879](https://github.com/duckdb/duckdb-iceberg/pull/879))
* [CTAS]({% link docs/current/sql/statements/create_table.md %}#create-table--as-select-ctas) statements in DuckDB-Iceberg using [ADBC]({% link docs/current/clients/adbc.md %}) are now possible via ([duckdb-iceberg#974](https://github.com/duckdb/duckdb-iceberg/pull/974))
* We added the `iceberg_schema_properties`, `set_iceberg_schema_properties`, and `remove_iceberg_schema_properties` functions to allow getting, setting, and removing Iceberg schema properties ([duckdb-iceberg#960](https://github.com/duckdb/duckdb-iceberg/pull/960))
* `ALTER TABLE` support has been added for Iceberg tables ([duckdb-iceberg#932](https://github.com/duckdb/duckdb-iceberg/pull/932), [duckdb-iceberg#928](https://github.com/duckdb/duckdb-iceberg/pull/928), [duckdb-iceberg#924](https://github.com/duckdb/duckdb-iceberg/pull/924), [duckdb-iceberg#912](https://github.com/duckdb/duckdb-iceberg/pull/912), [duckdb-iceberg#904](https://github.com/duckdb/duckdb-iceberg/pull/904), [duckdb-iceberg#853](https://github.com/duckdb/duckdb-iceberg/pull/853), [duckdb-iceberg#985](https://github.com/duckdb/duckdb-iceberg/pull/985), [duckdb-iceberg#981](https://github.com/duckdb/duckdb-iceberg/pull/981))
* Support for the `GEOMETRY` type has been added for Iceberg tables ([duckdb-iceberg#968](https://github.com/duckdb/duckdb-iceberg/pull/968), [#902](https://github.com/duckdb/duckdb-iceberg/pull/902))

## Linux

The [`jemalloc` allocator]({% link docs/current/internals/jemalloc.md %}) is now part of core DuckDB ([duckdb#22603](https://github.com/duckdb/duckdb/pull/22603)) as a static third-party library which is included and linked by default on Linux.
Previously `jemalloc` was a statically-linked extension – the new packaging is cleaner since other DuckDB extensions can be loaded dynamically.

## Coming Up

We have two events coming up in the next few weeks:

**DuckCon #7.** On June 24, we'll host our next user conference, [DuckCon #7]({% link _events/2026-06-24-duckcon7.html %}), in Amsterdam's beautiful [Royal Tropical Institute](https://www.kit.nl/about-us/).

**Ubuntu Summit Talk.** Next week, Gábor Szárnyas of DuckDB Labs will give a talk titled [“DuckDB: Not Quack Science”]({% link _library/2026-05-27-duckdb-not-quack-science.md %}) at the [Ubuntu Summit](https://ubuntu.com/summit). Yes, his talk will include the new [Quack](#quack) protocol.

## Conclusion

This post is a short summary of the changes in v1.5.3. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.3).
