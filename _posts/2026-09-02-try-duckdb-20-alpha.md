---
layout: post
title: "Try DuckDB v2.0-alpha"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-preview-2-0.svg"
image: "/images/blog/thumbs/duckdb-preview-2-0.png"
excerpt: "DuckDB's development in Amsterdam has started getting DuckDB v2.0 ready for release in October. If you like shiny new things, try out the alpha releases now and report anything that might not be working as expected!"
tags: ["release"]
---

## The State of DuckDB v2.0

A few weeks ago, we published a [preview of DuckDB v2.0]({% post_url 2026-08-17-duckdb-20-highlights %}).

Today, we just branched off `v2.0-cyanoptera` from the `main` development branch in the `duckdb/duckdb` repository. This marks a feature freeze – in the coming weeks, development work will be targeted on testing, bugfixing, and iterating toward the next best DuckDB release to date: v2.0 Cyanoptera, with the release [projected for mid-October]({% link release_calendar.md %}).

The Duck ecosystem has `duckdb/duckdb` at the center, since that's a dependency for most other work, so stabilizing that unlocks work across other repositories. There are two main directions: clients and extensions.

## Clients

On the client side, Python and CLI are already available in alpha versions.
To install the command-line client on Linux or macOS, run:

```batch
curl https://install.duckdb.org | DUCKDB_VERSION=alpha sh
```

```batch
~/.duckdb/cli/latest/duckdb -c "SELECT version() AS version;"
```

```text
┌───────────────────┐
│      version      │
│      varchar      │
├───────────────────┤
│ v2.0.0-alpha39764 │
└───────────────────┘
```

To install the Python client, run:

```batch
pip install duckdb --pre --upgrade
```

```batch
python3 -c "import duckdb; print(duckdb.version())"
```

This prints the versions of both the Python client (currently 1.6-dev) and of the underlying DuckDB library (2.0.0-alpha):

```text
1.6.0.dev365 (with duckdb 2.0.0-alpha38615)
```

We'll add other clients gradually to this list. Each new client that moves to 2.0 improves coverage for the DuckDB project, given that different clients will often have very different test environments and setups.

## Extensions

In DuckDB v2.0, the [`quack` extension]({% link quack/index.html %}) will move from version 0.x to 1.0. The new version will unlock higher throughput for queries (both server to client *and* client to server), and better compatibility.

Other core extensions, like `httpfs`, `ducklake`, `iceberg` or `spatial` are also available in the alpha stage – please report any issues that you might encounter.

Community extensions can already be tested by providing a `ref_next` SHA, and that will allow extensions to be tested against the `v2.0-cyanoptera` branch before the release date. If no `ref_next` is provided, the `ref` SHA will be used once v2.0.0 is finalized.

## Can I Help?

Yes, you can! DuckDB alpha clients are explicitly **not** production ready, but you can already install them and throw some SQL queries at them to see whether your existing workloads work. Most are expected to be fine, some are expected to complete visibly faster, and some might result in an error. For the next few weeks, we are particularly interested in the latter group: are there environments, situations or queries where DuckDB v2.0 alpha releases are not there yet?

If you find an issue, please open a bug report, either to duckdb/duckdb or to the relevant client or extension, and submit a reproducible issue.

DuckDB's main strength is its community: [given enough eyeballs, all bugs are shallow](https://en.wikipedia.org/wiki/Linus%27s_law), and your bug reports translate to stability gains for every user.
