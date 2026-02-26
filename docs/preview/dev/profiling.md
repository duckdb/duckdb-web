---
layout: docu
title: Profiling
---

Profiling is essential to help understand why certain queries exhibit specific performance characteristics.
DuckDB contains several built-in features to enable query profiling, which this page covers.
For a high-level example of using `EXPLAIN`, see the [“Inspect Query Plans” page]({% link docs/preview/guides/meta/explain.md %}).

## Statements

### The `EXPLAIN` Statement

The first step to profiling a query can include examining the query plan.
The [`EXPLAIN`]({% link docs/preview/guides/meta/explain.md %}) statement shows the query plan and describes what is going on under the hood.

### The `EXPLAIN ANALYZE` Statement

The query plan helps developers understand the performance characteristics of the query.
However, it is often also necessary to examine the performance numbers of individual operators and the cardinalities that pass through them.
The [`EXPLAIN ANALYZE`]({% link docs/preview/guides/meta/explain_analyze.md %}) statement enables obtaining these, as it pretty-prints the query plan and also executes the query.
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
For more information, see the [“Profiling”]({% link docs/preview/configuration/pragmas.md %}#profiling) section of the pragmas page.

| Setting                                                                                                                                                                            | Description                                     | Default                                                  | Options                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [`enable_profiling`]({% link docs/preview/configuration/pragmas.md %}#enable_profiling), [`enable_profile`]({% link docs/preview/configuration/pragmas.md %}#enable_profiling)     | Turn on profiling                               | `query_tree`                                             | `query_tree`, `json`, `query_tree_optimizer`, `no_output`                                                               |
| [`profiling_coverage`]({% link docs/preview/configuration/pragmas.md %}#profiling_coverage)                                                                                        | Set the operators to profile                    | `SELECT`                                                 | `SELECT`, `ALL`                                                                                                         |
| [`profiling_output`]({% link docs/preview/configuration/pragmas.md %}#profiling_output)                                                                                            | Set a profiling output file                     | Console                                                  | A filepath                                                                                                              |
| [`profiling_mode`]({% link docs/preview/configuration/pragmas.md %}#profiling_mode)                                                                                                | Toggle additional optimizer and planner metrics | `standard`                                               | `standard`, `detailed`                                                                                                  |
| [`custom_profiling_settings`]({% link docs/preview/configuration/pragmas.md %}#custom_profiling_metrics)                                                                           | Enable or disable specific metrics              | All metrics except those activated by detailed profiling | A JSON object that matches the following: `{"METRIC_NAME": "boolean", ...}`. See the [metrics](#metrics) section below. |
| [`disable_profiling`]({% link docs/preview/configuration/pragmas.md %}#disable_profiling), [`disable_profile`]({% link docs/preview/configuration/pragmas.md %}#disable_profiling) | Turn off profiling                              |                                                          |                                                                                                                         |

## Table Functions

> These table functions were introduced in DuckDB v1.4.2.

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

The query tree has two types of nodes: the `QUERY_ROOT` and `OPERATOR` nodes.
The `QUERY_ROOT` refers exclusively to the top-level node, and the metrics it contains are measured over the entire query.
The `OPERATOR` nodes refer to the individual operators in the query plan.
Some metrics are only available for `QUERY_ROOT` nodes, while others are only for `OPERATOR` nodes.
The table below describes each metric and which nodes they are available for.

Other than `QUERY_NAME` and `OPERATOR_TYPE`, it is possible to turn all metrics on or off.

| Metric                  | Return type |   Unit   | Query | Operator | Description                                                                                                                   |
|-------------------------|-------------|----------|:-----:|:--------:|-------------------------------------------------------------------------------------------------------------------------------|
| `BLOCKED_THREAD_TIME`   | `double`    | seconds  |   ✅  |          | The total time threads are blocked                                                                                           |
| `EXTRA_INFO`            | `string`    |          |   ✅  |    ✅    | Unique operator metrics                                                                                                      |
| `LATENCY`               | `double`    | seconds  |   ✅  |          | The total elapsed query execution time                                                                                       |
| `OPERATOR_CARDINALITY`  | `uint64`    | absolute |       |    ✅    | The cardinality of each operator, i.e., the number of rows it returns to its parent. Operator equivalent of `ROWS_RETURNED`  |
| `OPERATOR_ROWS_SCANNED` | `uint64`    | absolute |       |    ✅    | The total rows scanned by each operator                                                                                      |
| `OPERATOR_TIMING`       | `double`    | seconds  |       |    ✅    | The time taken by each operator. Operator equivalent of `LATENCY`                                                            |
| `OPERATOR_TYPE`         | `string`    |          |       |    ✅    | The name of each operator                                                                                                    |
| `QUERY_NAME`            | `string`    |          |   ✅  |          | The query string                                                                                                             |
| `RESULT_SET_SIZE`       | `uint64`    |  bytes   |   ✅  |    ✅    | The size of the result                                                                                                       |
| `ROWS_RETURNED`         | `uint64`    | absolute |   ✅  |          | The number of rows returned by the query                                                                                     |

### Cumulative Metrics

DuckDB also supports several cumulative metrics that are available in all nodes.
In the `QUERY_ROOT` node, these metrics represent the sum of the corresponding metrics across all operators in the query.
The `OPERATOR` nodes represent the sum of the operator's specific metric and those of all its children recursively.

These cumulative metrics can be enabled independently, even if the underlying specific metrics are disabled.
The table below shows the cumulative metrics.
It also depicts the metric based on which DuckDB calculates the cumulative metric.

| Metric                    | Unit     | Metric calculated cumulatively |
|---------------------------|----------|--------------------------------|
| `CPU_TIME`                | seconds  | `OPERATOR_TIMING`              |
| `CUMULATIVE_CARDINALITY`  | absolute | `OPERATOR_CARDINALITY`         |
| `CUMULATIVE_ROWS_SCANNED` | absolute | `OPERATOR_ROWS_SCANNED`        |

`CPU_TIME` measures the cumulative operator timings.
It does not include time spent in other stages, like parsing, query planning, etc.
Thus, for some queries, the `LATENCY` in the `QUERY_ROOT` can be greater than the `CPU_TIME`.

## Detailed Profiling

When the `profiling_mode` is set to `detailed`, an extra set of metrics are enabled, which are only available in the `QUERY_ROOT` node.
These include [`OPTIMIZER`](#optimizer-metrics), [`PLANNER`](#planner-metrics), and [`PHYSICAL_PLANNER`](#physical-planner-metrics) metrics.
They are measured in seconds and returned as a `double`.
It is possible to toggle each of these additional metrics individually.

### Optimizer Metrics

At the `QUERY_ROOT` node, there are metrics that measure the time taken by each [optimizer]({% link docs/preview/internals/overview.md %}#optimizer).
These metrics are only available when the specific optimizer is enabled.
The available optimizations can be queried using the [`duckdb_optimizers()`{:.language-sql .highlight} table function]({% link docs/preview/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers).

Each optimizer has a corresponding metric that follows the template: `OPTIMIZER_⟨OPTIMIZER_NAME⟩`{:.language-sql .highlight}.
For example, the `OPTIMIZER_JOIN_ORDER` metric corresponds to the `JOIN_ORDER` optimizer.

Additionally, the following metrics are available to support the optimizer metrics:

* `ALL_OPTIMIZERS`: Enables all optimizer metrics and measures the time the optimizer parent node takes.
* `CUMULATIVE_OPTIMIZER_TIMING`: The cumulative sum of all optimizer metrics. It is usable without turning on all optimizer metrics.

### Planner Metrics

The planner is responsible for generating the logical plan. Currently, DuckDB measures two metrics in the planner:

* `PLANNER`: The time to generate the logical plan from the parsed SQL nodes.
* `PLANNER_BINDING`: The time taken to bind the logical plan.

### Physical Planner Metrics

The physical planner is responsible for generating the physical plan from the logical plan.
The following are the metrics supported in the physical planner:

* `PHYSICAL_PLANNER`: The time spent generating the physical plan.
* `PHYSICAL_PLANNER_COLUMN_BINDING`: The time spent binding the columns in the logical plan to physical columns.
* `PHYSICAL_PLANNER_RESOLVE_TYPES`: The time spent resolving the types in the logical plan to physical types.
* `PHYSICAL_PLANNER_CREATE_PLAN`: The time spent creating the physical plan.

## Custom Metrics Examples

The following examples demonstrate how to enable custom profiling and set the output format to `json`.
In the first example, we enable profiling and set the output to a file.
We only enable `EXTRA_INFO`, `OPERATOR_CARDINALITY`, and `OPERATOR_TIMING`.

```sql
CREATE TABLE students (name VARCHAR, sid INTEGER);
CREATE TABLE exams (eid INTEGER, subject VARCHAR, sid INTEGER);
INSERT INTO students VALUES ('Mark', 1), ('Joe', 2), ('Matthew', 3);
INSERT INTO exams VALUES (10, 'Physics', 1), (20, 'Chemistry', 2), (30, 'Literature', 3);

PRAGMA enable_profiling = 'json';
PRAGMA profiling_output = '/path/to/file.json';

PRAGMA custom_profiling_settings = '{"CPU_TIME": "false", "EXTRA_INFO": "true", "OPERATOR_CARDINALITY": "true", "OPERATOR_TIMING": "true"}';

SELECT name
FROM students
JOIN exams USING (sid)
WHERE name LIKE 'Ma%';
```

The file's content after executing the query:

```json
{
    "extra_info": {},
    "query_name": "SELECT name\nFROM students\nJOIN exams USING (sid)\nWHERE name LIKE 'Ma%';",
    "children": [
        {
            "operator_timing": 0.000001,
            "operator_cardinality": 2,
            "operator_type": "PROJECTION",
            "extra_info": {
                "Projections": "name",
                "Estimated Cardinality": "1"
            },
            "children": [
                {
                    "extra_info": {
                        "Join Type": "INNER",
                        "Conditions": "sid = sid",
                        "Build Min": "1",
                        "Build Max": "3",
                        "Estimated Cardinality": "1"
                    },
                    "operator_cardinality": 2,
                    "operator_type": "HASH_JOIN",
                    "operator_timing": 0.00023899999999999998,
                    "children": [
...
```

The second example adds detailed metrics to the output.

```sql
PRAGMA profiling_mode = 'detailed';

SELECT name
FROM students
JOIN exams USING (sid)
WHERE name LIKE 'Ma%';
```

The contents of the outputted file:

```json
{
  "all_optimizers": 0.001413,
  "cumulative_optimizer_timing": 0.0014120000000000003,
  "planner": 0.000873,
  "planner_binding": 0.000869,
  "physical_planner": 0.000236,
  "physical_planner_column_binding": 0.000005,
  "physical_planner_resolve_types": 0.000001,
  "physical_planner_create_plan": 0.000226,
  "optimizer_expression_rewriter": 0.000029,
  "optimizer_filter_pullup": 0.000002,
  "optimizer_filter_pushdown": 0.000102,
...
  "optimizer_column_lifetime": 0.000009999999999999999,
  "rows_returned": 2,
  "latency": 0.003708,
  "cumulative_rows_scanned": 6,
  "cumulative_cardinality": 11,
  "extra_info": {},
  "cpu_time": 0.000095,
  "optimizer_build_side_probe_side": 0.000017,
  "result_set_size": 32,
  "blocked_thread_time": 0.0,
  "query_name": "SELECT name\nFROM students\nJOIN exams USING (sid)\nWHERE name LIKE 'Ma%';",
  "children": [
    {
      "operator_timing": 0.000001,
      "operator_rows_scanned": 0,
      "cumulative_rows_scanned": 6,
      "operator_cardinality": 2,
      "operator_type": "PROJECTION",
      "cumulative_cardinality": 11,
      "extra_info": {
        "Projections": "name",
        "Estimated Cardinality": "1"
      },
      "result_set_size": 32,
      "cpu_time": 0.000095,
      "children": [
...
```

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
