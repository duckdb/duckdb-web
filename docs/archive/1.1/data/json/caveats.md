---
layout: docu
title: Caveats
---

## Equality Comparison

> Warning Currently, equality comparison of JSON files can differ based on the context. In some cases, it is based on raw text comparison, while in other cases, it uses logical content comparison.

The following query returns true for all fields:

```sql
SELECT
    a != b, -- Space is part of physical JSON content. Despite equal logical content, values are treated as not equal.
    c != d, -- Same.
    c[0] = d[0], -- Equality because space was removed from physical content of fields:
    a = c[0], -- Indeed, field is equal to empty list without space...
    b != c[0], -- ... but different from empty list with space.
FROM (
    SELECT
        '[]'::JSON AS a,
        '[ ]'::JSON AS b,
        '[[]]'::JSON AS c,
        '[[ ]]'::JSON AS d
    );
```

<div class="monospace_table"></div>

| (a != b) | (c != d) | (c[0] = d[0]) | (a = c[0]) | (b != c[0]) |
|----------|----------|---------------|------------|-------------|
| true     | true     | true          | true       | true        |