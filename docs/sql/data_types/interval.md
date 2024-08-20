---
layout: docu
title: Interval Type
blurb: Intervals represent periods of time measured in months, days, microseconds, or a combination thereof.
---

`INTERVAL`s represent periods of time that can be added to or subtracted from `DATE`, `TIMESTAMP`, `TIMESTAMPTZ`, or `TIME` values.

<div class="narrow_table"></div>

| Name | Description |
|:---|:---|
| `INTERVAL` | Period of time |

An `INTERVAL` can be constructed by providing amounts together with units.
Units that aren't *months*, *days*, or *microseconds* are converted to equivalent amounts in the next smaller of these three basis units.

```sql
SELECT
    INTERVAL 1 YEAR, -- single unit using YEAR keyword; stored as 12 months
    INTERVAL (random() * 10) YEAR, -- parentheses necessary for variable amounts;
                                   -- stored as integer number of months
    INTERVAL '1 month 1 day', -- string type necessary for multiple units; stored as (1 month, 1 day)
    '16 months'::INTERVAL, -- string cast supported; stored as 16 months
    '48:00:00'::INTERVAL, -- HH::MM::SS string supported; stored as (48 * 60 * 60 * 1e6 microseconds)
;
```
> Warning Decimal values can be used in strings but are rounded to integers.
> ```sql
> SELECT INTERVAL '1.5' YEARS;
> -- Returns 12 months; equivalent to `to_years(CAST(trunc(1.5) AS INTEGER))`
> ```
> For more precision, use a more granular unit; e.g., `18 MONTHS` instead of `'1.5' YEARS`.

Three basis units are necessary because a month does not correspond to a fixed amount of days (February has fewer days than March) and a day doesn't correspond to a fixed amount of microseconds.
The division into components makes the `INTERVAL` class suitable for adding or subtracting specific time units to a date. For example, we can generate a table with the first day of every month using the following SQL query:

```sql
SELECT DATE '2000-01-01' + INTERVAL (i) MONTH
FROM range(12) t(i);
```

When `INTERVAL`s are deconstructed via the `datepart` function, the *months* component is additionally split into years and months, and the *microseconds* component is split into hours, minutes, and microseconds. The *days* component is not split into additional units. To demonstrate this, the following query generates an `INTERVAL` called `period` by summing random amounts of the three basis units. It then extracts the aforementioned six parts from `period`, adds them back together, and confirms that the result is always equal to the original `period`.

```sql
SELECT
    period = list_reduce(
        [INTERVAL (datepart(part, period) || part) FOR part IN
             ['year', 'month', 'day', 'hour', 'minute', 'microsecond']
        ],
        (i1, i2) -> i1 + i2
    ) -- always true
FROM (
    VALUES (
        INTERVAL (random() * 123_456_789_123) MICROSECONDS
        + INTERVAL (random() * 12_345) DAYS
        + INTERVAL (random() * 12_345) MONTHS
    )
) _(period);
```

> Warning The *microseconds* component is split only into hours, minutes, and microseconds, rather than hours, minutes, *seconds*, and microseconds.

Additionally, the amounts of centuries, decades, quarters, seconds, and milliseconds in an `INTERVAL`, rounded down to the nearest integer, can be extracted via the `datepart` function. However, these components are not required to reassemble the original `INTERVAL`. In fact, if the previous query additionally extracted decades or seconds, then the sum of extracted parts would generally be larger than the original `period` since this would double count the months and microseconds components, respectively.

> All units use 0-based indexing, except for quarters, which use 1-based indexing.

For example:

```sql
SELECT
    datepart('decade', INTERVAL 12 YEARS), -- returns 1
    datepart('year', INTERVAL 12 YEARS), -- returns 12
    datepart('second', INTERVAL 1_234 MILLISECONDS), -- returns 1
    datepart('microsecond', INTERVAL 1_234 MILLISECONDS), -- returns 1_234_000
```

## Arithmetic with Timestamps, Dates and Intervals

`INTERVAL`s can be added to and subtracted from `TIMESTAMP`s, `TIMESTAMPTZ`s, `DATE`s, and `TIME`s using the `+` and `-` operators.

```sql
SELECT
    DATE '2000-01-01' + INTERVAL 1 YEAR,
    TIMESTAMP '2000-01-01 01:33:30' - INTERVAL '1 month 13 hours',
    TIME '02:00:00' - INTERVAL '3 days 23 hours', -- wraps; equals TIME '03:00:00'
;
```

Conversely, subtracting two `TIMESTAMP`s or two `TIMESTAMPTZ`s from one another creates an `INTERVAL` describing the difference between the timestamps with only the *days and microseconds* components. For example:

```sql
SELECT
    TIMESTAMP '2000-02-06 12:00:00' - TIMESTAMP '2000-01-01 11:00:00', -- 36 days 1 hour
    TIMESTAMP '2000-02-01' + (TIMESTAMP '2000-02-01' - TIMESTAMP '2000-01-01'), -- '2000-03-03', NOT '2000-03-01'
;
```

Subtracting two `DATE`s from one another does not create an `INTERVAL` but rather returns the number of days between the given dates as integer value.

> Warning Extracting a component of the `INTERVAL` difference between two `TIMESTAMP`s is not equivalent to computing the number of partition boundaries between the two `TIMESTAMP`s for the corresponding unit, as computed by the `datediff` function:
> ```sql
> SELECT
>     datediff('day', TIMESTAMP '2020-01-01 01:00:00', TIMESTAMP '2020-01-02 00:00:00'), -- 1
>     datepart('day', TIMESTAMP '2020-01-02 00:00:00' - TIMESTAMP '2020-01-01 01:00:00'), -- 0
> ;
> ```

## Equality and Comparison

For equality and ordering comparisons only, the total number of microseconds in an `INTERVAL` is computed by converting the days basis unit to `24 * 60 * 60 * 1e6` microseconds and the months basis unit to 30 days, or `30 * 24 * 60 * 60 * 1e6` microseconds.

As a result, `INTERVAL`s can compare equal even when they are functionally different, and the ordering of `INTERVAL`s is not always preserved when they are added to dates or timestamps.

For example:

* `INTERVAL 30 DAYS = INTERVAL 1 MONTH`
* but `DATE '2020-01-01' + INTERVAL 30 DAYS != DATE '2020-01-01' + INTERVAL 1 MONTH`.

and

* `INTERVAL '30 days 12 hours' > INTERVAL 1 MONTH`
* but `DATE '2020-01-01' + INTERVAL '30 days 12 hours' < DATE '2020-01-01' + INTERVAL 1 MONTH`.

## Functions

See the [Date Part Functions page]({% link docs/sql/functions/datepart.md %}) for a list of available date parts for use with an `INTERVAL`.

See the [Interval Operators page]({% link docs/sql/functions/interval.md %}) for functions that operate on intervals.
