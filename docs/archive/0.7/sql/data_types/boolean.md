---
layout: docu
title: Boolean Type
selected: Documentation/Data Types/Boolean
expanded: Data Types
blurb: The BOOLEAN type represents a statement of truth ("true" or "false").
---

| Name | Aliases | Description |
|:---|:---|:---|
| `BOOLEAN` | bool | logical boolean (true/false) |

The `BOOLEAN` type represents a statement of truth ("true" or "false"). In SQL, the boolean field can also have a third state "unknown" which is represented by the SQL NULL value.

```sql
-- select the three possible values of a boolean column
SELECT TRUE, FALSE, NULL::BOOLEAN;
```

Boolean values can be explicitly created using the literals `TRUE` and `FALSE`. However, they are most often created as a result of comparisons or conjunctions. For example, the comparison `i > 10` results in a boolean value. Boolean values can be used in the `WHERE` and `HAVING` clauses of a SQL statement to filter out tuples from the result. In this case, tuples for which the predicate evaluates to `TRUE` will pass the filter, and tuples for which the predicate evaluates to `FALSE` or `NULL` will be filtered out. Consider the following example:

```sql
-- create a table with the value (5), (15) and (NULL)
CREATE TABLE integers(i INTEGER);
INSERT INTO integers VALUES (5), (15), (NULL);

-- select all entries where i > 10
SELECT * FROM integers WHERE i > 10;
-- in this case (5) and (NULL) are filtered out:
-- 5 > 10    = FALSE
-- NULL > 10 = NULL
-- The result is (15)
```

## Conjunctions
The `AND`/`OR` conjunctions can be used to combine boolean values.

Below is a truth table for the `AND` conjunction (i.e. `x AND y`).

|  X  | X AND TRUE  | X AND FALSE | X AND NULL  |
|-------|-------|-------|-------|
| TRUE  | TRUE  | FALSE | NULL  |
| FALSE | FALSE | FALSE | FALSE |
| NULL  | NULL  | FALSE | NULL  |

Below is a truth table for the `OR` conjunction (i.e. `x OR y`).

|  X   | X OR TRUE | X OR FALSE | X OR NULL |
|-------|------|-------|------|
| TRUE  | TRUE | TRUE  | TRUE |
| FALSE | TRUE | FALSE | NULL |
| NULL  | TRUE | NULL  | NULL |

## Expressions
See [Logical Operators](../expressions/logical_operators) and [Comparison Operators](../expressions/comparison_operators).
