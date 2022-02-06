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
| `coalesce(expr, ...)` | Return the first expression that evaluates to a non-`NULL` value. Accepts 1 or more parameters. Each expression can be a column, literal value, function result, or many others.  | `coalesce(NULL,NULL,'default_string')` | `'default_string'` |
| `current_setting('setting_name')` | Return the current value of the configuration setting | `current_setting('access_mode')` | `'automatic'` |
| `currval('sequence_name')` | Return the current value of the sequence. Note that `nextval` must be called at least once prior to calling `currval`. | `currval('my_sequence_name')` | `1` |
| `nextval('sequence_name')` | Return the following value of the sequence. | `nextval('my_sequence_name')` | `2` |