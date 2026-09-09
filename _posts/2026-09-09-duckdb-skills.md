---
layout: post
title: "DuckDB Skills for Claude Code"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/macbook-pro.svg"
image: "/images/blog/thumbs/macbook-pro.png"
excerpt: "We published duckdb-skills, a Claude Code plugin that teaches the agent to use the DuckDB CLI for reading files, running queries, looking up documentation and searching its own session logs."
tags: ["using DuckDB"]
---

*TL;DR: Did you know that there are DuckDB skills for Claude Code? The [`duckdb-skills`](https://github.com/duckdb/duckdb-skills) plugin contains a growing number of skills that use the DuckDB CLI to read data files, run queries, attach databases, convert between formats, explore object storage, work with spatial data, search the documentation, install extensions and search previous Claude Code sessions.*

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

The skills are then available as `/duckdb-skills:<skill-name>` in all subsequent sessions.
To update to the latest version, update the marketplace first and then the plugin:

```text
/plugin marketplace update duckdb-skills
/plugin update duckdb-skills@duckdb-skills
```

You need the [DuckDB CLI](https://duckdb.org/install/) installed.
If it is not found, the skills will offer to install it.
We have also submitted the plugin to the Anthropic marketplace; once it is listed, it will show up in the **Discover** tab of `/plugin`.

## Skills

### `read-file`

Reads a data file and answers questions about it.
The file can be CSV, JSON, Parquet, Avro, Excel, a spatial format, SQLite, a Jupyter notebook, and so on, and it can be on local disk or on S3, GCS, Azure or an HTTPS URL.
The skill ships a `read_any` table macro that picks the right reader based on the file extension.

```text
/duckdb-skills:read-file variants.parquet what columns does it have?
/duckdb-skills:read-file s3://my-bucket/data.parquet describe the schema
/duckdb-skills:read-file https://example.com/data.csv how many rows?
```

### `convert-file`

Converts a data file from one format to another, for example CSV to Parquet, Parquet to Excel or a spatial format to GeoJSON.
It is also useful when the agent needs to write a binary format that it cannot produce on its own.

```text
/duckdb-skills:convert-file sales.csv sales.parquet
/duckdb-skills:convert-file data.json data.xlsx
```

### `query`

Runs a query, either against databases attached in the session or directly against a file.
You can pass SQL or a question in plain English.
The skill uses the [friendly SQL](https://duckdb.org/docs/stable/sql/dialect/friendly_sql) features of DuckDB, e.g., `FROM`-first syntax and `GROUP BY ALL`.

```text
/duckdb-skills:query FROM sales LIMIT 10
/duckdb-skills:query "what are the top 5 customers by revenue?"
/duckdb-skills:query FROM 'exports.csv' WHERE amount > 100
```

### `attach-db`

Attaches a DuckDB database file and lists its tables, columns and row counts.
It also writes the `ATTACH` statement to the session state file (see below), so the database is available in the other skills without attaching it again.
You can attach several databases; each call appends to the state file.

```text
/duckdb-skills:attach-db my_analytics.duckdb
```

### `s3-explore`

Explores and queries data on S3, Cloudflare R2, GCS, MinIO or any S3-compatible storage.
It can list the contents of a bucket and preview or query remote Parquet, CSV and JSON files without downloading them first.

```text
/duckdb-skills:s3-explore s3://my-bucket/
/duckdb-skills:s3-explore s3://my-bucket/data.parquet how many rows?
```

### `spatial`

Answers questions about spatial data: distances, nearest neighbors, spatial joins and geographic lookups.
It reads formats such as GeoJSON, Shapefile, GeoPackage, GPX and GeoParquet, and can pull free global data from Overture Maps on S3 without an API key.

```text
/duckdb-skills:spatial what are the 5 closest cafes to this point?
/duckdb-skills:spatial districts.geojson which districts overlap?
```

### `duckdb-docs`

Searches the DuckDB and [DuckLake](https://ducklake.select/) documentation and blog posts.
This uses a full-text search index hosted on duckdb.org, queried over HTTPS, so there is nothing to set up.
If you prefer, the index can be cached locally.
The `query`, `read-file` and `read-memories` skills call `duckdb-docs` when they hit a DuckDB error, which cuts down on trial-and-error.

```text
/duckdb-skills:duckdb-docs window functions
/duckdb-skills:duckdb-docs "how do I read a CSV with custom delimiters?"
```

### `read-memories`

Claude Code keeps logs of previous sessions on disk.
This skill searches them for earlier decisions, conventions and open TODOs, so a new session can pick up where an old one left off.
If the result set is large, it is written to a temporary DuckDB file that you can query further.

```text
/duckdb-skills:read-memories duckdb --here
```

### `install-duckdb`

Installs or updates extensions.
[Community extensions](https://duckdb.org/community_extensions/) can be installed with the `name@repo` syntax.
With `--update`, the skill also checks whether the CLI itself is on the latest stable version.

```text
/duckdb-skills:install-duckdb spatial httpfs
/duckdb-skills:install-duckdb gcs@community
/duckdb-skills:install-duckdb --update
```

## Session State

The skills share a single `state.sql` file per project.
It is an ordinary SQL script with `ATTACH`, `USE` and `LOAD` statements, [secrets](https://duckdb.org/docs/stable/configuration/secrets_manager) and macro definitions.
The first time a skill needs it, you are asked where to put it: either in the project directory as `.duckdb-skills/state.sql` (which you may want to add to `.gitignore`), or under your home directory as `~/.duckdb-skills/<project>/state.sql`.

The file is append-only and every statement in it is idempotent, so it is safe to run repeatedly.
Restoring a session is simply:

```bash
duckdb -init state.sql
```

Because it is plain SQL, you can open it in an editor to see exactly what the agent has set up, and fix it by hand if needed.

## Local Development

To work on the skills, clone the repository and start Claude Code with the plugin loaded from disk:

```bash
git clone https://github.com/duckdb/duckdb-skills.git
cd duckdb-skills
claude --plugin-dir .
```

Changes to `skills/*/SKILL.md` are picked up when you start a new conversation or re-run the slash command.

## Platform Support

We have tested the skills on macOS and Linux.
On Windows, some of the shell commands and path handling may not work yet.
We intend to fix this in a later release.

## Conclusion

The duckdb-skills plugin is available at [github.com/duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills).
If you run into problems or have suggestions, please [open an issue](https://github.com/duckdb/duckdb-skills/issues).
For DuckDB-related errors, it helps if you include the output of `duckdb --version` and the full error message.
