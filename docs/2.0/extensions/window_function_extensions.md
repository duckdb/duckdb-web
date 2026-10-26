---
layout: docu
redirect_from:
- /docs/current/extensions/window_function_extensions
- /docs/lts/extensions/window_function_extensions
- /docs/preview/extensions/window_function_extensions
title: Window Function Extensions
---

> New Support for defining window functions in extensions was introduced in DuckDB 2.0. The API is part of the C++ extension API and may still change.

Every [aggregate function]({% link docs/2.0/sql/functions/aggregates.md %}) can be used as a [window function]({% link docs/2.0/sql/functions/window_functions.md %}), but not every windowed operation is an aggregate. For example, [`fill`]({% link docs/2.0/sql/functions/window_functions.md %}#fillexpr-order-by-ordering) interpolates missing values, a `reduce(init, lambda)` function could apply running updates without a frame and a `rank(value)` function could compute the “hypothetical rank” of a value. Since DuckDB 2.0, window functions are catalog entries, so extensions can define new ones using the same API that the built-in window functions use.

## Registering Window Functions

To define a window function, derive from the [`WindowFunction` class](https://github.com/duckdb/duckdb/blob/v2.0.0/src/include/duckdb/function/window_function.hpp) and register it in the extension's load function using the `ExtensionLoader`:

```cpp
DuckWeedFunction duckweed;
loader.RegisterFunction(duckweed);
```

Registered window functions are listed by [`duckdb_functions()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_functions) with the function type `window` and can be looked up with the CLI's [`.manual` dot command]({% link docs/2.0/clients/cli/dot_commands.md %}#displaying-function-documentation).

## Binding

The `WindowFunction` constructor takes the function's name, argument types, return type and callbacks. The optional `bind` callback receives the arguments along with the types of the window's `ORDER BY` and the argument `ORDER BY` clauses, so it can resolve the return type and add bind data. The following methods declare which modifiers the function supports:

| Method | Modifier | Default |
|---|---|---|
| `SetCanDistinct` | `DISTINCT` arguments | `false` |
| `SetCanFilter` | `FILTER` clause | `false` |
| `SetCanOrderBy` | `ORDER BY` arguments | `true` |
| `SetCanExclude` | `EXCLUDE` clause | `false` |
| `SetCanIgnoreNulls` | `IGNORE NULLS` | `true` |

## Blocking Interface

Window functions are typically evaluated in a blocking fashion: the window operator first partitions and sorts the input into hash groups, then evaluates the function on each hash group. A blocking window function implements the following callbacks:

| Callback | Description |
|---|---|
| `bounds` | Requests the bounds that the function needs: partition (`PARTITION BY`), peers (`RANGE` and `GROUPS`), valid values (`NULL` handling) and frame (`BETWEEN`). |
| `sharing` | Registers the argument expressions so that their values are shared with other window functions, either as a fully materialized collection or as chunks during the sink and evaluate phases. |
| `global`, `local` | Construct the global and thread-local states for a hash group. |
| `sink`, `finalize` | Make a first pass over the data to construct acceleration structures such as merge sort trees. This phase is fully parallel. There is no combine step, so updates to the global state must be synchronized, e.g., using locks. |
| `evaluate` | Computes the result `Vector` for a chunk of rows using the arguments, the index of the first row within the hash group, the requested bounds and the global and local states. Evaluation is fully parallel, so the chunks are usually but not necessarily consecutive. |

## Streaming Interface

Some window functions can also be streamed, i.e., evaluated one chunk at a time without materializing the input. DuckDB only considers streaming if the window has no `PARTITION BY`, no `ORDER BY` and no `EXCLUDE` clause. For aggregates, this covers “running totals” (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`). A window function opts in by implementing the following callbacks:

| Callback | Description |
|---|---|
| `can_stream` | Decides whether the window expression can be streamed, given the maximum number of rows that the operator can buffer. |
| `streaming_state` | Constructs the state, which derives from `WindowExecutorStreamingState`. Its `offset` field sets the buffering offset, which is how `lead` and `lag` are streamed. Streaming is single-threaded, so there is only one state. |
| `stream` | Computes the result `Vector` for a chunk of rows using the input, the buffered (delayed) input and the state. |

## Example

The [loadable extension demo](https://github.com/duckdb/duckdb/blob/v2.0.0/test/extension/loadable_extension_demo.cpp) defines `duckweed`, a “fill down” window function that replaces `NULL` values with the last non-`NULL` value and implements both the blocking and the streaming interface. With the demo extension loaded, the following query uses the streaming interface:

```sql
SELECT i, m, duckweed(m) OVER () AS d
FROM (
    SELECT i, if(i % 5, i, NULL) AS m
    FROM range(8) t(i)
);
```

| i | m    | d    |
|--:|-----:|-----:|
| 0 | NULL | NULL |
| 1 | 1    | 1    |
| 2 | 2    | 2    |
| 3 | 3    | 3    |
| 4 | 4    | 4    |
| 5 | NULL | 4    |
| 6 | 6    | 6    |
| 7 | 7    | 7    |

Adding `PARTITION BY` or `ORDER BY` to the `OVER` clause switches to the blocking interface.

For more details, see Richard Wesley's talk [“Window Extensions: Defining New Window Functions”](https://blobs.duckdb.org/events/duckdb-boston/meetup/richard-wesley-windowing.pdf).
