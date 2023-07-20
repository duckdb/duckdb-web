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
| `+` | addition of a variable `INTERVAL` | `SELECT DATE '1992-03-22' + INTERVAL 1 DAY * d.days FROM (VALUES (5), (11)) AS d(days)` |1992-03-27 1992-04-02 |
| `-` | subtraction of `DATE`s | `DATE '1992-03-27' - DATE '1992-03-22'` | 5 |
| `-` | subtraction of an `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY'` | 1992-03-22 |
| `-` | subtraction of a variable `INTERVAL` | `SELECT DATE '1992-03-27' - INTERVAL 1 DAY * d.days FROM (VALUES (5), (11)) AS d(days)` |1992-03-22 1992-03-16 |

Adding to or subtracting from [infinite values](../../sql/data_types/date#special-values) produces the same infinite value.

## Date Functions
The table below shows the available functions for `DATE` types.
Dates can also be manipulated with the [timestamp functions](../../sql/functions/timestamp) through type promotion.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `current_date` | Current date (at start of current transaction) | `current_date` | `2022-10-08` |
| `date_diff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the dates | `date_diff('month', DATE '1992-09-15', DATE '1992-11-14')` | `2` |
| `datediff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_diff. The number of [partition](../../sql/functions/datepart) boundaries between the dates | `datediff('month', DATE '1992-09-15', DATE '1992-11-14')` | `2` |
| `date_part(`*`part`*`, `*`date`*`)` | Get the [subfield](../../sql/functions/datepart) (equivalent to `extract`) | `date_part('year', DATE '1992-09-20')` | `1992` |
| `datepart(`*`part`*`, `*`date`*`)` | Alias of date_part. Get the [subfield](../../sql/functions/datepart) (equivalent to `extract`) | `datepart('year', DATE '1992-09-20')` | `1992` |
| `date_sub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the dates | `date_sub('month', DATE '1992-09-15', DATE '1992-11-14')` | `1` |
| `datesub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the dates | `datesub('month', DATE '1992-09-15', DATE '1992-11-14')` | `1` |
| `date_trunc(`*`part`*`, `*`date`*`)` | Truncate to specified [precision](../../sql/functions/datepart) | `date_trunc('month', DATE '1992-03-07')` | `1992-03-01` |
| `datetrunc(`*`part`*`, `*`date`*`)` | Alias of date_trunc. Truncate to specified [precision](../../sql/functions/datepart) | `datetrunc('month', DATE '1992-03-07')` | `1992-03-01` |
| `dayname(`*`date`*`)` | The (English) name of the weekday | `dayname(DATE '1992-09-20')` | `Sunday` |
| `isfinite(`*`date`*`)` | Returns true if the date is finite, false otherwise | `isfinite(DATE '1992-03-07')` | true |
| `isinf(`*`date`*`)` | Returns true if the date is infinite, false otherwise | `isinf(DATE '-infinity')` | true |
| `extract(`*`part`* `from `*`date`*`)` | Get [subfield](../../sql/functions/datepart) from a date | `extract('year' FROM DATE '1992-09-20')` | `1992` |
| `greatest(`*`date`*`, `*`date`*`)` | The later of two dates | `greatest(DATE '1992-09-20', DATE '1992-03-07')` | `1992-09-20` |
| `last_day(`*`date`*`)` | The last day of the corresponding month in the date | `last_day(DATE '1992-09-20')` | `1992-09-30` |
| `least(`*`date`*`, `*`date`*`)` | The earlier of two dates | `least(DATE '1992-09-20', DATE '1992-03-07')` | `1992-03-07` |
| `make_date(`*`bigint`*`, `*`bigint`*`, `*`bigint`*`)` | The date for the given parts | `make_date(1992, 9, 20)` | `1992-09-20` |
| `monthname(`*`date`*`)` | The (English) name of the month | `monthname(DATE '1992-09-20')` | `September` |
| `strftime(date, format)` | Converts a date to a string according to the [format string](../../sql/functions/dateformat) | `strftime(date '1992-01-01', '%a, %-d %B %Y')` | `Wed, 1 January 1992` |
| `time_bucket(`*`bucket_width`*`, `*`date`*`[, `*`origin`*`])` | Truncate `date` by the specified interval `bucket_width`. Buckets are aligned relative to `origin` date. `origin` defaults to 2000-01-03 for buckets that don't include a month or year interval, and to 2000-01-01 for month and year buckets. | `time_bucket(INTERVAL '2 weeks', DATE '1992-04-20', DATE '1992-04-01')` | `1992-04-15` |
| `time_bucket(`*`bucket_width`*`, `*`date`*`[, `*`offset`*`])` | Truncate `date` by the specified interval `bucket_width`. Buckets are offset by `offset` interval. | `time_bucket(INTERVAL '2 months', DATE '1992-04-20', INTERVAL '1 month')` | `1992-04-01` |
| `today()` | Current date (start of current transaction) | `today()` | `2022-10-08` |

There are also dedicated extraction functions to get the [subfields](../../sql/functions/datepart#part-functions).
A few examples include extracting the day from a date, or the day of the week from a date. 

Functions applied to infinite dates will either return the same infinite dates
(e.g, `greatest`) or `NULL` (e.g., `date_part`) depending on what "makes sense".
In general, if the function needs to examine the parts of the infinite date, the result will be `NULL`.
