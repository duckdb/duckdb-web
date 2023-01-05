---
layout: docu
title: Enum Types
selected: Documentation/Data Types/Enum
expanded: Data Types
blurb: The ENUM type represents a dictionary data structure with all possible unique values of a column.
---
| Name | Description |
|:---|:---|
| ENUM | Dictionary Encoding representing all possible string values of a column. |

## Enums

The `ENUM` type represents a dictionary data structure with all possible unique values of a column. For example, a column storing the days of the week can be an Enum holding all possible days. Enums are particularly interesting for string columns with high cardinality. This is because the column only stores a numerical reference to the string in the Enum dictionary, resulting in immense savings in disk storage and faster query performance.


### Enum Definition
Enum types are created from either a hardcoded set of values or from a select statement that returns a single column of varchars. The set of values in the select statement will be deduplicated, but if the enum is created from a hardcoded set there may not be any duplicates.
```sql
-- Create enum using hardcoded values
CREATE TYPE ${enum_name} AS ENUM ([${value_1},${value_2},...])

-- Create enum using a select statement that returns a single column of varchars
CREATE TYPE ${enum_name} AS ENUM (${SELECT expression})
```
For example:
```sql
-- Creates new user defined type 'mood' as an Enum
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');

-- This will fail since the mood type already exists
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy', 'anxious');

-- This will fail since Enums cannot hold null values
CREATE TYPE breed AS ENUM ('maltese', NULL);

-- This will fail since Enum values must be unique
CREATE TYPE breed AS ENUM ('maltese', 'maltese');

-- Create an enum from a select statement
-- First create an example table of values
CREATE TABLE my_inputs AS 
    SELECT 'duck'  AS my_varchar UNION ALL
    SELECT 'duck'  AS my_varchar UNION ALL
    SELECT 'goose' AS my_varchar;

-- Create an enum using the unique string values in the my_varchar column
CREATE TYPE birds AS ENUM (SELECT my_varchar FROM my_inputs);

-- Show the available values in the birds enum using the enum_range function
SELECT enum_range(NULL::birds) AS my_enum_range;
```

| my_enum_range |
|---------------|
| [duck, goose] |

### Enum Usage
After an enum has been created, it can be used anywhere a standard built-in type is used. For example, we can create a table with a column that references the enum.
```sql
-- Creates a table person, with attributes name (string type) and current_mood (mood type)
CREATE TABLE person (
    name text,
    current_mood mood
);

-- Inserts tuples in the person table
INSERT INTO person VALUES ('Pedro','happy'), ('Mark', NULL), ('Pagliacci', 'sad'), ('Mr. Mackey', 'ok');

-- This will fail since the mood type does not have a 'quackity-quack' value.
INSERT INTO person VALUES ('Hannes','quackity-quack');

-- The string 'sad' is cast to the type Mood, returning a numerical reference value.
-- This makes the comparison a numerical comparison instead of a string comparison.
SELECT * FROM person WHERE current_mood = 'sad';
----
Pagliacci

-- If you are importing data from a file, you can create an Enum for a VARCHAR column before importing
-- The subquery select automatically selects only distinct values
CREATE TYPE mood AS ENUM (SELECT mood FROM 'path/to/file.csv');

-- Then you can create a table with the ENUM type and import using any data import statement
CREATE TABLE person(name text, current_mood mood);
COPY person FROM 'path/to/file.csv' (AUTO_DETECT TRUE);

```

### Enum Vs. Strings
DuckDB Enums are automatically cast to `VARCHAR` types whenever necessary. This characteristic allows for `ENUM` columns to be used in any `VARCHAR` function. In addition, it also allows for comparisons between different `ENUM` columns, or an `ENUM` and a `VARCHAR` column.

For example:
```sql
-- regexp_matches is a function that takes a VARCHAR, hence current_mood is cast to VARCHAR
SELECT regexp_matches(current_mood, '.*a.*') FROM person
----
TRUE
FALSE
TRUE
FALSE


CREATE TYPE new_mood AS ENUM ('happy', 'anxious');

CREATE TABLE person_2(
    name text,
    current_mood mood,
    future_mood new_mood
    past_mood VARCHAR
);

-- Since current_mood and future_mood are constructed on different ENUMs
-- DuckDB will cast both ENUMs to strings and perform a string comparison.
SELECT * FROM person_2 where current_mood = future_mood;

-- Since current_mood is an ENUM
-- DuckDB will cast the current_mood ENUM to VARCHAR and perform a string comparison
SELECT * FROM person_2 where current_mood = past_mood;
```


### Enum Removal
Enum types are stored in the catalog, and a catalog dependency is added to each table that uses them. It is possible to drop an Enum from the catalog using the following command:
```sql
DROP TYPE ${enum_name}
```
Note that any dependent must be removed before dropping the enum, or the enum must be dropped with the additional `CASCADE` parameter.

For example:
```sql
-- This will fail since person has a catalog dependency to the mood type
DROP TYPE mood

DROP TABLE person;
DROP TABLE person_2;

-- This successfully removes the mood type.
-- Another option would be to DROP TYPE mood CASCADE (Drops the type and its dependents)
DROP TYPE mood
```
