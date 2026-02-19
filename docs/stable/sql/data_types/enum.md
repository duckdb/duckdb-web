---
blurb: The Enum type represents a dictionary data structure with all possible unique
  values of a column.
layout: docu
redirect_from:
  - /docs/sql/data_types/enum
title: Enum Data Type
---

| Name | Description |
|:--|:-----|
| `ENUM` | Dictionary representing all possible string values of a column |

The enum type represents a dictionary data structure with all possible unique values of a column. For example, a column storing the days of the week can be an enum holding all possible days. Enums are particularly interesting for string columns with low cardinality (i.e., fewer distinct values). This is because the column only stores a numerical reference to the string in the enum dictionary, resulting in immense savings in disk storage and faster query performance.

## Creating Enums

You can create an enum using hardcoded values:

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
-- This statement will fail since enums cannot hold NULL values:
-- CREATE TYPE mood AS ENUM ('sad', NULL);
-- This statement will fail since enum values must be unique:
-- CREATE TYPE mood AS ENUM ('sad', 'sad');
```

You can create enums in a specific schema:

```sql
CREATE SCHEMA my_schema;
CREATE TYPE my_schema.mood AS ENUM ('sad', 'ok', 'happy');
```

Anonymous enums can be created on the fly during [casting]({% link docs/preview/sql/expressions/cast.md %}):

```sql
SELECT 'clubs'::ENUM ('spades', 'hearts', 'diamonds', 'clubs');
```

You can also create an enum using a `SELECT` statement that returns a single column of `VARCHAR`s.
The set of values from the select statement will be deduplicated automatically,
and `NULL` values will be ignored:

```sql
CREATE TYPE region AS ENUM (SELECT region FROM sales_data);
```

If you are importing data from a file, you can create an enum for a `VARCHAR` column before importing:

```sql
CREATE TYPE region AS ENUM (SELECT region FROM 'sales_data.csv');
CREATE TABLE sales_data (amount INTEGER, region region);
COPY sales_data FROM 'sales_data.csv';
```

## Using Enums

Enum values are case-sensitive, so 'maltese' and 'Maltese' are considered different values:

```sql
CREATE TYPE breed AS ENUM ('maltese', 'Maltese');
-- Will return false
SELECT 'maltese'::breed = 'Maltese'::breed;
-- Will error
SELECT 'MALTESE'::breed;
```

After an enum has been created, it can be used anywhere a standard built-in type is used.
For example, we can create a table with a column that references the enum.

```sql
CREATE TABLE person (
    name TEXT,
    current_mood mood
);
INSERT INTO person VALUES
    ('Pedro', 'happy'),
    ('Mark', NULL),
    ('Pagliacci', 'sad'),
    ('Mr. Mackey', 'ok');
```

The following query will fail since the mood type does not have a `quackity-quack` value.

```sql
INSERT INTO person VALUES ('Hannes', 'quackity-quack');
```

## Enums vs. Strings

DuckDB enums are automatically cast to `VARCHAR` types whenever necessary.
This characteristic allows for comparisons between different enums, or an enum and a `VARCHAR` column.

It also allows for an enum to be used in any `VARCHAR` function. For example:

```sql
SELECT current_mood, regexp_matches(current_mood, '.*a.*') AS contains_a FROM person;
```

| current_mood | contains_a |
|:-------------|:-----------|
| happy        | true       |
| NULL         | NULL       |
| sad          | true       |
| ok           | false      |

When comparing two different enum types, DuckDB will cast both to strings and perform a string comparison:

```sql
CREATE TYPE new_mood AS ENUM ('happy', 'anxious');
SELECT * FROM person
WHERE current_mood = 'happy'::new_mood;
-- Equivalent to `WHERE current_mood::VARCHAR = 'happy'::VARCHAR`
```

|   name    | current_mood |
|:----------|:-------------|
| Pedro     | happy        |


When comparing an enum to a `VARCHAR`, DuckDB will cast the enum to `VARCHAR` and perform a string comparison:

```sql
SELECT * FROM person
WHERE current_mood = name;
-- Equivalent to `WHERE current_mood::VARCHAR = name`
-- No rows returned
```

When comparing against a constant string, DuckDB will perform an optimization
and `try_cast(⟨constant string⟩, enum_type)`{:.language-sql .highlight} so that physically
we are doing an integer comparison instead of a string comparison
(but logically it is still a string comparison):

```sql
SELECT * FROM person
WHERE current_mood = 'sad';
-- Equivalent to `WHERE current_mood::VARCHAR = 'sad'`
```

|   name    | current_mood |
|:----------|:-------------|
| Pagliacci | sad          |


> Warning This means that comparing against a random (non-equivalent) string always results in `false` (and does not error):

```sql
SELECT * FROM person
WHERE current_mood = 'bogus';
-- Equivalent to `WHERE current_mood::VARCHAR = 'bogus'`
-- No rows returned
```

If you want to enforce type-safety, cast to the enum explicitly:

```sql
SELECT * FROM person
WHERE current_mood = 'bogus'::mood;
-- Conversion Error: Could not convert string 'bogus' to UINT8
```

## Ordering of Enums

Enum values are ordered according to their order in the enum's definition. For example:

```sql
CREATE TYPE priority AS ENUM ('low', 'medium', 'high');
SELECT 'low'::priority < 'high'::priority AS comp;
-- note that 'low'::VARCHAR < 'high'::VARCHAR is false!
```

| comp |
|-----:|
| true |

```sql
SELECT unnest(['medium'::priority, 'high'::priority, 'low'::priority]) AS m
ORDER BY m;
```

|   m    |
|:-------|
| low    |
| medium |
| high   |

> Warning If you compare an enum to a non-enum (e.g., a `VARCHAR` or a different enum type),
the enum will first be cast to a string (as described in the previous section),
and the comparison will be done lexicographically as with strings:

```sql
CREATE TABLE tasks (name TEXT, priority_level priority);
INSERT INTO tasks VALUES ('a', 'low'), ('b', 'medium'), ('c', 'high');
-- WARNING!
-- Equivalent to `WHERE priority_level::VARCHAR >= 'medium'`
SELECT * FROM tasks
WHERE priority_level >= 'medium';  
-- Misses the 'high' priority task!
```

| name | priority_level  |
|:-----|:----------------|
| b    | medium          |


So, if you want to e.g. "get all priorities at or above `medium`" then explicitly cast to the enum type:

```sql
SELECT * FROM tasks
WHERE priority_level >= 'medium'::priority;
```

| name | priority_level  |
|:-----|:----------------|
| b    | medium          |
| c    | high            |

## Functions

See [Enum Functions]({% link docs/preview/sql/functions/enum.md %}).

For example, show the available values in the `moods` enum using the `enum_range` function:

```sql
SELECT enum_range(NULL::moods) AS my_enum_range;
```

|  my_enum_range     |
|--------------------|
| `[sad, ok, happy]` |


## Enum Removal

Enum types are stored in the catalog, and a catalog dependency is added to each table that uses them. It is possible to drop an enum from the catalog using the following command:

```sql
DROP TYPE ⟨enum_name⟩;
```

Currently, it is possible to drop enums that are used in tables without affecting the tables.

> Warning This behavior of the enum removal feature is subject to change. In future releases, it is expected that any dependent columns must be removed before dropping the enum, or the enum must be dropped with the additional `CASCADE` parameter.
