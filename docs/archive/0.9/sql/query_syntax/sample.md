---
layout: docu
railroad: query_syntax/sample.js
redirect_from:
- docs/archive/0.9.2/sql/query_syntax/sample
- docs/archive/0.9.1/sql/query_syntax/sample
title: SAMPLE Clause
---

`The SAMPLE clause` allows you to run the query on a sample from the base table. This can significantly speed up processing of queries, at the expense of accuracy in the result. Samples can also be used to quickly see a snapshot of the data when exploring a data set. The sample clause is applied right after anything in the `FROM` clause (i.e., after any joins, but before the where clause or any aggregates). See the [sample](../../sql/samples) page for more information.

## Examples

```sql
-- select a sample of 1% of the addresses table using default (system) sampling
SELECT *
FROM addresses
USING SAMPLE 1%;
-- select a sample of 1% of the addresses table using bernoulli sampling
SELECT *
FROM addresses
USING SAMPLE 1% (BERNOULLI);
-- select a sample of 10 rows from the subquery
SELECT *
FROM (SELECT * FROM addresses)
USING SAMPLE 10 ROWS;
```

## Syntax

<div id="rrdiagram"></div>