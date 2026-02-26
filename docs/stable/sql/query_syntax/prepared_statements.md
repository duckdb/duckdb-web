---
layout: docu
redirect_from:
  - /docs/sql/query_syntax/prepared_statements
title: Prepared Statements
---

DuckDB supports prepared statements where parameters are substituted when the query is executed.
This can improve readability and is useful for preventing [SQL injections](https://en.wikipedia.org/wiki/SQL_injection).

## Syntax

There are three syntaxes for denoting parameters in prepared statements:
auto-incremented (`?`),
positional (`$1`),
and named (`$param`).
Note that not all clients support all of these syntaxes, e.g., the [JDBC client]({% link docs/stable/clients/java.md %}) only supports auto-incremented parameters in prepared statements.

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

## Dropping Prepared Statements: `DEALLOCATE`

To drop a prepared statement, use the `DEALLOCATE` statement:

```sql
DEALLOCATE query_person;
```

Alternatively, use:

```sql
DEALLOCATE PREPARE query_person;
```
