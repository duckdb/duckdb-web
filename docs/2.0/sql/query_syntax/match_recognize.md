---
layout: docu
redirect_from:
- /docs/sql/query_syntax/match_recognize
- /docs/stable/sql/query_syntax/match_recognize
- /docs/current/sql/query_syntax/match_recognize
- /docs/preview/sql/query_syntax/match_recognize
title: MATCH_RECOGNIZE
---

> New This feature was introduced in DuckDB 2.0.

`MATCH_RECOGNIZE` finds sequences of rows that match a pattern, similar to regular expressions over an ordered partition of a table.
It is used for tasks such as detecting trends, sessions, or event sequences in time-series data.

## Syntax

```sql
FROM ⟨table⟩ MATCH_RECOGNIZE (
    [ PARTITION BY ⟨columns⟩ ]
    [ ORDER BY ⟨columns⟩ ]
    [ MEASURES ⟨measure_list⟩ ]
    [ ONE ROW PER MATCH | ALL ROWS PER MATCH ]
    [ AFTER MATCH SKIP PAST LAST ROW | AFTER MATCH SKIP TO NEXT ROW ]
    PATTERN ( ⟨pattern⟩ )
    DEFINE ⟨definitions⟩
)
```

## Example

Detect a price dip followed by a climb within each symbol:

```sql
FROM ticks MATCH_RECOGNIZE (
    PARTITION BY symbol
    ORDER BY ts
    MEASURES
        FIRST(ts) AS started,
        count(*) AS len
    ONE ROW PER MATCH
    AFTER MATCH SKIP PAST LAST ROW
    PATTERN (onset dip+ climb+)
    DEFINE
        dip AS dip.price < PREV(dip.price),
        climb AS climb.price > PREV(climb.price)
);
```

* `PATTERN` names row variables (`onset`, `dip`, `climb`) and uses quantifiers such as `+`.
* `DEFINE` gives a boolean condition for each variable; `PREV()` refers to the previous row of that variable.
* `MEASURES` projects values from the matched rows (for example `FIRST(ts)` or `count(*)`).
* `ONE ROW PER MATCH` returns a single summary row per match; `ALL ROWS PER MATCH` returns every matched row.
* `AFTER MATCH SKIP PAST LAST ROW` continues searching after the end of the current match.

## See Also

* [Pattern Matching]({% link docs/2.0/sql/functions/pattern_matching.md %}) for `LIKE`, `SIMILAR TO`, `GLOB`, and regular expressions on strings
* [Window Functions]({% link docs/2.0/sql/functions/window_functions.md %}) for ordered analytic calculations without pattern matching
