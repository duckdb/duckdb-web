---
layout: docu
redirect_from:
- /dev/profiling
- /docs/dev/profiling
- /docs/stable/dev/profiling
- /docs/current/dev/profiling
- /docs/lts/dev/profiling
- /docs/preview/dev/profiling
title: Profiling
---

Profiling is essential to help understand why certain queries exhibit specific performance characteristics.
DuckDB contains several built-in features to enable query profiling, which this page covers.
For a high-level example of using `EXPLAIN`, see the [“Inspect Query Plans” page]({% link docs/2.0/guides/meta/explain.md %}).

## Statements

### The `EXPLAIN` Statement

The first step to profiling a query can include examining the query plan.
The [`EXPLAIN`]({% link docs/2.0/guides/meta/explain.md %}) statement shows the query plan and describes what is going on under the hood.

### The `EXPLAIN ANALYZE` Statement

The query plan helps developers understand the performance characteristics of the query.
However, it is often also necessary to examine the performance numbers of individual operators and the cardinalities that pass through them.
The [`EXPLAIN ANALYZE`]({% link docs/2.0/guides/meta/explain_analyze.md %}) statement enables obtaining these, as it pretty-prints the query plan and also executes the query.
Thus, it provides the actual run-time performance numbers.

### The `FORMAT` Option

The `EXPLAIN [ANALYZE]` statement allows exporting to several formats:

* `text` – default ASCII-art style output
* `graphviz` – produces a DOT output, which can be rendered with [Graphviz](https://graphviz.org/)
* `html` – produces an HTML output, which can be rendered with [treeflex](https://dumptyd.github.io/treeflex/)
* `json` – produces a JSON output
* `mermaid` – produces a [Mermaid](https://mermaid.js.org/) flowchart
* `web` – opens the query graph in a web browser (command line client only)

To specify a format, use the `FORMAT` tag:

```sql
EXPLAIN (FORMAT html) SELECT 42 AS x;
```

> New As of DuckDB 2.0, the `web` format is available in the [command line client]({% link docs/2.0/clients/cli/overview.md %}). `EXPLAIN ANALYZE (FORMAT WEB)` renders the query graph and opens it in a web browser, and the [`.web`]({% link docs/2.0/clients/cli/dot_commands.md %}) dot command does the same for the previous query. Both are disabled in [safe mode]({% link docs/2.0/clients/cli/safe_mode.md %}).

## Pragmas

DuckDB supports several pragmas for turning profiling on and off and controlling the level of detail in the profiling output.

The following pragmas are available and can be set using either `PRAGMA` or `SET`.
They can also be reset using `RESET`, followed by the setting name.
For more information, see the [“Profiling”]({% link docs/2.0/configuration/pragmas.md %}#profiling) section of the pragmas page.

| Setting                                                                                                                                                                            | Description                                     | Default                                                  | Options                                                                                                                                                            |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`enable_profiling`]({% link docs/2.0/configuration/pragmas.md %}#enable-profiling), [`enable_profile`]({% link docs/2.0/configuration/pragmas.md %}#enable-profiling)     | Turn on profiling                               | `query_tree`                                             | `query_tree`, `json`, `query_tree_optimizer`, `no_output`                                                                                                          |
| [`profiling_coverage`]({% link docs/2.0/configuration/pragmas.md %}#profiling-coverage)                                                                                        | Set the operators to profile                    | `SELECT`                                                 | `SELECT`, `ALL`                                                                                                                                                    |
| [`profiling_output`]({% link docs/2.0/configuration/pragmas.md %}#profiling-output)                                                                                            | Set a profiling output file                     | Console                                                  | A filepath                                                                                                                                                         |
| [`profiling_mode`]({% link docs/2.0/configuration/pragmas.md %}#profiling-mode)                                                                                                | Toggle additional optimizer and planner metrics | `standard`                                               | `standard`, `detailed`, `all`                                                                                                                                       |
| [`tracked_metrics`]({% link docs/2.0/configuration/pragmas.md %}#custom-metrics)                                                                                               | Select which metrics to collect                 | `['*']` (all metrics)                                    | A list of metric glob patterns, e.g. `['query.*', 'optimizer.*']`. ([List of all available metrics]({% link docs/2.0/dev/metrics.md %}#all-metrics)) |
| [`disable_profiling`]({% link docs/2.0/configuration/pragmas.md %}#disable-profiling), [`disable_profile`]({% link docs/2.0/configuration/pragmas.md %}#disable-profiling) | Turn off profiling                              |                                                          |                                                                                                                                                                    |

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
    metrics := ['query.sql', 'query.total_time', 'operator.timing']
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
CALL enable_profiling(['query.total_time', 'query.total_intermediate_size_bytes']);
```

### `disable_profiling()`

The `disable_profiling()` function turns off profiling.

```sql
CALL disable_profiling();
```

## Metrics

DuckDB supports a wide range of metrics that can be enabled or disabled independently. To learn more and to see the full list of available metrics, refer to the [metrics documentation]({% link docs/2.0/dev/metrics.md %}#all-metrics).

> New In DuckDB 2.0, the set of collected metrics is controlled with the `tracked_metrics` setting, which takes a list of metric glob patterns such as `['query.*', 'optimizer.*']`. This replaces the `custom_profiling_settings` `PRAGMA` used in earlier versions. The available metric names, types, and units can be listed with the `duckdb_available_metrics()` table function:
>
> ```sql
> SELECT metric_name, metric_type, unit
> FROM duckdb_available_metrics();
> ```

## Detailed Profiling

When the `profiling_mode` is set to `detailed`, an extra set of metrics are enabled, which are only available in the `QUERY_ROOT` node.
These include all the metrics in the [Phase timing]({% link docs/2.0/dev/metrics.md %}#phase_timing-metrics) metric group.
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
