---
layout: docu
title: Interval Type
blurb: Intervals represent a period of time measured in months, days, microseconds, or a combination thereof.
---

Intervals represent a period of time and are generally used to *modify* timestamps or dates by either adding them to or subtracting them from `DATE` or `TIMESTAMP` values.


<div class="narrow_table"></div>

| Name | Description |
|:---|:---|
| `INTERVAL` | Period of time |

An `INTERVAL` can be constructed by providing an amount together with a unit. Units that aren't *months*, *days*, or *milliseconds* are converted to equivalent amounts in the next smaller of these three basis units. 
Conversely, units aren't ever converted to the next larger basis unit, that is, no amount of days is ever converted to months. 

Three base units are necessary because a month does not correspond to a fixed amount of days (February has fewer days than March) and days don't have a fixed amount of microseconds.
The division into components makes the `INTERVAL` class suitable for adding or subtracting specific time units to a date. For example, we can generate a table with the first day of every month using the following SQL query:

```sql
SELECT DATE '2000-01-01' + INTERVAL (i) MONTH
FROM range(12) t(i);
```

When `INTERVAL`s are deconstructed via the `datepart` function, the *months* component is additionally split into years and months, and the *microseconds* component into hours, minutes, and microseconds.

> Warning Note that the smallest component is split only into hours, minutes, and microseconds, rather than hours, minutes, seconds, and microseconds.

Additionally, 

## Examples

1 year:

```sql
SELECT INTERVAL 1 YEAR;
```

Add 1 year to a specific date:

```sql
SELECT DATE '2000-01-01' + INTERVAL 1 YEAR;
```

Subtract 1 year from a specific date:

```sql
SELECT DATE '2000-01-01' - INTERVAL 1 YEAR;
```

Construct an interval from a column, instead of a constant:

```sql
SELECT INTERVAL (i) YEAR FROM range(1, 5) t(i);
```

Construct an interval with mixed units:

```sql
SELECT INTERVAL '1 month 1 day';
```

Intervals greater than 24 hours/12 months/etc. are supported:

```sql
SELECT '540:58:47.210'::INTERVAL;
SELECT INTERVAL '16 MONTHS';
```

> Warning  If a decimal value is specified, it will be automatically rounded to an integer.
> To use more precise values, simply use a more granular date part
> In this example, use `18 MONTHS` instead of `1.5 YEARS`.
> The statement below is equivalent to `to_years(CAST(1.5 AS INTEGER))`
>
> ```sql
> SELECT INTERVAL '1.5' YEARS; -- WARNING! This returns 2 years!
> ```

## Difference between Dates

If we subtract two timestamps from one another, we obtain an interval describing the difference between the timestamps with the *days and microseconds* components. For example:

```sql
SELECT TIMESTAMP '2000-02-01 12:00:00' - TIMESTAMP '2000-01-01 11:00:00' AS diff;
```

|       diff       |
|------------------|
| 31 days 01:00:00 |

The `datediff` function can be used to obtain the difference between two dates for a specific unit.

```sql
SELECT datediff('month', TIMESTAMP '2000-01-01 11:00:00', TIMESTAMP '2000-02-01 12:00:00') AS diff;
```

| diff |
|-----:|
| 1    |

## Functions

See the [Date Part Functions page](../../sql/functions/datepart) for a list of available date parts for use with an `INTERVAL`.

See the [Interval Operators page](../../sql/functions/interval) for functions that operate on intervals.
