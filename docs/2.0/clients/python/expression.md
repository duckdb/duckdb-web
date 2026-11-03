---
layout: docu
redirect_from:
- /docs/api/python/expression
- /docs/clients/python/expression
- /docs/stable/clients/python/expression
- /docs/current/clients/python/expression
- /docs/lts/clients/python/expression
- /docs/preview/clients/python/expression
title: Expression API
---

The `Expression` class represents an instance of an [expression]({% link docs/2.0/sql/expressions/overview.md %}).

## Why Would I Use the Expression API?

Use expressions to build filters and computed columns in Python. They are useful when column names or conditions depend on your code.

```python
import duckdb
import pandas as pd
from duckdb import col

sales = pd.DataFrame({"item": ["jeans", "hammer"], "price": [20, 42]})
price_column = "price"
rel = duckdb.from_df(sales)
print(rel.filter(col(price_column) > 30).fetchall())
```

```text
[('hammer', 42)]
```

An expression is passed to a method of a [relation]({% link docs/2.0/clients/python/relational_api.md %}), such as `select`, `filter`, `aggregate`, or `sort`. `str()` of an expression returns its SQL text, with the identifiers quoted and every operation in parentheses:

```python
print((col("a") > 1) & col("b"))
```

```text
(("a" > 1) AND "b")
```

The `duckdb` module has a short helper for each kind of expression, and this page uses them throughout. The constructors of the earlier expression API still work and build the same expressions, but new code should use the helpers:

| Helper | Older constructor |
|:--|:--|
| `col(name)` | `ColumnExpression(name)` |
| `lit(value)` | `ConstantExpression(value)` |
| `when(condition).then(value)` | `CaseExpression(condition, value)` |
| `fn(name, *args)` | `FunctionExpression(name, *args)` |
| `star(exclude=...)` | `StarExpression(exclude=...)` |
| `sql_expr(text)` | `SQLExpression(text)` |
| `coalesce(*values)` | `CoalesceOperator(*values)` |
| a Python function, such as `lambda x: x * 2` | `LambdaExpression(lhs, rhs)` |
| `.is_null()`, `.is_not_null()` | `.isnull()`, `.isnotnull()` |

## Values and Operators

Python operators combine expressions with each other and with Python values. The arithmetic operators are `+`, `-`, `*`, `/`, `//`, `%`, and `**`; the comparisons are `==`, `!=`, `<`, `<=`, `>`, and `>=`; `&`, `|`, and `~` are `AND`, `OR`, and `NOT`. A Python value in an operation is a constant. This holds for a string too: `col("s") == "x"` compares the column `s` with the text `x`. Use `col("x")` to compare with the column `x`, and `lit("x")` to make a constant explicit:

```python
rel = duckdb.sql("SELECT * FROM (VALUES ('x', 'y'), ('y', 'x')) t(s, x)")
print(rel.filter(col("s") == col("x")).fetchall())
print(rel.filter(col("s") == duckdb.lit("x")).fetchall())
```

```text
[]
[('x', 'y')]
```

When a plain string is also the name of a column of the relation, as in `rel.filter(col("s") == "x")`, DuckDB uses the string as a value and warns: `UserWarning: 'x' is used as a string value, and it is also a column name; use col('x') for the column, or lit('x') to keep the value and silence this warning`.

An expression has no truth value: `bool()` of an expression, as in `if col("a") == 1:`, raises `TypeError: an expression has no truth value; combine with & | ~, and test with .is_null()`. An operand that is neither an expression nor a value also raises a `TypeError`.

Below is a list of currently supported expressions that can be created through the API.

## Column Expression

This expression references a column by name, with `col(name)`.

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
a_column = duckdb.col('a')
duckdb.from_df(df).select(a_column).show()
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
        duckdb.col('a') * 10,
        duckdb.col('b').is_null(),
        duckdb.col('c') + 5
    ]
duckdb.from_df(df).select(*col_list).show()
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

