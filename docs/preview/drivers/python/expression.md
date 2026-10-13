---
layout: docu
title: Expression API
---

The `Expression` class represents an instance of an [expression]({% link docs/preview/sql/expressions/overview.md %}).

## Why Would I Use the Expression API?

Using this API makes it possible to dynamically build up expressions, which are typically created by the parser from the query string.
This allows you to skip that and have more fine-grained control over the used expressions.

Below is a list of currently supported expressions that can be created through the API.

## Column Expression

This expression references a column by name.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})
```

Selecting a single column:

```python
col = duckdb.ColumnExpression('a')
duckdb.df(df).select(col).show()
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│     1 │
│     2 │
│     3 │
│     4 │
└───────┘
```

Selecting multiple columns:

```python
col_list = [
        duckdb.ColumnExpression('a') * 10,
        duckdb.ColumnExpression('b').isnull(),
        duckdb.ColumnExpression('c') + 5
    ]
duckdb.df(df).select(*col_list).show()
```

```text
┌──────────┬─────────────┬─────────┐
│ (a * 10) │ (b IS NULL) │ (c + 5) │
│  int64   │   boolean   │  int64  │
├──────────┼─────────────┼─────────┤
│       10 │ false       │      47 │
│       20 │ true        │      26 │
│       30 │ false       │      18 │
│       40 │ false       │      19 │
└──────────┴─────────────┴─────────┘
```

## Star Expression

This expression selects all columns of the input source.

Optionally it's possible to provide an `exclude` list to filter out columns of the table.
This `exclude` list can contain either strings or Expressions.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

star = duckdb.StarExpression(exclude = ['b'])
duckdb.df(df).select(star).show()
```

```text
┌───────┬───────┐
│   a   │   c   │
│ int64 │ int64 │
├───────┼───────┤
│     1 │    42 │
│     2 │    21 │
│     3 │    13 │
│     4 │    14 │
└───────┴───────┘
```

## Constant Expression

This expression contains a single value.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

const = duckdb.ConstantExpression('hello')
duckdb.df(df).select(const).show()
```

```text
┌─────────┐
│ 'hello' │
│ varchar │
├─────────┤
│ hello   │
│ hello   │
│ hello   │
│ hello   │
└─────────┘
```

## Case Expression

This expression contains a `CASE WHEN (...) THEN (...) ELSE (...) END` expression.
By default `ELSE` is `NULL` and it can be set using `.else(value = ...)`.
Additional `WHEN (...) THEN (...)` blocks can be added with `.when(condition = ..., value = ...)`.

```python
import duckdb
import pandas as pd
from duckdb import (
    ConstantExpression,
    ColumnExpression,
    CaseExpression
)

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

hello = ConstantExpression('hello')
world = ConstantExpression('world')

case = \
    CaseExpression(condition = ColumnExpression('b') == False, value = world) \
    .otherwise(hello)
duckdb.df(df).select(case).show()
```

```text
┌──────────────────────────────────────────────────────────┐
│ CASE  WHEN ((b = false)) THEN ('world') ELSE 'hello' END │
│                         varchar                          │
├──────────────────────────────────────────────────────────┤
│ hello                                                    │
│ hello                                                    │
│ world                                                    │
│ hello                                                    │
└──────────────────────────────────────────────────────────┘
```

## Function Expression

This expression contains a function call.
It can be constructed by providing the function name and an arbitrary amount of Expressions as arguments.

```python
import duckdb
import pandas as pd
from duckdb import (
    ConstantExpression,
    ColumnExpression,
    FunctionExpression
)

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

multiply_by_2 = FunctionExpression('multiply', ColumnExpression('a'), ConstantExpression(2))
duckdb.df(df).select(multiply_by_2).show()
```

```text
┌────────────────┐
│ multiply(a, 2) │
│     int64      │
├────────────────┤
│              2 │
│              4 │
│              6 │
│              8 │
└────────────────┘
```

## SQL Expression

This expression contains any valid SQL expression.

```python
import duckdb
import pandas as pd

from duckdb import SQLExpression

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

duckdb.df(df).filter(
    SQLExpression("b is true")
).select(
    SQLExpression("a").alias("selecting_column_a"),
    SQLExpression("case when a = 1 then 1 else 0 end").alias("selecting_case_expression"),
    SQLExpression("1").alias("constant_numeric_column"),
    SQLExpression("'hello'").alias("constant_text_column")
).aggregate(
    aggr_expr=[
        SQLExpression("SUM(selecting_column_a)").alias("sum_a"), 
        "selecting_case_expression" , 
        "constant_numeric_column", 
        "constant_text_column"
    ],
).show()
```

```text
┌────────┬───────────────────────────┬─────────────────────────┬──────────────────────┐
│ sum_a  │ selecting_case_expression │ constant_numeric_column │ constant_text_column │
│ int128 │           int32           │          int32          │       varchar        │
├────────┼───────────────────────────┼─────────────────────────┼──────────────────────┤
│      4 │                         0 │                       1 │ hello                │
│      1 │                         1 │                       1 │ hello                │
└────────┴───────────────────────────┴─────────────────────────┴──────────────────────┘
```

## Common Operations

The Expression class also contains many operations that can be applied to any Expression type.

| Operation                      | Description                                                                                                                 |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `.alias(name: str)`            | Applies an alias to the expression                                                                                          |
| `.cast(type: DuckDBPyType)`    | Applies a cast to the provided type on the expression                                                                       |
| `.isin(*exprs: Expression)`    | Creates an [`IN` expression]({% link docs/preview/sql/expressions/in.md %}#in) against the provided expressions as the list         |
| `.isnotin(*exprs: Expression)` | Creates a [`NOT IN` expression]({% link docs/preview/sql/expressions/in.md %}#not-in) against the provided expressions as the list  |
| `.isnotnull()`                 | Checks whether the expression is not `NULL`                                                                                 |
| `.isnull()`                    | Checks whether the expression is `NULL`                                                                                     |

### Order Operations

When expressions are provided to `DuckDBPyRelation.order()`, the following order operations can be applied.

| Operation                      | Description                                                                        |
|--------------------------------|------------------------------------------------------------------------------------|
| `.asc()`                       | Indicates that this expression should be sorted in ascending order                 |
| `.desc()`                      | Indicates that this expression should be sorted in descending order                |
| `.nulls_first()`               | Indicates that the nulls in this expression should precede the non-null values     |
| `.nulls_last()`                | Indicates that the nulls in this expression should come after the non-null values  |
