---
layout: post
title: "Traversing Query Results in DuckDB's C++ API"
author: "Geertjan Wielenga"
thumb: "/images/blog/thumbs/command-line.svg"
image: "/images/blog/thumbs/command-line.png"
excerpt: "DuckDB's C++ API returns a fully materialized result, but the documentation never showed how to read the values back out. This post covers the issue behind the missing example, the ways to traverse a result, how value access works, and how we checked the example against the DuckDB source."
tags: ["using DuckDB"]
---

The DuckDB [C++ API]({% link docs/current/clients/cpp.md %}) is built around a `Connection` whose `Query()` method runs a SQL statement and returns a result. For a one-off look, `result->ToString()` or `result->Print()` is enough. To use the individual values in your own program, you read the result one cell at a time. The documentation described the result object in detail but did not show how to do that. The example meant to cover it was never written, and the code block that would have held it was left empty.

This post covers the issue that tracked the gap, the change that had made the surrounding prose wrong, the ways to traverse a result and the trade-offs between them, how value access works, and how we verified the new example against the DuckDB source.

## The Gap in the Docs

The missing example was tracked in [duckdb-web#1024](https://github.com/duckdb/duckdb-web/issues/1024), opened by Gábor Szárnyas in August 2023. The C++ page described a `MaterializedQueryResult` and its fields, the statement type, the column types, the column names, but the code sample meant to show traversal held only a placeholder. The issue noted that the block was removed until someone could complete it. That took two years.

The example matters because a materialized result is not something you print and discard. It is a table in memory, and the reason to use the C++ API over the [CLI]({% link docs/current/clients/cli/overview.md %}) is to pull those values into your own program. Without a worked example, every reader had to guess at the method names, and some of those names had changed.

## Why the Surrounding Prose Was Wrong

The C++ API is internal. The page says so in a warning at the top: it is not guaranteed to be stable and can change without notice, which is why DuckDB recommends the [C API]({% link docs/current/clients/c/overview.md %}) for building applications. The result-traversal gap was one case of this. While the example sat unwritten, the result classes changed.

The old prose told you to read fields directly: the statement type was "in `statement_type`", the column types were "in `types`", and the names were "in the `names` string vector". That is no longer true. In the current `BaseQueryResult`, those three members are private. Reading them from outside the class does not compile. The values are still there, but you reach them through public accessors instead:

* `GetStatementType()` for the kind of statement that ran
* `GetTypes()` for the logical types of the columns
* `GetNames()` for the column names

So the fix was two changes in one. The prose had to move from naming fields to naming the accessors that replaced them, and the empty code block had to be filled with a traversal that uses those same accessors.

## Ways to Traverse a Result

There is more than one way to read a `MaterializedQueryResult`, and they trade simplicity against speed. It is worth seeing them side by side before picking one for the docs.

The simplest is not traversal at all. If you only want to see the result, render the whole thing:

```cpp
auto result = con.Query("SELECT * FROM integers");
cout << result->ToString() << endl;
```

The next step up is access by index. A materialized result reports its shape through `ColumnCount()` and `RowCount()`, and `GetValue(column, row)` returns a single cell. The example uses this approach, because it treats the result as a grid you index into, which is how most readers expect to read one:

```cpp
auto result = con.Query("SELECT * FROM integers");
if (result->HasError()) {
    cerr << result->GetError() << endl;
} else {
    // Print the column names as a header row
    for (idx_t col_idx = 0; col_idx < result->ColumnCount(); col_idx++) {
        cout << result->GetNames()[col_idx];
        cout << (col_idx + 1 < result->ColumnCount() ? "\t" : "\n");
    }
    // Iterate over every row and column of the materialized result
    for (idx_t row_idx = 0; row_idx < result->RowCount(); row_idx++) {
        for (idx_t col_idx = 0; col_idx < result->ColumnCount(); col_idx++) {
            // GetValue returns a duckdb::Value; ToString renders it (NULL values become "NULL")
            cout << result->GetValue(col_idx, row_idx).ToString();
            cout << (col_idx + 1 < result->ColumnCount() ? "\t" : "\n");
        }
    }
}
```

The fastest option on large results is to scan the result in chunks rather than cell by cell. A materialized result is backed by a column data collection, and both the chunked `Fetch()` loop and the streaming result API read whole vectors at a time instead of doing a lookup per value. That code is longer to write, so it fits performance-sensitive paths rather than a first example.

The documentation leads with the index-based version on purpose. It answers the question most readers have, "how do I get the values out", without the vectorized code in the way. The chunked scan is a follow-up once the shape of a result is clear.

## How Value Access Works

Two details in that example are easy to get wrong.

`GetValue(column, row)` takes the column first and the row second. A result reads as rows of columns, so the loop nests rows on the outside and columns on the inside, while the call itself is still `(col_idx, row_idx)`. Swapping the two arguments compiles and then reads the wrong cell, or runs off the end of a narrow result.

The call returns a `duckdb::Value`, DuckDB's boxed single value, not a raw `int` or `std::string`. Calling `.ToString()` on it renders whatever it holds as text, and a SQL `NULL` comes back as the string `"NULL"` instead of crashing or printing an empty cell. That is why the example can treat every column the same way regardless of its type. To get the raw C++ value instead of its text form, use the templated `GetValue<T>(column, row)`, which returns type `T`.

There is a cost to this approach. Reading the collection one value at a time is convenient but not cheap, which is the trade-off behind the chunked scan for large results. For printing a result or reading a handful of cells, the index-based version is a good fit.

## Verifying Against the Source

Because the C++ API can change without notice, every signature in the example was verified against the headers on the DuckDB `main` branch rather than from memory.

Two headers carry the relevant declarations. [`query_result.hpp`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/main/query_result.hpp) defines `BaseQueryResult`, and it confirms the central point of the fix: `statement_type`, `types`, and `names` sit in the private section, while `GetStatementType()`, `GetTypes()`, `GetNames()`, `HasError()`, and `GetError()` are the public accessors. `ColumnCount()` is public here too, which is why it is available on the materialized result.

[`materialized_query_result.hpp`](https://github.com/duckdb/duckdb/blob/main/src/include/duckdb/main/materialized_query_result.hpp) defines `MaterializedQueryResult` and confirms the rest. `RowCount()` returns an `idx_t`, and `GetValue` is declared as `Value GetValue(idx_t column, idx_t index)`, with the column parameter first. The same header carries the comment that this per-value access is slow and that scanning the underlying collection is faster, which is where the recommendation to scan large results comes from.

Checking the example against the headers is what caught the drift that left the old prose wrong. The members had gone private, the accessors were the supported way in, and the example now matches the code it documents.

## Conclusion

DuckDB's C++ API returns a fully materialized result, and the documentation now shows how to read it: check for an error, read the column names, and index each cell with `GetValue(column, row)`, rendering values with `ToString()`. The surrounding prose points at the public accessors that replaced the old fields, and every signature was checked against the current DuckDB headers. You can see the finished version on the [C++ API page]({% link docs/current/clients/cpp.md %}).
