---
layout: post
title: "Iceberg Extension Improvements in DuckDB 2.0 and Later"
authors:
  - Geertjan Wielenga
excerpt: "DuckDB 2.0 and 2.0.1 bring substantial improvements to Iceberg workflows. DuckDB 2.0 addresses security and compatibility gaps, while 2.0.1 adds new operational features, performance optimizations, and correctness improvements for production deployments."
tag: release
---

The Iceberg extension in DuckDB 2.0 and 2.0.1 includes significant security fixes, new capabilities, and performance improvements. DuckDB 2.0 (October 19) established critical correctness and security foundations, while DuckDB 2.0.1 (November 24) expanded operational capabilities and optimization.

## DuckDB 2.0: Security and Compatibility Foundations

DuckDB 2.0 established critical security and correctness foundations for Iceberg workflows, particularly for cloud deployments where credential handling and cross-engine compatibility matter.

### TLS Protection with Vended S3 Credentials

Cloud environments use temporary credentials (vended by IAM services) for S3 access, often paired with specific S3 endpoint configurations. DuckDB 2.0 ensures TLS remains enabled when using path-style S3 credentials, regardless of credential type or endpoint configuration. A silently disabled TLS connection doesn't fail the query. It silently exposes data in transit.

- **Contributor:** [@rutb327](https://github.com/rutb327)
- **Reference:** [duckdb-iceberg#1527](https://github.com/duckdb/duckdb-iceberg/pull/1527)

### Iceberg Data Rewrite Compatibility

The `iceberg_rewrite_data_files` function now returns column names matching Spark's output exactly, enabling seamless integration when both engines operate on the same tables.

```sql
-- Output now matches Spark's format exactly
SELECT * FROM iceberg_rewrite_data_files('my_table');
```

- **Contributor:** [@The-Alchemist](https://github.com/The-Alchemist)
- **Reference:** [duckdb-iceberg#1597](https://github.com/duckdb/duckdb-iceberg/pull/1597)

## DuckDB 2.0.1: Enhanced Operations and Performance

DuckDB 2.0.1 expands Iceberg's capabilities with new operational features, production-focused correctness improvements, and significant performance optimizations for large-scale deployments.

### New Features and Capabilities

DuckDB 2.0.1 introduces two major new capabilities for Iceberg tables: column reordering and efficient update operations on V2 format tables. Table comments support was added in DuckDB 2.0.

#### Move Column Operation

DuckDB 2.0.1 adds `iceberg_move_column()`, allowing you to reorder columns or relocate struct fields within an Iceberg table. The operation respects Iceberg's field IDs for compatibility with other engines.

```sql
-- Reorder columns in an existing Iceberg table
SELECT * FROM iceberg_move_column('my_table', 'column_name', 'after', 'reference_column');
```

- **Contributor:** [@xiaoxuandev](https://github.com/xiaoxuandev)
- **Reference:** [duckdb-iceberg#1801](https://github.com/duckdb/duckdb-iceberg/pull/1801)

#### Table Comments

Iceberg table comments are exposed in DuckDB 2.0 and later, allowing you to document tables and retrieve that metadata through DuckDB queries. Use `COMMENT ON TABLE` to set documentation, then query the information schema to retrieve it.

```sql
-- Set a comment on an Iceberg table
COMMENT ON TABLE my_iceberg_table IS 'Production events from the last 90 days. Updated daily.';

-- Retrieve the comment through the information schema
SELECT table_name, table_comment FROM information_schema.tables 
WHERE table_schema = 'my_schema' AND table_name = 'my_iceberg_table';
```

- **Contributor:** [@vitaliytv](https://github.com/vitaliytv)
- **Reference:** [duckdb-iceberg#1799](https://github.com/duckdb/duckdb-iceberg/pull/1799)

#### Copy-on-Write UPDATE Support

DuckDB 2.0.1 adds support for copy-on-write UPDATE operations on Iceberg V2 tables, enabling efficient updates without full table rewrites while maintaining transaction isolation. Instead of rewriting all affected files, only modified rows are written, leaving unchanged data files in place.

```sql
-- Update rows in an Iceberg V2 table efficiently
UPDATE my_iceberg_table 
SET status = 'processed' 
WHERE created_date < current_date - interval '30 days' 
  AND status = 'pending';

-- Only changed rows are written; unchanged files remain in place
```

- **Contributor:** [@dor-bernstein](https://github.com/dor-bernstein)
- **Reference:** [duckdb-iceberg#1662](https://github.com/duckdb/duckdb-iceberg/pull/1662)

### Correctness and Reliability

DuckDB 2.0.1 strengthens error handling and data safety with improved bounds checking, better error reporting, and stricter validation of table metadata. These fixes prevent silent data issues and provide clear diagnostics when metadata corruption occurs.

#### Deletion Vector Bounds Checking

DuckDB 2.0.1 adds bounds checking for deletion vector blob reads to prevent out-of-bounds reads. The fix also improves error reporting to distinguish between actual bitmap read failures and deletion vector blobs that are too small, surfacing these as corruption errors rather than crashes. If a table's deletion vectors are corrupted, you'll now receive a clear error message instead of a silent crash.

- **Contributor:** [@lliangyu-lin](https://github.com/lliangyu-lin)
- **Reference:** [duckdb-iceberg#1775](https://github.com/duckdb/duckdb-iceberg/pull/1775)

#### Manifest Content Error Reporting

Instead of crashing when encountering invalid manifest content, DuckDB 2.0.1 now reports these issues as proper error messages. If a manifest file is malformed or incomplete, DuckDB surfaces this as a clear error so operations fail gracefully rather than with an internal crash, enabling you to identify and fix metadata issues.

- **Contributor:** [@lliangyu-lin](https://github.com/lliangyu-lin)
- **Reference:** [duckdb-iceberg#1781](https://github.com/duckdb/duckdb-iceberg/pull/1781)

#### Decimal Width Validation

Iceberg tables support decimals up to 38 digits of precision. DuckDB 2.0.1 explicitly validates and rejects decimals wider than Iceberg's limit, preventing silent data loss or truncation. If you attempt to create a column with a decimal wider than 38 digits, the operation now fails with a clear error rather than silently truncating or corrupting data.

```sql
-- This now fails with a clear error instead of silent truncation
CREATE TABLE my_iceberg_table (
    amount DECIMAL(50, 2)  -- Error: exceeds Iceberg's 38-digit limit
);

-- Use this instead
CREATE TABLE my_iceberg_table (
    amount DECIMAL(38, 2)  -- Valid: within Iceberg's limit
);
```

- **Contributor:** [@h4nsmuller](https://github.com/h4nsmuller)
- **Reference:** [duckdb-iceberg#1817](https://github.com/duckdb/duckdb-iceberg/pull/1817)

#### Transaction and Concurrency Improvements

Data rewrite operations now support transactions, ensuring consistency in multi-statement workflows. Concurrent table updates are properly locked to prevent metadata corruption. This means you can safely nest data rewrites within larger transactions and rely on all-or-nothing semantics.

```sql
-- Data rewrites now work safely within transactions
BEGIN TRANSACTION;
  UPDATE my_table SET status = 'archived' WHERE year < 2023;
  CALL iceberg_rewrite_data_files('my_table', {'target_file_size': '128MB'});
COMMIT;
-- Either both succeed or both roll back. No partial state.
```

- **Contributors:** [@themisvaltinos](https://github.com/themisvaltinos), [@xiaoxuandev](https://github.com/xiaoxuandev), [@The-Alchemist](https://github.com/The-Alchemist), [@Richard-Durkee](https://github.com/Richard-Durkee)
- **References:** [#1771](https://github.com/duckdb/duckdb-iceberg/pull/1771), [#1773](https://github.com/duckdb/duckdb-iceberg/pull/1773), [#1596](https://github.com/duckdb/duckdb-iceberg/pull/1596), [#1678](https://github.com/duckdb/duckdb-iceberg/pull/1678)

### Performance Optimizations

DuckDB 2.0.1 includes substantial optimizations for query planning and execution, reducing I/O, planning time, and CPU overhead for large-scale workloads.

#### Manifest Filtering

DuckDB 2.0.1 skips manifests without live files during planning, reducing unnecessary I/O and planning time for tables with many snapshots.

- **Contributor:** [@elpetrak](https://github.com/elpetrak)
- **Reference:** [duckdb-iceberg#1769](https://github.com/duckdb/duckdb-iceberg/pull/1769)

#### Statistics-Driven Scan Planning

Iceberg statistics are now used to populate distinct value counts in DuckDB's `iceberg_scan`, enabling the optimizer to make better decisions about query execution. When Iceberg tables store statistics about cardinality and distinct values, DuckDB now uses this information during planning, resulting in better join orders and aggregation strategies.

- **Contributor:** [@rutb327](https://github.com/rutb327)
- **Reference:** [duckdb-iceberg#1772](https://github.com/duckdb/duckdb-iceberg/pull/1772)

#### ORDER BY LIMIT Optimization with NaN Handling

The ORDER BY LIMIT scan optimization now correctly handles NaN values, preventing incorrect pruning when sorting over data files containing NaN.

- **Contributor:** [@mustafahasankhan](https://github.com/mustafahasankhan)
- **Reference:** [duckdb-iceberg#1779](https://github.com/duckdb/duckdb-iceberg/pull/1779)

#### Parallel Deletion Vector Reads

Deletion vector files are now read in parallel, reducing query latency when scanning tables with many deleted rows.

- **Contributor:** [@xiaoxuandev](https://github.com/xiaoxuandev)
- **Reference:** [duckdb-iceberg#1766](https://github.com/duckdb/duckdb-iceberg/pull/1766)

#### Copy-on-Write DELETE Optimization

Constant filenames in copy-on-write DELETE operations are now looked up once per chunk rather than per row, significantly reducing CPU overhead for large bulk deletes.

- **Contributor:** [@elpetrak](https://github.com/elpetrak)
- **Reference:** [duckdb-iceberg#1778](https://github.com/duckdb/duckdb-iceberg/pull/1778)

#### Row Lineage Prepared Statements

Iceberg row lineage scans now support prepared statements, allowing efficient repeated scans with different parameters. This is useful for data lineage tracking and audit queries that need to run repeatedly with different input values.

```sql
-- Prepare a row lineage scan to reuse efficiently
PREPARE get_lineage AS SELECT * FROM iceberg_lineage('my_table') WHERE row_id = ?;

-- Execute with different row IDs without re-planning
EXECUTE get_lineage(12345);
EXECUTE get_lineage(67890);
```

- **Contributor:** [@rutb327](https://github.com/rutb327)
- **Reference:** [duckdb-iceberg#1797](https://github.com/duckdb/duckdb-iceberg/pull/1797)

## Infrastructure and Metadata Handling

DuckDB 2.0.1 also improves handling of Iceberg metadata:

- **Manifest block ordering** now preserves row IDs correctly across blocks ([#1765](https://github.com/duckdb/duckdb-iceberg/pull/1765) by [@lliangyu-lin](https://github.com/lliangyu-lin))
- **Field ID preservation** in table replacement operations ([#1767](https://github.com/duckdb/duckdb-iceberg/pull/1767) by [@themisvaltinos](https://github.com/themisvaltinos))
- **Column field ID matching** when moving columns ([#1801](https://github.com/duckdb/duckdb-iceberg/pull/1801) by [@xiaoxuandev](https://github.com/xiaoxuandev))
- **Position delete handling** improvements for accurate file-scoped deletes ([#1762](https://github.com/duckdb/duckdb-iceberg/pull/1762) by [@Tishj](https://github.com/Tishj))

## Upgrading

The Iceberg extension is included with DuckDB and receives updates with each release. DuckDB 2.0 addresses critical security and compatibility issues. DuckDB 2.0.1 adds operational capabilities and performance improvements. If you're deploying DuckDB with Iceberg tables in production, upgrading to 2.0.1 or later is recommended.

To upgrade, download DuckDB 2.0.0 or later from [duckdb.org/docs/installation](https://duckdb.org/docs/installation). Then try the improvements with sample Iceberg data. After downloading and extracting [iceberg_data.zip](https://duckdb.org/data/iceberg_data.zip):

```sql
INSTALL iceberg FROM core;
LOAD iceberg;

-- Query the sample TPC-H lineitem Iceberg table
SELECT COUNT(*), SUM(l_extendedprice) 
FROM iceberg_scan('/data/iceberg/lineitem_iceberg', allow_moved_paths = true)
WHERE l_shipdate >= '1994-01-01';
```

```text
┌──────────────┬──────────────────────┐
│ count_star() │ sum(l_extendedprice) │
│    int64     │    decimal(38,2)     │
├──────────────┼──────────────────────┤
│        37370 │        1522015146.33 │
└──────────────┴──────────────────────┘
```

```sql
-- DuckDB 2.0 and later: Table comments now supported
CREATE TABLE my_iceberg_table AS 
  SELECT * FROM iceberg_scan('/data/iceberg/lineitem_iceberg', allow_moved_paths = true);

-- Add a comment to document the table
COMMENT ON TABLE my_iceberg_table IS 'Production Iceberg data. Updated daily.';

-- Retrieve table comments
SELECT table_name, table_comment 
FROM information_schema.tables 
WHERE table_name = 'my_iceberg_table';
```

```text
┌──────────────────┬─────────────────────────────────────────┐
│    table_name    │              TABLE_COMMENT              │
│     varchar      │                 varchar                 │
├──────────────────┼─────────────────────────────────────────┤
│ my_iceberg_table │ Production Iceberg data. Updated daily. │
└──────────────────┴─────────────────────────────────────────┘
```

For production Iceberg workflows with cloud catalogs (Amazon S3 Tables, Nessie, etc.), see the [Iceberg catalogs documentation]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}).

## Further Reading

- [DuckDB Iceberg extension documentation]({% link docs/2.0/core_extensions/iceberg/overview.md %})
- [Inside an Iceberg Table]({% post_url 2026-10-13-inside-iceberg-table %})
- [Announcing DuckDB 2.0](https://duckdb.org/2026/11/15/announcing-duckdb-20)
- [Announcing DuckDB 2.0.1](https://duckdb.org/2026/11/20/announcing-duckdb-201)
