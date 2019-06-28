---
layout: default
title: Logical Operators
selected: Documentation/Functions/Logical Functions
expanded: Functions
---
The following logical operators are available: `AND`, `OR` and `NOT`. SQL uses a three-valuad logic system with `TRUE`, `FALSE` and `NULL`. Note that logical operators involving `NULL` do not always evaluate to `NULL`. For example, `NULL AND FALSE` will evaluate to `FALSE`, and `NULL OR TRUE` will evaluate to `TRUE`. Below are the complete truth tables:

| a | b | a AND b | a OR b |
|:---|:---|:---|:---|
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | NULL | NULL | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | NULL | FALSE | NULL |
| NULL | NULL | NULL | NULL |

| a | NOT a |
|:---|:---|
| TRUE | FALSE |
| FALSE | TRUE |
| NULL | NULL |

The operators `AND` and `OR` are commutative, that is, you can switch the left and right operand without affecting the result.
