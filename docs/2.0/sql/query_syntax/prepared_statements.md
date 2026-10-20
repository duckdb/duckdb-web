---
layout: docu
redirect_from:
- /docs/sql/query_syntax/prepared_statements
- /docs/stable/sql/query_syntax/prepared_statements
- /docs/current/sql/query_syntax/prepared_statements
- /docs/lts/sql/query_syntax/prepared_statements
- /docs/preview/sql/query_syntax/prepared_statements
tested: true
title: Prepared Statements
---

DuckDB supports prepared statements where parameters are substituted when the query is executed.
This can improve readability and is useful for preventing [SQL injections](https://en.wikipedia.org/wiki/SQL_injection).

## Syntax

There are three syntaxes for denoting parameters in prepared statements:
auto-incremented (`?`),
positional (`$1`),
and named (`$param`).
Note that not all clients support all of these syntaxes, e.g., the [JDBC client]({% link docs/2.0/clients/java/querying.md %}) only supports auto-incremented parameters in prepared statements.

### Example Dataset

In the following, we introduce the three different syntaxes and illustrate them with examples using the following table.

```sql
CREATE TABLE person (name VARCHAR, age BIGINT);
INSERT INTO person VALUES ('Alice', 37), ('Ana', 35), ('Bob', 41), ('Bea', 25);
```

In our example query, we'll look for people whose name starts with a `B` and are at least 40 years old.
This will return a single row `<'Bob', 41>`.

### Auto-Incremented Parameters: `?`

DuckDB supports using prepared statements with auto-incremented indexing,
i.e., the position of the parameters in the query corresponds to their position in the execution statement.
For example:

```sql
PREPARE query_person AS
    SELECT *
    FROM person
    WHERE starts_with(name, ?)
      AND age >= ?;
```

Using the CLI client, the statement is executed as follows.

```sql
EXECUTE query_person('B', 40);
```

### Positional Parameters: `$1`

Prepared statements can use positional parameters, where parameters are denoted with an integer (`$1`, `$2`).
For example:

```sql
PREPARE query_person AS
    SELECT *
    FROM person
    WHERE starts_with(name, $2)
      AND age >= $1;
```

Using the CLI client, the statement is executed as follows.
Note that the first parameter corresponds to `$1`, the second to `$2`, and so on.

```sql
EXECUTE query_person(40, 'B');
```

### Named Parameters: `$parameter`

DuckDB also supports named parameters where parameters are denoted with `$parameter_name`.
For example:

```sql
PREPARE query_person AS
    SELECT *
    FROM person
    WHERE starts_with(name, $name_start_letter)
      AND age >= $minimum_age;
```

Using the CLI client, the statement is executed as follows.

```sql
EXECUTE query_person(name_start_letter := 'B', minimum_age := 40);
```

## Session Variables as Default Values

> New Using [session variables]({% link docs/2.0/sql/statements/set_variable.md %}) as default values for named parameters was introduced in DuckDB 2.0.

When a named parameter is not supplied at execution time, DuckDB fills it from the [session variable]({% link docs/2.0/sql/statements/set_variable.md %}) of the same name, if one is set. An explicit argument always takes precedence over the variable.

```sql
SET VARIABLE multiplier = 10;
SET VARIABLE x = 42;
PREPARE compute AS SELECT $multiplier * $x AS result;
```

With no arguments, both parameters come from the variables, computing `10 * 42`:

```sql
EXECUTE compute;
```

| result |
|-------:|
| 420    |

Supplying an argument overrides the matching variable, while omitted parameters still fall back to theirs:

```sql
EXECUTE compute(multiplier := 3);
```

| result |
|-------:|
| 126    |

Because the fallback is resolved at execution time, re-executing the statement after changing a variable picks up the new value:

```sql
SET VARIABLE multiplier = 100;
EXECUTE compute;
```

| result |
|-------:|
| 4200   |

The fallback applies to named parameters only. Auto-incremented (`?`) and positional (`$1`) parameters are matched by position and are never filled from a session variable, even one whose name is a number such as `1`.

## Dropping Prepared Statements: `DEALLOCATE`

To drop a prepared statement, use the `DEALLOCATE` statement:

```sql
DEALLOCATE query_person;
```

Alternatively, use:

```sql
DEALLOCATE PREPARE query_person;
```
