---
layout: docu
title: GROUPING SETS
selected: Documentation/SQL/Query Syntax/Grouping Sets
expanded: SQL
railroad: query_syntax/groupby.js
---
`GROUPING SETS`, `ROLLUP` and `CUBE` can be used in the `GROUP BY` clause to perform a grouping over multiple dimensions within the same query. 
Note that this syntax is not compatible with [`GROUP BY ALL`](./groupby#group-by-all).

### Examples

```sql
-- compute the average income along the provided four different dimensions
-- () signifies the empty set (i.e. computing an ungrouped aggregate)
SELECT city, street_name, AVG(income)
FROM addresses
GROUP BY GROUPING SETS ((city, street_name), (city), (street_name), ());
-- compute the average income along the same dimensions
SELECT city, street_name, AVG(income)
FROM addresses
GROUP BY CUBE (city, street_name);
-- compute the average income along the dimensions (city, street_name), (city) and ()
SELECT city, street_name, AVG(income)
FROM addresses
GROUP BY ROLLUP (city, street_name);
```

### Description
`GROUPING SETS` perform the same aggregate across different `GROUP BY clauses` in a single query.

```sql
CREATE TABLE students (course VARCHAR, type VARCHAR);
INSERT INTO students (course, type) VALUES ('CS', 'Bachelor'), ('CS', 'Bachelor'), ('CS', 'PhD'), ('Math', 'Masters'), ('CS', NULL), ('CS', NULL), ('Math', NULL);
```

```sql
SELECT course, type, COUNT(*)
FROM students
GROUP BY GROUPING SETS ((course, type), course, type, ());
```
```
┌────────┬──────────┬──────────────┐
│ course │   type   │ count_star() │
├────────┼──────────┼──────────────┤
│ CS     │ Bachelor │ 2            │
│ CS     │ PhD      │ 1            │
│ Math   │ Masters  │ 1            │
│ CS     │ NULL     │ 2            │
│ Math   │ NULL     │ 1            │
│ CS     │ NULL     │ 5            │
│ Math   │ NULL     │ 2            │
│ NULL   │ Bachelor │ 2            │
│ NULL   │ PhD      │ 1            │
│ NULL   │ Masters  │ 1            │
│ NULL   │ NULL     │ 3            │
│ NULL   │ NULL     │ 7            │
└────────┴──────────┴──────────────┘
```

In the above query, we group across four different sets: `course, type`, `course`, `type` and `()` (the empty group). The result contains `NULL` for a group which is not in the grouping set for the result, i.e. the above query is equivalent to the following UNION statement:

```sql
-- group by course, type
SELECT course, type, COUNT(*)
FROM students
GROUP BY course, type
UNION ALL
-- group by type
SELECT NULL AS course, type, COUNT(*)
FROM students
GROUP BY type
UNION ALL
-- group by course
SELECT course, NULL AS type, COUNT(*)
FROM students
GROUP BY course
UNION ALL
-- group by nothing
SELECT NULL AS course, NULL AS type, COUNT(*)
FROM students
```

`CUBE` and `ROLLUP` are syntactic sugar to easily produce commonly used grouping sets.

The `ROLLUP` clause will produce all "sub-groups" of a grouping set, e.g. `ROLLUP (country, city, zip)` produces the grouping sets `(country, city, zip), (country, city), (country), ()`. This can be useful for producing different levels of detail of a group by clause. This produces `n+1` grouping sets where n is the amount of terms in the `ROLLUP` clause.

`CUBE` produces grouping sets for all combinations of the inputs, e.g. `CUBE (country, city, zip)` will produce `(country, city, zip), (country, city), (country, zip), (city, zip), (country), (city), (zip), ()`. This produces `2^n` grouping sets.

`GROUPING` (alias `GROUPING_ID`) is a special aggregate function that can be used in combination with grouping sets. The `GROUPING` function takes as parameters a group, and returns 0 if the group is included in the grouping for that row, or 1 otherwise. This is primarily useful because the grouping columns by which we do not aggregate return NULL, which is ambiguous with groups that are actually the value `NULL`. The `GROUPING` (or `GROUPING_ID`) function can be used to distinguish these two cases.

### Syntax
<div id="rrdiagram"></div>
