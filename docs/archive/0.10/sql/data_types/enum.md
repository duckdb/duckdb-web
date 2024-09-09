---
blurb: The Enum type represents a dictionary data structure with all possible unique
  values of a column.
layout: docu
title: Enum Data Type
---

<div class="narrow_table"></div>

| Name | Description |
|:--|:-----|
| enum | Dictionary Encoding representing all possible string values of a column. |

The enum type represents a dictionary data structure with all possible unique values of a column. For example, a column storing the days of the week can be an enum holding all possible days. Enums are particularly interesting for string columns with low cardinality (i.e., fewer distinct values). This is because the column only stores a numerical reference to the string in the enum dictionary, resulting in immense savings in disk storage and faster query performance.

## Enum Definition

Enum types are created from either a hardcoded set of values or from a select statement that returns a single column of `VARCHAR`s. The set of values in the select statement will be deduplicated, but if the enum is created from a hardcoded set there may not be any duplicates.

Create enum using hardcoded values:

```sql
CREATE TYPE ⟨enum_name⟩ AS ENUM ([⟨value_1⟩, ⟨value_2⟩,...]);
```

Create enum using a `SELECT` statement that returns a single column of `VARCHAR`s:

```sql
CREATE TYPE ⟨enum_name⟩ AS ENUM (select_expression⟩);
```

For example:

Creates new user defined type 'mood' as an enum:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

This will fail since the `mood` type already exists:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy', 'anxious');
```

This will fail since enums cannot hold `NULL` values:

```sql
CREATE TYPE breed AS ENUM ('maltese', NULL);
```

This will fail since enum values must be unique:

```sql
CREATE TYPE breed AS ENUM ('maltese', 'maltese');
```

Create an enum from a select statement. First create an example table of values:

```sql
CREATE TABLE my_inputs AS
    SELECT 'duck'  AS my_varchar UNION ALL
    SELECT 'duck'  AS my_varchar UNION ALL
    SELECT 'goose' AS my_varchar;
```

Create an enum using the unique string values in the `my_varchar` column:

```sql
CREATE TYPE birds AS ENUM (SELECT my_varchar FROM my_inputs);
```

Show the available values in the `birds` enum using the `enum_range` function:

```sql
SELECT enum_range(NULL::birds) AS my_enum_range;
```

<div class="narrow_table"></div>

|  my_enum_range  |
|-----------------|
| `[duck, goose]` |

## Enum Usage

After an enum has been created, it can be used anywhere a standard built-in type is used. For example, we can create a table with a column that references the enum.

Creates a table `person`, with attributes `name` (string type) and `current_mood` (mood type):

```sql
CREATE TABLE person (
    name TEXT,
    current_mood mood
);
```

Inserts tuples in the `person` table:

```sql
INSERT INTO person
VALUES ('Pedro', 'happy'), ('Mark', NULL), ('Pagliacci', 'sad'), ('Mr. Mackey', 'ok');
```

The following query will fail since the mood type does not have `quackity-quack` value.

```sql
INSERT INTO person
VALUES ('Hannes', 'quackity-quack');
```

The string `sad` is cast to the type `mood`, returning a numerical reference value.
This makes the comparison a numerical comparison instead of a string comparison.

```sql
SELECT *
FROM person
WHERE current_mood = 'sad';
```

|   name    | current_mood |
|-----------|--------------|
| Pagliacci | sad          |

If you are importing data from a file, you can create an enum for a `VARCHAR` column before importing.
Given this, the following subquery selects automatically selects only distinct values:

```sql
CREATE TYPE mood AS ENUM (SELECT mood FROM 'path/to/file.csv');
```

Then you can create a table with the enum type and import using any data import statement:

```sql
CREATE TABLE person (name TEXT, current_mood mood);
COPY person FROM 'path/to/file.csv';
```

## Enums vs. Strings

DuckDB enums are automatically cast to `VARCHAR` types whenever necessary. This characteristic allows for enum columns to be used in any `VARCHAR` function. In addition, it also allows for comparisons between different enum columns, or an enum and a `VARCHAR` column.

For example:

Regexp_matches is a function that takes a VARCHAR, hence current_mood is cast to VARCHAR:

```sql
SELECT regexp_matches(current_mood, '.*a.*') AS contains_a
FROM person;
```

| contains_a |
|:-----------|
| true       |
| NULL       |
| true       |
| false      |

Create a new mood and table:

```sql
CREATE TYPE new_mood AS ENUM ('happy', 'anxious');
CREATE TABLE person_2 (
    name text,
    current_mood mood,
    future_mood new_mood,
    past_mood VARCHAR
);
```

Since the `current_mood` and `future_mood` columns are constructed on different enum types, DuckDB will cast both enums to strings and perform a string comparison:

```sql
SELECT *
FROM person_2
WHERE current_mood = future_mood;
```

When comparing the `past_mood` column (string), DuckDB will cast the `current_mood` enum to `VARCHAR` and perform a string comparison:

```sql
SELECT *
FROM person_2
WHERE current_mood = past_mood;
```

## Enum Removal

Enum types are stored in the catalog, and a catalog dependency is added to each table that uses them. It is possible to drop an enum from the catalog using the following command:

```sql
DROP TYPE ⟨enum_name⟩;
```

Currently, it is possible to drop enums that are used in tables without affecting the tables.

> Warning This behavior of the enum removal feature is subject to change. In future releases, it is expected that any dependent columns must be removed before dropping the enum, or the enum must be dropped with the additional `CASCADE` parameter.

## Comparison of Enums

Enum values are compared according to their order in the enum's definition. For example:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
```

```sql
SELECT 'sad'::mood < 'ok'::mood AS comp;
```

| comp |
|-----:|
| true |

```sql
SELECT unnest(['ok'::mood, 'happy'::mood, 'sad'::mood]) AS m
ORDER BY m;
```

|   m   |
|-------|
| sad   |
| ok    |
| happy |