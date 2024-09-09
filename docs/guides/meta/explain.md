---
layout: docu
title: "EXPLAIN: Inspect Query Plans"
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

EXPLAIN ANALYZE
    SELECT name
    FROM students
    JOIN exams USING (sid)
    WHERE name LIKE 'Ma%';
```

```text
┌─────────────────────────────┐
│┌───────────────────────────┐│
││       Physical Plan       ││
│└───────────────────────────┘│
└─────────────────────────────┘
┌───────────────────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            name           │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         HASH_JOIN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           INNER           │
│         sid = sid         ├──────────────┐
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │
│           EC: 1           │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││           FILTER          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           exams           ││     prefix(name, 'Ma')    │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            sid            ││           EC: 1           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││                           │
│           EC: 3           ││                           │
└───────────────────────────┘└─────────────┬─────────────┘
                             ┌─────────────┴─────────────┐
                             │         SEQ_SCAN          │
                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
                             │          students         │
                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
                             │            sid            │
                             │            name           │
                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
                             │ Filters: name>=Ma AND name│
                             │  <Mb AND name IS NOT NULL │
                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
                             │           EC: 1           │
                             └───────────────────────────┘
```

Note that the query is not actually executed – therefore, we can only see the estimated cardinality (`EC`) for each operator, which is calculated by using the statistics of the base tables and applying heuristics for each operator.

## Additional Explain Settings
The `EXPLAIN` statement supports additional settings that can be used to control the output. The following settings are available:

The default setting. Only shows the physical plan.
```sql
PRAGMA explain_output = 'physical_only';
```

Shows only the optimized plan.
```sql
PRAGMA explain_output = 'optimized_only';
```

Shows both the physical and optimized plans.
```sql
PRAGMA explain_output = 'all';
```

## See Also

For more information, see the [Profiling page]({% link docs/dev/profiling.md %}).