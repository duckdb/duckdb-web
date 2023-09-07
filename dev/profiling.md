---
layout: docu
title: Profiling
---

Profiling is important to help understand why certain queries exhibit specific performance characteristics. DuckDB contains several built-in features to enable query profiling that will be explained on this page.

For the examples on this page we will use the following example data set:

```sql
CREATE TABLE students(sid INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE exams(cid INTEGER, sid INTEGER, grade INTEGER, PRIMARY KEY(cid, sid));

INSERT INTO students VALUES (1, 'Mark'), (2, 'Hannes'), (3, 'Pedro');
INSERT INTO exams VALUES (1, 1, 8), (1, 2, 8), (1, 3, 7), (2, 1, 9), (2, 2, 10);
```

### Explain Statement

The first step to profiling a database engine is figuring out what execution plan the engine is using. The `EXPLAIN` statement allows you to peek into the query plan and see what is going on under the hood.

The `EXPLAIN` statement displays the physical plan, i.e., the query plan that will get executed.

To demonstrate, see the below example:

```sql
CREATE TABLE students(name VARCHAR, sid INT);
CREATE TABLE exams(eid INT, subject VARCHAR, sid INT);
INSERT INTO students VALUES ('Mark', 1), ('Joe', 2), ('Matthew', 3);
INSERT INTO exams VALUES (10, 'Physics', 1), (20, 'Chemistry', 2), (30, 'Literature', 3);
EXPLAIN SELECT name FROM students JOIN exams USING (sid) WHERE name LIKE 'Ma%';
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

### Run-Time Profiling

The query plan helps understand the performance characteristics of the system. However, often it is also necessary to look at the performance numbers of individual operators and the cardinalities that pass through them. For this, you can create a query-profile graph.

To create the query graphs it is first necessary to gather the necessary data by running the query. In order to do that, we must first enable the run-time profiling. This can be done by prefixing the query with `EXPLAIN ANALYZE`:

```sql
EXPLAIN ANALYZE SELECT name FROM students JOIN exams USING (sid) WHERE name LIKE 'Ma%';
```

```text
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││        Total Time: 0.0008s        ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
┌───────────────────────────┐
│      EXPLAIN_ANALYZE      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             0             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            name           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             2             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         HASH_JOIN         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           INNER           │
│         sid = sid         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ├──────────────┐
│           EC: 1           │              │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │              │
│             2             │              │
│          (0.00s)          │              │
└─────────────┬─────────────┘              │
┌─────────────┴─────────────┐┌─────────────┴─────────────┐
│         SEQ_SCAN          ││           FILTER          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           exams           ││     prefix(name, 'Ma')    │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│            sid            ││           EC: 1           │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│           EC: 3           ││             2             │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ││          (0.00s)          │
│             3             ││                           │
│          (0.00s)          ││                           │
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
                             │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
                             │             2             │
                             │          (0.00s)          │
                             └───────────────────────────┘
```

The output of `EXPLAIN ANALYZE` contains the estimated cardinality (`EC`), the actual cardinality, and the execution time for each operator.

It is also possible to save the query plan to a file, e.g., in JSON format:

```sql
-- All queries performed will be profiled, with output in json format.
-- By default the result is still printed to stdout.
PRAGMA enable_profiling='json';
-- Instead of writing to stdout, write the profiling output to a specific file on disk.
-- This has no effect for `EXPLAIN ANALYZE` queries, which will *always* be
-- returned as query results.
PRAGMA profile_output='/path/to/file.json';
```

> This file is overwritten with each query that is issued. If you want to store the profile output for later it should be copied to a different file.

Now let us run the query that we inspected before:

```sql
SELECT name FROM students JOIN exams USING (sid) WHERE name LIKE 'Ma%';
```

After the query is completed, the JSON file containing the profiling output has been written to the specified file. We can then render the query graph using the Python script, provided we have the `duckdb` python module installed. This script will generate a HTML file and open it in your web browser.

```sql
python scripts/generate_querygraph.py /path/to/file.json
```
