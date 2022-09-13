---
layout: docu
title: Interval Type
selected: Documentation/Data Types/Interval
expanded: Data Types
blurb: An interval specifies a period of time measured in units of a specific date part like years, days, seconds, or others.
---
Intervals represent a period of time. This period can be measured in a variety of units,
for example years, days, or seconds. See the [Date Part Functions docs](../../sql/functions/datepart) for a list of available
date parts for use with an `INTERVAL`.


| Name | Description |
|:---|:---|
| `INTERVAL` | Period of time |

An `INTERVAL` can be generated directly or can be a result of a function (for example, calculating the difference between two timestamps). 
Intervals can be used to modify `DATE`, `TIMESTAMP`, or `TIMESTAMP WITH TIME ZONE` data types. See the [Interval Operators](../../sql/functions/interval) for details.

```sql
-- Each Date Part can be either singular or plural
-- In this example, YEAR or YEARS can be used interchangeably
-- 1 year
SELECT INTERVAL 1 YEAR;
-- 1 year
SELECT INTERVAL 1 YEARS;
-- The number used to specify an interval can optionally be wrapped in single quotes
-- 28 days
SELECT INTERVAL '28' DAYS;
-- The number and date part can optionally be wrapped entirely in single quotes
-- 28 days
SELECT INTERVAL '28 DAYS';
-- Intervals can also be used to specify a time period rather than a date period
-- 00:00:30
SELECT INTERVAL 30 SECONDS;

-- Intervals can also be produced as a result of a timestamp operator like subtraction
-- These can include a date and time component on the Interval
-- 1 day 01:00:00
SELECT '2022-01-02 01:00:00'::TIMESTAMP - '2022-01-01'::TIMESTAMP;

-- WARNING: If a decimal value is specified, it will be automatically truncated to an integer
-- To use more precise values, simply use a more granular date part 
-- (In this example use 18 MONTHS instead of 1.5 YEARS)
-- The statement below is equivalent to to_years(CAST(1.5 AS INTEGER))
-- 1 year
SELECT INTERVAL '1.5' YEARS; --WARNING! This returns 1 year!
```

## Functions
See [Interval Functions](../../sql/functions/interval).
