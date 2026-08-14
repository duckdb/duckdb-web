---
layout: docu
redirect_from:
- /dev/metrics
- /docs/dev/metrics
- /docs/preview/dev/metrics
- /docs/stable/dev/metrics
title: Metrics
---

DuckDB provides a set of metrics that can be used to monitor the performance and health of the database.

The query tree has two types of nodes: the `QUERY_ROOT` and `OPERATOR` nodes.
The `QUERY_ROOT` refers exclusively to the top-level node, and the metrics it contains are measured over the entire query.
The `OPERATOR` nodes refer to the individual operators in the query plan.
Some metrics are only available for `QUERY_ROOT` nodes, while others are only for `OPERATOR` nodes.
The table below describes each metric and which nodes they are available for.

Other than `OPERATOR_TYPE`, all metrics can be turned on or off.

## All Metrics

| Name                                                                  | Group                                 | Description                                                                |
|-----------------------------------------------------------------------|---------------------------------------|----------------------------------------------------------------------------|
| [`CPU_TIME`](#cpu_time)                                               | [core](#core-metrics)                 | CPU time spent on the query                                                |
| [`CUMULATIVE_CARDINALITY`](#cumulative_cardinality)                   | [core](#core-metrics)                 | Cumulative cardinality of the query                                        |
| [`CUMULATIVE_ROWS_SCANNED`](#cumulative_rows_scanned)                 | [core](#core-metrics)                 | Cumulative number of rows scanned by the query                             |
| [`EXTRA_INFO`](#extra_info)                                           | [core](#core-metrics)                 | Unique operator metrics                                                    |
| [`LATENCY`](#latency)                                                 | [core](#core-metrics)                 | Time spent executing the entire query                                      |
| [`QUERY_NAME`](#query_name)                                           | [core](#core-metrics)                 | The SQL string of the query                                                |
| [`RESULT_SET_SIZE`](#result_set_size)                                 | [core](#core-metrics)                 | The size of the result                                                     |
| [`ROWS_RETURNED`](#rows_returned)                                     | [core](#core-metrics)                 | The number of rows returned by the query                                   |
| [`BLOCKED_THREAD_TIME`](#blocked_thread_time)                         | [execution](#execution-metrics)       | Time spent waiting for a thread to become available                        |
| [`SYSTEM_PEAK_BUFFER_MEMORY`](#system_peak_buffer_memory)             | [execution](#execution-metrics)       | Peak memory usage of the system                                            |
| [`SYSTEM_PEAK_TEMP_DIR_SIZE`](#system_peak_temp_dir_size)             | [execution](#execution-metrics)       | Peak size of the temporary directory                                       |
| [`TOTAL_MEMORY_ALLOCATED`](#total_memory_allocated)                   | [execution](#execution-metrics)       | The total memory allocated by the buffer manager.                          |
| [`ATTACH_LOAD_STORAGE_LATENCY`](#attach_load_storage_latency)         | [file](#file-metrics)                 | Time spent loading from storage.                                           |
| [`ATTACH_REPLAY_WAL_LATENCY`](#attach_replay_wal_latency)             | [file](#file-metrics)                 | Time spent replaying the WAL file.                                         |
| [`CHECKPOINT_LATENCY`](#checkpoint_latency)                           | [file](#file-metrics)                 | Time spent running checkpoints                                             |
| [`COMMIT_LOCAL_STORAGE_LATENCY`](#commit_local_storage_latency)       | [file](#file-metrics)                 | Time spent committing the transaction-local storage.                       |
| [`TOTAL_BYTES_READ`](#total_bytes_read)                               | [file](#file-metrics)                 | The total bytes read by the file system.                                   |
| [`TOTAL_BYTES_WRITTEN`](#total_bytes_written)                         | [file](#file-metrics)                 | The total bytes written by the file system.                                |
| [`WAITING_TO_ATTACH_LATENCY`](#waiting_to_attach_latency)             | [file](#file-metrics)                 | Time spent waiting to ATTACH a file.                                       |
| [`WAL_REPLAY_ENTRY_COUNT`](#wal_replay_entry_count)                   | [file](#file-metrics)                 | The total number of entries to replay in the WAL.                          |
| [`WRITE_TO_WAL_LATENCY`](#write_to_wal_latency)                       | [file](#file-metrics)                 | Time spent writing to the WAL.                                             |
| [`ALL_OPTIMIZERS`](#all_optimizers)                                   | [phase_timing](#phase_timing-metrics) | Enables all optimizers                                                     |
| [`CUMULATIVE_OPTIMIZER_TIMING`](#cumulative_optimizer_timing)         | [phase_timing](#phase_timing-metrics) | Time spent in all optimizers                                               |
| [`PHYSICAL_PLANNER`](#physical_planner)                               | [phase_timing](#phase_timing-metrics) | The time spent generating the physical plan                                |
| [`PHYSICAL_PLANNER_COLUMN_BINDING`](#physical_planner_column_binding) | [phase_timing](#phase_timing-metrics) | The time spent binding the columns in the logical plan to physical columns |
| [`PHYSICAL_PLANNER_CREATE_PLAN`](#physical_planner_create_plan)       | [phase_timing](#phase_timing-metrics) | The time spent creating the physical plan                                  |
| [`PHYSICAL_PLANNER_RESOLVE_TYPES`](#physical_planner_resolve_types)   | [phase_timing](#phase_timing-metrics) | The time spent resolving the types in the logical plan to physical types   |
| [`PLANNER`](#planner)                                                 | [phase_timing](#phase_timing-metrics) | The time to generate the logical plan from the parsed SQL nodes.           |
| [`PLANNER_BINDING`](#planner_binding)                                 | [phase_timing](#phase_timing-metrics) | The time taken to bind the logical plan.                                   |
| [`OPERATOR_CARDINALITY`](#operator_cardinality)                       | [operator](#operator-metrics)         | Cardinality of the operator                                                |
| [`OPERATOR_NAME`](#operator_name)                                     | [operator](#operator-metrics)         | Name of the operator                                                       |
| [`OPERATOR_ROWS_SCANNED`](#operator_rows_scanned)                     | [operator](#operator-metrics)         | Number of rows scanned by the operator                                     |
| [`OPERATOR_TIMING`](#operator_timing)                                 | [operator](#operator-metrics)         | Time spent in the operator                                                 |
| [`OPERATOR_TYPE`](#operator_type)                                     | [operator](#operator-metrics)         | Type of the operator                                                       |



## Metric Groups

The metrics are organized into groups, which can be used to enable or disable related metrics together.
The following is a list of the available metric groups:
- `ALL`: All metrics
- `DEFAULT`: The default set of metrics
- [`CORE`](#core-metrics)
- [`EXECUTION`](#execution-metrics)
- [`FILE`](#file-metrics)
- [`OPERATOR`](#operator-metrics)
- [`OPTIMIZER`](#optimizer-metrics)
- [`PHASE_TIMING`](#phase_timing-metrics)


### Core Metrics

core metrics


#### `CPU_TIME`

<div class="nostroke_table"></div>

| **Description** | CPU time spent on the query |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |
| **[Cumulative](#cumulative-metrics)** | ✅ |
| **Child** | OPERATOR_TIMING |

**Note:**

`CPU_TIME` measures the cumulative operator timings.
It does not include time spent in other stages, like parsing, query planning, etc.
Thus, for some queries, the `LATENCY` in the `QUERY_ROOT` can be greater than the `CPU_TIME`.



#### `CUMULATIVE_CARDINALITY`

<div class="nostroke_table"></div>

| **Description** | Cumulative cardinality of the query |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |
| **[Cumulative](#cumulative-metrics)** | ✅ |
| **Child** | OPERATOR_CARDINALITY |


#### `CUMULATIVE_ROWS_SCANNED`

<div class="nostroke_table"></div>

| **Description** | Cumulative number of rows scanned by the query |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |
| **[Cumulative](#cumulative-metrics)** | ✅ |
| **Child** | OPERATOR_ROWS_SCANNED |


#### `EXTRA_INFO`

<div class="nostroke_table"></div>

| **Description** | Unique operator metrics |
| **Type** | Value::MAP |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |


#### `LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent executing the entire query |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `QUERY_NAME`

<div class="nostroke_table"></div>

| **Description** | The SQL string of the query |
| **Type** | string |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `RESULT_SET_SIZE`

<div class="nostroke_table"></div>

| **Description** | The size of the result |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |
| **Child** | RESULT_SET_SIZE |


#### `ROWS_RETURNED`

<div class="nostroke_table"></div>

| **Description** | The number of rows returned by the query |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Child** | OPERATOR_CARDINALITY |


### Execution Metrics

Metrics that are collected during query execution


#### `BLOCKED_THREAD_TIME`

<div class="nostroke_table"></div>

| **Description** | Time spent waiting for a thread to become available |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `SYSTEM_PEAK_BUFFER_MEMORY`

<div class="nostroke_table"></div>

| **Description** | Peak memory usage of the system |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |


#### `SYSTEM_PEAK_TEMP_DIR_SIZE`

<div class="nostroke_table"></div>

| **Description** | Peak size of the temporary directory |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | ✅ |
| **Query Node** | ✅ |
| **Operator Node** | ✅ |


#### `TOTAL_MEMORY_ALLOCATED`

<div class="nostroke_table"></div>

| **Description** | The total memory allocated by the buffer manager. |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | ✅ |
| **Query Node** | ✅ |


### File Metrics

metrics that are collected during file operations


#### `ATTACH_LOAD_STORAGE_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent loading from storage. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `ATTACH_REPLAY_WAL_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent replaying the WAL file. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `CHECKPOINT_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent running checkpoints |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `COMMIT_LOCAL_STORAGE_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent committing the transaction-local storage. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `TOTAL_BYTES_READ`

<div class="nostroke_table"></div>

| **Description** | The total bytes read by the file system. |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `TOTAL_BYTES_WRITTEN`

<div class="nostroke_table"></div>

| **Description** | The total bytes written by the file system. |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `WAITING_TO_ATTACH_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent waiting to ATTACH a file. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `WAL_REPLAY_ENTRY_COUNT`

<div class="nostroke_table"></div>

| **Description** | The total number of entries to replay in the WAL. |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | ✅ |
| **Query Node** | ✅ |


#### `WRITE_TO_WAL_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent writing to the WAL. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Query Node** | ✅ |


### Operator Metrics

metrics that are collected for each operator


#### `OPERATOR_CARDINALITY`

<div class="nostroke_table"></div>

| **Description** | Cardinality of the operator |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | ✅ |
| **Operator Node** | ✅ |


#### `OPERATOR_NAME`

<div class="nostroke_table"></div>

| **Description** | Name of the operator |
| **Type** | string |
| **Default** | ✅ |
| **Operator Node** | ✅ |


#### `OPERATOR_ROWS_SCANNED`

<div class="nostroke_table"></div>

| **Description** | Number of rows scanned by the operator |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | ✅ |
| **Operator Node** | ✅ |


#### `OPERATOR_TIMING`

<div class="nostroke_table"></div>

| **Description** | Time spent in the operator |
| **Type** | double |
| **Unit** | seconds |
| **Default** | ✅ |
| **Operator Node** | ✅ |


#### `OPERATOR_TYPE`

<div class="nostroke_table"></div>

| **Description** | Type of the operator |
| **Type** | uint8 |
| **Default** | ✅ |
| **Operator Node** | ✅ |


### Phase_timing Metrics

This group contains metrics related to the planner and the physical planner. The planner is responsible for generating the logical plan, whereas the physical planner is responsible for generating the physical plan from the logical plan.


#### `ALL_OPTIMIZERS`

<div class="nostroke_table"></div>

| **Description** | Enables all optimizers |
| **Type** | double |
| **Query Node** | ✅ |


#### `CUMULATIVE_OPTIMIZER_TIMING`

<div class="nostroke_table"></div>

| **Description** | Time spent in all optimizers |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |
| **[Cumulative](#cumulative-metrics)** | ✅ |


#### `PHYSICAL_PLANNER`

<div class="nostroke_table"></div>

| **Description** | The time spent generating the physical plan |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |


#### `PHYSICAL_PLANNER_COLUMN_BINDING`

<div class="nostroke_table"></div>

| **Description** | The time spent binding the columns in the logical plan to physical columns |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |


#### `PHYSICAL_PLANNER_CREATE_PLAN`

<div class="nostroke_table"></div>

| **Description** | The time spent creating the physical plan |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |


#### `PHYSICAL_PLANNER_RESOLVE_TYPES`

<div class="nostroke_table"></div>

| **Description** | The time spent resolving the types in the logical plan to physical types |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |


#### `PLANNER`

<div class="nostroke_table"></div>

| **Description** | The time to generate the logical plan from the parsed SQL nodes. |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |


#### `PLANNER_BINDING`

<div class="nostroke_table"></div>

| **Description** | The time taken to bind the logical plan. |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | ✅ |



### Optimizer Metrics

Optimizer metrics sit at the `QUERY_ROOT` level, and measure the time taken by each [optimizer]({% link docs/current/internals/overview.md %}#optimizer).
These metrics are only available when the specific optimizer is enabled.
The available optimizations can be queried using the [`duckdb_optimizers()`{:.language-sql .highlight} table function]({% link docs/current/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers).

Each optimizer has a corresponding metric that follows the template: `OPTIMIZER_⟨OPTIMIZER_NAME⟩`{:.language-sql .highlight}.
For example, the `OPTIMIZER_JOIN_ORDER` metric corresponds to the `JOIN_ORDER` optimizer.

Additionally, the following metrics are available to support the optimizer metrics:
- [`ALL_OPTIMIZERS`](#all_optimizers)
- [`CUMULATIVE_OPTIMIZER_TIMING`](#cumulative_optimizer_timing)


## Cumulative Metrics

DuckDB also supports several cumulative metrics that are available in all nodes.
In the `QUERY_ROOT` node, these metrics represent the sum of the corresponding metrics across all operators in the query.
The `OPERATOR` nodes represent the sum of the operator's specific metric and those of all its children recursively.

These cumulative metrics can be enabled independently, even if the underlying specific metrics are disabled.

The following is a list of the available cumulative metrics:
- [`CPU_TIME`](#cpu_time)
- [`CUMULATIVE_CARDINALITY`](#cumulative_cardinality)
- [`CUMULATIVE_ROWS_SCANNED`](#cumulative_rows_scanned)
- [`CUMULATIVE_OPTIMIZER_TIMING`](#cumulative_optimizer_timing)


## Examples

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

PRAGMA configure_profiling = '{"CPU_TIME": "false", "EXTRA_INFO": "true", "OPERATOR_CARDINALITY": "true", "OPERATOR_TIMING": "true"}';

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
