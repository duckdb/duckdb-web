---
layout: docu
redirect_from:
- /docs/sql/functions/interval
title: Interval Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions and operators for examining and manipulating [`INTERVAL`]({% link docs/stable/sql/data_types/interval.md %}) values.

## Interval Operators

The table below shows the available mathematical operators for `INTERVAL` types.

| Operator | Description | Example | Result |
|:-|:--|:----|:--|
| `+` | Addition of an `INTERVAL` | `INTERVAL 1 HOUR + INTERVAL 5 HOUR` | `INTERVAL 6 HOUR` |
| `+` | Addition to a `DATE` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27` |
| `+` | Addition to a `TIMESTAMP` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `+` | Addition to a `TIME` | `TIME '01:02:03' + INTERVAL 5 HOUR` | `06:02:03` |
| `-` | Subtraction of an `INTERVAL` | `INTERVAL 5 HOUR - INTERVAL 1 HOUR` | `INTERVAL 4 HOUR` |
| `-` | Subtraction from a `DATE` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22` |
| `-` | Subtraction from a `TIMESTAMP` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |
| `-` | Subtraction from a `TIME` | `TIME '06:02:03' - INTERVAL 5 HOUR` | `01:02:03` |

## Interval Functions

The table below shows the available scalar functions for `INTERVAL` types.

| Name | Description |
|:--|:-------|
| [`date_part(part, interval)`](#date_partpart-interval) | Extract [datepart component]({% link docs/stable/sql/functions/datepart.md %}) (equivalent to `extract`). See [`INTERVAL`]({% link docs/stable/sql/data_types/interval.md %}) for the sometimes surprising rules governing this extraction. |
| [`datepart(part, interval)`](#datepartpart-interval) | Alias of `date_part`. |
| [`extract(part FROM interval)`](#extractpart-from-interval) | Alias of `date_part`. |
| [`epoch(interval)`](#epochinterval) | Get total number of seconds, as double precision floating point number, in interval. |
| [`to_centuries(integer)`](#to_centuriesinteger) | Construct a century interval. |
| [`to_days(integer)`](#to_daysinteger) | Construct a day interval. |
| [`to_decades(integer)`](#to_decadesinteger) | Construct a decade interval. |
| [`to_hours(integer)`](#to_hoursinteger) | Construct an hour interval. |
| [`to_microseconds(integer)`](#to_microsecondsinteger) | Construct a microsecond interval. |
| [`to_millennia(integer)`](#to_millenniainteger) | Construct a millennium interval. |
| [`to_milliseconds(integer)`](#to_millisecondsinteger) | Construct a millisecond interval. |
| [`to_minutes(integer)`](#to_minutesinteger) | Construct a minute interval. |
| [`to_months(integer)`](#to_monthsinteger) | Construct a month interval. |
| [`to_quarters(integer`)](#to_quartersinteger) | Construct an interval of `integer` quarters. |
| [`to_seconds(integer)`](#to_secondsinteger) | Construct a second interval. |
| [`to_weeks(integer)`](#to_weeksinteger) | Construct a week interval. |
| [`to_years(integer)`](#to_yearsinteger) | Construct a year interval. |

> Only the documented [date part components]({% link docs/stable/sql/functions/datepart.md %}) are defined for intervals.

#### `date_part(part, interval)`

<div class="nostroke_table"></div>

| **Description** | Extract [datepart component]({% link docs/stable/sql/functions/datepart.md %}) (equivalent to `extract`). See [`INTERVAL`]({% link docs/stable/sql/data_types/interval.md %}) for the sometimes surprising rules governing this extraction. |
| **Example** | `date_part('year', INTERVAL '14 months')` |
| **Result** | `1` |

#### `datepart(part, interval)`

<div class="nostroke_table"></div>

| **Description** | Alias of `date_part`. |
| **Example** | `datepart('year', INTERVAL '14 months')` |
| **Result** | `1` |

#### `extract(part FROM interval)`

<div class="nostroke_table"></div>

| **Description** | Alias of `date_part`. |
| **Example** | `extract('month' FROM INTERVAL '14 months')` |
| **Result** | 2 |

#### `epoch(interval)`

<div class="nostroke_table"></div>

| **Description** | Get total number of seconds, as double precision floating point number, in interval. |
| **Example** | `epoch(INTERVAL 5 HOUR)` |
| **Result** | `18000.0` |

#### `to_centuries(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a century interval. |
| **Example** | `to_centuries(5)` |
| **Result** | `INTERVAL 500 YEAR` |

#### `to_days(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a day interval. |
| **Example** | `to_days(5)` |
| **Result** | `INTERVAL 5 DAY` |

#### `to_decades(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a decade interval. |
| **Example** | `to_decades(5)` |
| **Result** | `INTERVAL 50 YEAR` |

#### `to_hours(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct an hour interval. |
| **Example** | `to_hours(5)` |
| **Result** | `INTERVAL 5 HOUR` |

#### `to_microseconds(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a microsecond interval. |
| **Example** | `to_microseconds(5)` |
| **Result** | `INTERVAL 5 MICROSECOND` |

#### `to_millennia(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a millennium interval. |
| **Example** | `to_millennia(5)` |
| **Result** | `INTERVAL 5000 YEAR` |

#### `to_milliseconds(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a millisecond interval. |
| **Example** | `to_milliseconds(5)` |
| **Result** | `INTERVAL 5 MILLISECOND` |

#### `to_minutes(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a minute interval. |
| **Example** | `to_minutes(5)` |
| **Result** | `INTERVAL 5 MINUTE` |

#### `to_months(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a month interval. |
| **Example** | `to_months(5)` |
| **Result** | `INTERVAL 5 MONTH` |

#### `to_quarters(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct an interval of `integer` quarters. |
| **Example** | `to_quarters(5)` |
| **Result** | `INTERVAL 1 YEAR 3 MONTHS` |

#### `to_seconds(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a second interval. |
| **Example** | `to_seconds(5)` |
| **Result** | `INTERVAL 5 SECOND` |

#### `to_weeks(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a week interval. |
| **Example** | `to_weeks(5)` |
| **Result** | `INTERVAL 35 DAY` |

#### `to_years(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a year interval. |
| **Example** | `to_years(5)` |
| **Result** | `INTERVAL 5 YEAR` |
