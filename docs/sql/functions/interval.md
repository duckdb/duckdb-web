---
layout: docu
title: Interval Functions
selected: Documentation/Functions/Interval Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating `INTERVAL` values.

## Interval Operators
The table below shows the available mathematical operators for `INTERVAL` types.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `+` | addition of an `INTERVAL` | `INTERVAL 1 HOUR + INTERVAL 5 HOUR` | INTERVAL 6 HOUR |
| `+` | addition to a `DATE` | `DATE '1992-03-22' + INTERVAL 5 DAY` | 1992-03-27 |
| `+` | addition to a `TIMESTAMP` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | 1992-03-27 01:02:03 |
| `+` | addition to a `TIME` | `TIME '01:02:03' + INTERVAL 5 HOUR` | 06:02:03 |
| `-` | subtraction of an `INTERVAL` | `INTERVAL 5 HOUR - INTERVAL 1 HOUR` | INTERVAL 4 HOUR |
| `-` | subtraction from a `DATE` | `DATE '1992-03-27' - INTERVAL 5 DAY` | 1992-03-22 |
| `-` | subtraction from a `TIMESTAMP` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | 1992-03-22 01:02:03 |
| `-` | subtraction from a `TIME` | `TIME '06:02:03' - INTERVAL 5 HOUR` | 01:02:03 |

## Interval Functions
The table below shows the available scalar functions for `INTERVAL` types.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `date_part(`*`part`*`, `*`interval`*`)` | Get [subfield](/docs/sql/functions/datepart) (equivalent to *extract*) | `date_part('year', INTERVAL '14 months')` | 1 |
| `extract(`*`part`* `from` *`interval`*`)` | Get [subfield](/docs/sql/functions/datepart) from a date | `extract('month' FROM INTERVAL '14 months')` | 2 |
| `to_years(`*`integer`*`)` | Construct a year interval | `to_years(5)` | INTERVAL 5 YEAR |
| `to_months(`*`integer`*`)` | Construct a month interval | `to_months(5)` | INTERVAL 5 MONTH |
| `to_days(`*`integer`*`)` | Construct a day interval | `to_days(5)` | INTERVAL 5 DAY |
| `to_hours(`*`integer`*`)` | Construct a hour interval | `to_hours(5)` | INTERVAL 5 HOUR |
| `to_minutes(`*`integer`*`)` | Construct a minute interval | `to_minutes(5)` | INTERVAL 5 MINUTE |
| `to_seconds(`*`integer`*`)` | Construct a second interval | `to_seconds(5)` | INTERVAL 5 SECOND |
| `to_milliseconds(`*`integer`*`)` | Construct a millisecond interval | `to_milliseconds(5)` | INTERVAL 5 MILLISECOND |
| `to_microseconds(`*`integer`*`)` | Construct a microsecond interval | `to_microseconds(5)` | INTERVAL 5 MICROSECOND |

All [date parts](/docs/sql/functions/datepart) are defined for intervals except `dow`, `isodow`, `doy`, `week` and `yearweek`.
