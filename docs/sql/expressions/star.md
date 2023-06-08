---
layout: docu
title: Star Expression
selected: Documentation/Expressions/Star
expanded: Expressions
railroad: expressions/star.js
---

### Examples
```sql
-- select all columns present in the FROM clause
SELECT * FROM table_name;
-- select all columns from the table called "table_name"
SELECT table_name.* FROM table_name JOIN other_table_name USING (id);
-- select all columns except the city column from the addresses table
SELECT * EXCLUDE (city) FROM addresses;
-- select all columns from the addresses table, but replace city with LOWER(city)
SELECT * REPLACE (LOWER(city) AS city) FROM addresses;
-- select all columns matching the given expression
SELECT COLUMNS(c -> c LIKE '%num%') FROM addresses;
-- select all columns matching the given regex from the table
SELECT COLUMNS('number\d+') FROM addresses;
```

### Syntax

<div id="rrdiagram"></div>

### Star Expression
The `*` expression can be used in a `SELECT` statement to select all columns that are projected in the `FROM` clause.

```sql
SELECT * FROM tbl;
```

The `*` expression can be modified using the `EXCLUDE` and `REPLACE`.

#### EXCLUDE Clause
`EXCLUDE` allows us to exclude specific columns from the `*` expression.

```sql
SELECT * EXCLUDE (col) FROM tbl;
```

#### Replace Clause
`REPLACE` allows us to replace specific columns with different expressions.

```sql
SELECT * REPLACE (col / 1000 AS col) FROM tbl;
```

### COLUMNS

The `COLUMNS` expression can be used to execute the same expression on multiple columns. Like the `*` expression, it can only be used in the `SELECT` clause.

```sql
CREATE TABLE numbers(id int, number int);
INSERT INTO numbers VALUES (1, 10), (2, 20), (3, NULL);
SELECT MIN(COLUMNS(*)), COUNT(COLUMNS(*)) from numbers;
```

| min(numbers.id) | min(numbers.number) | count(numbers.id) | count(numbers.number) |
|-----------------|---------------------|-------------------|-----------------------|
| 1               | 10                  | 3                 | 2                     |

The `*` expression in the `COLUMNS` statement can also contain `EXCLUDE` or `REPLACE`, similar to regular star expressions.

```sql
SELECT MIN(COLUMNS(* REPLACE (number + id AS number))), COUNT(COLUMNS(* EXCLUDE (number))) from numbers;
```

| min(numbers.id) | min(number := (number + id)) | count(numbers.id) |
|-----------------|------------------------------|-------------------|
| 1               | 11                           | 3                 |

COLUMNS expressions can also be combined, as long as the `COLUMNS` contains the same (star) expression:

```sql
SELECT COLUMNS(*) + COLUMNS(*) FROM numbers;
```

| (numbers.id + numbers.id) | (numbers.number + numbers.number) |
|---------------------------|-----------------------------------|
| 2                         | 20                                |
| 4                         | 40                                |
| 6                         | NULL                              |


### COLUMNS Regular Expression
`COLUMNS` supports passing a regex in as a string constant:

```sql
SELECT COLUMNS('(id|numbers?)') FROM numbers;
```

| id | number |
|----|--------|
| 1  | 10     |
| 2  | 20     |
| 3  | NULL   |

### COLUMNS Lambda Function
`COLUMNS` also supports passing in a lambda function. The lambda function will be evaluated for all columns present in the `FROM` clause, and only columns that match the lambda function will be returned. This allows the execution of arbitrary expressions in order to select columns.

```sql
SELECT COLUMNS(c -> c LIKE '%num%') FROM numbers;
```

| number |
|--------|
| 10     |
| 20     |
| NULL   |

### Struct.*

The `*` expression can also be used to retrieve all keys from a struct as separate columns.
This is particularly useful when a prior operation creates a struct of unknown shape, or if a query must handle any potential struct keys.
See the [struct](../data_types/struct) and [nested function](../functions/nested) pages for more details on working with structs. 

```sql
-- All keys within a struct can be returned as separate columns using *
SELECT a.* FROM (SELECT {'x':1, 'y':2, 'z':3} as a);
```

| x | y | z |
|:---|:---|:---|
| 1 | 2 | 3 |