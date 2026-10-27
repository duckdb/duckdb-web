---
layout: docu
redirect_from:
- /docs/current/clients/cli/agent_mode
- /docs/lts/clients/cli/agent_mode
- /docs/preview/clients/cli/agent_mode
title: Agent Mode
---

> New Agent mode was introduced in DuckDB 2.0.

Agent mode renders the CLI's output for consumption by an AI coding agent rather than a human at a terminal. It produces compact [Markdown]({% link docs/2.0/clients/cli/output_formats.md %}) tables with explicit result limits, machine-readable errors, and progress information on `stderr`, so that an agent can run queries and reliably parse the results.

For the motivation behind agent mode and a benchmark of its effect, see the [“Agent Mode in the DuckDB CLI” blog post]({% post_url 2026-10-09-agent-mode %}).

## Activating Agent Mode

Agent mode is activated automatically when all of the following hold:

* A known AI agent environment variable (such as `AI_AGENT`) is set.
* The standard output is not a terminal (for example, it is piped to another process).
* No [output mode]({% link docs/2.0/clients/cli/output_formats.md %}) flag (such as `-csv` or `-json`) was passed.

You can also control agent mode explicitly:

* The `-agent` and `-no-agent` [command line arguments]({% link docs/2.0/clients/cli/arguments.md %}) force the mode on or off.
* The `DUCKDB_AGENT_MODE` environment variable forces the mode on (`1`) or off (`0`).

The command line flags take precedence over the environment variable. To hide the startup line that announces agent mode, set `.startup_text none` as the first line in `~/.duckdbrc`.

For example, to force agent mode on when running a single command:

```batch
duckdb -agent -c "SELECT 42 AS answer;"
```

To force it off:

```batch
duckdb -no-agent -c "SELECT 42 AS answer;"
```

## Output Format

In agent mode, DuckDB:

* Renders results as compact Markdown tables.
* Prints a footer with the row count and, when the whole result was read, an order-independent hash of the result.
* Emits errors as JSON on `stderr`.
* Renders compact query plans and cost estimates.
* Prints an estimate line and progress on `stderr` for a query that reads more than 1,000,000 rows.

By default, a result of up to 1,000 rows and 10,000 bytes is rendered whole; a larger result is rendered as its first and last rows together with the total row count. Cells are truncated at 500 characters.

These limits can be adjusted with [dot commands]({% link docs/2.0/clients/cli/dot_commands.md %}):

| Dot command           | Description                                                     |
| --------------------- | -------------------------------------------------------------- |
| `.maxrows ⟨count⟩`    | Maximum number of rows to render whole (`-1` for all)          |
| `.maxbytes ⟨count⟩`   | Maximum number of bytes of rows to render whole (`0` for all)  |
| `.maxcellwidth ⟨count⟩` | Maximum number of characters per cell (`0` for all)          |

## Tips for Agents

The `.help agent` command prints a summary of agent mode. A few things that help when driving DuckDB programmatically:

* `SET max_execution_time = ⟨milliseconds⟩`{:.language-sql .highlight} bounds how long a query may run.
* `DESCRIBE ⟨query⟩` returns the result columns without running the query.
* [`SUMMARIZE ⟨table⟩`]({% link docs/2.0/sql/statements/summarize.md %}) returns summary statistics for a table.
* `.tables` lists the available tables.
* `duckdb_functions()` returns function descriptions and examples.
