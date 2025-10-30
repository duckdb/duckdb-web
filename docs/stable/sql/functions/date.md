---
layout: docu
redirect_from:
- /docs/test/functions/date
- /docs/test/functions/date/
- /docs/sql/functions/date
title: Date Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions and operators for examining and manipulating [`DATE`]({% link docs/stable/sql/data_types/date.md %}) values.

## Date Operators

The table below shows the available mathematical operators for `DATE` types.

| Operator | Description | Example | Result |
|:-|:--|:---|:--|
| `+` | addition of days (integers) | `DATE '1992-03-22' + 5` | `1992-03-27` |
| `+` | addition of an `INTERVAL` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27 00:00:00` |
| `+` | addition of a variable `INTERVAL` | `SELECT DATE '1992-03-22' + INTERVAL (d.days) DAY FROM (VALUES (5), (11)) d(days)` | `1992-03-27 00:00:00` and `1992-04-02 00:00:00` |
| `-` | subtraction of `DATE`s | `DATE '1992-03-27' - DATE '1992-03-22'` | `5` |
| `-` | subtraction of an `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22 00:00:00` |
| `-` | subtraction of a variable `INTERVAL` | `SELECT DATE '1992-03-27' - INTERVAL (d.days) DAY FROM (VALUES (5), (11)) d(days)` | `1992-03-22 00:00:00` and `1992-03-16 00:00:00` |

Adding to or subtracting from [infinite values]({% link docs/stable/sql/data_types/date.md %}#special-values) produces the same infinite value.

## Date Functions

The table below shows the available functions for `DATE` types.
Dates can also be manipulated with the [timestamp functions]({% link docs/stable/sql/functions/timestamp.md %}) through type promotion.

| Name | Description |
|:--|:-------|
| [`date_add(date, interval)`](#date_adddate-interval) | Add the interval to the date and return a `DATETIME` value. |
| [`date_diff(part, startdate, startdate)`](#date_diffpart-startdate-enddate) | The number of [`part`]({% link docs/stable/sql/functions/datepart.md %}) boundaries between `startdate` and `enddate`, inclusive of the larger date and exclusive of the smaller date. |
| [`date_part(part, date)`](#date_partpart-date) | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) (equivalent to `extract`). |
| [`date_sub(part, startdate, enddate)`](#date_subpart-startdate-enddate) | The signed length of the interval between `startdate` and `enddate`, truncated to whole multiples of [`part`]({% link docs/stable/sql/functions/datepart.md %}). |
| [`date_trunc(part, date)`](#date_truncpart-date) | Truncate to specified [precision]({% link docs/stable/sql/functions/datepart.md %}). |
| [`dayname(date)`](#daynamedate) | The (English) name of the weekday. |
| [`extract(part from date)`](#extractpart-from-date) | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) from a date. |
| [`greatest(date, date)`](#greatestdate-date) | The later of two dates. |
| [`isfinite(date)`](#isfinitedate) | Returns true if the date is finite, false otherwise. |
| [`isinf(date)`](#isinfdate) | Returns true if the date is infinite, false otherwise. |
| [`julian(date)`](#juliandate) | Extract the Julian Day number from a date. |
| [`last_day(date)`](#last_daydate) | The last day of the corresponding month in the date. |
| [`least(date, date)`](#leastdate-date) | The earlier of two dates. |
| [`make_date(year, month, day)`](#make_dateyear-month-day) | The date for the given parts. |
| [`monthname(date)`](#monthnamedate) | The (English) name of the month. |
| [`strftime(date, format)`](#strftimedate-format) | Converts a date to a string according to the [format string]({% link docs/stable/sql/functions/dateformat.md %}). |
| [`time_bucket(bucket_width, date[, offset])`](#time_bucketbucket_width-date-offset) | Truncate `date` to a grid of width `bucket_width`. The grid is anchored at `2000-01-01[ + offset]` when `bucket_width` is a number of months or coarser units, else `2000-01-03[ + offset]`. Note that `2000-01-03` is a Monday. |
| [`time_bucket(bucket_width, date[, origin])`](#time_bucketbucket_width-date-origin) | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01` when `bucket_width` is a number of months or coarser units, else `2000-01-03`. Note that `2000-01-03` is a Monday. |
| [`today()`](#today) | Current date (start of current transaction) in the local time zone. |

#### `date_add(date, interval)`

<div class="nostroke_table"></div>

| **Description** | Add the interval to the date and return a `DATETIME` value. |
| **Example** | `date_add(DATE '1992-09-15', INTERVAL 2 MONTH)` |
| **Result** | `1992-11-15 00:00:00` |

#### `date_diff(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **Description** | The number of [`part`]({% link docs/stable/sql/functions/datepart.md %}) boundaries between `startdate` and `enddate`, inclusive of the larger date and exclusive of the smaller date. |
| **Example** | `date_diff('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **Result** | `2` |
| **Alias** | `datediff` |

#### `date_part(part, date)`

<div class="nostroke_table"></div>

| **Description** | Get the [subfield]({% link docs/stable/sql/functions/datepart.md %}) (equivalent to `extract`). |
| **Example** | `date_part('year', DATE '1992-09-20')` |
| **Result** | `1992` |
| **Alias** | `datepart` |

#### `date_sub(part, startdate, enddate)`

<div class="nostroke_table"></div>

| **Description** | The signed length of the interval between `startdate` and `enddate`, truncated to whole multiples of [`part`]({% link docs/stable/sql/functions/datepart.md %}). |
| **Example** | `date_sub('month', DATE '1992-09-15', DATE '1992-11-14')` |
| **Result** | `1` |
| **Alias** | `datesub` |

#### `date_trunc(part, date)`

<div class="nostroke_table"></div>

| **Description** | Truncate to specified [precision]({% link docs/stable/sql/functions/datepart.md %}). |
| **Example** | `date_trunc('month', DATE '1992-03-07')` |
| **Result** | `1992-03-01` |
| **Alias** | `datetrunc` |

#### `dayname(date)`

<div class="nostroke_table"></div>

| **Description** | The (English) name of the weekday. |
| **Example** | `dayname(DATE '1992-09-20')` |
| **Result** | `Sunday` |

#### `extract(part from date)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) from a date. |
| **Example** | `extract('year' FROM DATE '1992-09-20')` |
| **Result** | `1992` |