A name is never split at a dot: `col("st.a")` is the column named `st.a`. For a qualified column or a field of a `STRUCT`, give the parts, as in `col("st", "a")`, or index the expression, as in `col("st")["a"]`. Indexing with `[]` also takes an entry of a map by key, or an element of a list by position as in [SQL]({% link docs/2.0/sql/data_types/list.md %}#retrieving-from-lists): the first element is at position 1, a negative position counts from the end, and position 0 or a position out of range gives `NULL`.

```python
rel = duckdb.sql("SELECT {'a': 1} AS st, 2 AS \"st.a\"")
print(rel.select(duckdb.col("st.a"), duckdb.col("st", "a"), col("st")["a"]).fetchall())
```

```text
[(2, 1, 1)]
```

## Star Expression

This expression selects all columns of the input source.

Optionally it's possible to provide an `exclude` list to filter out columns of the table.
This `exclude` list holds column names. To leave out a column of one side of a join, such as `b` of `t`, give it by its parts with the older constructor, as in `StarExpression(exclude=[col("t", "b")])`; `star()` takes plain names only.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

all_but_b = duckdb.star(exclude = ['b'])
duckdb.from_df(df).select(all_but_b).show()
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

`star(exclude=..., rename=...)` also renames columns, as in `star(exclude="b", rename={"c": "total"})`.

## Constant Expression

This expression contains a single value, with `lit(value)`. Operators, `fn()`, and the case builder take Python values directly, so `lit()` is needed only where a value must be an expression of its own, as in a select list. Values convert as described in [Conversion between DuckDB and Python]({% link docs/2.0/clients/python/conversion.md %}); a `dict` with string keys is a `STRUCT`, and a `dict` with other keys is a `MAP`.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

const = duckdb.lit('hello')
duckdb.from_df(df).select(const).show()
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

This expression is a [`CASE` expression]({% link docs/2.0/sql/expressions/case.md %}). `when(condition).then(value)` starts it, each further `.when(condition).then(value)` adds a branch, tried in order, and `.otherwise(value)` gives the value where no branch matches. `.end()` closes it without an `otherwise`, which leaves `NULL` there.

```python
import duckdb
import pandas as pd
from duckdb import col, when

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

size = (
    when(col("c") > 40).then("large")
    .when(col("c") > 20).then("medium")
    .otherwise("small")
    .alias("size")
)
duckdb.from_df(df).select(col("c"), size).show()
```

```text
┌───────┬─────────┐
│   c   │  size   │
│ int64 │ varchar │
├───────┼─────────┤
│    42 │ large   │
│    21 │ medium  │
│    13 │ small   │
│    14 │ small   │
└───────┴─────────┘
```

The older constructor builds the same expression: `CaseExpression(condition, value)` takes the first branch, `.when(condition, value)` adds one, and `.otherwise(value)` closes it:

```python
from duckdb import CaseExpression

older = CaseExpression(col("c") > 40, "large").when(col("c") > 20, "medium").otherwise("small")
print(older)
```

```text
(CASE WHEN ("c" > 40) THEN 'large' WHEN ("c" > 20) THEN 'medium' ELSE 'small' END)
```

## Function Expression

This expression contains a function call.
It is built from the function name and any number of arguments, with `fn(name, *args)`.
An argument that is a plain string is a value, so `fn('upper', 's')` passes the text `s`; use `col('s')` for the column.

```python
import duckdb
import pandas as pd
from duckdb import col, fn

df = pd.DataFrame({
    'a': [1, 2, 3, 4],
    'b': [True, None, False, True],
    'c': [42, 21, 13, 14]
})

multiply_by_2 = fn('multiply', col('a'), 2)
duckdb.from_df(df).select(multiply_by_2).show()
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

`fn` also passes keyword arguments by name: `fn("round", col("x"), precision=1)` is `round("x", "precision" := 1)`. `coalesce(*values)` gives the first of its arguments that is not `NULL`. A Python function given as an argument becomes a SQL [lambda]({% link docs/2.0/sql/functions/lambda.md %}); it is called once, with expressions, to build the lambda's body:

```python
from duckdb import fn

rel = duckdb.sql("SELECT [1, 2, 3] AS l")
print(rel.select(fn("list_transform", col("l"), lambda v: v * 10)).fetchall())
```

```text
[([10, 20, 30],)]
```

## SQL Expression

This expression contains any valid SQL expression, written as text with `sql_expr(text)`, which splices the text in as it is. The older `SQLExpression(text)` also checks that the text is one expression. Never build either from untrusted input. With the `sales` DataFrame from the top of the page:

```python
from duckdb import sql_expr

rel = duckdb.from_df(sales)
print(rel.select(sql_expr("price * 2").alias("double_price")).fetchall())
```

```text
[(40,), (84,)]
```

## Aggregates and Window Functions

An expression has a method for each common aggregate function, such as `.sum()`, `.mean()`, `.min()`, `.max()`, `.count()`, `.median()`, `.string_agg()`, and `.array_agg()`; `fn()` calls any other. `col("g").arg_max(col("x"))` is the value of `g` in the row where `x` is largest, and `.arg_min()` takes the row where it is smallest. `count_all()` is `count(*)`. `.where(condition)` makes an aggregate use only the rows where the condition holds. A projection may hold aggregates without a `GROUP BY`:

```python
from duckdb import count_all

rel = duckdb.sql("SELECT * FROM (VALUES ('a', 1), ('a', 2), ('b', 3)) t(g, x)")
print(rel.select(col("x").sum(), col("x").sum().where(col("g") == "a"), count_all()).fetchall())
print(rel.aggregate([col("g"), col("x").max().alias("top")], "g").order("g").fetchall())
```

```text
[(6, 3, 3)]
[('a', 2), ('b', 3)]
```

`.over(partition_by=..., order_by=..., rows=..., range=...)` turns an aggregate into a window function. `rows` and `range` bound the window as a pair (start, end) relative to the current row, where `None` means unbounded; `rows` counts rows and `range` measures the distance in the `order_by` value: `rows=(-2, 0)` is the current row and the two before it. The window functions `row_number()`, `rank()`, `dense_rank()`, `ntile(n)`, `lag(expr)`, `lead(expr)`, `first_value(expr)`, and `last_value(expr)` are in the `duckdb` module, and `.ignore_nulls()` makes the last four skip `NULL` values:

```python
from duckdb import lag, row_number

print(rel.select(
    col("g"),
    col("x"),
    row_number().over(partition_by=col("g"), order_by=col("x")).alias("n"),
    lag(col("x")).over(order_by=col("x")).alias("previous"),
).order("x").fetchall())
```

```text
[('a', 1, 1, None), ('a', 2, 2, 1), ('b', 3, 1, 2)]
```

## Function Families

`.str()`, `.dt()`, `.list()`, and `.json()` give the string, date and time, list, and JSON functions as methods that apply the function to the expression: `col("s").str().upper()` is `upper("s")`.

```python
rel = duckdb.sql("SELECT 'duck' AS s, DATE '2024-05-01' AS d, [3, 1, 2] AS l")
print(rel.select(
    col("s").str().upper(),
    col("d").dt().year(),
    col("l").list().sort(),
).fetchall())
```

```text
[('DUCK', 2024, [1, 2, 3])]
```

## Common Operations

The Expression class also contains many operations that can be applied to any Expression type.

| Operation                                    | Description                                                                                                                      |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `.alias(name: str)`                          | Applies an alias to the expression                                                                                               |
| `.cast(type)`                                | Applies a cast to the provided type on the expression: a `DuckDBPyType`, a Python type, or a SQL type name such as `"VARCHAR"`    |
| `.try_cast(type)`                            | Like `.cast`, but gives `NULL` where the cast fails                                                                              |
| `.isin(*values)`                             | Creates an [`IN` expression]({% link docs/2.0/sql/expressions/in.md %}) against the provided values                          |
| `.isnotin(*values)`                          | Creates a [`NOT IN` expression]({% link docs/2.0/sql/expressions/in.md %}#not-in) against the provided values                |
| `.between(low, high)`                        | Checks whether the expression is between `low` and `high`, both included                                                         |
| `.like(pattern)`, `.ilike(pattern)`          | Matches the text against a [`LIKE` pattern]({% link docs/2.0/sql/functions/pattern_matching.md %}), `ilike` ignoring case    |
| `.is_null()`                                 | Checks whether the expression is `NULL`                                                                                          |
| `.is_not_null()`                             | Checks whether the expression is not `NULL`                                                                                      |
| `.collate(collation: str)`                   | Compares and sorts by a [collation]({% link docs/2.0/sql/expressions/collations.md %}), such as `nocase`                     |
| `.concat(*values)`                           | Concatenates text values                                                                                                         |
| `[key]`                                      | Takes a field of a `STRUCT` by name, an element of a list by position, counting from 1, or an entry of a map by key              |

### Order Operations

When expressions are provided to `DuckDBPyRelation.order()`, which takes one expression, or to `DuckDBPyRelation.sort()`, which takes several, the following order operations can be applied.

| Operation                      | Description                                                                        |
|--------------------------------|------------------------------------------------------------------------------------|
| `.asc()`                       | Indicates that this expression should be sorted in ascending order                 |
| `.desc()`                      | Indicates that this expression should be sorted in descending order                |
| `.nulls_first()`               | Indicates that the nulls in this expression should precede the non-null values     |
| `.nulls_last()`                | Indicates that the nulls in this expression should come after the non-null values  |
