---
layout: docu
railroad: statements/update.js
title: UPDATE Statement
---

The `UPDATE` statement modifies the values of rows in a table.

## Examples

For every row where `i` is `NULL`, set the value to 0 instead:

```sql
UPDATE tbl
SET i = 0
WHERE i IS NULL;
```

Set all values of `i` to 1 and all values of `j` to 2:

```sql
UPDATE tbl
SET i = 1, j = 2;
```

## Syntax

<div id="rrdiagram"></div>

`UPDATE` changes the values of the specified columns in all rows that satisfy the condition. Only the columns to be modified need be mentioned in the `SET` clause; columns not explicitly modified retain their previous values.

## Update from Other Table

A table can be updated based upon values from another table. This can be done by specifying a table in a `FROM` clause, or using a sub-select statement. Both approaches have the benefit of completing the `UPDATE` operation in bulk for increased performance.

```sql
CREATE OR REPLACE TABLE original AS
    SELECT 1 AS key, 'original value' AS value
    UNION ALL
    SELECT 2 AS key, 'original value 2' AS value;

CREATE OR REPLACE TABLE new AS
    SELECT 1 AS key, 'new value' AS value
    UNION ALL
    SELECT 2 AS key, 'new value 2' AS value;

SELECT *
FROM original;
```

| key |      value       |
|-----|------------------|
| 1   | original value   |
| 2   | original value 2 |

```sql
UPDATE original
    SET value = new.value
    FROM new
    WHERE original.key = new.key;
```

Or:

```sql
UPDATE original
    SET value = (
        SELECT
            new.value
        FROM new
        WHERE original.key = new.key
    );
```

```sql
SELECT *
FROM original;
```

| key |    value    |
|-----|-------------|
| 1   | new value   |
| 2   | new value 2 |

## Update from Same Table

The only difference between this case and the above is that a different table alias must be specified on both the target table and the source table.
In this example `AS true_original` and `AS new` are both required.

```sql
UPDATE original AS true_original
    SET value = (
        SELECT
            new.value || ' a change!' AS value
        FROM original AS new
        WHERE true_original.key = new.key
    );
```

## Update Using Joins

To select the rows to update, `UPDATE` statements can use the `FROM` clause and express joins via the `WHERE` clause. For example:

```sql
CREATE TABLE city (name VARCHAR, revenue BIGINT, country_code VARCHAR);
CREATE TABLE country (code VARCHAR, name VARCHAR);
INSERT INTO city VALUES ('Paris', 700, 'FR'), ('Lyon', 200, 'FR'), ('Brussels', 400, 'BE');
INSERT INTO country VALUES ('FR', 'France'), ('BE', 'Belgium');
```

To increase the revenue of all cities in France, join the `city` and the `country` tables, and filter on the latter:

```sql
UPDATE city
SET revenue = revenue + 100
FROM country
WHERE city.country_code = country.code
  AND country.name = 'France';
```

```sql
SELECT *
FROM city;
```

|   name   | revenue | country_code |
|----------|--------:|--------------|
| Paris    | 800     | FR           |
| Lyon     | 300     | FR           |
| Brussels | 400     | BE           |

## Upsert (Insert or Update)

See the [Insert documentation]({% link docs/archive/1.1/sql/statements/insert.md %}#on-conflict-clause) for details.