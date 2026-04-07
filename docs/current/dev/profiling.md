---
layout: docu
redirect_from:
- /dev/profiling
- /docs/dev/profiling
- /docs/preview/dev/profiling
- /docs/stable/dev/profiling
title: Profiling
---

Profiling is essential to help understand why certain queries exhibit specific performance characteristics.
DuckDB contains several built-in features to enable query profiling, which this page covers.
For a high-level example of using `EXPLAIN`, see the [“Inspect Query Plans” page]({% link docs/current/guides/meta/explain.md %}).

## Statements

### The `EXPLAIN` Statement

The first step to profiling a query can include examining the query plan.
The [`EXPLAIN`]({% link docs/current/guides/meta/explain.md %}) statement shows the query plan and describes what is going on under the hood.

### The `EXPLAIN ANALYZE` Statement

The query plan helps developers understand the performance characteristics of the query.
However, it is often also necessary to examine the performance numbers of individual operators and the cardinalities that pass through them.
The [`EXPLAIN ANALYZE`]({% link docs/current/guides/meta/explain_analyze.md %}) statement enables obtaining these, as it pretty-prints the query plan and also executes the query.
Thus, it provides the actual run-time performance numbers.

### The `FORMAT` Option

The `EXPLAIN [ANALYZE]` statement allows exporting to several formats:

* `text` – default ASCII-art style output
* `graphviz` – produces a DOT output, which can be rendered with [Graphviz](https://graphviz.org/)
* `html` – produces an HTML output, which can be rendered with [treeflex](https://dumptyd.github.io/treeflex/)
* `json` – produces a JSON output

To specify a format, use the `FORMAT` tag:

```sql
EXPLAIN (FORMAT html) SELECT 42 AS x;
```

## Pragmas

DuckDB supports several pragmas for turning profiling on and off and controlling the level of detail in the profiling output.

The following pragmas are available and can be set using either `PRAGMA` or `SET`.
They can also be reset using `RESET`, followed by the setting name.
For more information, see the [“Profiling”]({% link docs/current/configuration/pragmas.md %}#profiling) section of the pragmas page.

| Setting                                                                                                                                                                            | Description                                     | Default                                                  | Options                                                                                                                                                            |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`enable_profiling`]({% link docs/current/configuration/pragmas.md %}#enable_profiling), [`enable_profile`]({% link docs/current/configuration/pragmas.md %}#enable_profiling)     | Turn on profiling                               | `query_tree`                                             | `query_tree`, `json`, `query_tree_optimizer`, `no_output`                                                                                                          |
| [`profiling_coverage`]({% link docs/current/configuration/pragmas.md %}#profiling_coverage)                                                                                        | Set the operators to profile                    | `SELECT`                                                 | `SELECT`, `ALL`                                                                                                                                                    |
| [`profiling_output`]({% link docs/current/configuration/pragmas.md %}#profiling_output)                                                                                            | Set a profiling output file                     | Console                                                  | A filepath                                                                                                                                                         |
| [`profiling_mode`]({% link docs/current/configuration/pragmas.md %}#profiling_mode)                                                                                                | Toggle additional optimizer and planner metrics | `standard`                                               | `standard`, `detailed`                                                                                                                                             |
| [`configure_profiling`]({% link docs/current/configuration/pragmas.md %}#custom_profiling_metrics)                                                                                 | Enable or disable specific metrics              | All metrics except those activated by detailed profiling | A JSON object that matches the following: `{"METRIC_NAME": "boolean", ...}`. ([List of all available metrics]({% link docs/current/dev/metrics.md %}#all_metrics)) |
| [`disable_profiling`]({% link docs/current/configuration/pragmas.md %}#disable_profiling), [`disable_profile`]({% link docs/current/configuration/pragmas.md %}#disable_profiling) | Turn off profiling                              |                                                          |                                                                                                                                                                    |

## Table Functions

> These table functions were introduced in DuckDB v1.5.0.

DuckDB provides table functions to enable and disable profiling, consolidating multiple settings into a single call.

### `enable_profiling()`

The `enable_profiling()` function configures profiling with the specified options.

```sql
CALL enable_profiling(
    format := 'json',
    save_location := '/path/to/output.json',
    coverage := 'select',
    mode := 'standard',
    metrics := ['QUERY_NAME', 'LATENCY', 'OPERATOR_TIMING']
);
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `metrics` | `LIST`, `STRUCT`, or JSON | Specifies which metrics to enable |
| `mode` | `VARCHAR` | Profiling level: `'standard'` or `'detailed'` |
| `save_location` | `VARCHAR` | File path for profiling output |
| `coverage` | `VARCHAR` | Query coverage: `'select'` or `'all'` |
| `format` | `VARCHAR` | Output format: `'query_tree'`, `'json'`, `'query_tree_optimizer'`, `'no_output'` |

All parameters are optional and named. You can also pass metrics as an unnamed parameter:

```sql
CALL enable_profiling(['LATENCY', 'RESULT_SET_SIZE']);
```

### `disable_profiling()`

The `disable_profiling()` function turns off profiling.

```sql
CALL disable_profiling();
```

## Metrics

DuckDB supports a wide range of metrics that can be enabled or disabled independently. To learn more and to see the full list of available metrics, refer to the [metrics documentation]({% link docs/current/dev/metrics.md %}#all_metrics).

## Detailed Profiling

When the `profiling_mode` is set to `detailed`, an extra set of metrics are enabled, which are only available in the `QUERY_ROOT` node.
These include all the metrics in the [Phase timing]({% link docs/current/dev/metrics.md %}#phase_timing_metrics) metric group.
It is possible to toggle each of these additional metrics individually.

## Query Graphs

It is also possible to render the profiling output as a query graph.
The query graph visually represents the query plan, showing the operators and their relationships.
The query plan must be output in the `json` format and stored in a file.
After writing a profiling output to its designated file, the Python script can render it as a query graph.
The script requires the `duckdb` Python module to be installed.
It generates an HTML file and opens it in your web browser.

```batch
python -m duckdb.query_graph /path/to/file.json
```

## Notation in Query Plans

In query plans, the [hash join](https://en.wikipedia.org/wiki/Hash_join) operators adhere to the following convention:
the _probe side_ of the join is the left operand, while the _build side_ is the right operand.

Join operators in the query plan show the join type used:

* Inner joins are denoted as `INNER`.
* Left outer joins and right outer joins are denoted as `LEFT` and `RIGHT`, respectively.
* Full outer joins are denoted as `FULL`.

> Tip To visualize query plans, consider using the [DuckDB execution plan visualizer](https://db.cs.uni-tuebingen.de/explain/) developed by the [Database Systems Research Group at the University of Tübingen](https://github.com/DBatUTuebingen).
