---
layout: post
title: "Agent Mode in the DuckDB CLI"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/agent-mode.svg"
image: "/images/blog/thumbs/agent-mode.png"
excerpt: "The DuckDB v2.0 CLI has an agent mode that gets AI coding agents to a correct result faster and with fewer tokens. When the CLI detects an agent, it prints compact Markdown tables instead of padded boxes, says clearly when a result was cut, stops runaway queries early and reports errors as JSON. Long queries announce their expected cost before they start, so the agent can decide whether to wait."
tags: ["using DuckDB"]
---

The DuckDB CLI was built for a person sitting at a terminal. Its default renderer pads columns so they line up, draws borders around the result and prints the column types under the names:

```text
┌────────────┬───────┬────────┬───────────────┐
│    name    │   n   │ total  │  avg_amount   │
│  varchar   │ int64 │ int128 │ decimal(10,2) │
├────────────┼───────┼────────┼───────────────┤
│ customer_0 │     3 │    777 │        259.00 │
│ customer_1 │     3 │    888 │        296.00 │
└────────────┴───────┴────────┴───────────────┘
```

For a large result, it shows the first and last 20 rows with a row of dots in the middle. A person sees the dots and knows that rows are missing.

Today, many CLI invocations do not come from a person at all. Coding agents such as Claude Code, Codex, Cursor, Gemini CLI and GitHub Copilot run `duckdb -c "..."` once per shell call, capture stdout through a pipe and pass the text to a language model. This has quickly become a common way to use DuckDB. This reader differs from a person in a few ways:

* It has no terminal, so there is no scrolling and no pager.
* It cannot ask for more. Whatever was printed is all it gets.
* It pays for every token it reads, including padding and border characters.
* It handles errors by pattern matching on text.

For this reader, the box renderer is a poor fit. The alignment padding costs tokens and carries no information for a model. A truncated result also looks a lot like a complete one. The footer says `(40 shown)`, but a model can skim past that line and then draw conclusions from data it never saw.

Agent mode changes the CLI’s defaults for this reader. This post describes how the CLI detects an agent, what changes in the output and how to try it.

> Agent mode ships with DuckDB v2.0.

## Detecting an Agent

Agents mark the commands they run with environment variables. There is no single convention for this yet, so the shell checks a list of them:

| Variable | Set by |
| -------- | ------ |
| `AI_AGENT`, `AGENT` | Claude Code, Goose, Amp |
| `CLAUDECODE` | Claude Code |
| `CODEX_CI`, `CODEX_SANDBOX`, `CODEX_THREAD_ID` | Codex |
| `CURSOR_AGENT` | Cursor |
| `GEMINI_CLI` | Gemini CLI |
| `COPILOT_AGENT`, `COPILOT_CLI`, `COPILOT_AGENT_SESSION_ID` | GitHub Copilot |

Agent mode turns on when three things are true: one of these variables is set, stdout is not a terminal, and no output format was given on the command line. If you pass `-csv`, `-json` or `-markdown`, you asked for a specific format, and agent mode stays out of the way entirely.

Two flags override detection. `-agent` forces the mode on and `-no-agent` forces it off. The two combine with format flags, so `duckdb -agent -csv` keeps the agent behavior and only changes how the rows are printed. The `.show` command reports whether the mode is active and which agent was detected:

```text
agent: claude-code
```

Not every agent sets a variable. For those, a run that fails while writing to a pipe prints one hint line on stderr, as long as no agent was identified and neither flag was given:

```text
hint: -agent renders errors as JSON and results compactly for AI coding agents (duckdb -help lists all options)
```

An agent that nobody told about the mode can find it this way the first time something goes wrong.

## What Changes in Agent Mode

Everything below is a default. Explicit settings such as `.mode`, `.maxrows`, `EXPLAIN (FORMAT ...)` or anything in your `.duckdbrc` still take precedence.

### Compact Tables

Results are printed as Markdown tables without alignment padding, with the column type in the header cell:

```text
| name:VARCHAR | n:BIGINT | total:HUGEINT | avg_amount:DECIMAL(10,2) |
|---|---|---|---|
| customer_0 | 3 | 777 | 259.00 |
| customer_1 | 3 | 888 | 296.00 |
```

A model reads the `|` separators and does not need the columns lined up. Since this is still valid Markdown, a person reading the agent’s transcript gets a rendered table. On typical results this format is 25 to 65% smaller than the box output, with the largest savings on wide results.

### Large Results

Printing every row would avoid silent truncation, but a million rows is 17 MB on the pipe. Agent mode prints a result of up to 1,000 rows and 10,000 bytes in full. Anything larger becomes a sample of the first and last 20 rows around an explicit marker row, with a footer that says what happened:

```text
| 19 | customer_19 | 13.3 |
| … 4960 rows omitted … |
| 4980 | customer_30 | 86.0 |
...
first 20 and last 20 of 5000 rows (.maxbytes 0 for all), hash 7389c2f5ff3cefb6
```

The footer also tells the reader how to get the rest. The limits can be changed with `.maxrows N` and `.maxbytes N`, where `-1` or `0` means no limit. Long cell values are cut at 500 characters with a visible marker such as `…(+4500 chars)`, adjustable with `.maxcellwidth N`.

### Stopping Early

The compact table needs no column widths, so the result can be streamed. Once the cap is reached, the remaining rows are only counted and hashed. After 100,000 more rows, the query is stopped and the count is reported as a lower bound. For example:

