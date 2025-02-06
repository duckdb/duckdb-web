---
layout: docu
railroad: query_syntax/sample.js
title: SAMPLE Clause
---

The `SAMPLE` clause allows you to run the query on a sample from the base table. This can significantly speed up processing of queries, at the expense of accuracy in the result. Samples can also be used to quickly see a snapshot of the data when exploring a data set. The sample clause is applied right after anything in the `FROM` clause (i.e., after any joins, but before the `WHERE` clause or any aggregates). See the [`SAMPLE`]({% link docs/archive/1.1/sql/samples.md %}) page for more information.

## Examples

Select a sample of 1% of the addresses table using default (system) sampling:

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