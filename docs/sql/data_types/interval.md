---
layout: docu
title: Interval Type
selected: Documentation/Data Types/Interval
expanded: Data Types
blurb: An interval specifies a period of time measured in units of a specific date part like years, days, seconds, or others.
---

Intervals represent a period of time. This period can be measured in a specific unit or combination of units, for example years, days, or seconds. Intervals are generally used to *modify* timestamps or dates by either adding or substracting them.


| Name | Description |
|:---|:---|
| `INTERVAL` | Period of time |

An `INTERVAL` can be constructed by providing an amount together with a unit.
Intervals can be added or subtracted from `DATE` or `TIMESTAMP` values.

```sql
-- 1 year
SELECT INTERVAL 1 YEAR;
-- add 1 year to a specific date
SELECT DATE '2000-01-01' + INTERVAL 1 YEAR;
-- subtract 1 year from a specific date
SELECT DATE '2000-01-01' - INTERVAL 1 YEAR;
-- construct an interval from a column, instead of a constant
SELECT INTERVAL (i) YEAR FROM range(1, 5) t(i);
-- construct an interval with mixed units
SELECT INTERVAL '1 month 1 day';

-- WARNING: If a decimal value is specified, it will be automatically rounded to an integer
-- To use more precise values, simply use a more granular date part 
-- (In this example use 18 MONTHS instead of 1.5 YEARS)
-- The statement below is equivalent to to_years(CAST(1.5 AS INTEGER))
-- 2 years
SELECT INTERVAL '1.5' YEARS; --WARNING! This returns 2 years!
```

## Details

The interval class represents a period of time using three distinct components: the *month*, *day* and *microsecond*. These three components are required because there is no direct translation between them. For example, a month does not correspond to a fixed amount of days. That depends on *which month is referenced*. February has fewer days than March.

The division into components makes the interval class suitable for adding or subtracting specific time units to a date. For example, we can generate a table with the first day of every month using the following SQL query:

```sql
SELECT DATE '2000-01-01' + INTERVAL (i) MONTH FROM range(12) t(i);
```

## Difference Between Dates

If we subtract two timestamps from one another, we obtain an interval describing the difference between the timestamps with the *days and microseconds* components. For example:

```sql
SELECT TIMESTAMP '2000-02-01 12:00:00' - TIMESTAMP '2000-01-01 11:00:00' AS diff;
┌──────────────────┐
│       diff       │
│     interval     │
├──────────────────┤
│ 31 days 01:00:00 │
└──────────────────┘
```

The `datediff` function can be used to obtain the difference between two dates for a specific unit.

```sql
SELECT datediff('month', TIMESTAMP '2000-01-01 11:00:00', TIMESTAMP '2000-02-01 12:00:00') AS diff;
┌───────┐
│ diff  │
│ int64 │
├───────┤
│     1 │
└───────┘
```

## Functions
See the [Date Part Functions docs](../../sql/functions/datepart) for a list of available
date parts for use with an `INTERVAL`.

See the [Interval Operators](../../sql/functions/interval) for various functions that operate on intervals.