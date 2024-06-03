---
layout: docu
redirect_from:
- docs/archive/0.10/test/functions/date
title: Date Functions
---

This section describes functions and operators for examining and manipulating date values.

## Date Operators

The table below shows the available mathematical operators for `DATE` types.

| Operator | Description | Example | Result |
|:-|:--|:---|:--|
| `+` | addition of days (integers) | `DATE '1992-03-22' + 5` | `1992-03-27` |
| `+` | addition of an `INTERVAL` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27` |
| `+` | addition of a variable `INTERVAL` | `SELECT DATE '1992-03-22' + INTERVAL (d.days) DAY FROM (VALUES (5), (11)) AS d(days)` | `1992-03-27` and `1992-04-02` |
| `-` | subtraction of `DATE`s | `DATE '1992-03-27' - DATE '1992-03-22'` | `5` |
| `-` | subtraction of an `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22` |
| `-` | subtraction of a variable `INTERVAL` | `SELECT DATE '1992-03-27' - INTERVAL (d.days) DAY FROM (VALUES (5), (11)) AS d(days)` | `1992-03-22` and `1992-03-16` |

Adding to or subtracting from [infinite values](../../sql/data_types/date#special-values) produces the same infinite value.

## Date Functions

The table below shows the available functions for `DATE` types.
Dates can also be manipulated with the [timestamp functions](../../sql/functions/timestamp) through type promotion.

| Name | Description |
|:--|:-------|
| [`current_date`](#current_date) | Current date (at start of current transaction). |
| [`date_add(date, interval)`](#date_adddate-interval) | Add the interval to the date. |
| [`date_diff(part, startdate, enddate)`](#date_diffpart-startdate-enddate) | The number of [partition](../../sql/functions/datepart) boundaries between the dates. |
| [`date_part(part, date)`](#date_partpart-date) | Get the [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| [`date_sub(part, startdate, enddate)`](#date_subpart-startdate-enddate) | The number of complete [partitions](../../sql/functions/datepart) between the dates. |
| [`date_trunc(part, date)`](#date_truncpart-date) | Truncate to specified [precision](../../sql/functions/datepart). |
| [`datediff(part, startdate, enddate)`](#datediffpart-startdate-enddate) | The number of [partition](../../sql/functions/datepart) boundaries between the dates. Alias of `date_diff`. |
| [`datepart(part, date)`](#datepartpart-date) | Get the [subfield](../../sql/functions/datepart) (equivalent to `extract`). Alias of `date_part`. |
| [`datesub(part, startdate, enddate)`](#datesubpart-startdate-enddate) | The number of complete [partitions](../../sql/functions/datepart) between the dates. Alias of `date_sub`. |
| [`datetrunc(part, date)`](#datetruncpart-date) | Truncate to specified [precision](../../sql/functions/datepart). Alias of `date_trunc`. |
| [`dayname(date)`](#daynamedate) | The (English) name of the weekday. |
| [`extract(part from date)`](#extractpart-from-date) | Get [subfield](../../sql/functions/datepart) from a date. |
| [`greatest(date, date)`](#greatestdate-date) | The later of two dates. |
| [`isfinite(date)`](#isfinitedate) | Returns true if the date is finite, false otherwise. |
| [`isinf(date)`](#isinfdate) | Returns true if the date is infinite, false otherwise. |
| [`last_day(date)`](#last_daydate) | The last day of the corresponding month in the date. |
| [`least(date, date)`](#leastdate-date) | The earlier of two dates. |
| [`make_date(year, month, day)`](#make_dateyear-month-day) | The date for the given parts. |
| [`monthname(date)`](#monthnamedate) | The (English) name of the month. |
| [`strftime(date, format)`](#strftimedate-format) | Converts a date to a string according to the [format string](../../sql/functions/dateformat). |
| [`time_bucket(bucket_width, date[, offset])`](#time_bucketbucket_width-date-offset) | Truncate `date` by the specified interval `bucket_width`. Buckets are offset by `offset` interval. |
| [`time_bucket(bucket_width, date[, origin])`](#time_bucketbucket_width-date-origin) | Truncate `date` by the specified interval `bucket_width`. Buckets are aligned relative to `origin` date. `origin` defaults to 2000-01-03 for buckets that don't include a month or year interval, and to 2000-01-01 for month and year buckets. |
| [`today()`](#today) | Current date (start of current transaction). |

### `current_date`

<div class="nostroke_table"></div>

| **Description** | Current date (at start of current transaction). |
| **Example** | `current_date` |
| **Result** | `2022-10-08` |

### `date_add(date, interval)`

<div class="nostroke_table"></div>

| **Description** | Add the interval to the date. |
| **Example** | `date_add(DATE '1992-09-15', INTERVAL 2 MONTH)` |
| **Result** | `1992-11-15` |

### `date_diff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **Description** | The number of [partition](../../sql/functions/datepart) boundaries between the dates. |
| **Example** | `date_diff('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **Result** | `2` |

### `date_part(part, date)`

<div class="nostroke_table"></div>

| **Description** | Get the [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| **Example** | `date_part('year', DATE '1992-09-20')` |
| **Result** | `1992` |

### `date_sub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **Description** | The number of complete [partitions](../../sql/functions/datepart) between the dates. |
| **Example** | `date_sub('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **Result** | `1` |

### `date_trunc(part, date)`

<div class="nostroke_table"></div>

| **Description** | Truncate to specified [precision](../../sql/functions/datepart). |
| **Example** | `date_trunc('month', DATE '1992-03-07')` |
| **Result** | `1992-03-01` |

### `datediff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **Description** | The number of [partition](../../sql/functions/datepart) boundaries between the dates. |
| **Example** | `datediff('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **Result** | `2` |
| **Alias** | `date_diff`. |

### `datepart(part, date)`

<div class="nostroke_table"></div>

| **Description** | Get the [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| **Example** | `datepart('year', DATE '1992-09-20')` |
| **Result** | `1992` |
| **Alias** | `date_part`. |

### `datesub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **Description** | The number of complete [partitions](../../sql/functions/datepart) between the dates. |
| **Example** | `datesub('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **Result** | `1` |
| **Alias** | `date_sub`. |

### `datetrunc(part, date)`

<div class="nostroke_table"></div>

| **Description** | Truncate to specified [precision](../../sql/functions/datepart). |
| **Example** | `datetrunc('month', DATE '1992-03-07')` |
| **Result** | `1992-03-01` |
| **Alias** | `date_trunc`. |

### `dayname(date)`

<div class="nostroke_table"></div>

| **Description** | The (English) name of the weekday. |
| **Example** | `dayname(DATE '1992-09-20')` |
| **Result** | `Sunday` |

### `extract(part from date)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield](../../sql/functions/datepart) from a date. |
| **Example** | `extract('year' FROM DATE '1992-09-20')` |
| **Result** | `1992` |

