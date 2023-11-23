---
layout: docu
title: Rules for Case Sensitivity
---

## Keywords and Function Names

SQL keywords and function names are case-insensitive in DuckDB.

### Examples

The following two queries are equivalent:

<!-- 
    syntax highlighting is omitted here on purpose:
    our SQL formatter only picks up uppercase keywords and lowercase functions,
    so applying it would be confusing
-->
```text
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
CREATE TABLE t1(idfield INT, x INT);
CREATE TABLE t2(IdField INT, y INT);
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
