---
github_repository: https://github.com/duckdb/ducklake
layout: docu
redirect_from:
- /ducklake
- /docs/extensions/ducklake
title: DuckLake
---

> DuckLake has been released in May 2025.
> Read the [announcement blog post]({% post_url 2025-05-27-ducklake %}).

The `ducklake` extension adds support for attaching to databases stored in the [DuckLake format](http://ducklake.select/). 
The complete documentation of this extension is available at the [DuckLake website](https://ducklake.select/docs/stable/duckdb/introduction).

## Installing and Loading

To install `ducklake`, run:

```sql
INSTALL ducklake;
```

The `ducklake` extension will be transparently [autoloaded]({% link docs/stable/core_extensions/overview.md %}#autoloading-extensions) on first use in an `ATTACH` clause.
If you would like to load it manually, run:

```sql
LOAD ducklake;
```

## Usage

```sql
ATTACH 'ducklake:metadata.ducklake' AS my_ducklake (DATA_PATH 'data_files');
USE my_ducklake;
```

## Tables

In DuckDB, the `ducklake` extension stores the [catalog tables](http://ducklake.select/docs/stable/specification/tables/overview) for a DuckLake named `my_ducklake` in the `__ducklake_metadata_⟨my_ducklake⟩`{:.language-sql .highlight} catalog.

## Functions

Note that DuckLake registers several functions.
These should be called with the catalog name as the first argument, e.g.:

```sql
FROM ducklake_snapshots('my_ducklake');
```

```text
┌─────────────┬────────────────────────────┬────────────────┬──────────────────────────┐
│ snapshot_id │       snapshot_time        │ schema_version │         changes          │
│    int64    │  timestamp with time zone  │     int64      │ map(varchar, varchar[])  │
├─────────────┼────────────────────────────┼────────────────┼──────────────────────────┤
│      0      │ 2025-05-26 11:41:10.838+02 │       0        │ {schemas_created=[main]} │
└─────────────┴────────────────────────────┴────────────────┴──────────────────────────┘
```

### `ducklake_snapshots`

Returns the snapshots stored in the DuckLake catalog name `catalog`.

| Parameter name | Parameter type | Named parameter | Description |
| -------------- | -------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`      | no              |             |

The information is encoded into a table with the following schema:

| Column name      | Column type                |
| ---------------- | -------------------------- |
| `snapshot_id`    | `BIGINT`                   |
| `snapshot_time`  | `TIMESTAMP WITH TIME ZONE` |
| `schema_version` | `BIGINT`                   |
| `changes`        | `MAP(VARCHAR, VARCHAR[])`  |

### `ducklake_table_info`

The `ducklake_table_info` function returns information on the tables stored in the DuckLake catalog named `catalog`.

| Parameter name | Parameter type | Named parameter | Description |
| -------------- | -------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`      | no              |             |

The information is encoded into a table with the following schema:

| Column name              | Column type |
| ------------------------ | ----------- |
| `table_name`             | `VARCHAR`   |
| `schema_id`              | `BIGINT`    |
| `table_id`               | `BIGINT`    |
| `table_uuid`             | `UUID`      |
| `file_count`             | `BIGINT`    |
| `file_size_bytes`        | `BIGINT`    |
| `delete_file_count`      | `BIGINT`    |
| `delete_file_size_bytes` | `BIGINT`    |

### `ducklake_table_insertions`

The `ducklake_table_insertions` function returns the rows inserted in a given table between snapshots of given versions or timestamps.
The function has two variants, depending on whether `start_snapshot` and `end_snapshot` have types `BIGINT` or `TIMESTAMP WITH TIME ZONE`.

| Parameter name   | Parameter type                        | Named parameter | Description |
| ---------------- | ------------------------------------- | --------------- | ----------- |
| `catalog`        | `VARCHAR`                             | no              |             |
| `schema_name`    | `VARCHAR`                             | no              |             |
| `table_name`     | `VARCHAR`                             | no              |             |
| `start_snapshot` | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | no              |             |
| `end_snapshot`   | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | no              |             |

The schema of the table returned by the function is equivalent to that of the table `table_name`.

### `ducklake_table_deletions`

The `ducklake_table_deletions` function returns the rows deleted from a given table between snapshots of given versions or timestamps.
The function has two variants, depending on whether `start_snapshot` and `end_snapshot` have types `BIGINT` or `TIMESTAMP WITH TIME ZONE`.

| Parameter name   | Parameter type                        | Named parameter | Description |
| ---------------- | ------------------------------------- | --------------- | ----------- |
| `catalog`        | `VARCHAR`                             | no              |             |
| `schema_name`    | `VARCHAR`                             | no              |             |
| `table_name`     | `VARCHAR`                             | no              |             |
| `start_snapshot` | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | no              |             |
| `end_snapshot`   | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | no              |             |

The schema of the table returned by the function is equivalent to that of the table `table_name`.

### `ducklake_table_changes`

The `ducklake_table_changes` function returns the rows changed in a given table between snapshots of given versions or timestamps.
The function has two variants, depending on whether `start_snapshot` and `end_snapshot` have types `BIGINT` or `TIMESTAMP WITH TIME ZONE`.

| Parameter name   | Parameter type                        | Named parameter | Description |
| ---------------- | ------------------------------------- | --------------- | ----------- |
| `catalog`        | `VARCHAR`                             | no              |             |
| `schema_name`    | `VARCHAR`                             | no              |             |
| `table_name`     | `VARCHAR`                             | no              |             |
| `start_snapshot` | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | no              |             |
| `end_snapshot`   | `BIGINT` / `TIMESTAMP WITH TIME ZONE` | no              |             |

The schema of the table returned by the function contains the following three columns plus the schema of the table `table_name`.

| Column name   | Column type | Description                              |
| ------------- | ----------- | ---------------------------------------- |
| `snapshot_id` | `BIGINT`    |                                          |
| `rowid`       | `BIGINT`    |                                          |
| `change_type` | `VARCHAR`   | The type of change: `insert` or `delete` |

## Commands

### `ducklake_cleanup_old_files`

The `ducklake_cleanup_old_files` function cleans up old files in the DuckLake denoted by `catalog`.
Upon success, it returns a table with a single column (`Success`) and 0 rows.

| Parameter name | Parameter type             | Named parameter | Description |
| -------------- | -------------------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`                  | no              |             |
| `cleanup_all`  | `BOOLEAN`                  | yes             |             |
| `dry_run`      | `BOOLEAN`                  | yes             |             |
| `older_than`   | `TIMESTAMP WITH TIME ZONE` | yes             |             |

### `ducklake_expire_snapshots`

The `ducklake_expire_snapshots` function expires snapshots with the versions specified by the `versions` parameter or the ones older than the `older_than` parameter.
Upon success, it returns a table with a single column (`Success`) and 0 rows.

| Parameter name | Parameter type             | Named parameter | Description |
| -------------- | -------------------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`                  | no              |             |
| `versions`     | `UBIGINT[]`                | yes             |             |
| `older_than`   | `TIMESTAMP WITH TIME ZONE` | yes             |             |

### `ducklake_merge_adjacent_files`

The `ducklake_merge_adjacent_files` function merges adjacent files in the storage.
Upon success, it returns a table with a single column (`Success`) and 0 rows.

| Parameter name | Parameter type | Named parameter | Description |
| -------------- | -------------- | --------------- | ----------- |
| `catalog`      | `VARCHAR`      | no              |             |

## Compatibility Matrix

The DuckLake specification and the `ducklake` DuckDB extension are currently released together. This may not be the case in the future, where the specification and the extension may have different release cadences. It can also be the case that the extension needs a DuckDB core update, therefore DuckDB versions are also included in this compatibility matrix.

| DuckDB | DuckLake Extension | DuckLake Spec |
|--------|--------------------|---------------|
| 1.4.x  | 0.3                | 0.3           |
| 1.3.x  | 0.2                | 0.2           |
| 1.3.x  | 0.1                | 0.1           |
