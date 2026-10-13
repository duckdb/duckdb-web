---
layout: docu
title: CREATE TRIGGER Statement
---

> New The `CREATE TRIGGER` feature is introduced in DuckDB 2.0.

The `CREATE TRIGGER` statement registers a trigger: a set of SQL statements that run automatically in response to `INSERT`, `UPDATE`, or `DELETE` events on a table.

## Examples

Record every statement that modifies a table in an audit table using a statement-level `AFTER` trigger. The `REFERENCING OLD TABLE` and `NEW TABLE` clauses expose the rows before and after the change as transition tables:

```sql
CREATE TABLE target (id INTEGER, val INTEGER);
CREATE TABLE audit (id INTEGER, old_val INTEGER, new_val INTEGER);

CREATE TRIGGER trg_audit AFTER UPDATE ON target
REFERENCING OLD TABLE AS o NEW TABLE AS n
FOR EACH STATEMENT
    INSERT INTO audit
    SELECT n.id, o.val, n.val
    FROM o
    JOIN n ON o.id = n.id;

INSERT INTO target VALUES (1, 10), (2, 20);
UPDATE target SET val = val * 10 WHERE id <= 2;
SELECT * FROM audit;
```

|   id | old_val | new_val |
| ---: | ------: | ------: |
|    1 |      10 |     100 |
|    2 |      20 |     200 |

Fire a trigger once per affected row with a row-level `AFTER` trigger. Row-level triggers refer to the affected row through the `NEW` and `OLD` qualifiers:

```sql
CREATE TABLE t (id INTEGER);
CREATE TABLE log (id INTEGER);

CREATE TRIGGER trg_log AFTER INSERT ON t
FOR EACH ROW
    INSERT INTO log VALUES (NEW.id);

INSERT INTO t VALUES (1), (2);
SELECT * FROM log;
```

Restrict a trigger to changes of specific columns with `UPDATE OF`:

```sql
CREATE TRIGGER trg_price AFTER UPDATE OF price ON products
FOR EACH STATEMENT
    INSERT INTO price_changes DEFAULT VALUES;
```

Drop a trigger:

```sql
DROP TRIGGER trg_audit ON target;
```

## Syntax

```sql
CREATE [OR REPLACE] TRIGGER ⟨name⟩
    { BEFORE | AFTER } { INSERT | UPDATE [OF ⟨column⟩, ...] | DELETE } ON ⟨table⟩
    [REFERENCING { OLD | NEW } TABLE AS ⟨alias⟩ [{ OLD | NEW } TABLE AS ⟨alias⟩]]
    FOR EACH { ROW | STATEMENT }
    ⟨triggered_statement⟩;
```

The triggered statement is a single SQL statement, typically a data modification statement such as `INSERT`, `UPDATE`, or `DELETE`.

### Timing

* `BEFORE` triggers run before the triggering statement is applied.
* `AFTER` triggers run after the triggering statement is applied.

### Granularity

* `FOR EACH ROW` fires the trigger once for every row affected by the statement. The triggered statement can refer to the affected row through `NEW` (for `INSERT` and `UPDATE`) and `OLD` (for `UPDATE` and `DELETE`).
* `FOR EACH STATEMENT` fires the trigger once per statement, regardless of how many rows are affected. Use `REFERENCING OLD TABLE` and `NEW TABLE` to access the affected rows as transition tables.

### Transition Tables

Statement-level triggers can expose the rows involved in the change as transition tables:

* `NEW TABLE` contains the inserted or post-update rows and is available for `INSERT` and `UPDATE`.
* `OLD TABLE` contains the deleted or pre-update rows and is available for `UPDATE` and `DELETE`.

### Multiple Triggers

A table can have multiple triggers for the same event. They fire in the order in which they were created.

## Inspecting Triggers

The triggers defined in the catalog can be listed with the [`duckdb_triggers()` function]({% link docs/preview/sql/meta/duckdb_table_functions.md %}):

```sql
SELECT trigger_name, table_name, action_timing, event_manipulation, for_each
FROM duckdb_triggers();
```

## Dropping Triggers

A trigger is dropped with `DROP TRIGGER`. The table the trigger is attached to must be specified:

```sql
DROP TRIGGER ⟨name⟩ ON ⟨table⟩;
```

## Limitations

The current preview build has the following limitations, which may be lifted before the v2.0 release:

* `BEFORE ... FOR EACH ROW` triggers are not yet supported.
* `UPDATE ... FOR EACH ROW` triggers are not yet supported.
* `INSTEAD OF` triggers and triggers on views are not supported; a trigger requires a base table.
* Temporary triggers are not supported.
