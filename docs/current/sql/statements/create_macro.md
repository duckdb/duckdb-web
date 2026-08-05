---
layout: docu
railroad: statements/createmacro.js
redirect_from:
- /docs/preview/sql/statements/create_macro
- /docs/sql/statements/create_macro
- /docs/stable/sql/statements/create_macro
title: CREATE MACRO Statement
---

The `CREATE MACRO` statement defines a named, callable SQL expression as a database schema object.

Macros may declare parameters, which can be referenced by its expression.
Once a macro is created, it may be called by referencing its name and by passing values to its parameters; this causes its expression to be evaluated, yielding a value.
Depending on the macro type, the value may be scalar, or a `TABLE` value.
The `CREATE FUNCTION` statement is an alias for `CREATE MACRO`.

The simplified syntax for creating a macro is:

```sql
CREATE [OR REPLACE] [TEMPORARY] MACRO [IF NOT EXISTS] ⟨identifier⟩( [⟨parameters⟩] ) AS [TABLE] ⟨expression⟩;
```

* The identifier consists of the macro's name, which can be any valid SQL identifier. A macro may be explicitly qualified with an existing database schema. If a schema is specified, then it appears in the usual way: before the name, with a dot separating schema name and macro name. When not explicitly specified, the macro will be associated with the current schema.
* When connected to a persistent database file, the macro will be stored in the database. The optional `TEMPORARY` keyword indicates that the macro is not to be persisted.
* An `OR REPLACE` clause may occur immediately after the `CREATE` keyword, which causes an existing macro with the same name (within the schema) to be overwritten. Without `OR REPLACE` such an attempt will fail with a `Macro Function already exists` error.
* An `IF NOT EXISTS` clause may occur immediately before the identifier, and has the effect of only creating the macro if it does not already exist. Either the `OR REPLACE` or the `IF NOT EXISTS` clause may be present, but not both.
* The macro name is followed by parentheses. If the macro has [parameters](#declaring-parameters), then they must be declared within the parentheses.
* The `AS` keyword appears after the right parenthesis but before the expression
* The `TABLE` keyword may appear right after the `AS` keyword, directly before the expression, indicating the macro is a [table macro](#types-of-macros) and returns a result set. When omitted, the macro is automatically a scalar macro.
* The expression can be any valid SQL expression provided the expression's type is aligned with the [macro's type](#types-of-macros).

Please review the [syntax diagram](#syntax) for a more precise and detailed overview of the `CREATE MACRO` statement. 

## Types of Macros

The contexts where a particular macro may be called depends on the data type of its result value:
* Scalar macros evaluate to a scalar value. For scalar macros, the expression can either be a simple expression, or a scalar subquery.
* Table macros return a tabular result: when called, they act essentially as [table functions]({% link docs/current/sql/query_syntax/from.md %}#table-functions) and return a table value. Their expression can be a `SELECT` statement, or a call to another table function.

## Declaring Parameters

Macros may declare parameters. The parameter declarations appear as a comma-separated list between the parentheses before the `AS` keyword. The simplified syntax for a single parameter declaration is:

```sql
⟨parameter-name⟩ [⟨datatype⟩] [ := ⟨default-value⟩ ]
```
* The parameter name is mandatory and can be any valid SQL identifier. Parameter names must be unique within the parameter list. An attempt to define multiple parameters with the same name results in a `Duplicate parameter` error.
* Optionally, a parameter may explicitly specify a particular datatype. This can be any of the existing DuckDB [data types]({% link docs/current/sql/data_types/overview.md %}). Note: there is no way to specify a parameter of a `TABLE` type.
* A parameter can optionally specify a default value. This is done with the assignment operator `:=`, followed by the expression that is to be used as default value. 
* The default value expression is in principle evaluated at definition-time - NOT at run-time. (There are a few exceptions, like `CURRENT_SCHEMA`. But it's best not to rely on that: if you need a default value to be dynamic, use a well-known value like `NULL` as default and use conditional logic in the expression to produce the run-time value).
* Specifying a default value expression effectively makes the parameter optional: when the macro is called, the DuckDb binder will find candidate signatures based on passed parameters, but backfilled by signatures that specify default values for missing parameters.  
* A parameter that specifies a default value cannot appear before a definition of a parameter that does not have a default value. In other words, parameters without default values have to be defined "in the front"; any parameters with default values appear "at the back".
* Multiple parameter declarations are separated from one another with a comma.

### Overloading

Macros support overloading:

* A single `CREATE MACRO` statement can define multiple implementations (sometimes called 'overloads'), each having its own parameter list, `AS` keyword, and expression. Note that all of the implementations are defined in the same `CREATE MACRO` statement: it is not possible to add, remove, or alter individual implementations after the macro is created.
* Multiple implementations are separated from one another by a comma.
* Each implementation must have a unique parameter-type signature: that is, in one `CREATE MACRO` statement, all implementations having the same number of parameters must each have a unique sequence of parameter types - regardless of the parameter names. If a parameter type signature is not unique, it results in a `Ambiguity in macro overloads` error.
* Overloading only applies to the parameter-types, but not to the macro type itself: for a single macro, all of its implementations are either scalar or `TABLE`.
* When overloading table functions that are defined using a `SELECT` statement as expression, you will probably need to wrap the `SELECT` statement in parentheses.

## Calling Macros
Macros are called by mentioning their name, followed by parentheses. A comma-separated list of value-expressions may appear between the parentheses - these are the actual parameters. 
The DuckDB binder examines the data types of the actual parameters and tries to find an implementation of the macro that has a matching signature.
If an implementation is found, the parameter values are passed and the implementation's expression is evaluated; finally, its resulting value is returned and used in place where the macro was called.
This is similar to calling a [function]({% link docs/current/sql/functions/overview.md %}).
 
In general, a call to a macro is valid if its expression could also appear in that context:
* A call to a scalar macro can be used in the `SELECT` clause or in the `WHERE` clause of a `SELECT`statement.
* If the expression of a scalar macro references an [aggregate function]({% link docs/current/sql/functions/aggregates.md %}), then the macro behaves like an aggregate function too.
* A call to a table macro can appear in the `FROM` clause of a `SELECT` statement, or in a [`CALL` statement]({% link docs/current/sql/statements/call.md %}).

### Passing Parameters

Parameter values can be passed to the macro as a comma-separated list of expressions appearing between the parentheses following the macro's name.

Parameter values may be passed either positionally or by name.

* Positional parameter passing means that only the value expression is passed;
* In contrast to positional parameter passing, named parameter passing explicitly assigns the actual parameter value to a specific formal parameter. This is done by mentioning the parameter name followed by the assignment operator `:=`, followed by the parameter value expression. 
* Note that some built-in functions also allow named parameters, but allow `=` as assignment operator. For macros, this won't work! Instead, the `=` is interpreted as comparison operator. This effectively turns the - intended - named parameter into a positional parameter passing the result of comparing the parameter name with the parameter value expression. 
* If a macro call contains named parameters, then they must appear after any positional parameters. In other words, any positional parameters must appear "in the front"; while all named parameters must appear "at the back".
* By definition, positional parameters are passed in the same order as they were declared. But named parameters can appear in any order (provided they appear after any of the positional parameters).

## Examples

### Scalar Macros

Create a macro that adds two expressions (`a` and `b`):

```sql
CREATE MACRO add(a, b) AS a + b;
```

Create a macro, replacing possible existing definitions:

```sql
CREATE OR REPLACE MACRO add(a, b) AS a + b;
```

Create a macro if it does not already exist, else do nothing:

```sql
CREATE MACRO IF NOT EXISTS add(a, b) AS a + b;
```

Create a macro for a `CASE` expression:

```sql
CREATE MACRO ifelse(a, b, c) AS CASE WHEN a THEN b ELSE c END;
```

Create a macro that does a subquery:

```sql
CREATE MACRO one() AS (SELECT 1);
```

Macros are schema-dependent, and have an alias, `FUNCTION`:

```sql
CREATE FUNCTION main.my_avg(x) AS sum(x) / count(x);
```

Create a macro with a default parameter:

```sql
CREATE MACRO add_default(a, b := 5) AS a + b;
```

Create a macro `arr_append` (with functionality equivalent to `array_append`):

```sql
CREATE MACRO arr_append(l, e) AS list_concat(l, list_value(e));
```

Create a macro with a typed parameter:

```sql
CREATE MACRO is_maximal(a INTEGER) AS a = 2^31 - 1;
```

### Table Macros

Create a table macro without parameters:

```sql
CREATE MACRO static_table() AS TABLE
    SELECT 'Hello' AS column1, 'World' AS column2;
```

Create a table macro with parameters (that can be of any type):

```sql
CREATE MACRO dynamic_table(col1_value, col2_value) AS TABLE
    SELECT col1_value AS column1, col2_value AS column2;
```

Create a table macro that returns multiple rows. It will be replaced if it already exists, and it is temporary (will be automatically deleted when the connection ends):

```sql
CREATE OR REPLACE TEMP MACRO dynamic_table(col1_value, col2_value) AS TABLE
    SELECT col1_value AS column1, col2_value AS column2
    UNION ALL
    SELECT 'Hello' AS col1_value, 456 AS col2_value;
```

Pass an argument as a list:

```sql
CREATE MACRO get_users(i) AS TABLE
    SELECT * FROM users WHERE uid IN (SELECT unnest(i));
```

An example of how to use the `get_users` table macro is the following:

```sql
CREATE TABLE users AS
    SELECT *
    FROM (VALUES (1, 'Ada'), (2, 'Bob'), (3, 'Carl'), (4, 'Dan'), (5, 'Eve')) t(uid, name);
SELECT * FROM get_users([1, 5]);
```

To define macros on arbitrary tables, use the [`query_table` function]({% link docs/current/guides/sql_features/query_and_query_table_functions.md %}). For example, the following macro computes a column-wise checksum on a table:

```sql
CREATE MACRO checksum(tbl) AS TABLE
    SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR))
    FROM query_table(tbl);

CREATE TABLE tbl AS SELECT unnest([42, 43]) AS x, 100 AS y;
SELECT * FROM checksum('tbl');
```

## Overloading

It is possible to overload a macro based on the types or the number of its parameters; this works for both scalar and table macros.

By providing overloads we can have both `add_x(a, b)` and `add_x(a, b, c)` with different function bodies.

```sql
CREATE MACRO add_x
    (a, b) AS a + b,
    (a, b, c) AS a + b + c;
```

```sql
SELECT
    add_x(21, 42) AS two_args,
    add_x(21, 42, 21) AS three_args;
```

| two_args | three_args |
| -------- | ---------- |
| 63       | 84         |


```sql
CREATE OR REPLACE MACRO is_maximal
    (a TINYINT) AS a = 2^7 - 1,
    (a INT) AS a = 2^31 - 1;
```

```sql
SELECT
    is_maximal(127::TINYINT) AS tiny,
    is_maximal(127) AS regular;
```

| tiny | regular |
| ---- | ------- |
| true | false   |


## Syntax

<div id="rrdiagram"></div>

Macros allow you to create shortcuts for combinations of expressions.

```sql
CREATE MACRO add(a) AS a + b;
```

```console
Binder Error:
Referenced column "b" not found in FROM clause!
```

This works:

```sql
CREATE MACRO add(a, b) AS a + b;
```

Usage example:

```sql
SELECT add(1, 2) AS x;
```

|    x |
| ---: |
|    3 |

However, this fails:

```sql
SELECT add('hello', 3);
```

```console
Binder Error:
Could not choose a best candidate function for the function call "add(STRING_LITERAL, INTEGER_LITERAL)". In order to select one, please add explicit type casts.
    Candidate functions:
    add(DATE, INTEGER) -> DATE
    add(INTEGER, INTEGER) -> INTEGER
```

Macros can have default parameters.

`b` is a default parameter:

```sql
CREATE MACRO add_default(a, b := 5) AS a + b;
```

The following will result in 42:

```sql
SELECT add_default(37);
```

The order of named parameters does not matter:

```sql
CREATE MACRO triple_add(a, b := 5, c := 10) AS a + b + c;
```

```sql
SELECT triple_add(40, c := 1, b := 1) AS x;
```

|    x |
| ---: |
|   42 |

When macros are used, they are expanded (i.e., replaced with the original expression), and the parameters within the expanded expression are replaced with the supplied arguments. Step by step:

The `add` macro we defined above is used in a query:

```sql
SELECT add(40, 2) AS x;
```

Internally, `add` is replaced with its definition of `a + b`:

```sql
SELECT a + b AS x;
```

Then, the parameters are replaced by the supplied arguments:

```sql
SELECT 40 + 2 AS x;
```

## Limitations

### Using Subquery Macros

Table macros as well as scalar macros defined using scalar subqueries cannot be used in the arguments of table functions. DuckDB will return the following error:

```console
Binder Error:
Table function cannot contain subqueries
```

### Overloads

Overloads for macro functions have to be set at creation, it is not possible to define a macro by the same name twice without first removing the first definition.

### Recursive Functions

Defining recursive functions is not supported.
For example, the following macro – supposed to compute the *n*th number of the Fibonacci sequence – fails:

```sql
CREATE OR REPLACE FUNCTION fibo(n) AS (SELECT 1);
CREATE OR REPLACE FUNCTION fibo(n) AS (
    CASE
        WHEN n <= 1 THEN 1
        ELSE fibo(n - 1)
    END
);
SELECT fibo(3);
```

```console
Binder Error:
Max expression depth limit of 1000 exceeded. Use "SET max_expression_depth TO x" to increase the maximum expression depth.
```

### Function Chaining on the First Function Does Not Work

Macros do not support the dot operator for function chaining on the first function.
To illustrate this, see an example with the `lower` function, which works:

```sql
CREATE OR REPLACE MACRO low(s) AS lower(s);
SELECT low('AA');
```

However, rewriting `lower(s)` to use function chaining does not work:

```sql
CREATE OR REPLACE MACRO low(s) AS s.lower();
SELECT low('AA');
```

```console
Binder Error:
Referenced column "s" not found in FROM clause!
```

### Viewing the List of Macros and Table Macros

You can use the following query to display the list of macros and table macros:

```sql
SELECT schema_name, function_name, function_type, parameters
FROM duckdb_functions();
```
