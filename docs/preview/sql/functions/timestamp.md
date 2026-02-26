---
layout: docu
title: Timestamp Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions and operators for examining and manipulating [`TIMESTAMP` values]({% link docs/preview/sql/data_types/timestamp.md %}).
See also the related [`TIMESTAMPTZ` functions]({% link docs/preview/sql/functions/timestamptz.md %}).

## Timestamp Operators

The table below shows the available mathematical operators for `TIMESTAMP` types.

| Operator | Description | Example | Result |
|:-|:--|:----|:--|
| `+` | addition of an `INTERVAL` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `-` | subtraction of `TIMESTAMP`s | `TIMESTAMP '1992-03-27' - TIMESTAMP '1992-03-22'` | `5 days` |
| `-` | subtraction of an `INTERVAL` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |

Adding to or subtracting from [infinite values]({% link docs/preview/sql/data_types/timestamp.md %}#special-values) produces the same infinite value.

## Scalar Timestamp Functions

The table below shows the available scalar functions for `TIMESTAMP` values.

| Name | Description |
|:--|:-------|
| [`age(timestamp, timestamp)`](#agetimestamp-timestamp) | Subtract arguments, resulting in the time difference between the two timestamps. |
| [`age(timestamp)`](#agetimestamp) | Subtract from current_date. |
| [`ago(interval)`](#agointerval) | Subtracts an interval from the current timestamp. |
| [`century(timestamp)`](#centurytimestamp) | Extracts the century of a timestamp. |
| [`current_localtimestamp()`](#current_localtimestamp) | Returns the current timestamp (at the start of the transaction). |
| [`date_diff(part, starttimestamp, endtimestamp)`](#date_diffpart-starttimestamp-endtimestamp) | The number of [`part`]({% link docs/preview/sql/functions/datepart.md %}) boundaries between `starttimestamp` and `endtimestamp`, inclusive of the larger timestamp and exclusive of the smaller timestamp. |
| [`date_part([part, ...], timestamp)`](#date_partpart--timestamp) | Get the listed [subfields]({% link docs/preview/sql/functions/datepart.md %}) as a `struct`. The list must be constant. |
| [`date_part(part, timestamp)`](#date_partpart-timestamp) | Get [subfield]({% link docs/preview/sql/functions/datepart.md %}) (equivalent to `extract`). |
| [`date_sub(part, starttimestamp, endtimestamp)`](#date_subpart-starttimestamp-endtimestamp) | The signed length of the interval between `starttimestamp` and `endtimestamp`, truncated to whole multiples of [`part`]({% link docs/preview/sql/functions/datepart.md %}). |
| [`date_trunc(part, timestamp)`](#date_truncpart-timestamp) | Truncate to specified [precision]({% link docs/preview/sql/functions/datepart.md %}). |
| [`dayname(timestamp)`](#daynametimestamp) | The (English) name of the weekday. |
| [`epoch_ms(timestamp)`](#epoch_mstimestamp) | Returns the total number of milliseconds since the epoch. |
| [`epoch_ns(timestamp)`](#epoch_nstimestamp) | Returns the total number of nanoseconds since the epoch. |
| [`epoch_us(timestamp)`](#epoch_ustimestamp) | Returns the total number of microseconds since the epoch. |
| [`epoch(timestamp)`](#epochtimestamp) | Returns the total number of seconds since the epoch. |
| [`extract(field FROM timestamp)`](#extractfield-from-timestamp) | Get [subfield]({% link docs/preview/sql/functions/datepart.md %}) from a timestamp. |
| [`greatest(timestamp, timestamp)`](#greatesttimestamp-timestamp) | The later of two timestamps. |
| [`isfinite(timestamp)`](#isfinitetimestamp) | Returns true if the timestamp is finite, false otherwise. |
| [`isinf(timestamp)`](#isinftimestamp) | Returns true if the timestamp is infinite, false otherwise. |
| [`julian(timestamp)`](#juliantimestamp) | Extract the Julian Day number from a timestamp. |
| [`last_day(timestamp)`](#last_daytimestamp) | The last day of the month. |
| [`least(timestamp, timestamp)`](#leasttimestamp-timestamp) | The earlier of two timestamps. |
| [`make_timestamp(bigint, bigint, bigint, bigint, bigint, double)`](#make_timestampbigint-bigint-bigint-bigint-bigint-double) | The timestamp for the given parts. |
| [`make_timestamp(microseconds)`](#make_timestampmicroseconds) | Converts microseconds since the epoch to a timestamp. |
| [`make_timestamp_ms(milliseconds)`](#make_timestamp_msmilliseconds) | Converts milliseconds since the epoch to a timestamp. |
| [`make_timestamp_ns(nanoseconds)`](#make_timestamp_nsnanoseconds) | Converts nanoseconds since the epoch to a timestamp. |
| [`monthname(timestamp)`](#monthnametimestamp) | The (English) name of the month. |
| [`strftime(timestamp, format)`](#strftimetimestamp-format) | Converts timestamp to string according to the [format string]({% link docs/preview/sql/functions/dateformat.md %}#format-specifiers). |
| [`strptime(text, format-list)`](#strptimetext-format-list) | Converts the string `text` to timestamp applying the [format strings]({% link docs/preview/sql/functions/dateformat.md %}) in the list until one succeeds. Throws an error on failure. To return `NULL` on failure, use [`try_strptime`](#try_strptimetext-format-list). |
| [`strptime(text, format)`](#strptimetext-format) | Converts the string `text` to timestamp according to the [format string]({% link docs/preview/sql/functions/dateformat.md %}#format-specifiers). Throws an error on failure. To return `NULL` on failure, use [`try_strptime`](#try_strptimetext-format). |
| [`time_bucket(bucket_width, timestamp[, offset])`](#time_bucketbucket_width-timestamp-offset) | Truncate `timestamp` to a grid of width `bucket_width`. The grid is anchored at `2000-01-01 00:00:00[ + offset]` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00[ + offset]`. Note that `2000-01-03` is a Monday. |
| [`time_bucket(bucket_width, timestamp[, origin])`](#time_bucketbucket_width-timestamp-origin) | Truncate `timestamp` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01 00:00:00` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00`. Note that `2000-01-03` is a Monday. |
| [`try_strptime(text, format-list)`](#try_strptimetext-format-list) | Converts the string `text` to timestamp applying the [format strings]({% link docs/preview/sql/functions/dateformat.md %}) in the list until one succeeds. Returns `NULL` on failure. |
| [`try_strptime(text, format)`](#try_strptimetext-format) | Converts the string `text` to timestamp according to the [format string]({% link docs/preview/sql/functions/dateformat.md %}#format-specifiers). Returns `NULL` on failure. |

There are also dedicated extraction functions to get the [subfields]({% link docs/preview/sql/functions/datepart.md %}).

Functions applied to infinite dates will either return the same infinite dates
(e.g., `greatest`) or `NULL` (e.g., `date_part`) depending on what “makes sense”.
In general, if the function needs to examine the parts of the infinite date, the result will be `NULL`.

#### `age(timestamp, timestamp)`

<div class="nostroke_table"></div>

| **Description** | Subtract arguments, resulting in the time difference between the two timestamps. |
| **Example** | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20')` |
| **Result** | `8 years 6 months 20 days` |

#### `age(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Subtract from current_date. |
| **Example** | `age(TIMESTAMP '1992-09-20')` |
| **Result** | `29 years 1 month 27 days 12:39:00.844` |

#### `ago(interval)`

<div class="nostroke_table"></div>

| **Description** | Subtracts an interval from the current timestamp, returning a timestamp in the past. Equivalent to `current_timestamp - interval`. |
| **Example** | `ago(INTERVAL 1 HOUR)` |
| **Result** | `2024-11-30 12:28:48.895` (if current time is `2024-11-30 13:28:48.895`) |

#### `century(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Extracts the century of a timestamp. |
| **Example** | `century(TIMESTAMP '1992-03-22')` |
| **Result** | `20` |

#### `current_localtimestamp()`

<div class="nostroke_table"></div>

| **Description** | Returns the current timestamp with time zone (at the start of the transaction). |
| **Example** | `current_localtimestamp()` |
| **Result** | `2024-11-30 13:28:48.895` |

#### `date_diff(part, starttimestamp, endtimestamp)`

<div class="nostroke_table"></div>

| **Description** | The signed number of [`part`]({% link docs/preview/sql/functions/datepart.md %}) boundaries between `starttimestamp` and `endtimestamp`, inclusive of the larger timestamp and exclusive of the smaller timestamp. |
| **Example** | `date_diff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` |
| **Result** | `2` |

#### `date_part([part, ...], timestamp)`

<div class="nostroke_table"></div>

| **Description** | Get the listed [subfields]({% link docs/preview/sql/functions/datepart.md %}) as a `struct`. The list must be constant. |
| **Example** | `date_part(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` |
| **Result** | `{year: 1992, month: 9, day: 20}` |

#### `date_part(part, timestamp)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield]({% link docs/preview/sql/functions/datepart.md %}) (equivalent to `extract`). |
| **Example** | `date_part('minute', TIMESTAMP '1992-09-20 20:38:40')` |
| **Result** | `38` |

#### `date_sub(part, starttimestamp, endtimestamp)`

<div class="nostroke_table"></div>

| **Description** | The signed length of the interval between `starttimestamp` and `endtimestamp`, truncated to whole multiples of [`part`]({% link docs/preview/sql/functions/datepart.md %}). |
| **Example** | `date_sub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` |
| **Result** | `1` |

#### `date_trunc(part, timestamp)`

<div class="nostroke_table"></div>

| **Description** | Truncate to specified [precision]({% link docs/preview/sql/functions/datepart.md %}). |
| **Example** | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` |
| **Result** | `1992-09-20 20:00:00` |

#### `dayname(timestamp)`

<div class="nostroke_table"></div>

| **Description** | The (English) name of the weekday. |
| **Example** | `dayname(TIMESTAMP '1992-03-22')` |
| **Result** | `Sunday` |

#### `epoch_ms(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Returns the total number of milliseconds since the epoch. |
| **Example** | `epoch_ms(TIMESTAMP '2021-08-03 11:59:44.123456')` |
| **Result** | `1627991984123` |

#### `epoch_ns(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Returns the total number of nanoseconds since the epoch. |
| **Example** | `epoch_ns(TIMESTAMP '2021-08-03 11:59:44.123456')` |
| **Result** | `1627991984123456000` |

#### `epoch_us(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Returns the total number of microseconds since the epoch. |
| **Example** | `epoch_us(TIMESTAMP '2021-08-03 11:59:44.123456')` |
| **Result** | `1627991984123456` |

#### `epoch(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Returns the total number of seconds since the epoch. |
| **Example** | `epoch('2022-11-07 08:43:04'::TIMESTAMP);` |
| **Result** | `1667810584` |

#### `extract(field FROM timestamp)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield]({% link docs/preview/sql/functions/datepart.md %}) from a timestamp. |
| **Example** | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` |
| **Result** | `20` |

#### `greatest(timestamp, timestamp)`

<div class="nostroke_table"></div>

| **Description** | The later of two timestamps. |
| **Example** | `greatest(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **Result** | `1992-09-20 20:38:48` |

#### `isfinite(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the timestamp is finite, false otherwise. |
| **Example** | `isfinite(TIMESTAMP '1992-03-07')` |
| **Result** | `true` |

#### `isinf(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the timestamp is infinite, false otherwise. |
| **Example** | `isinf(TIMESTAMP '-infinity')` |
| **Result** | `true` |

#### `julian(timestamp)`

<div class="nostroke_table"></div>

| **Description** | Extract the Julian Day number from a timestamp. |
| **Example** | `julian(TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **Result** | `2448704.043091706` |

#### `last_day(timestamp)`

<div class="nostroke_table"></div>

| **Description** | The last day of the month. |
| **Example** | `last_day(TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **Result** | `1992-03-31` |

#### `least(timestamp, timestamp)`

<div class="nostroke_table"></div>

| **Description** | The earlier of two timestamps. |
| **Example** | `least(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` |
| **Result** | `1992-03-22 01:02:03.1234` |

#### `make_timestamp(bigint, bigint, bigint, bigint, bigint, double)`

<div class="nostroke_table"></div>

| **Description** | The timestamp for the given parts. |
| **Example** | `make_timestamp(1992, 9, 20, 13, 34, 27.123456)` |
| **Result** | `1992-09-20 13:34:27.123456` |

#### `make_timestamp(microseconds)`

<div class="nostroke_table"></div>

| **Description** | Converts microseconds since the epoch to a timestamp. |
| **Example** | `make_timestamp(1667810584123456)` |
| **Result** | `2022-11-07 08:43:04.123456` |

#### `make_timestamp_ms(milliseconds)`

<div class="nostroke_table"></div>

| **Description** | Converts milliseconds since the epoch to a timestamp. |
| **Example** | `make_timestamp(1667810584123)` |
| **Result** | `2022-11-07 08:43:04.123` |

#### `make_timestamp_ns(nanoseconds)`

<div class="nostroke_table"></div>

| **Description** | Converts nanoseconds since the epoch to a timestamp. |
| **Example** | `make_timestamp_ns(1667810584123456789)` |
| **Result** | `2022-11-07 08:43:04.123456789` |

#### `monthname(timestamp)`

<div class="nostroke_table"></div>

| **Description** | The (English) name of the month. |
| **Example** | `monthname(TIMESTAMP '1992-09-20')` |
| **Result** | `September` |

#### `strftime(timestamp, format)`

<div class="nostroke_table"></div>

| **Description** | Converts timestamp to string according to the [format string]({% link docs/preview/sql/functions/dateformat.md %}#format-specifiers). |
| **Example** | `strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **Result** | `Wed, 1 January 1992 - 08:38:40 PM` |

#### `strptime(text, format-list)`

<div class="nostroke_table"></div>

| **Description** | Converts the string `text` to timestamp applying the [format strings]({% link docs/preview/sql/functions/dateformat.md %}) in the list until one succeeds. Throws an error on failure. To return `NULL` on failure, use [`try_strptime`](#try_strptimetext-format-list). |
| **Example** | `strptime('4/15/2023 10:56:00', ['%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'])` |
| **Result** | `2023-04-15 10:56:00` |

#### `strptime(text, format)`

<div class="nostroke_table"></div>

| **Description** | Converts the string `text` to timestamp according to the [format string]({% link docs/preview/sql/functions/dateformat.md %}#format-specifiers). Throws an error on failure. To return `NULL` on failure, use [`try_strptime`](#try_strptimetext-format). |
| **Example** | `strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **Result** | `1992-01-01 20:38:40` |

#### `time_bucket(bucket_width, timestamp[, offset])`

<div class="nostroke_table"></div>

| **Description** | Truncate `timestamp` to a grid of width `bucket_width`. The grid includes `2000-01-01 00:00:00[ + offset]` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00[ + offset]`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '10 minutes', TIMESTAMP '1992-04-20 15:26:00-07', INTERVAL '5 minutes')` |
| **Result** | `1992-04-20 15:25:00` |

#### `time_bucket(bucket_width, timestamp[, origin])`

<div class="nostroke_table"></div>

| **Description** | Truncate `timestamp` to a grid of width `bucket_width`. The grid includes the `origin` timestamp, which defaults to `2000-01-01 00:00:00` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '2 weeks', TIMESTAMP '1992-04-20 15:26:00', TIMESTAMP '1992-04-01 00:00:00')` |
| **Result** | `1992-04-15 00:00:00` |

#### `try_strptime(text, format-list)`

<div class="nostroke_table"></div>

| **Description** | Converts the string `text` to timestamp applying the [format strings]({% link docs/preview/sql/functions/dateformat.md %}) in the list until one succeeds. Returns `NULL` on failure. |
| **Example** | `try_strptime('4/15/2023 10:56:00', ['%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'])` |
| **Result** | `2023-04-15 10:56:00` |

#### `try_strptime(text, format)`

<div class="nostroke_table"></div>

| **Description** | Converts the string `text` to timestamp according to the [format string]({% link docs/preview/sql/functions/dateformat.md %}#format-specifiers). Returns `NULL` on failure. |
| **Example** | `try_strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **Result** | `1992-01-01 20:38:40` |

## Timestamp Table Functions

The table below shows the available table functions for `TIMESTAMP` types.

| Name | Description |
|:--|:-------|
| [`generate_series(timestamp, timestamp, interval)`](#generate_seriestimestamp-timestamp-interval) | Generate a table of timestamps in the closed range, stepping by the interval. |
| [`range(timestamp, timestamp, interval)`](#rangetimestamp-timestamp-interval) | Generate a table of timestamps in the half open range, stepping by the interval. |

> Infinite values are not allowed as table function bounds.

#### `generate_series(timestamp, timestamp, interval)`

<div class="nostroke_table"></div>

| **Description** | Generate a table of timestamps in the closed range, stepping by the interval. |
| **Example** | `generate_series(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)` |

#### `range(timestamp, timestamp, interval)`

<div class="nostroke_table"></div>

| **Description** | Generate a table of timestamps in the half open range, stepping by the interval. |
| **Example** | `range(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)` |