#### `greatest(date, date)`

<div class="nostroke_table"></div>

| **Description** | The later of two dates. |
| **Example** | `greatest(DATE '1992-09-20', DATE '1992-03-07')` |
| **Result** | `1992-09-20` |

#### `isfinite(date)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the date is finite, false otherwise. |
| **Example** | `isfinite(DATE '1992-03-07')` |
| **Result** | `true` |

#### `isinf(date)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if the date is infinite, false otherwise. |
| **Example** | `isinf(DATE '-infinity')` |
| **Result** | `true` |

#### `julian(date)`

<div class="nostroke_table"></div>

| **Description** | Extract the Julian Day number from a date. |
| **Example** | `julian(DATE '1992-09-20')` |
| **Result** | `2448886.0` |

#### `last_day(date)`

<div class="nostroke_table"></div>

| **Description** | The last day of the corresponding month in the date. |
| **Example** | `last_day(DATE '1992-09-20')` |
| **Result** | `1992-09-30` |

#### `least(date, date)`

<div class="nostroke_table"></div>

| **Description** | The earlier of two dates. |
| **Example** | `least(DATE '1992-09-20', DATE '1992-03-07')` |
| **Result** | `1992-03-07` |

#### `make_date(year, month, day)`

<div class="nostroke_table"></div>

| **Description** | The date for the given parts. |
| **Example** | `make_date(1992, 9, 20)` |
| **Result** | `1992-09-20` |

#### `monthname(date)`

<div class="nostroke_table"></div>

| **Description** | The (English) name of the month. |
| **Example** | `monthname(DATE '1992-09-20')` |
| **Result** | `September` |

#### `strftime(date, format)`

<div class="nostroke_table"></div>

| **Description** | Converts a date to a string according to the [format string]({% link docs/stable/sql/functions/dateformat.md %}). |
| **Example** | `strftime(DATE '1992-01-01', '%a, %-d %B %Y')` |
| **Result** | `Wed, 1 January 1992` |

#### `time_bucket(bucket_width, date[, offset])`

<div class="nostroke_table"></div>

| **Description** | Truncate `date` to a grid of width `bucket_width`. The grid is anchored at `2000-01-01[ + offset]` when `bucket_width` is a number of months or coarser units, else `2000-01-03[ + offset]`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '2 months', DATE '1992-04-20', INTERVAL '1 month')` |
| **Result** | `1992-04-01` |

#### `time_bucket(bucket_width, date[, origin])`

<div class="nostroke_table"></div>

| **Description** | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01` when `bucket_width` is a number of months or coarser units, else `2000-01-03`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '2 weeks', DATE '1992-04-20', DATE '1992-04-01')` |
| **Result** | `1992-04-15` |

#### `today()`

<div class="nostroke_table"></div>

| **Description** | Current date (start of current transaction) in the local time zone. |
| **Example** | `today()` |
| **Result** | `2022-10-08` |
| **Alias** | `current_date` (no parentheses necessary) |

## Date Part Extraction Functions

There are also dedicated extraction functions to get the [subfields]({% link docs/stable/sql/functions/datepart.md %}#part-functions).
A few examples include extracting the day from a date, or the day of the week from a date.

Functions applied to infinite dates will either return the same infinite dates
(e.g., `greatest`) or `NULL` (e.g., `date_part`) depending on what “makes sense”.
In general, if the function needs to examine the parts of the infinite date, the result will be `NULL`.
