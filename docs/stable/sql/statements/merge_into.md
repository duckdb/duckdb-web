---
layout: docu
railroad: statements/merge_into.js
title: MERGE INTO Statement
redirect_from:
- /cal/10
---

The `MERGE INTO` statement is an alternative to `INSERT INTO ... ON CONFLICT` that doesn't need a primary key since it allows for a custom match condition. This is a very useful alternative for upserting use cases (`INSERT` + `UPDATE`) when the destination table does not have a primary key constraint.

## Examples

First, let's create a simple table.

```sql
CREATE TABLE people (id INTEGER, name VARCHAR, salary FLOAT);
INSERT INTO people VALUES (1, 'John', 92_000.0), (2, 'Anna', 100_000.0);
```

The simplest upsert would be updating or inserting a whole row.

```sql
MERGE INTO people
    USING (
        SELECT
            unnest([3, 1]) AS id,
            unnest(['Sarah', 'John']) AS name,
            unnest([95_000.0, 105_000.0]) AS salary
    ) AS upserts
    ON (upserts.id = people.id)
    WHEN MATCHED THEN UPDATE
    WHEN NOT MATCHED THEN INSERT;

FROM people
ORDER BY id;
```

| id | name  |  salary  |
|---:|-------|---------:|
| 1  | John  | 105000.0 |
| 2  | Anna  | 100000.0 |
| 3  | Sarah | 95000.0  |


In the previous example we are updating the whole row if `id` matches. However, it is also a common pattern to receive a _change set_ with some keys and the changed value. This is a good use for `SET`. If the match condition uses a column that has the same name in the source and destination, the keyword `USING` can be used in the match condition.

```sql
MERGE INTO people
    USING (
        SELECT
            1 AS id, 
            98_000.0 AS salary
    ) AS salary_updates
    USING (id)
    WHEN MATCHED THEN UPDATE SET salary = salary_updates.salary;

FROM people
ORDER BY id;
```

| id | name  |  salary  |
|---:|-------|---------:|
| 1  | John  | 98000.0  |
| 2  | Anna  | 100000.0 |
| 3  | Sarah | 95000.0  |

Another common pattern is to receive a _delete set_ of rows, which may only contain ids of rows to be deleted.

```sql
MERGE INTO people
    USING (
        SELECT
            1 AS id, 
    ) AS deletes
    USING (id)
    WHEN MATCHED THEN DELETE;

FROM people
ORDER BY id;
```

| id | name  |  salary  |
|---:|-------|---------:|
| 2  | Anna  | 100000.0 |
| 3  | Sarah | 95000.0  |

`MERGE INTO` also supports more complex conditions, for example, for a given _delete set_ we can decide to only remove rows that contain a `salary` bigger or equal than a certain amount.

```sql
MERGE INTO people
    USING (
        SELECT
            unnest([3, 2]) AS id, 
    ) AS deletes
    USING (id)
    WHEN MATCHED AND people.salary >= 100_000.0 THEN DELETE;

FROM people
ORDER BY id;
```

| id | name  | salary  |
|---:|-------|--------:|
| 3  | Sarah | 95000.0 |

If needed, DuckDB also supports multiple `UPDATE` and `DELETE` conditions. The `RETURNING` clause can be used to indicate which rows were affected by the `MERGE` statement.

```sql
-- Let's get John back in!
INSERT INTO people VALUES (1, 'John', 105_000.0);

MERGE INTO people
    USING (
        SELECT
            unnest([3, 1]) AS id,
            unnest([89_000.0, 70_000.0]) AS salary
    ) AS upserts
    USING (id)
    WHEN MATCHED AND people.salary < 100_000.0 THEN UPDATE SET salary = upserts.salary
    -- Second update or delete condition
    WHEN MATCHED AND people.salary > 100_000.0 THEN DELETE
    WHEN NOT MATCHED THEN INSERT BY NAME
    RETURNING merge_action, *;
```

| merge_action | id | name  |  salary  |
|--------------|---:|-------|---------:|
| UPDATE       | 3  | Sarah | 89000.0  |
| DELETE       | 1  | John  | 105000.0 |

In some cases, you may want to perform a different action specifically if the source doesn't meet a condition. For example, if we expect that data that is not present on the source shouldn't be present in the target:

```sql
CREATE TABLE target AS
    SELECT unnest([1,2]) AS id;

MERGE INTO target
    USING (SELECT 1 AS id) source
    USING (id)
    WHEN MATCHED THEN UPDATE
    WHEN NOT MATCHED BY SOURCE THEN DELETE
    RETURNING merge_action, *;
```

| merge_action | id |
|--------------|---:|
| UPDATE       | 1  |
| DELETE       | 2  |

There is also the possibility of specifying `WHEN NOT MATCHED BY TARGET`. However, the behavior is, as you may expect, the same as `WHEN NOT MATCHED` since by default when specifying conditions, we look at the target.

## Syntax

<div id="rrdiagram"></div>
