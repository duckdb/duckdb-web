---
layout: docu
title: Merge Statement for SCD Type 2
---

This is a practical, step-by-step guide to using DuckDB’s `MERGE` statement (introduced in v1.4.0) to perform upserts and build [Slowly Changing Dimension Type 2 (SCD Type 2) tables](https://en.wikipedia.org/wiki/Slowly_changing_dimension). Type 2 SCDs let you keep full historical versions of records while clearly identifying the current version, perfect for audit trails, data warehousing, and analytical workloads. Type 2 SCDs are practical when you want to know previous values of your primary key data, when it changed and for how long it was in a particular state.

## Why Use MERGE in DuckDB?

- Single SQL statement for `INSERT`, `UPDATE`, and soft `DELETE` (upsert and expire).
- Much cleaner and faster than equivalent Python/Pandas logic.
- Full history tracking without hard deletes.
- Works directly on Parquet, CSV, databases, thanks to DuckDB's connectivity!

## Prerequisites

- DuckDB ≥ 1.4.0
- Basic SQL knowledge

## Key Terminology

| Term                          | Meaning                                                                                   |
|-------------------------------|-------------------------------------------------------------------------------------------|
| **Target table**              | The main/master table you are updating (e.g., `master_ducks`)                             |
| **Source table**              | The incoming/new data (e.g., `incoming_ducks`)                                            |
| **MERGE INTO**                | Specifies the target table                                                                |
| **USING**                     | Specifies the source table/query                                                          |
| **ON**                        | Join condition (usually primary/business key + current flag)                             |
| **WHEN MATCHED**              | Row exists in both → typically UPDATE (or DELETE)                                         |
| **WHEN NOT MATCHED BY TARGET**| New row (insert)                                                                          |
| **WHEN NOT MATCHED BY SOURCE**| Row disappeared → soft-delete/expire old version                                          |
| **RETURNING merge_action**    | Optional: shows what happened to each row (INSERT/UPDATE/DELETE)                          |

## Build an SCD Type 2 Dimension Table

We’ll track ducks and preserve history whenever their name, breed, or location changes.

> DuckDB has a frontend notebook UI, this is great for managing several SQL statements and segmenting your code.
> The UI ships with the DuckDB CLI, so if you have the CLI installed you can use the front end.
> To start the notebook front end just run: `duckdb -ui` and you can navigate to [http://localhost:4213/](http://localhost:4213/) to start writing your SQL code inside of your notebooks. Just copy and paste the following code blocks to follow this guide.

### Step 1: Create the Incoming (source) Table

This table represents today’s transactional data.

```sql
CREATE TABLE IF NOT EXISTS incoming_ducks (
    duck_id     INTEGER,
    duck_name   VARCHAR,
    breed       VARCHAR,
    location    VARCHAR,
    begin_date  DATE,
    end_date    DATE,
    is_current  BOOLEAN
);

INSERT INTO incoming_ducks VALUES
    (101, 'Quackers',   'Mallard',       'Pond B',      CURRENT_DATE - INTERVAL '1 day', NULL, true),
    (102, 'Waddles',    'Pekin',         'Pond A',      CURRENT_DATE - INTERVAL '1 day', NULL, true),
    (104, 'Splash',     'Muscovy',       'Pond C',      CURRENT_DATE - INTERVAL '1 day', NULL, true),
    (105, 'Puddles',    'Indian Runner', 'Relocated',   CURRENT_DATE - INTERVAL '1 day', NULL, true);

```

### Step 2: Create the Master (target) Table

This table represents the type 2 SCD data (i.e., transaction data with history).

```sql
CREATE TABLE IF NOT EXISTS master_ducks (
    record_id   INTEGER PRIMARY KEY,
    duck_id     INTEGER NOT NULL,
    duck_name   VARCHAR,
    breed       VARCHAR,
    location    VARCHAR,
    begin_date  DATE NOT NULL,
    end_date    DATE,
    is_current  BOOLEAN NOT NULL DEFAULT true
);

CREATE SEQUENCE IF NOT EXISTS duck_record_seq START 1;

INSERT INTO master_ducks VALUES
    (nextval('duck_record_seq'), 101, 'Quackers', 'Mallard',       'Pond A', CURRENT_DATE - INTERVAL '2 days', NULL, true),
    (nextval('duck_record_seq'), 102, 'Waddles',  'Pekin',         'Pond A', CURRENT_DATE - INTERVAL '2 days', NULL, true),
    (nextval('duck_record_seq'), 103, 'Feathers', 'Rouen',         'Pond B', CURRENT_DATE - INTERVAL '2 days', NULL, true),
    (nextval('duck_record_seq'), 105, 'Puddles',  'Indian Runner', 'Pond A', CURRENT_DATE - INTERVAL '2 days', NULL, true);
```

### Step 3: Perform the Merge Statement

This statement will perform the merge, it will check for differences between the data of target and source and follow the `WHEN MATCHED` or `WHEN NOT MATCHED` logic specified.

```sql
MERGE INTO master_ducks AS target
USING incoming_ducks AS source
ON target.duck_id = source.duck_id AND target.is_current = true

WHEN MATCHED AND (
       target.duck_name <> source.duck_name OR
       target.breed     <> source.breed     OR
       target.location  <> source.location
) THEN UPDATE SET
    end_date    = CURRENT_DATE - INTERVAL '1 day',
    is_current  = false

WHEN NOT MATCHED BY SOURCE AND target.is_current = true THEN UPDATE SET
    end_date    = CURRENT_DATE - INTERVAL '1 day',
    is_current  = false

WHEN NOT MATCHED BY TARGET THEN INSERT (
    record_id, duck_id, duck_name, breed, location,
    begin_date, end_date, is_current
) VALUES (
    nextval('duck_record_seq'),
    source.duck_id, source.duck_name, source.breed, source.location,
    source.begin_date, source.end_date, source.is_current
)

RETURNING merge_action, *;
```

### Step 4: Insert New Current Versions for Changed Records

This statement inserts the new current records into the master table. While it's possible to achieve the same result using the `MERGE` statement's `RETURNING` clause, this two-step approach is more straightforward and easier to understand.

```sql
INSERT INTO master_ducks (
    record_id, duck_id, duck_name, breed, location,
    begin_date, end_date, is_current
)
SELECT
    nextval('duck_record_seq'),
    source.duck_id,
    source.duck_name,
    source.breed,
    source.location,
    CURRENT_DATE AS begin_date,
    NULL AS end_date,
    true AS is_current
FROM incoming_ducks AS source
INNER JOIN master_ducks AS target
    ON source.duck_id = target.duck_id
WHERE target.is_current = false
  AND target.end_date = CURRENT_DATE - INTERVAL '1 day';
```

### Step 5: Query The Results

The following queries can be used to examine the data resulting from the `MERGE` statement.

```sql
-- All history
SELECT * FROM master_ducks ORDER BY duck_id, begin_date DESC;

-- Only current records
SELECT * FROM master_ducks WHERE is_current = true;

-- Only expired historical records
SELECT * FROM master_ducks WHERE is_current = false ORDER BY duck_id, begin_date DESC;
```

### Step 6: Examine a Single Duck

To better illustrate the concept, let's examine a single duck, to drive home the value add for type 2 SCDs.
If we select from the master table after running the merge statement and the post update insert statement, we can see the individual rows for `Quackers`.

To view the original row of data that is historical: 

```sql
SELECT * FROM master_ducks where duck_name = 'Quackers' and is_current = false;
```

Returns:

| record_id | duck_id | duck_name | breed   | location | begin_date   | end_date     | is_current |
|----------:|--------:|----------:|---------|----------|-------------|--------------|------------|
| 1         | 101     | Quackers  | Mallard | Pond A   | 2025-11-24  | 2025-11-25   | false      |

**Note**: 

- The `end date` is NOT NULL, it has the date when this duck's data was updated.
- The `is_current` is `false` indicating this is a historical record.
- The field that will change is `location`, it is currently `Pond A` and will be updated to `Pond B`.

To view the current row of data:

```sql
SELECT * FROM master_ducks where duck_name = 'Quackers' and is_current = true;
```

| record_id | duck_id | duck_name | breed   | location | begin_date   | end_date | is_current |
|----------:|--------:|----------:|---------|----------|-------------|----------|------------|
| 10        | 101     | Quackers  | Mallard | Pond B   | 2025-11-26  | NULL     | true       |

**Note**: 

- The `end date` is NULL, the NULL in this context indicates this is the latest record for this `duck_id`.
- The `is_current` is `true` also indicating this is a current record.
- The `location` is now `Pond B`.

To view all of `Quackers` data, which will contain both current and non-current rows:

```sql
SELECT * FROM master_ducks where duck_name = 'Quackers';
```

| record_id | duck_id | duck_name | breed   | location | begin_date   | end_date | is_current |
| 1         | 101     | Quackers  | Mallard | Pond A   | 2025-11-24  | 2025-11-25   | false      |
| 10        | 101     | Quackers  | Mallard | Pond B   | 2025-11-26  | NULL     | true       |

## Common Patterns and Variations

| Use Case                          | Clause to Use                                                      |
|-----------------------------------|--------------------------------------------------------------------|
| Simple upsert (no history)        | `WHEN MATCHED THEN UPDATE` and `WHEN NOT MATCHED BY TARGET THEN INSERT` |
| Upsert and delete missing rows      | Add `WHEN NOT MATCHED BY SOURCE THEN DELETE`                       |
| Only insert new, never update     | Omit `WHEN MATCHED`                                                |
| Return affected rows              | Add `RETURNING merge_action, *`                                    |

## Best Practices

- Remember that `TARGET` is the master table and `SOURCE` is the incoming table or query.
- Keep end_date NULL for current rows (makes queries faster).
- Wrap `MERGE` and `INSERT` statements in a transaction when needed.
- Use a primary key or a surrogate key for uniqueness.
- Test with RETURNING first.
