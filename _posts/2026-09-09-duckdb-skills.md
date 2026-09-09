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

When an AI agent needs to look at a data file, it often reaches for Python, writes a small script, runs it and reads the output. This works, but it is slow, and the agent tends to guess column names and types rather than check them. Since DuckDB reads pretty much any file directly, the DuckDB team built a set of Claude Code skills that point the agent at the DuckDB CLI instead.

## Installation

In Claude Code, add the repository as a plugin marketplace and install the plugin:

```text
/plugin marketplace add duckdb/duckdb-skills
/plugin install duckdb-skills@duckdb-skills
```

The skills are then available as `/duckdb-skills:<skill-name>` in all subsequent sessions. You need the [DuckDB CLI](https://duckdb.org/install/) installed; if it is not found, the skills will offer to install it.

## What's in the Plugin

Each skill wraps a common data task behind a slash command, for example reading a file, running a query, converting between formats, exploring S3, answering spatial questions, searching the DuckDB and [DuckLake](https://ducklake.select/) docs, and recalling past Claude Code sessions. The skills share a single per-project `state.sql` file, a plain SQL script of `ATTACH`, `USE` and `LOAD` statements, secrets and macros, so a session can be restored with `duckdb -init state.sql`.

For the full list of skills, usage examples, session-state details and local development instructions, see the [README](https://github.com/duckdb/duckdb-skills#readme).

## Platform Support

The skills have been tested on macOS and Linux. On Windows, some shell commands and path handling may not work yet; we intend to address this in a later release.

## Conclusion

The duckdb-skills plugin is available at [github.com/duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills). If you run into problems or have suggestions, please [open an issue](https://github.com/duckdb/duckdb-skills/issues). For DuckDB-related errors, it helps to include the output of `duckdb --version` and the full error message.
