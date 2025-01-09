---
layout: docu
redirect_from:
- docs/archive/0.9.2/api/python/expression
- docs/archive/0.9.1/api/python/expression
- docs/archive/0.9.0/api/python/expression
title: Expression API
---

The `Expression` class represents an instance of an [expression](../../sql/expressions/overview).

## Why would I use the API?

Using this API makes it possible to dynamically build up expressions, which are typically created by the parser from the query string.  
This allows you to skip that and have more fine-grained control over the used expressions.

Below is a list of currently supported expressions that can be created through the API.  

## Column Expression

This expression references a column by name.

```py
import duckdb
import pandas as pd

df = pd.DataFrame({'a': [1,2,3,4]})

col = duckdb.ColumnExpression('a')
res = duckdb.df(df).select(col).fetchall()
print(res)
# [(1,), (2,), (3,), (4,)]
```

## Star Expression

This expression selects all columns of the input source.  

Optionally it's possible to provide an `exclude` list to filter out columns of the table.  
This `exclude` list can contain either strings or Expressions.

```py
import duckdb
import pandas as pd

df = pd.DataFrame({
	'a': [1,2,3,4],
	'b': [True, None, False,True],
	'c': [42, 21, 13, 14]
})

star = duckdb.StarExpression(exclude=['b'])
res = duckdb.df(df).select(star).fetchall()
print(res)
# [(1, 42), (2, 21), (3, 13), (4, 14)]
```

## Constant Expression

This expression contains a single value.  

```py
import duckdb
import pandas as pd

df = pd.DataFrame({
	'a': [1,2,3,4],
	'b': [True, None, False,True],
	'c': [42, 21, 13, 14]
})

const = duckdb.ConstantExpression('hello')
res = duckdb.df(df).select(const).fetchall()
print(res)
# [('hello',), ('hello',), ('hello',), ('hello',)]
```

## Case Expression

This expression contains a CASE WHEN (...) THEN (...) ELSE (...) END expression.  
By default ELSE is NULL, it can be set using `.else(value=...)`  
Additional `WHEN (...) THEN (...)` blocks can be added with `.when(condition=..., value=...)`

```py
import duckdb
import pandas as pd
from duckdb import (
    ConstantExpression,
    ColumnExpression,
    CaseExpression
)

df = pd.DataFrame({
    'a': [1,2,3,4],
    'b': [True, None, False,True],
    'c': [42, 21, 13, 14]
})

hello = ConstantExpression('hello')
world = ConstantExpression('world')

case = CaseExpression(condition=ColumnExpression('b') == False, value=world).otherwise(hello)
res = duckdb.df(df).select(
    case
).fetchall()
print(res)
# [('hello',), ('hello',), ('world',), ('hello',)]
```

## Function Expression

This expression contains a function call.  
It can be constructed by providing the function name and an arbitrary amount of Expressions as arguments.

```py
import duckdb
import pandas as pd
from duckdb import (
    ConstantExpression,
    ColumnExpression,
    FunctionExpression
)

df = pd.DataFrame({
    'a': [
        'test',
        'pest',
        'text',
        'rest',
    ]
})

ends_with = FunctionExpression('ends_with', ColumnExpression('a'), ConstantExpression('est'))
res = duckdb.df(df).select(
    ends_with
).fetchall()
print(res)
# [(True,), (True,), (False,), (True,)]
```

## Common Operations

The Expression class also contains many operations that can be applied to any Expression type.  

`.cast(type: DuckDBPyType)`  
Applies a cast to the provided type on the expression.

`.alias(name: str)`  
Apply an alias to the expression.

`.isin(*exprs: Expression)`  
Create a IN expression against the provided expressions as the list.

`.isnotin(*exprs: Expression)`  
Create a NOT IN expression against the provided expressions as the list.

### Order Operations

When expressions are provided to `DuckDBPyRelation.order()` these take effect:

`.asc()`  
Indicates that this expression should be sorted in ascending order.

`.desc()`  
Indicates that this expression should be sorted in descending order.

`.nulls_first()`  
Indicates that the nulls in this expression should preceed the non-null values.

`.nulls_last()`  
Indicates that the nulls in this expression should come after the non-null values.