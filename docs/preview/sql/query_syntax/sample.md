---
layout: docu
railroad: query_syntax/sample.js
tested: true
title: SAMPLE Clause
---

The `SAMPLE` clause allows you to run the query on a sample from the base table. This can significantly speed up processing of queries, at the expense of accuracy in the result. Samples can also be used to quickly see a snapshot of the data when exploring a dataset. The sample clause is applied right after anything in the `FROM` clause (i.e., after any joins, but before the `WHERE` clause or any aggregates). See the [`SAMPLE`]({% link docs/preview/sql/samples.md %}) page for more information.

## Examples

Select a sample of 1% of the addresses table using default (system) sampling:

<!-- test:setup
CREATE TABLE addresses (city VARCHAR, street_name VARCHAR, income INTEGER);
INSERT INTO addresses VALUES
    ('Amsterdam', 'Damrak', 50000), ('Amsterdam', 'Kalverstraat', 65000),
    ('Rotterdam', 'Coolsingel', 45000), ('Rotterdam', 'Coolsingel', 55000);
-->

```sql
SELECT *
FROM addresses
USING SAMPLE 1%;
```

Select a sample of 1% of the addresses table using bernoulli sampling:

```sql
SELECT *
FROM addresses
USING SAMPLE 1% (bernoulli);
```

Select a sample of 10 rows from the subquery:

```sql
SELECT *
FROM (SELECT * FROM addresses)
USING SAMPLE 10 ROWS;
```

## Syntax

<div id="rrdiagram"></div>

## Placement in a Query

The statement above that the sample clause is "applied right after anything in the `FROM` clause" describes the *logical* point at which sampling takes effect, not where the clause is written. Syntactically, the `USING SAMPLE` clause appears at the end of the `SELECT` statement body: after the `WHERE`, `GROUP BY`, `HAVING`, and `QUALIFY` clauses, and before `ORDER BY` and `LIMIT`. So it is written after grouping and filtering, but it is *applied* to the result of the `FROM` clause before those operations run.

To sample an individual table expression rather than the result of the entire `FROM` clause, use the `TABLESAMPLE` clause, which is written directly after the table expression it applies to. See [Table Samples]({% link docs/preview/sql/samples.md %}#table-samples).