### `greatest(date, date)`

<div class="nostroke_table"></div>

| **Description** | The later of two dates. |
| **Example** | `greatest(DATE '1992-09-20', DATE '1992-03-07')` |
| **Result** | `1992-09-20` |

### `isfinite(date)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the date is finite, false otherwise. |
| **Example** | `isfinite(DATE '1992-03-07')` |
| **Result** | `true` |

### `isinf(date)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the date is infinite, false otherwise. |
| **Example** | `isinf(DATE '-infinity')` |
| **Result** | `true` |

### `last_day(date)`

<div class="nostroke_table"></div>

| **Description** | The last day of the corresponding month in the date. |
| **Example** | `last_day(DATE '1992-09-20')` |
| **Result** | `1992-09-30` |

### `least(date, date)`

<div class="nostroke_table"></div>

| **Description** | The earlier of two dates. |
| **Example** | `least(DATE '1992-09-20', DATE '1992-03-07')` |
| **Result** | `1992-03-07` |

### `make_date(year, month, day)`

<div class="nostroke_table"></div>

| **Description** | The date for the given parts. |
| **Example** | `make_date(1992, 9, 20)` |
| **Result** | `1992-09-20` |

### `monthname(date)`

<div class="nostroke_table"></div>

| **Description** | The (English) name of the month. |
| **Example** | `monthname(DATE '1992-09-20')` |
| **Result** | `September` |

### `strftime(date, format)`

<div class="nostroke_table"></div>

| **Description** | Converts a date to a string according to the [format string](../../sql/functions/dateformat). |
| **Example** | `strftime(date '1992-01-01', '%a, %-d %B %Y')` |
| **Result** | `Wed, 1 January 1992` |

### `time_bucket(bucket_width, date[, offset])`

<div class="nostroke_table"></div>

| **Description** | Truncate `date` by the specified interval `bucket_width`. Buckets are offset by `offset` interval. |
| **Example** | `time_bucket(INTERVAL '2 months', DATE '1992-04-20', INTERVAL '1 month')` |
| **Result** | `1992-04-01` |

### `time_bucket(bucket_width, date[, origin])`

<div class="nostroke_table"></div>

| **Description** | Truncate `date` by the specified interval `bucket_width`. Buckets are aligned relative to `origin` date. `origin` defaults to `2000-01-03` for buckets that don't include a month or year interval, and to `2000-01-01` for month and year buckets. |
| **Example** | `time_bucket(INTERVAL '2 weeks', DATE '1992-04-20', DATE '1992-04-01')` |
| **Result** | `1992-04-15` |

### `today()`

<div class="nostroke_table"></div>

| **Description** | Current date (start of current transaction). |
| **Example** | `today()` |
| **Result** | `2022-10-08` |

## Date Part Extraction Functions

There are also dedicated extraction functions to get the [subfields](../../sql/functions/datepart#part-functions).
A few examples include extracting the day from a date, or the day of the week from a date.

Functions applied to infinite dates will either return the same infinite dates
(e.g, `greatest`) or `NULL` (e.g., `date_part`) depending on what "makes sense".
In general, if the function needs to examine the parts of the infinite date, the result will be `NULL`.