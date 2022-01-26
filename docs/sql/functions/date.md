---
layout: docu
title: Date Functions
selected: Documentation/Functions/Date Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating date values.

## Date Operators
The table below shows the available mathematical operators for `DATE` types.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `+` | addition of days (integers) | `DATE '1992-03-22' + 5` | 1992-03-27 |
| `+` | addition of an `INTERVAL` | `DATE '1992-03-22' + INTERVAL 5 DAY` | 1992-03-27 |
| `-` | subtraction of `DATE`s | `DATE '1992-03-27' - DATE '1992-03-22'` | 5 |
| `-` | subtraction of an `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY'` | 1992-03-22 |

## Date Functions
The table below shows the available functions for `DATE` types.
Dates can also be manipulated with the [timestamp functions](/docs/sql/functions/timestamp) through type promotion.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `current_date` | Current date (at start of current transaction) | | |
| `date_diff(`*`part`*`, `*`startdate`*`, , `*`enddate`*`)` | The number of [partition](/docs/sql/functions/datepart) boundaries between the dates | `date_diff('month', DATE '1992-09-15', DATE '1992-11-14')` | `2` |
| `date_part(`*`part`*`, `*`date`*`)` | Get the [subfield](/docs/sql/functions/datepart) (equivalent to *extract*) | `date_part('year', DATE '1992-09-20')` | `1992` |
| `date_sub(`*`part`*`, `*`startdate`*`, , `*`enddate`*`)` | The number of complete [partitions](/docs/sql/functions/datepart) between the dates | `date_sub('month', DATE '1992-09-15', DATE '1992-11-14')` | `1` |
| `date_trunc(`*`part`*`, `*`date`*`)` | Truncate to specified [precision](/docs/sql/functions/datepart) | `date_trunc('month', DATE '1992-03-07')` | `1992-03-01` |
| `dayname(`*`date`*`)` | The (English) name of the weekday | `monthname(DATE '1992-09-20')` | `Sunday` |
| `extract(`*`part`* `from `*`date`*`)` | Get [subfield](/docs/sql/functions/datepart) from a date | `extract('year' FROM DATE '1992-09-20')` | `1992` |
| `greatest(`*`date`*`, `*`date`*`)` | The later of two dates | `greatest(DATE '1992-09-20', DATE '1992-03-07')` | `1992-09-20` |
| `last_day(`*`date`*`)` | The last day of the month | `last_day(DATE '1992-09-20')` | `1992-09-30` |
| `least(`*`date`*`, `*`date`*`)` | The earlier of two dates | `least(DATE '1992-09-20', DATE '1992-03-07')` | `1992-03-07` |
| `monthname(`*`date`*`)` | The (English) name of the month | `monthname(DATE '1992-09-20')` | `September` |
| `last_day(`*`date`*`)` | Last day of the corresponding month in the date | `last_day(DATE '1992-09-20')` | `1992-09-30` |
| `strftime(date, format)` | Converts a date to a string according to the [format string](/docs/sql/functions/dateformat) | `strftime(date '1992-01-01', '%a, %-d %B %Y')` | `Wed, 1 January 1992` |

There are also dedicated extraction functions to get the [subfields](/docs/sql/functions/datepart).
