---
layout: docu
title: Interval Functions
---

This section describes functions and operators for examining and manipulating `INTERVAL` values.

## Interval Operators

The table below shows the available mathematical operators for `INTERVAL` types.

| Operator | Description | Example | Result |
|:-|:--|:----|:--|
| `+` | addition of an `INTERVAL` | `INTERVAL 1 HOUR + INTERVAL 5 HOUR` | `INTERVAL 6 HOUR` |
| `+` | addition to a `DATE` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27` |
| `+` | addition to a `TIMESTAMP` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `+` | addition to a `TIME` | `TIME '01:02:03' + INTERVAL 5 HOUR` | `06:02:03` |
| `-` | subtraction of an `INTERVAL` | `INTERVAL 5 HOUR - INTERVAL 1 HOUR` | `INTERVAL 4 HOUR` |
| `-` | subtraction from a `DATE` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22` |
| `-` | subtraction from a `TIMESTAMP` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |
| `-` | subtraction from a `TIME` | `TIME '06:02:03' - INTERVAL 5 HOUR` | `01:02:03` |

## Interval Functions

The table below shows the available scalar functions for `INTERVAL` types.

| Name | Description |
|:--|:-------|
| [`date_part(part, interval)`](#date_partpart-interval) | Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| [`datepart(part, interval)`](#datepartpart-interval) | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| [`extract(part FROM interval)`](#extractpart-from-interval) | Get [subfield](../../sql/functions/datepart) from an interval. |
| [`epoch(interval)`](#epochinterval) | Get total number of seconds in interval. |
| [`to_centuries(integer)`](#to_centuriesinteger) | Construct a century interval. |
| [`to_days(integer)`](#to_daysinteger) | Construct a day interval. |
| [`to_decades(integer)`](#to_decadesinteger) | Construct a decade interval. |
| [`to_hours(integer)`](#to_hoursinteger) | Construct a hour interval. |
| [`to_microseconds(integer)`](#to_microsecondsinteger) | Construct a microsecond interval. |
| [`to_millennia(integer)`](#to_millenniainteger) | Construct a millenium interval. |
| [`to_milliseconds(integer)`](#to_millisecondsinteger) | Construct a millisecond interval. |
| [`to_minutes(integer)`](#to_minutesinteger) | Construct a minute interval. |
| [`to_months(integer)`](#to_monthsinteger) | Construct a month interval. |
| [`to_seconds(integer)`](#to_secondsinteger) | Construct a second interval. |
| [`to_weeks(integer)`](#to_weeksinteger) | Construct a week interval. |
| [`to_years(integer)`](#to_yearsinteger) | Construct a year interval. |

> Only the documented [date parts](../../sql/functions/datepart) are defined for intervals.

### `date_part(part, interval)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| **Example** | `date_part('year', INTERVAL '14 months')` |
| **Result** | `1` |

### `datepart(part, interval)`

<div class="nostroke_table"></div>

| **Description** | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| **Example** | `datepart('year', INTERVAL '14 months')` |
| **Result** | `1` |

### `extract(part FROM interval)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield](../../sql/functions/datepart) from an interval. |
| **Example** | `extract('month' FROM INTERVAL '14 months')` |
| **Result** | 2 |

### `epoch(interval)`

<div class="nostroke_table"></div>

| **Description** | Get total number of seconds in interval. |
| **Example** | `epoch(INTERVAL 5 HOUR)` |
| **Result** | `18000.0` |

### `to_centuries(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a century interval. |
| **Example** | `to_centuries(5)` |
| **Result** | `INTERVAL 500 YEAR` |

### `to_days(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a day interval. |
| **Example** | `to_days(5)` |
| **Result** | `INTERVAL 5 DAY` |

### `to_decades(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a decade interval. |
| **Example** | `to_decades(5)` |
| **Result** | `INTERVAL 50 YEAR` |

### `to_hours(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a hour interval. |
| **Example** | `to_hours(5)` |
| **Result** | `INTERVAL 5 HOUR` |

### `to_microseconds(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a microsecond interval. |
| **Example** | `to_microseconds(5)` |
| **Result** | `INTERVAL 5 MICROSECOND` |

### `to_millennia(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a millenium interval. |
| **Example** | `to_millennia(5)` |
| **Result** | `INTERVAL 5000 YEAR` |

### `to_milliseconds(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a millisecond interval. |
| **Example** | `to_milliseconds(5)` |
| **Result** | `INTERVAL 5 MILLISECOND` |

### `to_minutes(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a minute interval. |
| **Example** | `to_minutes(5)` |
| **Result** | `INTERVAL 5 MINUTE` |

### `to_months(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a month interval. |
| **Example** | `to_months(5)` |
| **Result** | `INTERVAL 5 MONTH` |

### `to_seconds(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a second interval. |
| **Example** | `to_seconds(5)` |
| **Result** | `INTERVAL 5 SECOND` |

### `to_weeks(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a week interval. |
| **Example** | `to_weeks(5)` |
| **Result** | `INTERVAL 35 DAY` |

### `to_years(integer)`

<div class="nostroke_table"></div>

| **Description** | Construct a year interval. |
| **Example** | `to_years(5)` |
| **Result** | `INTERVAL 5 YEAR` |
