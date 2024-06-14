---
layout: docu
title: Interval Type
blurb: Intervals represent a period of time measured in months, days, microseconds, or a combination thereof.
---

`INTERVAL`s represent periods of time and are generally used to *modify* timestamps or dates by either adding them to or subtracting them from `DATE`, `TIMESTAMP(TZ)`, or `TIME` values.

<div class="narrow_table"></div>

| Name | Description |
|:---|:---|
| `INTERVAL` | Period of time |

An `INTERVAL` can be constructed by providing amounts together with units. 
Units that aren't *months*, *days*, or *microseconds* are converted to equivalent amounts in the next smaller of these three basis units.

```sql
SELECT
  INTERVAL 1 YEAR, -- single unit using YEAR keyword; stored as 12 months
  INTERVAL (random() * 10) YEAR, -- parentheses necessary for variable amounts; stored as integer number of months
  INTERVAL '1 month 1 day', -- string type necessary for multiple units; stored as (1 month, 1 day)
  '16 months'::INTERVAL, -- string cast supported; stored as 16 months
  '48:00:00'::INTERVAL, -- HH::MM::SS string supported; stored as (48 * 60 * 60 * 1e6 microseconds)
;
```
> Warning Decimal values can be used in strings but are rounded to integers.
> ```sql
> SELECT INTERVAL '1.5' YEARS; -- Returns 24 months; equivalent to `to_years(CAST(1.5 AS INTEGER))`
> ```
> For more precision, use a more granular unit; e.g., `18 MONTHS` instead of `'1.5' YEARS`.

Three basis units are necessary because a month does not correspond to a fixed amount of days (February has fewer days than March) and a day doesn't correspond to a fixed amount of microseconds.
The division into components makes the `INTERVAL` class suitable for adding or subtracting specific time units to a date. For example, we can generate a table with the first day of every month using the following SQL query:

```sql
SELECT DATE '2000-01-01' + INTERVAL (i) MONTH
FROM range(12) t(i);
```

When `INTERVAL`s are deconstructed via the `datepart` function, the *months* component is additionally split into years and months, and the *microseconds* component is split into hours, minutes, and microseconds.

```sql
SELECT
  period = list_reduce(
    [INTERVAL (datepart(part, period) || part) for part in ['year', 'month', 'day', 'hour', 'minute', 'microsecond']],
    (i1, i2) -> i1 + i2
  ) -- always true
FROM (
  VALUES (
    INTERVAL (random() * 123456789123) MILLISECONDS
    + INTERVAL (random() * 12345) DAYS
    + INTERVAL (random() * 12345) MONTHS
  )
) _(period);
```

> Warning The *microseconds* component is split only into hours, minutes, and microseconds, rather than hours, minutes, *seconds*, and microseconds.

Additionally, the amounts of centuries, decades, quarters, seconds, and milliseconds in an `INTERVAL`, rounded down to the nearest integer, can be extracted via the `datepart` function, but these components are not required to reassemble the original `INTERVAL` since they are already captured by the exact amount of years and microseconds, respectively. 

For example, 

```sql
SELECT
datepart('decade', INTERVAL 12 YEARS) -- returns 1
datepart('second', INTERVAL 1234 MILLISECONDS) -- returns 1 
```

## Arithmetic with timestamps, dates, and intervals

`INTERVAL`s can be added to and subtracted from `TIMESTAMP(TZ)`s, `DATE`s, and `TIME`s using the `+` and `-` operators.

```sql
SELECT
  DATE '2000-01-01' + INTERVAL 1 YEAR,
  TIMESTAMP '2000-01-01 01:33:30' - INTERVAL '1 month 13 hours',
  TIME '02:00:00' - INTERVAL '3 days 23 hours', -- wraps; equals TIME '03:00:00'
;
```

Conversely, subtracting two `TIMESTAMP`s or two `TIMESTAMPTZ`s from one another creates an interval describing the difference between the timestamps with only the *days and microseconds* components. For example:

```sql
SELECT
  TIMESTAMP '2000-02-06 12:00:00' - TIMESTAMP '2000-01-01 11:00:00', -- 36 days 1 hour
  TIMESTAMP '2000-02-01' + (TIMESTAMP '2000-02-01' - TIMESTAMP '2000-01-01'), -- '2000-03-03', NOT '2000-03-01'
;
```

> Warning Extracting a component of  the `INTERVAL` difference between two `TIMESTAMP`s is not equivalent to computing the number of partition boundaries between the two `TIMESTAMP`s for the corresponding unit, as computed by the `datediff` function:
> ```sql
> SELECT
>   datediff('day', TIMESTAMP '2020-01-01 01:00:00', TIMESTAMP '2020-01-02 00:00:00'), -- 1
>   datepart('day', TIMESTAMP '2020-01-02 00:00:00' - TIMESTAMP '2020-01-01 01:00:00'), -- 0
> ;
> ```

## Equality and comparison

For equality and ordering comparisons only, the month component is converted to 30 days and the day component is converted 24 * 60 * 60 * 1e6 microseconds.

As a result, `INTERVAL`s can compare equal even when they are functionally different. 

For example `INTERVAL 30 DAYS = INTERVAL 1 MONTH` but `DATE '2020-01-01' + INTERVAL 30 DAYS != DATE '2020-01-01' + INTERVAL 1 MONTH`.

Equally, `INTERVAL '30 days 12 hours' > INTERVAL 1 MONTH` but `DATE '2020-01-01' + INTERVAL '30 days 12 hours' < DATE '2020-01-01' + INTERVAL 1 MONTH`.

## Functions

See the [Date Part Functions page](../../sql/functions/datepart) for a list of available date parts for use with an `INTERVAL`.

See the [Interval Operators page](../../sql/functions/interval) for functions that operate on intervals.
