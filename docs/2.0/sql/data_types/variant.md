---
layout: docu
redirect_from:
- /docs/current/sql/data_types/variant
- /docs/lts/sql/data_types/variant
- /docs/preview/sql/data_types/variant
- /docs/stable/sql/data_types/variant
title: Variant Type
---

The `VARIANT` type stores typed, binary data where each row is self-contained with its own type information. This differs from the [JSON type]({% link docs/2.0/data/json/json_type.md %}), which is physically stored as text. Because type metadata is embedded per-value, `VARIANT` provides better compression and query performance than JSON for semi-structured data.

The `VARIANT` type is inspired by [Snowflake's semi-structured `VARIANT` data type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured). It is available [in Parquet since 2025](https://github.com/apache/parquet-format/blob/master/VariantEncoding.md) and also supported by DuckDB's [Parquet reader](#parquet-support).

## Examples

### Storing Different Types in the Same Column

A `VARIANT` column can hold values of different types across rows:

```sql
CREATE TABLE events (id INTEGER, data VARIANT);
INSERT INTO events VALUES
    (1, 42::VARIANT),
    (2, 'hello world'::VARIANT),
    (3, [1, 2, 3]::VARIANT),
    (4, {'name': 'Alice', 'age': 30}::VARIANT);

SELECT * FROM events;
```

```text
┌───────┬────────────────────────────┐
│  id   │            data            │
│ int32 │          variant           │
├───────┼────────────────────────────┤
│     1 │ 42                         │
│     2 │ hello world                │
│     3 │ [1, 2, 3]                  │
│     4 │ {'age': 30, 'name': Alice} │
└───────┴────────────────────────────┘
```

Note that the keys of `VARIANT` objects are sorted: `{'name': 'Alice', 'age': 30}::VARIANT` is returned as `{'age': 30, 'name': Alice}`.

### Checking the Type of a Value

Use `variant_typeof` to inspect the underlying type of each row:

```sql
SELECT id, data, variant_typeof(data) AS vtype
FROM events;
```

```text
┌───────┬────────────────────────────┬───────────────────┐
│  id   │            data            │       vtype       │
│ int32 │          variant           │      varchar      │
├───────┼────────────────────────────┼───────────────────┤
│     1 │ 42                         │ INT32             │
│     2 │ hello world                │ VARCHAR           │
│     3 │ [1, 2, 3]                  │ ARRAY(3)          │
│     4 │ {'age': 30, 'name': Alice} │ OBJECT(age, name) │
└───────┴────────────────────────────┴───────────────────┘
```

### Extracting Fields from Nested Variants

Fields can be extracted from nested `VARIANT` values using dot notation or the `variant_extract` function:

```sql
SELECT data.name FROM events WHERE id = 4;
```

```sql
SELECT variant_extract(data, 'name') AS name FROM events WHERE id = 4;
```

```text
┌─────────┐
│  name   │
│ variant │
├─────────┤
│ Alice   │
└─────────┘
```

## Storage

> New Shredding `VARIANT` columns in DuckDB's storage was introduced in DuckDB 2.0.

When storing `VARIANT` columns in a DuckDB database file, DuckDB 2.0 automatically detects the common structure of the values and *shreds* them, i.e., stores the fields that share a type as separate, typed columns. Shredded data compresses well and can be scanned efficiently.

Shredding is only applied to row groups with at least `variant_minimum_shredding_size` rows (by default, 30,000 rows, roughly one fourth of the default row group size). Setting it to `-1` disables shredding:

```sql
SET variant_minimum_shredding_size = -1;
```

## Parquet Support

DuckDB supports reading and writing `VARIANT` types from [Parquet files]({% link docs/2.0/data/parquet/overview.md %}), including *shredding,* a technique that stores nested data as flat values for more efficient access.

### Writing VARIANT to Parquet

When writing `VARIANT` columns to Parquet, DuckDB can automatically shred (decompose) the variant data into typed columns based on the structure of the first row group. This auto-shredding improves read performance by enabling predicate pushdown and efficient column access.

To explicitly provide a schema for shredding, use the `SHREDDING` copy option:

```sql
COPY events TO 'events.parquet' (
    FORMAT parquet,
    SHREDDING {'data': 'STRUCT(name VARCHAR, age INTEGER)'}
);
```

### Reading Snowflake VARIANT from Parquet

DuckDB can read shredded `VARIANT` Parquet files produced by Snowflake, automatically reconstructing the variant values from the shredded columns.

## Functions

See the [Variant Functions page]({% link docs/2.0/sql/functions/variant.md %}) for the functions that operate on `VARIANT` values.