```sql
FROM range(1_000_000_000);
```

This returns in 30 milliseconds with the footer `first 20 of at least 102400 rows (query stopped early; .maxrows -1 for all)`.

### A Hash of the Result

The footer carries a hash of the entire result, including the rows past the cap. The hash does not depend on row order and distinguishes `NULL` from the string `'NULL'`. An agent that wants to know whether a result changed after an edit can compare two footers instead of printing two results. The footer is printed for empty results, for results of 10 rows or more, and whenever the output was capped. It is left out when the query was stopped early, because the hash would not cover the whole result.

### Errors as JSON

Errors go to stderr as JSON, using the existing `errors_as_json` setting. Errors raised by the shell itself, such as an unknown dot command, are wrapped in the same structure:

```json
{"exception_type":"Binder","exception_message":"Referenced column \"foo\" not found in FROM clause!\nCandidate bindings: \"bar\"","error_subtype":"COLUMN_NOT_FOUND","location":"[7,3]","position":"7","name":"foo"}
```

We drop the `candidates` field, because the message already lists the candidates. Without that change, a single “no matching function” error weighs 2.7 kB.

### Compact Query Plans

`EXPLAIN` defaults to a new `compact` format with one operator per line, indented by depth. Estimates, actual row counts and timings go in parentheses, followed by the operator’s properties:

```text
UNGROUPED_AGGREGATE (est=1) Aggregates: count_star()
  HASH_JOIN (est=0) Join Type: INNER; Conditions: range = range
    FILTER (est=2) Expression: (r > 2)
      RANGE (est=10) Function: RANGE
    FILTER (est=1) Expression: (s > 2)
      RANGE (est=5) Function: RANGE
```

`EXPLAIN ANALYZE` starts with a summary line such as `QUERY (time=0.0012s, read=1.2 MB)`. This is a regular format, so you can use `EXPLAIN (FORMAT compact)` outside agent mode too.

### Cost Estimates and Progress

When the planner expects a statement to read a million rows or more, its estimate goes to stderr before execution starts:

```text
estimate: ~7501215 rows read (lineitem ~6001215, orders ~1500000), ~4 rows returned
```

The agent can then decide whether to wait or to interrupt and rewrite the query. Smaller queries print nothing, since the line would only be noise. While a long query runs, the terminal progress bar is replaced by a plain line on stderr every 5 seconds:

```text
progress: 42% (elapsed 12.0s, remaining ~16.5s)
progress: done (elapsed 28.7s)
```

### Listing Tables

`.tables` prints one line per table, with an approximate row count and the columns:

```text
memory.main.t1 (table, ~15 rows): a INTEGER PK, b VARCHAR
```

The usual box layout is hard to read through a pipe, and this gives an agent the schema in a single call.

## The Startup Line

When agent mode turns on by detection, the shell prints one line on stderr before running anything:

```text
duckdb agent mode on: CLAUDECODE is set and stdout is not a terminal; -no-agent turns it off, .help agent explains the output
```

The line states why the mode is on and how to turn it off. Our first version printed three lines of explanation (634 bytes) on every run. That was larger than most query results, and a model keeps its context between runs anyway, so it only needs the explanation once. The longer text now lives behind `.help agent`. It describes the output rules and settings, and it points to a few features an agent might not find by itself:

* `SET max_execution_time = <ms>` to put an upper bound on a query’s runtime
* `DESCRIBE <query>` to get the result columns without running the query
* `SUMMARIZE` for a quick profile of a table or query
* `.tables` for the schema
* `duckdb_functions()` for function documentation

If you do not want the startup line, add `.startup_text none` to your `~/.duckdbrc`.

## Other Fixes

The work on agent mode also fixed two bugs that affect all users of the CLI:

* **Swallowed errors in streaming output.** This affected every streaming output mode, including CSV and JSON. If an error happened after the first rows of a result had already been produced, for example a division by zero or a `max_execution_time` timeout, the error was swallowed: the output simply ended and the shell exited with code 0. The reason was that the stream returns an empty chunk both at a clean end and on an error, and nothing checked which of the two it was. The shell now checks the stream’s error and reports it.
* **Wrong statement text with multiple statements.** The shell used the text of the first statement for all of them, so `duckdb -echo -c "a; b"` echoed `a` twice. Each statement now uses its own text.

We also changed the shell’s test harness to remove the agent variables from the environment. Otherwise our own tests would behave differently depending on whether a person or a coding agent runs them.

## Trying It Out

If you use a coding agent, there is nothing to configure. Point it at the v2.0 CLI and it will be detected. To see what the agent sees, run a query through a pipe with the flag set:

```bash
duckdb -agent -c "SUMMARIZE FROM 'my_data.parquet'" | cat
```

## Conclusion

With agent mode, an agent spends fewer tokens per call and does not act on partial results as if they were complete. That means fewer steps to a correct result.

The current behavior is our first attempt, and the conventions around agents are still settling. If your agent is not detected, or the output trips it up, please [open an issue](https://github.com/duckdb/duckdb/issues) or comment on the [pull request](https://github.com/duckdb/duckdb/pull/26167). Transcripts of an agent getting confused are especially useful to us.

## Further Reading

* [Shell: agent mode, render for AI coding agents when one is detected](https://github.com/duckdb/duckdb/pull/26167) (pull request #26167)
* [Shell: proposal to add `.mode llm`](https://github.com/carlopi/duckdb/pull/117) (Carlo Piovesan’s proposal, the basis for the byte budget and early stop)
