---
layout: docu
title: Expression API
---

The `Expression` class represents an instance of an [expression](../../sql/expressions/overview)

## Why would I use the API?

Using this API makes it possible to dynamically build up expressions, these expressions are typically created by the parser from the query string.
This allows you to skip that and have more fine-grained control over the used expressions.

### Column Expression

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

### Star Expression

This expression selects all columns of the input source.  

Optionally it's possible to provide an `exclude` list to filter out columns of the table.  
This `exclude` list can contain either strings or Expressions.
