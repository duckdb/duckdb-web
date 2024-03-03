---
layout: docu
redirect_from:
- docs/archive/0.9.2/sql/case_sensitivity
- docs/archive/0.9.1/sql/case_sensitivity
- docs/archive/0.9.0/sql/case_sensitivity
title: Rules for Case Sensitivity
---

## Keywords and Function Names

SQL keywords and function names are case-insensitive in DuckDB.

### Examples

The following two queries are equivalent:

```sql
select COS(Pi()) as CosineOfPi;
SELECT cos(pi()) AS CosineOfPi;
```
```text
┌────────────┐
│ CosineOfPi │
│   double   │
├────────────┤
│       -1.0 │
└────────────┘
```

## Identifiers

Following the convention of the SQL standard, identifiers in DuckDB are case-insensitive.
However, each character's case (uppercase/lowercase) is maintained as entered by the user.

### Examples

The case entered by the user is preserved even if a query uses different cases when referring to the identifier:

```sql
CREATE TABLE CosPi AS SELECT cos(pi()) AS CosineOfPi;
SELECT cosineofpi FROM CosPi;
```
```text
┌────────────┐
│ CosineOfPi │
│   double   │
├────────────┤
│       -1.0 │
└────────────┘
```

In case of a conflict, when the same identifier is spelt with different cases, one will be selected randomly. For example:

```sql
CREATE TABLE t1(idfield int, x int);
CREATE TABLE t2(IdField int, y int);
SELECT * FROM t1 NATURAL JOIN t2;
```

```text
┌─────────┬───────┬───────┐
│ idfield │   x   │   y   │
│  int32  │ int32 │ int32 │
├─────────────────────────┤
│         0 rows          │
└─────────────────────────┘
```