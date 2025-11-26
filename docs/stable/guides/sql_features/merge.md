# Guide: Efficient Data Upserts with DuckDB — Mastering the MERGE Statement for SCD Type 2

This is a practical, step-by-step guide to using DuckDB’s `MERGE` statement (introduced in v1.4.0) to perform upserts and build **Slowly Changing Dimension Type 2 (SCD Type 2)** tables. SCD Type 2 lets you keep full historical versions of records while clearly identifying the current version — perfect for audit trails, data warehousing, and analytical workloads.

### Why Use MERGE in DuckDB?
- Single SQL statement for INSERT + UPDATE + soft DELETE (upsert + expire)
- Much cleaner and faster than equivalent Python/Pandas logic
- Full history tracking without hard deletes
- Works directly on Parquet, CSV, databases, etc., thanks to DuckDB’s connectivity

### Prerequisites
- DuckDB ≥ 1.4.0
- Basic SQL knowledge
- (Optional) DuckDB notebook UI: run `duckdb -ui` → http://localhost:4213/

### Key Terminology

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

### Goal: Build an SCD Type 2 Dimension Table

We’ll track ducks and preserve history whenever their name, breed, or location changes.

#### Step 1: Create the Incoming (Source) Table
This represents today’s transactional data.

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

#### Step 1: Create the Incoming (Source) Table

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

#### Step 3: Create the Incoming (Source) Table

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

## Step 4: Insert New Current Versions for Changed Records

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

#### Step 5: Query The Results

```sql
-- All history
SELECT * FROM master_ducks ORDER BY duck_id, begin_date DESC;

-- Only current records
SELECT * FROM master_ducks WHERE is_current = true;

-- Only expired historical records
SELECT * FROM master_ducks WHERE is_current = false ORDER BY duck_id, begin_date DESC;
```

### Common Patterns and Variations

| Use Case                          | Clause to Use                                                      |
|-----------------------------------|--------------------------------------------------------------------|
| Simple upsert (no history)        | `WHEN MATCHED THEN UPDATE` + `WHEN NOT MATCHED BY TARGET THEN INSERT` |
| Upsert + delete missing rows      | Add `WHEN NOT MATCHED BY SOURCE THEN DELETE`                       |
| Only insert new, never update     | Omit `WHEN MATCHED`                                                |
| Return affected rows              | Add `RETURNING merge_action, *`                                    |

### Best Practices

Best Practices

- Always match on business key + is_current = true for SCD2
- Use a surrogate key + sequence for uniqueness
- Keep end_date NULL for current rows (makes queries faster)
- Test with RETURNING first
- Wrap MERGE + INSERT in a transaction when needed