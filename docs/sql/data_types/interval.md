---
layout: docu
title: Interval Type
blurb: Intervals represent a period of time measured in months, days, microseconds, or a combination thereof.
---

`INTERVAL`s represent periods of time and are generally used to *modify* timestamps or dates by either adding them to or subtracting them from `DATE` or `TIMESTAMP` values.


<div class="narrow_table"></div>

| Name | Description |
|:---|:---|
| `INTERVAL` | Period of time |

An `INTERVAL` can be constructed by providing amounts together with units. 
Units that aren't *months*, *days*, or *milliseconds* are converted to equivalent amounts in the next smaller of these three basis units. 
Conversely, units aren't ever converted to the next larger basis unit; for example, no amount of days is ever converted to months. 

```sql
SELECT
  INTERVAL 1 YEAR, -- single unit using YEAR keyword
  INTERVAL (random()) YEAR, -- parentheses necessary for variable amounts
  INTERVAL '1 month 1 day', -- string type necessary for multiple units
  '16 months'::INTERVAL, -- more than 12 months supported
  '48:00:00'::INTERVAL, -- HH::MM::SS string supported. More than 24 hours supported and not converted to days.
;
```

> Warning  If a decimal value is specified, it will be automatically rounded to an integer.
> ```sql
> SELECT INTERVAL '1.5' YEARS; -- WARNING! This returns 2 years = `to_years(CAST(1.5 AS INTEGER))`
> ```
> For more precision, use a more granular unit; e.g. `18 MONTHS` instead of `1.5 YEARS`.


Three base units are necessary because a month does not correspond to a fixed amount of days (February has fewer days than March) and a day doesn't correspond to a fixed amount of microseconds.
The division into components makes the `INTERVAL` class suitable for adding or subtracting specific time units to a date. For example, we can generate a table with the first day of every month using the following SQL query:

```sql
SELECT DATE '2000-01-01' + INTERVAL (i) MONTH
FROM range(12) t(i);
```

When `INTERVAL`s are deconstructed via the `datepart` function, the *months* component is additionally split into years and months, and the *microseconds* component into hours, minutes, and microseconds.

```sql
SELECT
period = list_reduce(
    [INTERVAL (datepart(part, period) || part) for part in ['year', 'month', 'day', 'hour', 'minute', 'microsecond']],
    (i1, i2) -> i1 + i2
) -- always true
FROM (VALUES (INTERVAL (random() * 123456789) MILLISECONDS)) _(period)
```

> Warning Note that the *microseconds* component is split only into hours, minutes, and microseconds, rather than hours, minutes, seconds, and microseconds.

Additionally, the rounded below integer amounts of centuries, decades, seconds, milliseconds in an `INTERVAL` can be extracted via the `datepart` function, but these components not required to reassemble the original interval since they are already captured by the exact amount of years and microseconds, respectively. 

For example, 

```sql
SELECT
datepart('decade', INTERVAL 12 YEARS) -- returns 1
datepart('second', INTERVAL 1234 MILLISECONDS) -- returns 1 
``

## Arithmetic with timestamps, dates, and intervals

`INTERVAL`s can be added to and subtracted from `TIMESTAMP`s, `TIMESTAMPTZ`s, and `DATE`s using the `+` and `-` operators.

```sql
SELECT
  DATE '2000-01-01' + INTERVAL 1 YEAR,
  TIMESTAMP '2000-01-01 01:33:30' - INTERVAL '1 month 13 hours'
;
```

Conversely, subtracting two `TIMESTAMP`s or two `TIMESTAMPTZ`s from one another creates an interval describing the difference between the timestamps with only the *days and microseconds* components. For example:

```sql
SELECT TIMESTAMP '2000-02-06 12:00:00' - TIMESTAMP '2000-01-01 11:00:00' AS diff;
```

|       diff       |
|------------------|
| 36 days 01:00:00 |

> Warning Extracting components from the `INTERVAL` difference between two timestamps or dates is not the same as computing the number of partition boundaries between two timestamps or dates for a specific unit using the `datediff` function:
> ```sql
> SELECT
>   datediff('day', TIMESTAMP '2020-01-01 01:00:00', TIMESTAMP '2020-01-02 00:00:00'), -- 1
>   datepart('day', TIMESTAMP '2020-01-02 00:00:00' - TIMESTAMP '2020-01-01 01:00:00'), -- 0
> ;
> ```

## Functions

See the [Date Part Functions page](../../sql/functions/datepart) for a list of available date parts for use with an `INTERVAL`.

See the [Interval Operators page](../../sql/functions/interval) for functions that operate on intervals.
