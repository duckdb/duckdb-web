---
layout: post
title: "DuckDB Skills for Claude Code"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/macbook-pro.svg"
image: "/images/blog/thumbs/macbook-pro.png"
excerpt: "We published duckdb-skills, a Claude Code plugin that teaches the agent to use the DuckDB CLI for reading files, running queries, looking up documentation and searching its own session logs."
tags: ["using DuckDB"]
---

*TL;DR: The [`duckdb-skills`](https://github.com/duckdb/duckdb-skills) plugin gives Claude Code a growing number of skills that use the DuckDB CLI to read data files, run queries, convert formats, explore object storage, work with spatial data, search the documentation and recall earlier sessions.*

More likely than not, you've been using AI tools such as Claude Code for day-to-day work. You may have noticed that when AI needs to look at a data file, it makes use of Python, writes a small script, runs it, and then reads the output.
This works, although it is slow, and the agent guesses column names and types and doesn't really check them.
Since DuckDB can read pretty much any file directly, the DuckDB team has written a set of skills that can tell your AI to use the DuckDB CLI instead.

This post describes what is in the plugin and how it works.

## Installation

In Claude Code, add the repository as a plugin marketplace and install the plugin:

```text
/plugin marketplace add duckdb/duckdb-skills
/plugin install duckdb-skills@duckdb-skills
```

The skills are then available as `/duckdb-skills:<skill-name>` in all subsequent sessions. You need the [DuckDB CLI](https://duckdb.org/install/) installed; if it is not found, the skills will offer to install it.

## What's in the Plugin

Each skill wraps a common data task behind a `/duckdb-skills:<skill-name>` slash command, grouped here by what they do.

Reading, querying and converting data:

* **`read-file`** reads and profiles any data file (CSV, JSON, Parquet, Avro, Excel, spatial, SQLite, Jupyter) on local disk or in S3, GCS, Azure or HTTPS.
    * `/duckdb-skills:read-file variants.parquet what columns does it have?`
    * `/duckdb-skills:read-file https://example.com/data.csv how many rows?`
* **`query`** runs SQL or a plain-English question against attached databases or a file.
    * `/duckdb-skills:query FROM sales LIMIT 10`
    * `/duckdb-skills:query "what are the top 5 customers by revenue?"`
* **`convert-file`** converts a file from one format to another.
    * `/duckdb-skills:convert-file sales.csv sales.parquet`
    * `/duckdb-skills:convert-file data.json data.xlsx`
* **`attach-db`** attaches a DuckDB database and records it in the session state.
    * `/duckdb-skills:attach-db my_analytics.duckdb`

Remote and spatial data:

* **`s3-explore`** lists and queries data on S3, R2, GCS, MinIO or any S3-compatible storage without downloading it.
    * `/duckdb-skills:s3-explore s3://my-bucket/`
    * `/duckdb-skills:s3-explore s3://my-bucket/data.parquet how many rows?`
* **`spatial`** answers spatial questions: distances, nearest neighbors, spatial joins and geographic lookups, including free Overture Maps data.
    * `/duckdb-skills:spatial what are the 5 closest cafes to this point?`
    * `/duckdb-skills:spatial districts.geojson which districts overlap?`

Documentation and session context:

* **`duckdb-docs`** searches the DuckDB and [DuckLake](https://ducklake.select/) documentation and blog posts.
    * `/duckdb-skills:duckdb-docs window functions`
    * `/duckdb-skills:duckdb-docs "how do I read a CSV with custom delimiters?"`
* **`read-memories`** searches past Claude Code session logs for earlier decisions, conventions and open TODOs.
    * `/duckdb-skills:read-memories duckdb --here`

Setup:

* **`install-duckdb`** installs or updates extensions, including community extensions.
    * `/duckdb-skills:install-duckdb spatial httpfs`
    * `/duckdb-skills:install-duckdb --update`

The skills share a single per-project `state.sql` file, a plain SQL script of `ATTACH`, `USE` and `LOAD` statements, secrets and macros, so a session can be restored with `duckdb -init state.sql`.

For session-state details and local development instructions, see the [README](https://github.com/duckdb/duckdb-skills#readme).

## Conclusion

The duckdb-skills plugin is available at [github.com/duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills). If you run into problems or have suggestions, please [open an issue](https://github.com/duckdb/duckdb-skills/issues). For DuckDB-related errors, it helps to include the output of `duckdb --version` and the full error message.
