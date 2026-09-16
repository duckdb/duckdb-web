---
layout: post
title: "DuckDB Skills for Claude Code"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/claude-skills.svg"
image: "/images/blog/thumbs/claude-skills.png"
excerpt: "The duckdb-skills plugin gives Claude Code a growing number of skills that use the DuckDB CLI to read data files, run queries, convert formats, explore object storage, work with spatial data, search the documentation and recall earlier sessions."
tags: ["using DuckDB"]
---

More likely than not, you've been using AI tools such as Claude Code for day-to-day work. You may have noticed that when AI needs to look at a data file, it makes use of Python, writes a small script, runs it, and then reads the output.
This works, although it is slow, and the agent guesses column names and types and doesn't really check them.

Since DuckDB can read pretty much any file directly, the DuckDB team has written a set of skills that can tell your AI to use the DuckDB CLI instead. Whether the data is a file on your machine, a file on the internet or an Iceberg table behind a login, to DuckDB it is still a table or a catalog that it can query and process efficiently.

This post describes what is in the plugin and how it works.

## Installation

In Claude Code, add the repository as a plugin marketplace and install the plugin:

```text
/plugin marketplace add duckdb/duckdb-skills
/plugin install duckdb-skills@duckdb-skills
```

The skills are then available as `/duckdb-skills:⟨skill-name⟩`{:.language-sql .highlight} in all subsequent sessions. You need the [DuckDB CLI]({% link install/index.html %}) installed; if it is not found, the skills will offer to install it.

## An Example Interaction

Here is what a short exchange looks like when you ask a question about a data file:

```text
You: How many taxi trips in that Parquet file were longer than 10 miles?

Claude runs:
    SELECT count(*) FROM 'trips.parquet' WHERE distance > 10;

DuckDB:
    Binder Error: Referenced column "distance" not found
    Candidate bindings: "trip_distance"

Claude reads the error, checks the columns and retries:
    SELECT count(*) FROM 'trips.parquet' WHERE trip_distance > 10;

DuckDB:
    ┌──────────────┐
    │ count_star() │
    ├──────────────┤
    │       184362 │
    └──────────────┘

Claude: 184,362 of the trips were longer than 10 miles.
```

What you see in the chat is a conversation in natural language between you and Claude. Underneath it runs a second conversation in SQL between Claude and DuckDB. People and Claude are both at home in natural language, and Claude and DuckDB are both at home in SQL, so each step uses the language that fits it. When a query fails, Claude reads the error, adjusts the SQL and tries again, as in the retry above.

The two tools cover different work. DuckDB gives exact answers to exact questions, and those exact answers give Claude a firm base to reason from and to turn back into a short, readable reply for you.

## What's in the Plugin

Each skill wraps a common data task behind a `/duckdb-skills:⟨skill-name⟩`{:.language-sql .highlight} slash command, grouped here by what they do. 

You do not have to type the slash command, though: each skill also has a description that tells Claude Code when it applies, so you can simply ask in plain language (for example, “convert this CSV to Parquet” or “how far is the nearest station?”) and the agent will pick the right skill on its own.

### Reading, Querying and Converting Data

**`attach-db`** attaches a DuckDB database and records it in the session state, so the other skills can use it:

* “Attach my_analytics.duckdb and show me its tables.”

**`query`** runs SQL or a plain-English question against attached databases or a file:

* “Show me the first 10 rows of the sales table.”
* “What are the top 5 customers by revenue?”

**`read-file`** reads and profiles any data file (CSV, JSON, Parquet, Avro, Excel, spatial, SQLite, Jupyter) on local disk or in S3, GCS, Azure or HTTPS:

* “What columns does variants.parquet have?”
* “How many rows are in the CSV file at that URL?”

**`convert-file`** converts a file from one format to another:

* “Convert sales.csv to Parquet.”
* “Save data.json as an Excel file.”

### Remote and Spatial Data

**`s3-explore`** lists and queries data on S3, R2, GCS, MinIO or any S3-compatible storage without downloading it:

* “What's in s3://my-bucket/?”
* “How many rows are in s3://my-bucket/data.parquet?”

**`spatial`** answers spatial questions: distances, nearest neighbors, spatial joins and geographic lookups, including free Overture Maps data:

* “What are the 5 closest cafes to this point?”
* “Which districts in districts.geojson overlap?”

### Documentation and Session Context

**`duckdb-docs`** searches the DuckDB and [DuckLake](https://ducklake.select/) documentation and blog posts:

* “How do window functions work in DuckDB?”
* “How do I read a CSV with custom delimiters?”

**`read-memories`** searches past Claude Code session logs for earlier decisions, conventions and open TODOs:

* “What did we decide about the DuckDB schema in earlier sessions?”

### Setup

**`install-duckdb`** installs or updates extensions, including community extensions:

* “Install the spatial and httpfs extensions.”
* “Update my DuckDB extensions.”

The skills share a single per-project `state.sql` file, a plain SQL script of `ATTACH`, `USE` and `LOAD` statements, secrets and macros, so a session can be restored with `duckdb -init state.sql`.

For session-state details and local development instructions, see the [README](https://github.com/duckdb/duckdb-skills#readme).

## Conclusion

The duckdb-skills plugin is available at [github.com/duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills). If you run into problems or have suggestions, please [open an issue](https://github.com/duckdb/duckdb-skills/issues). For DuckDB-related errors, it helps to include the output of `duckdb --version` and the full error message.
