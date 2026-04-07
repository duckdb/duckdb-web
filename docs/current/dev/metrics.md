
---
layout: docu
title: Metrics
redirect_from:
  - /dev/metrics
---

DuckDB provides a set of metrics that can be used to monitor the performance and health of the database.

The query tree has two types of nodes: the `QUERY_ROOT` and `OPERATOR` nodes.
The `QUERY_ROOT` refers exclusively to the top-level node, and the metrics it contains are measured over the entire query.
The `OPERATOR` nodes refer to the individual operators in the query plan.
Some metrics are only available for `QUERY_ROOT` nodes, while others are only for `OPERATOR` nodes.
The table below describes each metric and which nodes they are available for.

Other than `OPERATOR_TYPE`, all metrics can be turned on or off.

# All Metrics
| Name                                                                              | Group                                 | Description                                                                |
|-----------------------------------------------------------------------------------|---------------------------------------|----------------------------------------------------------------------------|
| [`CPU_TIME`](#CPU_TIME)                                                           | [core](#core-metrics)                 | CPU time spent on the query                                                |
| [`CUMULATIVE_CARDINALITY`](#CUMULATIVE_CARDINALITY)                               | [core](#core-metrics)                 | Cumulative cardinality of the query                                        |
| [`CUMULATIVE_ROWS_SCANNED`](#CUMULATIVE_ROWS_SCANNED)                             | [core](#core-metrics)                 | Cumulative number of rows scanned by the query                             |
| [`EXTRA_INFO`](#EXTRA_INFO)                                                       | [core](#core-metrics)                 | Unique operator metrics                                                    |
| [`LATENCY`](#LATENCY)                                                             | [core](#core-metrics)                 | Time spent executing the entire query                                      |
| [`QUERY_NAME`](#QUERY_NAME)                                                       | [core](#core-metrics)                 | The SQL string of the query                                                |
| [`RESULT_SET_SIZE`](#RESULT_SET_SIZE)                                             | [core](#core-metrics)                 | The size of the result                                                     |
| [`ROWS_RETURNED`](#ROWS_RETURNED)                                                 | [core](#core-metrics)                 | The number of rows returned by the query                                   |
| [`BLOCKED_THREAD_TIME`](#BLOCKED_THREAD_TIME)                                     | [execution](#execution-metrics)       | Time spent waiting for a thread to become available                        |
| [`SYSTEM_PEAK_BUFFER_MEMORY`](#SYSTEM_PEAK_BUFFER_MEMORY)                         | [execution](#execution-metrics)       | Peak memory usage of the system                                            |
| [`SYSTEM_PEAK_TEMP_DIR_SIZE`](#SYSTEM_PEAK_TEMP_DIR_SIZE)                         | [execution](#execution-metrics)       | Peak size of the temporary directory                                       |
| [`TOTAL_MEMORY_ALLOCATED`](#TOTAL_MEMORY_ALLOCATED)                               | [execution](#execution-metrics)       | The total memory allocated by the buffer manager.                          |
| [`ATTACH_LOAD_STORAGE_LATENCY`](#ATTACH_LOAD_STORAGE_LATENCY)                     | [file](#file-metrics)                 | Time spent loading from storage.                                           |
| [`ATTACH_REPLAY_WAL_LATENCY`](#ATTACH_REPLAY_WAL_LATENCY)                         | [file](#file-metrics)                 | Time spent replaying the WAL file.                                         |
| [`CHECKPOINT_LATENCY`](#CHECKPOINT_LATENCY)                                       | [file](#file-metrics)                 | Time spent running checkpoints                                             |
| [`COMMIT_LOCAL_STORAGE_LATENCY`](#COMMIT_LOCAL_STORAGE_LATENCY)                   | [file](#file-metrics)                 | Time spent committing the transaction-local storage.                       |
| [`TOTAL_BYTES_READ`](#TOTAL_BYTES_READ)                                           | [file](#file-metrics)                 | The total bytes read by the file system.                                   |
| [`TOTAL_BYTES_WRITTEN`](#TOTAL_BYTES_WRITTEN)                                     | [file](#file-metrics)                 | The total bytes written by the file system.                                |
| [`WAITING_TO_ATTACH_LATENCY`](#WAITING_TO_ATTACH_LATENCY)                         | [file](#file-metrics)                 | Time spent waiting to ATTACH a file.                                       |
| [`WAL_REPLAY_ENTRY_COUNT`](#WAL_REPLAY_ENTRY_COUNT)                               | [file](#file-metrics)                 | The total number of entries to replay in the WAL.                          |
| [`WRITE_TO_WAL_LATENCY`](#WRITE_TO_WAL_LATENCY)                                   | [file](#file-metrics)                 | Time spent writing to the WAL.                                             |
| [`ALL_OPTIMIZERS`](#ALL_OPTIMIZERS)                                               | [phase_timing](#phase_timing-metrics) | Enables all optimizers                                                     |
| [`CUMULATIVE_OPTIMIZER_TIMING`](#CUMULATIVE_OPTIMIZER_TIMING)                     | [phase_timing](#phase_timing-metrics) | Time spent in all optimizers                                               |
| [`PHYSICAL_PLANNER`](#PHYSICAL_PLANNER)                                           | [phase_timing](#phase_timing-metrics) | The time spent generating the physical plan                                |
| [`PHYSICAL_PLANNER_COLUMN_BINDING`](#PHYSICAL_PLANNER_COLUMN_BINDING)             | [phase_timing](#phase_timing-metrics) | The time spent binding the columns in the logical plan to physical columns |
| [`PHYSICAL_PLANNER_CREATE_PLAN`](#PHYSICAL_PLANNER_CREATE_PLAN)                   | [phase_timing](#phase_timing-metrics) | The time spent creating the physical plan                                  |
| [`PHYSICAL_PLANNER_RESOLVE_TYPES`](#PHYSICAL_PLANNER_RESOLVE_TYPES)               | [phase_timing](#phase_timing-metrics) | The time spent resolving the types in the logical plan to physical types   |
| [`PLANNER`](#PLANNER)                                                             | [phase_timing](#phase_timing-metrics) | The time to generate the logical plan from the parsed SQL nodes.           |
| [`PLANNER_BINDING`](#PLANNER_BINDING)                                             | [phase_timing](#phase_timing-metrics) | The time taken to bind the logical plan.                                   |
| [`OPERATOR_CARDINALITY`](#OPERATOR_CARDINALITY)                                   | [operator](#operator-metrics)         | Cardinality of the operator                                                |
| [`OPERATOR_NAME`](#OPERATOR_NAME)                                                 | [operator](#operator-metrics)         | Name of the operator                                                       |
| [`OPERATOR_ROWS_SCANNED`](#OPERATOR_ROWS_SCANNED)                                 | [operator](#operator-metrics)         | Number of rows scanned by the operator                                     |
| [`OPERATOR_TIMING`](#OPERATOR_TIMING)                                             | [operator](#operator-metrics)         | Time spent in the operator                                                 |
| [`OPERATOR_TYPE`](#OPERATOR_TYPE)                                                 | [operator](#operator-metrics)         | Type of the operator                                                       |
| [`OPTIMIZER_EXPRESSION_REWRITER`](#OPTIMIZER_EXPRESSION_REWRITER)                 | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_EXPRESSION_REWRITER                                |
| [`OPTIMIZER_FILTER_PULLUP`](#OPTIMIZER_FILTER_PULLUP)                             | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_FILTER_PULLUP                                      |
| [`OPTIMIZER_FILTER_PUSHDOWN`](#OPTIMIZER_FILTER_PUSHDOWN)                         | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_FILTER_PUSHDOWN                                    |
| [`OPTIMIZER_EMPTY_RESULT_PULLUP`](#OPTIMIZER_EMPTY_RESULT_PULLUP)                 | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_EMPTY_RESULT_PULLUP                                |
| [`OPTIMIZER_CTE_FILTER_PUSHER`](#OPTIMIZER_CTE_FILTER_PUSHER)                     | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_CTE_FILTER_PUSHER                                  |
| [`OPTIMIZER_REGEX_RANGE`](#OPTIMIZER_REGEX_RANGE)                                 | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_REGEX_RANGE                                        |
| [`OPTIMIZER_IN_CLAUSE`](#OPTIMIZER_IN_CLAUSE)                                     | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_IN_CLAUSE                                          |
| [`OPTIMIZER_JOIN_ORDER`](#OPTIMIZER_JOIN_ORDER)                                   | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_JOIN_ORDER                                         |
| [`OPTIMIZER_DELIMINATOR`](#OPTIMIZER_DELIMINATOR)                                 | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_DELIMINATOR                                        |
| [`OPTIMIZER_UNNEST_REWRITER`](#OPTIMIZER_UNNEST_REWRITER)                         | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_UNNEST_REWRITER                                    |
| [`OPTIMIZER_UNUSED_COLUMNS`](#OPTIMIZER_UNUSED_COLUMNS)                           | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_UNUSED_COLUMNS                                     |
| [`OPTIMIZER_STATISTICS_PROPAGATION`](#OPTIMIZER_STATISTICS_PROPAGATION)           | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_STATISTICS_PROPAGATION                             |
| [`OPTIMIZER_COMMON_SUBEXPRESSIONS`](#OPTIMIZER_COMMON_SUBEXPRESSIONS)             | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_COMMON_SUBEXPRESSIONS                              |
| [`OPTIMIZER_COMMON_AGGREGATE`](#OPTIMIZER_COMMON_AGGREGATE)                       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_COMMON_AGGREGATE                                   |
| [`OPTIMIZER_COLUMN_LIFETIME`](#OPTIMIZER_COLUMN_LIFETIME)                         | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_COLUMN_LIFETIME                                    |
| [`OPTIMIZER_BUILD_SIDE_PROBE_SIDE`](#OPTIMIZER_BUILD_SIDE_PROBE_SIDE)             | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_BUILD_SIDE_PROBE_SIDE                              |
| [`OPTIMIZER_LIMIT_PUSHDOWN`](#OPTIMIZER_LIMIT_PUSHDOWN)                           | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_LIMIT_PUSHDOWN                                     |
| [`OPTIMIZER_TOP_N`](#OPTIMIZER_TOP_N)                                             | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_TOP_N                                              |
| [`OPTIMIZER_COMPRESSED_MATERIALIZATION`](#OPTIMIZER_COMPRESSED_MATERIALIZATION)   | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_COMPRESSED_MATERIALIZATION                         |
| [`OPTIMIZER_DUPLICATE_GROUPS`](#OPTIMIZER_DUPLICATE_GROUPS)                       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_DUPLICATE_GROUPS                                   |
| [`OPTIMIZER_REORDER_FILTER`](#OPTIMIZER_REORDER_FILTER)                           | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_REORDER_FILTER                                     |
| [`OPTIMIZER_SAMPLING_PUSHDOWN`](#OPTIMIZER_SAMPLING_PUSHDOWN)                     | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_SAMPLING_PUSHDOWN                                  |
| [`OPTIMIZER_JOIN_FILTER_PUSHDOWN`](#OPTIMIZER_JOIN_FILTER_PUSHDOWN)               | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_JOIN_FILTER_PUSHDOWN                               |
| [`OPTIMIZER_EXTENSION`](#OPTIMIZER_EXTENSION)                                     | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_EXTENSION                                          |
| [`OPTIMIZER_MATERIALIZED_CTE`](#OPTIMIZER_MATERIALIZED_CTE)                       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_MATERIALIZED_CTE                                   |
| [`OPTIMIZER_AGGREGATE_FUNCTION_REWRITER`](#OPTIMIZER_AGGREGATE_FUNCTION_REWRITER) | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_AGGREGATE_FUNCTION_REWRITER                        |
| [`OPTIMIZER_LATE_MATERIALIZATION`](#OPTIMIZER_LATE_MATERIALIZATION)               | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_LATE_MATERIALIZATION                               |
| [`OPTIMIZER_CTE_INLINING`](#OPTIMIZER_CTE_INLINING)                               | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_CTE_INLINING                                       |
| [`OPTIMIZER_ROW_GROUP_PRUNER`](#OPTIMIZER_ROW_GROUP_PRUNER)                       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_ROW_GROUP_PRUNER                                   |
| [`OPTIMIZER_TOP_N_WINDOW_ELIMINATION`](#OPTIMIZER_TOP_N_WINDOW_ELIMINATION)       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_TOP_N_WINDOW_ELIMINATION                           |
| [`OPTIMIZER_COMMON_SUBPLAN`](#OPTIMIZER_COMMON_SUBPLAN)                           | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_COMMON_SUBPLAN                                     |
| [`OPTIMIZER_JOIN_ELIMINATION`](#OPTIMIZER_JOIN_ELIMINATION)                       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_JOIN_ELIMINATION                                   |
| [`OPTIMIZER_WINDOW_SELF_JOIN`](#OPTIMIZER_WINDOW_SELF_JOIN)                       | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_WINDOW_SELF_JOIN                                   |
| [`OPTIMIZER_PROJECTION_PULLUP`](#OPTIMIZER_PROJECTION_PULLUP)                     | [optimizer](#optimizer-metrics)       | Time spent in OPTIMIZER_PROJECTION_PULLUP                                  |


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
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |
| **[Cumulative](#cumulative_metrics)** | '✅' |
| **Child** | OPERATOR_TIMING |

#### `CUMULATIVE_CARDINALITY`

<div class="nostroke_table"></div>

| **Description** | Cumulative cardinality of the query |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |
| **[Cumulative](#cumulative_metrics)** | '✅' |
| **Child** | OPERATOR_CARDINALITY |

#### `CUMULATIVE_ROWS_SCANNED`

<div class="nostroke_table"></div>

| **Description** | Cumulative number of rows scanned by the query |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |
| **[Cumulative](#cumulative_metrics)** | '✅' |
| **Child** | OPERATOR_ROWS_SCANNED |

#### `EXTRA_INFO`

<div class="nostroke_table"></div>

| **Description** | Unique operator metrics |
| **Type** | Value::MAP |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |

#### `LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent executing the entire query |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `QUERY_NAME`

<div class="nostroke_table"></div>

| **Description** | The SQL string of the query |
| **Type** | string |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `RESULT_SET_SIZE`

<div class="nostroke_table"></div>

| **Description** | The size of the result |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |
| **Child** | RESULT_SET_SIZE |

#### `ROWS_RETURNED`

<div class="nostroke_table"></div>

| **Description** | The number of rows returned by the query |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Child** | OPERATOR_CARDINALITY |

### Execution Metrics
Metrics that are collected during query execution

#### `BLOCKED_THREAD_TIME`

<div class="nostroke_table"></div>

| **Description** | Time spent waiting for a thread to become available |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `SYSTEM_PEAK_BUFFER_MEMORY`

<div class="nostroke_table"></div>

| **Description** | Peak memory usage of the system |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |

#### `SYSTEM_PEAK_TEMP_DIR_SIZE`

<div class="nostroke_table"></div>

| **Description** | Peak size of the temporary directory |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | '✅' |
| **Query Node** | '✅' |
| **Operator Node** | '✅' |

#### `TOTAL_MEMORY_ALLOCATED`

<div class="nostroke_table"></div>

| **Description** | The total memory allocated by the buffer manager. |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | '✅' |
| **Query Node** | '✅' |

### File Metrics
metrics that are collected during file operations

#### `ATTACH_LOAD_STORAGE_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent loading from storage. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `ATTACH_REPLAY_WAL_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent replaying the WAL file. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `CHECKPOINT_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent running checkpoints |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `COMMIT_LOCAL_STORAGE_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent committing the transaction-local storage. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `TOTAL_BYTES_READ`

<div class="nostroke_table"></div>

| **Description** | The total bytes read by the file system. |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `TOTAL_BYTES_WRITTEN`

<div class="nostroke_table"></div>

| **Description** | The total bytes written by the file system. |
| **Type** | uint64 |
| **Unit** | bytes |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `WAITING_TO_ATTACH_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent waiting to ATTACH a file. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `WAL_REPLAY_ENTRY_COUNT`

<div class="nostroke_table"></div>

| **Description** | The total number of entries to replay in the WAL. |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | '✅' |
| **Query Node** | '✅' |

#### `WRITE_TO_WAL_LATENCY`

<div class="nostroke_table"></div>

| **Description** | Time spent writing to the WAL. |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Query Node** | '✅' |

### Operator Metrics
metrics that are collected for each operator

#### `OPERATOR_CARDINALITY`

<div class="nostroke_table"></div>

| **Description** | Cardinality of the operator |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | '✅' |
| **Operator Node** | '✅' |

#### `OPERATOR_NAME`

<div class="nostroke_table"></div>

| **Description** | Name of the operator |
| **Type** | string |
| **Default** | '✅' |
| **Operator Node** | '✅' |

#### `OPERATOR_ROWS_SCANNED`

<div class="nostroke_table"></div>

| **Description** | Number of rows scanned by the operator |
| **Type** | uint64 |
| **Unit** | absolute |
| **Default** | '✅' |
| **Operator Node** | '✅' |

#### `OPERATOR_TIMING`

<div class="nostroke_table"></div>

| **Description** | Time spent in the operator |
| **Type** | double |
| **Unit** | seconds |
| **Default** | '✅' |
| **Operator Node** | '✅' |

#### `OPERATOR_TYPE`

<div class="nostroke_table"></div>

| **Description** | Type of the operator |
| **Type** | uint8 |
| **Default** | '✅' |
| **Operator Node** | '✅' |

### Phase_timing Metrics
This group contains metrics related to the planner and the physical planner. The planner is responsible for generating the logical plan, whereas the physical planner is responsible for generating the physical plan from the logical plan.

#### `PHYSICAL_PLANNER`

<div class="nostroke_table"></div>

| **Description** | The time spent generating the physical plan |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |

#### `PHYSICAL_PLANNER_COLUMN_BINDING`

<div class="nostroke_table"></div>

| **Description** | The time spent binding the columns in the logical plan to physical columns |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |

#### `PHYSICAL_PLANNER_CREATE_PLAN`

<div class="nostroke_table"></div>

| **Description** | The time spent creating the physical plan |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |

#### `PHYSICAL_PLANNER_RESOLVE_TYPES`

<div class="nostroke_table"></div>

| **Description** | The time spent resolving the types in the logical plan to physical types |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |

#### `PLANNER`

<div class="nostroke_table"></div>

| **Description** | The time to generate the logical plan from the parsed SQL nodes. |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |

#### `PLANNER_BINDING`

<div class="nostroke_table"></div>

| **Description** | The time taken to bind the logical plan. |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |


### Optimizer Metrics
Optimizer metrics sit at the `QUERY_ROOT` level, and measure the time taken by each [optimizer]({% link docs/current/internals/overview.md %}#optimizer).
These metrics are only available when the specific optimizer is enabled.
The available optimizations can be queried using the [`duckdb_optimizers()`{:.language-sql .highlight} table function]({% link docs/current/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers).

Each optimizer has a corresponding metric that follows the template: `OPTIMIZER_⟨OPTIMIZER_NAME⟩`{:.language-sql .highlight}.
For example, the `OPTIMIZER_JOIN_ORDER` metric corresponds to the `JOIN_ORDER` optimizer.

Additionally, the following metrics are available to support the optimizer metrics:

#### `ALL_OPTIMIZERS`

<div class="nostroke_table"></div>

| **Description** | Enables all optimizers |
| **Type** | double |
| **Query Node** | '✅' |

#### `CUMULATIVE_OPTIMIZER_TIMING`

<div class="nostroke_table"></div>

| **Description** | Time spent in all optimizers |
| **Type** | double |
| **Unit** | milliseconds |
| **Query Node** | '✅' |


## Cumulative Metrics

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

