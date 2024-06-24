---
layout: docu
title: Boolean Type
blurb: The BOOLEAN type represents a statement of truth ("true" or "false").
---

<div class="narrow_table"></div>

| Name | Aliases | Description |
|:---|:---|:---|
| `BOOLEAN` | `BOOL` | logical boolean (`true`/`false`) |

The `BOOLEAN` type represents a statement of truth ("true" or "false"). In SQL, the `BOOLEAN` field can also have a third state "unknown" which is represented by the SQL `NULL` value.

Select the three possible values of a `BOOLEAN` column:

```sql
SELECT true, false, NULL::BOOLEAN;
```

Boolean values can be explicitly created using the literals `true` and `false`. However, they are most often created as a result of comparisons or conjunctions. For example, the comparison `i > 10` results in a boolean value. Boolean values can be used in the `WHERE` and `HAVING` clauses of a SQL statement to filter out tuples from the result. In this case, tuples for which the predicate evaluates to `true` will pass the filter, and tuples for which the predicate evaluates to `false` or `NULL` will be filtered out. Consider the following example:

Create a table with the values 5, 15 and `NULL`:

```sql
CREATE TABLE integers (i INTEGER);
INSERT INTO integers VALUES (5), (15), (NULL);
```

Select all entries where `i > 10`:

```sql
SELECT * FROM integers WHERE i > 10;
```

In this case 5 and `NULL` are filtered out (`5 > 10` is `false` and `NULL > 10` is `NULL`):

| i  |
|---:|
| 15 |

## Conjunctions

The `AND`/`OR` conjunctions can be used to combine boolean values.

Below is the truth table for the `AND` conjunction (i.e., `x AND y`).

<div class="narrow_table"></div>

|  X  | X AND true  | X AND false | X AND NULL  |
|-------|-------|-------|-------|
| true  | true  | false | NULL  |
| false | false | false | false |
| NULL  | NULL  | false | NULL  |

Below is the truth table for the `OR` conjunction (i.e., `x OR y`).

<div class="narrow_table"></div>

|  X   | X OR true | X OR false | X OR NULL |
|-------|------|-------|------|
| true  | true | true  | true |
| false | true | false | NULL |
| NULL  | true | NULL  | NULL |

## Expressions

See [Logical Operators]({% link docs/sql/expressions/logical_operators.md %}) and [Comparison Operators]({% link docs/sql/expressions/comparison_operators.md %}).
