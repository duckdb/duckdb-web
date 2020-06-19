---
layout: docu
title: Subqueries
selected: Documentation/Expressions/Subqueries
expanded: Expressions
railroad: expressions/subqueries.js
---
## Scalar Subquery
<div id="rrdiagram1"></div>

Scalar subqueries are subqueries that return a single value. They can be used anywhere where a regular expression can be used. If a scalar subquery returns more than a single value, the first value returned will be used.

Consider the following table:
### Grades
| grade | course |
|---:|:---|
| 7 | Math |
| 9 | Math |
| 8 | CS |

```sql
CREATE TABLE grades(grade INTEGER, course VARCHAR);
INSERT INTO grades VALUES (7, 'Math'), (9, 'Math'), (8, 'CS');
```

We can run the following query to obtain the minimum grade:

```sql
SELECT MIN(grade) FROM grades;
-- {7}
```

By using a scalar subquery in the `WHERE` clause, we can figure out for which course this grade was obtained:

```sql
SELECT course FROM grades WHERE grade = (SELECT MIN(grade) FROM grades);
-- {Math}
```

## Exists
<div id="rrdiagram2"></div>

The EXISTS operator is used to test for the existence of any row inside the subquery. It returns either true when the subquery returns one or more records, or false otherwise. The exists clause is generally the most useful as a *correlated* subquery. However, it can be used as an uncorrelated subquery as well.

For example, we can use it to figure out if there are any grades present for a given course:

```sql
SELECT EXISTS(SELECT * FROM grades WHERE course='Math');
-- {true}

SELECT EXISTS(SELECT * FROM grades WHERE course='History');
-- false
```

## In Clause
<div id="rrdiagram3"></div>

The IN clause checks containment of the left expression inside the result defined by the subquery or the set of expressions on the right side. The IN clause returns true if the expression is present in the RHS, false if the expression is not in the RHS and the RHS has no `NULL` values, or `NULL` if the expression is not in the RHS and the RHS has `NULL` values.

We can use the IN clause in a similar manner as we used the EXISTS clause:

```sql
SELECT 'Math' IN (SELECT course FROM grades);
-- true

```

## Correlated Subqueries
All the subqueries presented here so far have been **uncorrelated** subqueries, where the subqueries themselves are entirely self-contained and can be run without the parent query. There exists a second type of subqueries called **correlated** subqueries. For correlated subqueries, the subquery uses values from the parent subquery.

Conceptually, the subqueries are run once for every single row in the parent query. Perhaps a simple way of envisioning this is that the correlated subquery is a **function** that is applied to every row in the source data set.

For example, suppose that we want to find the minimum grade for every course. We could do that as follows:

```sql
SELECT *
FROM grades grades_parent
WHERE grade=
    (SELECT MIN(grade)
     FROM grades
     WHERE grades.course=grades_parent.course);
-- {7, Math}, {8, CS}
```

The subquery uses a column from the parent query (`grades_parent.course`). Conceptually, we can see the subquery as a function where the correlated column is a parameter to that function:

```sql
SELECT MIN(grade) FROM grades WHERE course=?;
```

Now when we execute this function for each of the rows, we can see that for `Math` this will return `7`, and for `CS` it will return `8`. We then compare it against the grade for that actual row. As a result, the row `(Math, 9)` will be filtered out, as `9 <> 7`.
