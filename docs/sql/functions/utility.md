---
layout: docu
title: Utility Functions
selected: Documentation/Functions/Utility Functions
expanded: Functions
---

## Utility Functions
The functions below are difficult to categorize into specific function types and are broadly useful. 

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `alias(column)` | Return the name of the column | `alias(column1)` | `'column1'` |
| `coalesce(expr, ...)` | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, 