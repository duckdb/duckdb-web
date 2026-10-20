---
layout: post
title: "Nicer Variable Syntax in DuckDB 2.0"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/variable-syntax.svg"
image: "/images/blog/thumbs/variable-syntax.png"
excerpt: "DuckDB 2.0 lets you read a session variable with a `$name` reference instead of a `getvariable` call, and prepared statements can fall back to session variables when a named parameter is not supplied. This post shows how the new syntax works and how the two features fit together."
tag: using-duckdb
---

DuckDB has long supported session variables through the [`SET VARIABLE` statement]({% link docs/preview/sql/statements/set_variable.md %}). You set a value once and read it back wherever you need it, which keeps a magic constant in a single place instead of scattering it across a script. Until now, reading a variable meant calling `getvariable`, and the call was more verbose than the idea behind it.

DuckDB 2.0 adds a shorthand. You can read a session variable with a `$name` reference, and [prepared statements]({% link docs/preview/sql/query_syntax/prepared_statements.md %}) can fall back to a session variable when a named parameter is left out. This post walks through both halves of the feature and shows how they work together.

## Reading a Variable with `$name`

Set a variable the way you always have.

```sql
SET VARIABLE x = 5;
```

Before DuckDB 2.0, you read it back with `getvariable`.

```sql
SELECT getvariable('x') AS x;
```

In DuckDB 2.0, `$x` is a shorthand for exactly that call.

```sql
SELECT $x AS x;
```

| x |
| -: |
| 5 |

For a variable that is set, the two forms are interchangeable. A `$name` reference resolves to the current value of the session variable with that name, so with `x` set to `5`, `$x` and `getvariable('x')` return the same result.

```sql
SET VARIABLE animal = 'duck';
SELECT $animal = getvariable('animal') AS same;
```

| same |
| --- |
| true |

If you reference a variable that is not set, DuckDB raises an error rather than returning `NULL`. The same is true after you remove a variable with `RESET VARIABLE`.

```sql
RESET VARIABLE animal;
SELECT $animal;
```

```console
Invalid Input Error:
Values were not provided for the following parameters: animal
```

The error talks about parameters because a `$name` reference and a named prepared statement parameter are the same construct under the hood: an unset variable leaves the parameter without a value. That overlap is what makes the second half of the feature work.

## Session Variables as Prepared Statement Defaults

A prepared statement declares parameters that you supply when you execute it. DuckDB names a parameter with the same `$name` syntax.

```sql
SET VARIABLE x = 5;
PREPARE double_value AS SELECT $x * 2 AS result;
```

Supply the parameter at execution time and it is used directly.

```sql
EXECUTE double_value(x := 1);
```

| result |
| -: |
| 2 |

Leave the parameter out and DuckDB 2.0 falls back to the session variable of the same name. Here `x` is still `5`, so the statement computes `5 * 2`.

```sql
EXECUTE double_value;
```

| result |
| -: |
| 10 |

The fallback value can itself come from another variable. Because `$y` resolves before it is passed in, this executes `10 * 2`.

```sql
SET VARIABLE y = 10;
EXECUTE double_value(x := $y);
```

| result |
| -: |
| 20 |

The two sources combine naturally when a statement has several parameters. Each parameter you supply overrides the matching variable, and each one you omit falls back to it.

```sql
SET VARIABLE multiplier = 10;
SET VARIABLE x = 42;
PREPARE compute AS SELECT $multiplier * $x AS result;
```

With no arguments, both parameters come from the variables, giving `10 * 42`.

```sql
EXECUTE compute;
```

| result |
| -: |
| 420 |

Override one parameter and the other still falls back. `EXECUTE compute(multiplier := 3)` computes `3 * 42`, while `EXECUTE compute(x := 1)` computes `10 * 1`.

| statement | result |
| --- | -: |
| `EXECUTE compute(multiplier := 3)` | `126` |
| `EXECUTE compute(x := 1)` | `10` |
| `EXECUTE compute(multiplier := 2, x := 5)` | `10` |

## Named and Positional Parameters

The fallback applies to named parameters only. Positional parameters, written as `$1`, `$2`, and so on, are matched by position and are never filled from a session variable, even one that happens to be named `1`.

If a positional parameter is not supplied, the statement still raises the missing parameter error. Keep this in mind when you mix the two styles: name the parameters you want to default from variables.

## Summary

DuckDB 2.0 makes session variables easier to read and easier to combine with prepared statements:

* `$name` is a shorthand for `getvariable('name')`, and referencing an unset variable raises an error.
* A named prepared statement parameter falls back to the session variable of the same name when you do not supply it, and an explicit argument always wins.
* Positional parameters are matched by position only and do not fall back to variables.

For the full reference, see the [`SET VARIABLE` statement]({% link docs/preview/sql/statements/set_variable.md %}) and [prepared statements]({% link docs/preview/sql/query_syntax/prepared_statements.md %}) pages, both listed among DuckDB's [friendly SQL features]({% link docs/preview/sql/dialect/friendly_sql.md %}).
