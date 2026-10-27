---
layout: docu
redirect_from:
- /docs/guides/meta/explain
- /docs/stable/guides/meta/explain
- /docs/current/guides/meta/explain
- /docs/lts/guides/meta/explain
- /docs/preview/guides/meta/explain
title: 'EXPLAIN: Inspect Query Plans'
---

```sql
EXPLAIN SELECT * FROM tbl;
```

The `EXPLAIN` statement displays the physical plan, i.e., the query plan that will get executed,
and is enabled by prepending the query with `EXPLAIN`.
The physical plan is a tree of operators that are executed in a specific order to produce the result of the query.
To generate an efficient physical plan, the query optimizer transforms the existing physical plan into a better physical plan.

To demonstrate, see the below example:

```sql
CREATE TABLE students (name VARCHAR, sid INTEGER);
CREATE TABLE exams (eid INTEGER, subject VARCHAR, sid INTEGER);
INSERT INTO students VALUES ('Mark', 1), ('Joe', 2), ('Matthew', 3);
INSERT INTO exams VALUES (10, 'Physics', 1), (20, 'Chemistry', 2), (30, 'Literature', 3);

EXPLAIN
    SELECT name
    FROM students
    JOIN exams USING (sid)
    WHERE name LIKE 'Ma%';
```

```text
╭─ Projection ─────────────╮
│ Projections: name        │
│ ~1 row                   │
╰─────────────┬────────────╯
╭─ Hash Join ─┴────────────╮
│ Join Type: INNER         │
│ Conditions: sid = sid    │
│ ~1 row                   │
╰─────────────┬────────────╯
              ├──────────────────────────────╮
╭─ Seq Scan ──┴────────────╮  ╭─ Seq Scan ───┴──────────────╮
│ Table: memory.main.exams │  │ Table: memory.main.students │
│ Type: Sequential Scan    │  │ Type: Sequential Scan       │
│ Projections: sid         │  │ Projections: sid, name      │
│ ~3 rows                  │  │ Filters: name >= 'Ma'       │
╰──────────────────────────╯  │ ~1 row                      │
                              ╰─────────────────────────────╯
```

Note that the query is not actually executed – therefore, we can only see the estimated cardinality for each operator (shown with a `~` prefix, e.g., `~3 rows`), which is calculated by using the statistics of the base tables and applying heuristics for each operator.

Table scan operators display the fully qualified table name including catalog and schema (e.g., `memory.main.exams`).

## Additional Explain Settings

The `EXPLAIN` statement supports additional settings that can be used to control the output. The following settings are available:

The default setting. Only shows the physical plan.

```sql
SET explain_output = 'physical_only';
```

Shows only the optimized plan.

```sql
SET explain_output = 'optimized_only';
```

Shows both the physical and optimized plans.

```sql
SET explain_output = 'all';
```

## See Also

For more information, see the [”Profiling” page]({% link docs/2.0/dev/profiling.md %}).
