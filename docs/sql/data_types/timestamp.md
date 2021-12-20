---
layout: docu
title: Timestamp Type
selected: Documentation/Data Types/Timestamp
expanded: Data Types
blurb: A timestamp specifies a combination of date (year, month, day) and a time (hour, minute, second, millisecond).
---
| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP` | datetime | time of day (no time zone) |

A timestamp specifies a combination of `DATE` (year, month, day) and a `TIME` (hour, minute, second, millisecond). Timestamps can be created using the `TIMESTAMP` keyword, where the data must be formatted according to the ISO 8601 format (`YYYY-MM-DD hh:mm:ss`).

```sql
-- 11:30 AM at 20 September, 1992
SELECT TIMESTAMP '1992-09-20 11:30:00';
-- 2:30 PM at 20 September, 1992
SELECT TIMESTAMP '1992-09-20 14:30:00';
```

## Functions
See [Timestamp Functions](/docs/sql/functions/timestamp).
