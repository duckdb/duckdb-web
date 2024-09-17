---
layout: docu
title: Profiling
redirect_from:
  - /dev/profiling
---

Profiling is important to help understand why certain queries exhibit specific performance characteristics. DuckDB contains several built-in features to enable query profiling that will be explained on this page.

## `EXPLAIN` Statement

The first step to profiling a query can include examining the query plan. The [`EXPLAIN`]({% link docs/guides/meta/explain.md %}) statement allows you to peek into the query plan and see what is going on under the hood.

## `EXPLAIN ANALYZE` Statement

The query plan helps understand the performance characteristics of the system. However, often it is also necessary to look at the performance numbers of individual operators and the cardinalities that pass through them. This is where the [`EXPLAIN_ANALYZE`]({% link docs/guides/meta/explain_analyze.md %}) statement comes in, which pretty-prints the query plan and also executes the query, providing the actual run-time performance numbers.

## Pragmas

DuckDB supports several pragmas that can be used to enable and disable profiling, as well as to control the level of detail in the profiling output.

The following pragmas are available, and can be set using either `PRAGMA` or `SET`.
They can also be reset using `RESET`, followed by the setting name.
For more information on the profiling pragmas and their usage,
see the [“Profiling Queries”]({% link docs/configuration/pragmas.md %}#profiling_queries)
section of the pragmas page.

| Setting | Description | Default | Options |
|---|-------|---|---|
| [`enable_profiling`]({% link docs/configuration/pragmas.md %}#enable_profiling) , [`enable_profile`]({% link docs/configuration/pragmas.md %}#enable_profiling)    | Turn on profiling                                                  | `query_tree`                                              | `query_tree`, `json`, `query_tree_optimizer`, [`no_output`]({% link docs/configuration/pragmas.md %}#disabling_output) |
| [`disable_profiling`]({% link docs/configuration/pragmas.md %}#disable_profiling), [`disable_profile`]({% link docs/configuration/pragmas.md %}#disable_profiling) | Turn off profiling                                                 |                                                           |                                                                                                                        |
| [`profiling_mode`]({% link docs/configuration/pragmas.md %}#profiling_mode)                                                                                        | Toggle additional optimizer, planner, and physical planner metrics | `standard`                                                | `standard`, `detailed`                                                                                                 |
| [`profiling_output`]({% link docs/configuration/pragmas.md %}#profiling_output)                                                                                    | Set a file to output the profiling to                              | Console                                                   | A path to a file                                                                                                       |
| [`custom_profiling_settings`]({% link docs/configuration/pragmas.md %}#custom_profiling_metrics)                                                                   | Enable or disable specific metrics.                                | All metrics except those activated by detailed profiling. | A JSON object that matches the following: `{"METRIC_NAME": "boolean", ...}`. See the [metrics](#metrics) section below |

## Metrics

There are two types of nodes in the query tree: the `QUERY_ROOT`, and `OPERATOR` nodes.  The `QUERY_ROOT` refers exclusively to the top level node and the metrics it contains are measured over the entire query. The `OPERATOR` nodes refer to the individual operators in the query plan. Some metrics are only available for `QUERY_ROOT` nodes, while others are only available for `OPERATOR` nodes.  The table below describes each metric, as well as which nodes they are available for.

Other than `QUERY_NAME` and `OPERATOR_TYPE`, all metrics can be turned on or off. 

| Metric                  | Return Type | Query | Operator | Description                                                                          |
|-------------------------|-------------|:-----:|:--------:|--------------------------------------------------------------------------------------|
| `BLOCKED_THREAD_TIME`   | `double`    |   ✅   |          | The total time threads are blocked                                                   |
| `EXTRA_INFO`            | `string`    |   ✅   |    ✅     | Each operator also has unique metrics, which can be accessed here.                   |
| `OPERATOR_CARDINALITY`  | `uint64`    |   ✅   |   ✅  ️   | The cardinality of each operator, i.e., the number of rows it returns to its parent. |
| `OPERATOR_ROWS_SCANNED` | `uint64`    |   ✅   |    ✅     | The total rows scanned by each operator                                              |
| `OPERATOR_TIMING`       | `uint64`    |   ✅   |    ✅     | The time taken by each operator                                                      |
| `OPERATOR_TYPE`         | `string`    |       |    ✅     | The name of each operator                                                            |
| `QUERY_NAME`            | `string`    |   ✅   |          | The input query                                                                      |
| `RESULT_SET_SIZE`       | `uint64`    |   ✅   |    ✅     | The size of the result in bytes                                                      |

### Cumulative Metrics

DuckDB also supports several cumulative metrics, available in all nodes. In the `QUERY_ROOT` node, these metrics represent the sum of the corresponding metrics across all operators in the query. In the `OPERATOR` nodes, they represent the sum of the operator's specific metric along with those of all its children recursively.

These cumulative metrics can be enabled independently, even if the underlying specific metrics are disabled.
The table below shows the cumulative metrics and the specific metrics they are calculated from.

| Metric                    | Metric Calculated Cumulatively |
|---------------------------|--------------------------------|
| `CPU_TIME`                | `OPERATOR_TIMING`              |
| `CUMULATIVE_CARDINALITY`  | `OPERATOR_CARDINALITY`         |
| `CUMULATIVE_ROWS_SCANNED` | `OPERATOR_ROWS_SCANNED`        |

## Detailed Profiling

As explained above, when the `profiling_mode` is set to `detailed`, an extra set of timing metrics are enabled, which are only available at the `QUERY_ROOT` level. These include [`OPTIMIZERS`](#optimizers), [`PLANNER`](#planner), and [`PHYSICAL_PLANNER`](#physical-planner) metrics, which are all measured in milliseconds, and returned as a `double`.

These metrics are automatically enabled, and added to the enabled settings, when the `profiling_mode` is set to `detailed`, however, they can also be toggled individually. 

### Optimizers

At the `QUERY_ROOT` level, there are also metrics that measure the time taken by each [optimizer]({% link docs/internals/overview.md %}#optimizer). These metrics are only available when the specific optimizer is enabled. The available optimizations can be queried using the [`duckdb_optimizers() table function`]({% link docs/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers).

Each optimizer has a corresponding metric that follows the template: `OPTIMIZER_<OPTIMIZER_NAME>`. For example, the `OPTIMIZER_JOIN_ORDER` metric corresponds to the `JOIN_ORDER` optimizer.

Additionally, the following metrics are available to support the optimizer metrics:
* `ALL_OPTIMIZERS` - Turns on all optimizer metrics, and measures the time taken by the optimizer parent node.
* `CUMMULATIVE_OPTIMIZER_TIMING` - The cumulative sum of all optimizer metrics, can be used without turning on all optimizer metrics.

### Planner

The `PLANNER` is responsible for generating the logical plan. Currently, two metrics are measured in the `PLANNER`:
* `PLANNER` - The time taken to generate the logical plan from the parsed SQL nodes.
* `PLANNER_BINDING` - The time taken to bind the logical plan.

### Physical Planner

The `PHYSICAL_PLANNER` is responsible for generating the physical plan from the logical plan.
The following are the metrics supported in the `PHYSICAL_PLANNER`:
* `PHYSICAL_PLANNER` - The time taken to generate the physical plan.
* `PHYSICAL_PLANNER_COLUMN_BINDING` - The time taken to bind the columns in the logical plan to physical columns.
* `PHYSICAL_PLANNER_RESOLVE_TYPES` - The time taken to resolve the types in the logical plan to physical types.
* `PHYSICAL_PLANNER_CREATE_PLAN` - The time taken to create the physical plan.

## Setting Custom Metrics Examples

The following examples demonstrate how to enable profiling and set the output format to `json`. 

In the first example, profiling is enabled, the output is set to a file, and only the `EXTRA_INFO`, `OPERATOR_CARDINALITY`, and `OPERATOR_TIMING` metrics are enabled.

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

The contents of the outputted file:

```json
"operator_timing": 0.000372,
"operator_cardinality": 0,
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
                "operator_timing": 0.000031,
                "operator_cardinality": 2,
                "operator_type": "HASH_JOIN",
                "extra_info": {
                    "Join Type": "INNER",
                    "Conditions": "sid = sid",
                    "Build Min": "1",
                    "Build Max": "3",
                    "Estimated Cardinality": "1"
                },
                "children": [
                    ...
}
```

The second example adds the detailed metrics to the output. 

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
    "all_optimizers": 0.00014299999999999998,
    "cumulative_optimizer_timing": 0.00014299999999999998,
    "planner": 0.000187,
    "planner_binding": 0.000185,
    "physical_planner": 0.000034,
    "physical_planner_column_binding": 0.000002,
    "physical_planner_resolve_types": 0.0,
    "physical_planner_create_plan": 0.000031,
    "optimizer_expression_rewriter": 0.000012,
    "optimizer_filter_pullup": 0.000001,
    "optimizer_filter_pushdown": 0.000035,
    ...
    "operator_cardinality": 0,
    "optimizer_compressed_materialization": 0.0,
    "optimizer_deliminator": 0.0,
    "extra_info": {},
    "query_name": "SELECT name\nFROM students\nJOIN exams USING (sid)\nWHERE name LIKE 'Ma%';",
    "children": [
        {
            "operator_timing": 0.0,
            "operator_cardinality": 2,
            "operator_type": "PROJECTION",
            "extra_info": {
                "Projections": "name",
                "Estimated Cardinality": "1"
            },
            "children": [
            {
                "operator_timing": 0.00010100000000000002,
                "operator_cardinality": 2,
                "operator_type": "HASH_JOIN",
                "extra_info": {
                    "Join Type": "INNER",
                    "Conditions": "sid = sid",
                    "Build Min": "1",
                    "Build Max": "3",
                    "Estimated Cardinality": "1"
                },
                "children": [
                ...
}
```

## Query Graphs

It is also possible to render the profiling output as a query graph.  The query graph is a visual representation of the query plan, showing the operators and their relationships. The query plan must be output in the `json` format and stored in a file.
After a profiling output is written to its designated file it can then be rendered as a query graph using the Python script, provided the `duckdb` python module is installed. This script will generate an HTML file and open it in your web browser.

```bash
python -m duckdb.query_graph /path/to/file.json
```

## Notation in Query Plans

In query plans, the [hash join](https://en.wikipedia.org/wiki/Hash_join) operators adhere to the following convention:
the _probe side_ of the join is the left operand,
while the _build side_ is the right operand.

Join operators in the query plan show the join type used:

* Inner joins are denoted as `INNER`.
* Left outer joins and right outer joins are denoted as `LEFT` and `RIGHT`, respectively.
* Full outer joins are denoted as `FULL`.
