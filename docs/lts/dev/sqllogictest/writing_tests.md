---
layout: docu
title: Writing Tests
---

## Development and Testing

It is crucial that any new features that get added have correct tests that not only test the “happy path”, but also test edge cases and incorrect usage of the feature. In this section, we describe how DuckDB tests are structured and how to make new tests for DuckDB.

The tests can be run by running the `unittest` program located in the `test` folder. For the default compilations this is located in either `build/release/test/unittest` (release) or `build/debug/test/unittest` (debug).

## Philosophy

When testing DuckDB, we aim to route all the tests through SQL. We try to avoid testing components individually because that makes those components more difficult to change later on. As such, almost all of our tests can (and should) be expressed in pure SQL. There are certain exceptions to this, which we will discuss in [Catch Tests]({% link docs/lts/dev/sqllogictest/catch.md %}). However, in most cases you should write your tests in plain SQL.

## Frameworks

SQL tests should be written using the [sqllogictest framework]({% link docs/lts/dev/sqllogictest/intro.md %}).

C++ tests can be written using the [Catch framework]({% link docs/lts/dev/sqllogictest/catch.md %}).

## Client Connector Tests

DuckDB also has tests for various client connectors. These are generally written in the relevant client language, and can be found in `tools/*/tests`.
They also double as documentation of what should be doable from a given client.

## Functions for Generating Test Data

DuckDB has built-in functions for generating test data.

### `test_all_types` Function

The `test_all_types` table function generates a table whose columns correspond to types (`BOOL`, `TINYINT`, etc.).
The table has three rows encoding the minimum value, the maximum value, and the `NULL` value for each type.

```sql
FROM test_all_types();
```

```text
┌─────────┬─────────┬──────────┬─────────────┬──────────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│  bool   │ tinyint │ smallint │     int     │        bigint        │       hugeint        │ … │        struct        │   struct_of_arrays   │   array_of_structs   │         map          │        union         │
│ boolean │  int8   │  int16   │    int32    │        int64         │        int128        │   │ struct(a integer, …  │ struct(a integer[]…  │ struct(a integer, …  │ map(varchar, varch…  │ union("name" varch…  │
├─────────┼─────────┼──────────┼─────────────┼──────────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ false   │    -128 │   -32768 │ -2147483648 │ -9223372036854775808 │  -17014118346046923… │ … │ {'a': NULL, 'b': N…  │ {'a': NULL, 'b': N…  │ []                   │ {}                   │ Frank                │
│ true    │     127 │    32767 │  2147483647 │  9223372036854775807 │  170141183460469231… │ … │ {'a': 42, 'b': 🦆…   │ {'a': [42, 999, NU…  │ [{'a': NULL, 'b': …  │ {key1=🦆🦆🦆🦆🦆🦆…  │ 5                    │
│ NULL    │    NULL │     NULL │        NULL │                 NULL │                 NULL │ … │ NULL                 │ NULL                 │ NULL                 │ NULL                 │ NULL                 │
├─────────┴─────────┴──────────┴─────────────┴──────────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┤
│ 3 rows                                                                                                                                                                                    44 columns (11 shown) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### `test_vector_types` Function

The `test_vector_types` table function takes _n_ arguments `col1`, ..., `coln` and an optional `BOOLEAN` argument `all_flat`.
The function generates a table with _n_ columns `test_vector`, `test_vector2`, ..., `test_vectorn`.
In each row, each field contains values conforming to the type of their respective column.

```sql
FROM test_vector_types(NULL::BIGINT);
```

```text
┌──────────────────────┐
│     test_vector      │
│        int64         │
├──────────────────────┤
│ -9223372036854775808 │
│  9223372036854775807 │
│                 NULL │
│         ...          │
└──────────────────────┘
```

```sql
FROM test_vector_types(NULL::ROW(i INTEGER, j VARCHAR, k DOUBLE), NULL::TIMESTAMP);
```

```text
┌──────────────────────────────────────────────────────────────────────┬──────────────────────────────┐
│                             test_vector                              │         test_vector2         │
│                struct(i integer, j varchar, k double)                │          timestamp           │
├──────────────────────────────────────────────────────────────────────┼──────────────────────────────┤
│ {'i': -2147483648, 'j': 🦆🦆🦆🦆🦆🦆, 'k': -1.7976931348623157e+308} │ 290309-12-22 (BC) 00:00:00   │
│ {'i': 2147483647, 'j': goo\0se, 'k': 1.7976931348623157e+308}        │ 294247-01-10 04:00:54.775806 │
│ {'i': NULL, 'j': NULL, 'k': NULL}                                    │ NULL                         │
│                                                  ...                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

`test_vector_types` has an optional argument called `all_flat` of type `BOOL`. This only affects the internal representation of the vector.

```sql
FROM test_vector_types(NULL::ROW(i INTEGER, j VARCHAR, k DOUBLE), NULL::TIMESTAMP, all_flat = true);
-- the output is the same as above but with a different internal representation
```
