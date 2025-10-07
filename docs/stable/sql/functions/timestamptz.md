---
layout: docu
redirect_from:
- /docs/sql/functions/timestamptz
title: Timestamp with Time Zone Functions
---

<!-- markdownlint-disable MD001 -->

This section describes functions and operators for examining and manipulating [`TIMESTAMP WITH TIME ZONE`
(or `TIMESTAMPTZ`) values]({% link docs/stable/sql/data_types/timestamp.md %}). See also the related [`TIMESTAMP` functions]({% link docs/stable/sql/functions/timestamp.md %}).

Time zone support is provided by the built-in [ICU extension]({% link docs/stable/core_extensions/icu.md %}).

In the examples below, the current time zone is presumed to be `America/Los_Angeles`
using the Gregorian calendar.

## Built-In Timestamp with Time Zone Functions

The table below shows the available scalar functions for `TIMESTAMPTZ` values.
Since these functions do not involve binning or display,
they are always available.

| Name | Description |
|:--|:-------|
| [`current_timestamp`](#current_timestamp) | Current date and time (start of current transaction). |
| [`get_current_timestamp()`](#get_current_timestamp) | Current date and time (start of current transaction). |
| [`greatest(timestamptz, timestamptz)`](#greatesttimestamptz-timestamptz) | The later of two timestamps. |
| [`isfinite(timestamptz)`](#isfinitetimestamptz) | Returns true if the timestamp with time zone is finite, false otherwise. |
| [`isinf(timestamptz)`](#isinftimestamptz) | Returns true if the timestamp with time zone is infinite, false otherwise. |
| [`least(timestamptz, timestamptz)`](#leasttimestamptz-timestamptz) | The earlier of two timestamps. |
| [`now()`](#now) | Current date and time (start of current transaction). |
| [`timetz_byte_comparable(timetz)`](#timetz_byte_comparabletimetz) | Converts a `TIME WITH TIME ZONE` to a `UBIGINT` sort key. |
| [`to_timestamp(double)`](#to_timestampdouble) | Converts seconds since the epoch to a timestamp with time zone. |
| [`transaction_timestamp()`](#transaction_timestamp) | Current date and time (start of current transaction). |

#### `current_timestamp`

<div class="nostroke_table"></div>

| **Description** | Current date and time (start of current transaction). |
| **Example** | `current_timestamp` |
| **Result** | `2022-10-08 12:44:46.122-07` |

#### `get_current_timestamp()`

<div class="nostroke_table"></div>

| **Description** | Current date and time (start of current transaction). |
| **Example** | `get_current_timestamp()` |
| **Result** | `2022-10-08 12:44:46.122-07` |

#### `greatest(timestamptz, timestamptz)`

<div class="nostroke_table"></div>

| **Description** | The later of two timestamps. |
| **Example** | `greatest(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` |
| **Result** | `1992-09-20 20:38:48-07` |

#### `isfinite(timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the timestamp with time zone is finite, false otherwise. |
| **Example** | `isfinite(TIMESTAMPTZ '1992-03-07')` |
| **Result** | `true` |

#### `isinf(timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Returns true if the timestamp with time zone is infinite, false otherwise. |
| **Example** | `isinf(TIMESTAMPTZ '-infinity')` |
| **Result** | `true` |

#### `least(timestamptz, timestamptz)`

<div class="nostroke_table"></div>

| **Description** | The earlier of two timestamps. |
| **Example** | `least(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` |
| **Result** | `1992-03-22 01:02:03.1234-08` |

#### `now()`

<div class="nostroke_table"></div>

| **Description** | Current date and time (start of current transaction). |
| **Example** | `now()` |
| **Result** | `2022-10-08 12:44:46.122-07` |

#### `timetz_byte_comparable(timetz)`

<div class="nostroke_table"></div>

| **Description** | Converts a `TIME WITH TIME ZONE` to a `UBIGINT` sort key. |
| **Example** | `timetz_byte_comparable('18:18:16.21-07:00'::TIMETZ)` |
| **Result** | `2494691656335442799` |

#### `to_timestamp(double)`

<div class="nostroke_table"></div>

| **Description** | Converts seconds since the epoch to a timestamp with time zone. |
| **Example** | `to_timestamp(1284352323.5)` |
| **Result** | `2010-09-13 04:32:03.5+00` |

#### `transaction_timestamp()`

<div class="nostroke_table"></div>

| **Description** | Current date and time (start of current transaction). |
| **Example** | `transaction_timestamp()` |
| **Result** | `2022-10-08 12:44:46.122-07` |

## Timestamp with Time Zone Strings

With no time zone extension loaded, `TIMESTAMPTZ` values will be cast to and from strings
using offset notation.
This will let you specify an instant correctly without access to time zone information.
For portability, `TIMESTAMPTZ` values will always be displayed using GMT offsets:

```sql
SELECT '2022-10-08 13:13:34-07'::TIMESTAMPTZ;
```

```text
2022-10-08 20:13:34+00
```

If a time zone extension such as ICU is loaded, then a time zone can be parsed from a string
and cast to a representation in the local time zone:

```sql
SELECT '2022-10-08 13:13:34 Europe/Amsterdam'::TIMESTAMPTZ::VARCHAR;
```

```text
2022-10-08 04:13:34-07 -- the offset will differ based on your local time zone
```

## ICU Timestamp with Time Zone Operators

The table below shows the available mathematical operators for `TIMESTAMP WITH TIME ZONE` values
provided by the ICU extension.

| Operator | Description | Example | Result |
|:-|:--|:----|:--|
| `+` | addition of an `INTERVAL` | `TIMESTAMPTZ '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `-` | subtraction of `TIMESTAMPTZ`s | `TIMESTAMPTZ '1992-03-27' - TIMESTAMPTZ '1992-03-22'` | `5 days` |
| `-` | subtraction of an `INTERVAL` | `TIMESTAMPTZ '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |

Adding to or subtracting from [infinite values]({% link docs/stable/sql/data_types/timestamp.md %}#special-values) produces the same infinite value.

## ICU Timestamp with Time Zone Functions

The table below shows the ICU provided scalar functions for `TIMESTAMP WITH TIME ZONE` values.

| Name | Description |
|:--|:-------|
| [`age(timestamptz, timestamptz)`](#agetimestamptz-timestamptz) | Subtract arguments, resulting in the time difference between the two timestamps. |
| [`age(timestamptz)`](#agetimestamptz) | Subtract from current_date. |
| [`date_diff(part, starttimestamptz, endtimestamptz)`](#date_diffpart-starttimestamptz-endtimestamptz) | The number of [`part`]({% link docs/stable/sql/functions/datepart.md %}) boundaries between `starttimestamptz` and `endtimestamptz` inclusive of the larger timstamp and exclusive of the smaller timestamp. |
| [`date_part([part, ...], timestamp)`](#date_partpart--timestamptz) | Get the listed [subfields]({% link docs/stable/sql/functions/datepart.md %}) as a `struct`. The list must be constant. |
| [`date_part(part, timestamp)`](#date_partpart-timestamptz) | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) (equivalent to `extract`). |
| [`date_sub(part, starttimestamptz, endtimestamptz)`](#date_subpart-starttimestamptz-endtimestamptz) | The signed length of the interval between `starttimestamptz` and `endtimestamptz`, truncated to whole multiples of [`part`]({% link docs/stable/sql/functions/datepart.md %}). |
| [`date_trunc(part, timestamptz)`](#date_truncpart-timestamptz) | Truncate to specified [precision]({% link docs/stable/sql/functions/datepart.md %}). |
| [`epoch_ns(timestamptz)`](#epoch_nstimestamptz) | Converts a timestamptz to nanoseconds since the epoch. |
| [`epoch_us(timestamptz)`](#epoch_ustimestamptz) | Converts a timestamptz to microseconds since the epoch. |
| [`extract(field FROM timestamptz)`](#extractfield-from-timestamptz) | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) from a `TIMESTAMP WITH TIME ZONE`. |
| [`last_day(timestamptz)`](#last_daytimestamptz) | The last day of the month. |
| [`make_timestamptz(bigint, bigint, bigint, bigint, bigint, double, string)`](#make_timestamptzbigint-bigint-bigint-bigint-bigint-double-string) | The `TIMESTAMP WITH TIME ZONE` for the given parts and time zone. |
| [`make_timestamptz(bigint, bigint, bigint, bigint, bigint, double)`](#make_timestamptzbigint-bigint-bigint-bigint-bigint-double) | The `TIMESTAMP WITH TIME ZONE` for the given parts in the current time zone. |
| [`make_timestamptz(microseconds)`](#make_timestamptzmicroseconds) | The `TIMESTAMP WITH TIME ZONE` for the given µs since the epoch. |
| [`strftime(timestamptz, format)`](#strftimetimestamptz-format) | Converts a `TIMESTAMP WITH TIME ZONE` value to string according to the [format string]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers). |
| [`strptime(text, format)`](#strptimetext-format) | Converts string to `TIMESTAMP WITH TIME ZONE` according to the [format string]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) if `%Z` is specified. |
| [`time_bucket(bucket_width, timestamptz[, offset])`](#time_bucketbucket_width-timestamptz-offset) | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at `2000-01-01 00:00:00+00:00[ + offset]` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00+00:00[ + offset]`. Note that `2000-01-03` is a Monday. |
| [`time_bucket(bucket_width, timestamptz[, origin])`](#time_bucketbucket_width-timestamptz-origin) | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01 00:00:00+00:00` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00+00:00`. Note that `2000-01-03` is a Monday. |
| [`time_bucket(bucket_width, timestamptz[, timezone])`](#time_bucketbucket_width-timestamptz-origin) | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01 00:00:00` in the provided `timezone` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00` in the provided `timezone`. The default timezone is `'UTC'`. Note that `2000-01-03` is a Monday. |



#### `age(timestamptz, timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Subtract arguments, resulting in the time difference between the two timestamps. |
| **Example** | `age(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '1992-09-20')` |
| **Result** | `8 years 6 months 20 days` |

#### `age(timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Subtract from current_date. |
| **Example** | `age(TIMESTAMP '1992-09-20')` |
| **Result** | `29 years 1 month 27 days 12:39:00.844` |

#### `date_diff(part, starttimestamptz, endtimestamptz)`

<div class="nostroke_table"></div>

| **Description** | The signed number of [`part`]({% link docs/stable/sql/functions/datepart.md %}) boundaries between `starttimestamptz` and `endtimestamptz`, inclusive of the larger timestamp and exclusive of the smaller timestamp. |
| **Example** | `date_diff('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` |
| **Result** | `2` |

#### `date_part([part, ...], timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Get the listed [subfields]({% link docs/stable/sql/functions/datepart.md %}) as a `struct`. The list must be constant. |
| **Example** | `date_part(['year', 'month', 'day'], TIMESTAMPTZ '1992-09-20 20:38:40-07')` |
| **Result** | `{year: 1992, month: 9, day: 20}` |

#### `date_part(part, timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) (equivalent to *extract*). |
| **Example** | `date_part('minute', TIMESTAMPTZ '1992-09-20 20:38:40')` |
| **Result** | `38` |

#### `date_sub(part, starttimestamptz, endtimestamptz)`

<div class="nostroke_table"></div>

| **Description** | The signed length of the interval between `starttimestamptz` and `endtimestamptz`, truncated to whole multiples of [`part`]({% link docs/stable/sql/functions/datepart.md %}). |
| **Example** | `date_sub('hour', TIMESTAMPTZ '1992-09-30 23:59:59', TIMESTAMPTZ '1992-10-01 01:58:00')` |
| **Result** | `1` |

#### `date_trunc(part, timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Truncate to specified [precision]({% link docs/stable/sql/functions/datepart.md %}). |
| **Example** | `date_trunc('hour', TIMESTAMPTZ '1992-09-20 20:38:40')` |
| **Result** | `1992-09-20 20:00:00` |

#### `epoch_ns(timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Converts a timestamptz to nanoseconds since the epoch. |
| **Example** | `epoch_ns('2022-11-07 08:43:04.123456+00'::TIMESTAMPTZ);` |
| **Result** | `1667810584123456000` |

#### `epoch_us(timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Converts a timestamptz to microseconds since the epoch. |
| **Example** | `epoch_us('2022-11-07 08:43:04.123456+00'::TIMESTAMPTZ);` |
| **Result** | `1667810584123456` |

#### `extract(field FROM timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield]({% link docs/stable/sql/functions/datepart.md %}) from a `TIMESTAMP WITH TIME ZONE`. |
| **Example** | `extract('hour' FROM TIMESTAMPTZ '1992-09-20 20:38:48')` |
| **Result** | `20` |

#### `last_day(timestamptz)`

<div class="nostroke_table"></div>

| **Description** | The last day of the month. |
| **Example** | `last_day(TIMESTAMPTZ '1992-03-22 01:02:03.1234')` |
| **Result** | `1992-03-31` |

#### `make_timestamptz(bigint, bigint, bigint, bigint, bigint, double, string)`

<div class="nostroke_table"></div>

| **Description** | The `TIMESTAMP WITH TIME ZONE` for the given parts and time zone. |
| **Example** | `make_timestamptz(1992, 9, 20, 15, 34, 27.123456, 'CET')` |
| **Result** | `1992-09-20 06:34:27.123456-07` |

#### `make_timestamptz(bigint, bigint, bigint, bigint, bigint, double)`

<div class="nostroke_table"></div>

| **Description** | The `TIMESTAMP WITH TIME ZONE` for the given parts in the current time zone. |
| **Example** | `make_timestamptz(1992, 9, 20, 13, 34, 27.123456)` |
| **Result** | `1992-09-20 13:34:27.123456-07` |

#### `make_timestamptz(microseconds)`

<div class="nostroke_table"></div>

| **Description** | The `TIMESTAMP WITH TIME ZONE` for the given µs since the epoch. |
| **Example** | `make_timestamptz(1667810584123456)` |
| **Result** | `2022-11-07 16:43:04.123456-08` |

#### `strftime(timestamptz, format)`

<div class="nostroke_table"></div>

| **Description** | Converts a `TIMESTAMP WITH TIME ZONE` value to string according to the [format string]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers). |
| **Example** | `strftime(timestamptz '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` |
| **Result** | `Wed, 1 January 1992 - 08:38:40 PM` |

#### `strptime(text, format)`

<div class="nostroke_table"></div>

| **Description** | Converts string to `TIMESTAMP WITH TIME ZONE` according to the [format string]({% link docs/stable/sql/functions/dateformat.md %}#format-specifiers) if `%Z` is specified. |
| **Example** | `strptime('Wed, 1 January 1992 - 08:38:40 PST', '%a, %-d %B %Y - %H:%M:%S %Z')` |
| **Result** | `1992-01-01 08:38:40-08` |

#### `time_bucket(bucket_width, timestamptz[, offset])`

<div class="nostroke_table"></div>

| **Description** | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at `2000-01-01 00:00:00+00:00[ + offset]` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00+00:00[ + offset]`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '10 minutes', TIMESTAMPTZ '1992-04-20 15:26:00-07', INTERVAL '5 minutes')` |
| **Result** | `1992-04-20 15:25:00-07` |

#### `time_bucket(bucket_width, timestamptz[, origin])`

<div class="nostroke_table"></div>

| **Description** | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01 00:00:00+00:00` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00+00:00`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '2 weeks', TIMESTAMPTZ '1992-04-20 15:26:00-07', TIMESTAMPTZ '1992-04-01 00:00:00-07')` |
| **Result** | `1992-04-15 00:00:00-07` |

#### `time_bucket(bucket_width, timestamptz[, timezone])`

<div class="nostroke_table"></div>

| **Description** | Truncate `timestamptz` to a grid of width `bucket_width`. The grid is anchored at the `origin` timestamp, which defaults to `2000-01-01 00:00:00` in the provided `timezone` when `bucket_width` is a number of months or coarser units, else `2000-01-03 00:00:00` in the provided `timezone`. The default timezone is `'UTC'`. Note that `2000-01-03` is a Monday. |
| **Example** | `time_bucket(INTERVAL '2 days', TIMESTAMPTZ '1992-04-20 15:26:00-07', 'Europe/Berlin')` |
| **Result** | `1992-04-19 15:00:00-07` (=`1992-04-20 00:00:00 Europe/Berlin`) |

There are also dedicated extraction functions to get the [subfields]({% link docs/stable/sql/functions/datepart.md %}).

## ICU Timestamp Table Functions

The table below shows the available table functions for `TIMESTAMP WITH TIME ZONE` types.

| Name | Description |
|:--|:-------|
| [`generate_series(timestamptz, timestamptz, interval)`](#generate_seriestimestamptz-timestamptz-interval) | Generate a table of timestamps in the closed range (including both the starting timestamp and the ending timestamp), stepping by the interval. |
| [`range(timestamptz, timestamptz, interval)`](#rangetimestamptz-timestamptz-interval) | Generate a table of timestamps in the half open range (including the starting timestamp, but stopping before the ending timestamp), stepping by the interval. |

> Infinite values are not allowed as table function bounds.

#### `generate_series(timestamptz, timestamptz, interval)`

<div class="nostroke_table"></div>

| **Description** | Generate a table of timestamps in the closed range (including both the starting timestamp and the ending timestamp), stepping by the interval. |
| **Example** | `generate_series(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '2001-04-11', INTERVAL 30 MINUTE)` |

#### `range(timestamptz, timestamptz, interval)`

<div class="nostroke_table"></div>

| **Description** | Generate a table of timestamps in the half open range (including the starting timestamp, but stopping before the ending timestamp), stepping by the interval. |
| **Example** | `range(TIMESTAMPTZ '2001-04-10', TIMESTAMPTZ '2001-04-11', INTERVAL 30 MINUTE)` |

## ICU Timestamp Without Time Zone Functions

The table below shows the ICU provided scalar functions that operate on plain `TIMESTAMP` values.
These functions assume that the `TIMESTAMP` is a “local timestamp”.

A local timestamp is effectively a way of encoding the part values from a time zone into a single value.
They should be used with caution because the produced values can contain gaps and ambiguities thanks to daylight savings time.
Often the same functionality can be implemented more reliably using the `struct` variant of the `date_part` function.

| Name | Description |
|:--|:-------|
| [`current_localtime()`](#current_localtime) | Returns a `TIME` whose GMT bin values correspond to local time in the current time zone. |
| [`current_localtimestamp()`](#current_localtimestamp) | Returns a `TIMESTAMP` whose GMT bin values correspond to local date and time in the current time zone. |
| [`localtime`](#localtime) | Synonym for the `current_localtime()` function call. |
| [`localtimestamp`](#localtimestamp) | Synonym for the `current_localtimestamp()` function call. |
| [`timezone(text, timestamp)`](#timezonetext-timestamp) | Use the [date parts]({% link docs/stable/sql/functions/datepart.md %}) of the timestamp in GMT to construct a timestamp in the given time zone. Effectively, the argument is a “local” time. |
| [`timezone(text, timestamptz)`](#timezonetext-timestamptz) | Use the [date parts]({% link docs/stable/sql/functions/datepart.md %}) of the timestamp in the given time zone to construct a timestamp. Effectively, the result is a “local” time. |

#### `current_localtime()`

<div class="nostroke_table"></div>

| **Description** | Returns a `TIME` whose GMT bin values correspond to local time in the current time zone. |
| **Example** | `current_localtime()` |
| **Result** | `08:47:56.497` |

#### `current_localtimestamp()`

<div class="nostroke_table"></div>

| **Description** | Returns a `TIMESTAMP` whose GMT bin values correspond to local date and time in the current time zone. |
| **Example** | `current_localtimestamp()` |
| **Result** | `2022-12-17 08:47:56.497` |

#### `localtime`

<div class="nostroke_table"></div>

| **Description** | Synonym for the `current_localtime()` function call. |
| **Example** | `localtime` |
| **Result** | `08:47:56.497` |

#### `localtimestamp`

<div class="nostroke_table"></div>

| **Description** | Synonym for the `current_localtimestamp()` function call. |
| **Example** | `localtimestamp` |
| **Result** | `2022-12-17 08:47:56.497` |

#### `timezone(text, timestamp)`

<div class="nostroke_table"></div>

| **Description** | Use the [date parts]({% link docs/stable/sql/functions/datepart.md %}) of the timestamp in GMT to construct a timestamp in the given time zone. Effectively, the argument is a “local” time. |
| **Example** | `timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40')` |
| **Result** | `2001-02-16 19:38:40-08` |

#### `timezone(text, timestamptz)`

<div class="nostroke_table"></div>

| **Description** | Use the [date parts]({% link docs/stable/sql/functions/datepart.md %}) of the timestamp in the given time zone to construct a timestamp. Effectively, the result is a “local” time. |
| **Example** | `timezone('America/Denver', TIMESTAMPTZ '2001-02-16 20:38:40-05')` |
| **Result** | `2001-02-16 18:38:40` |

## At Time Zone

The `AT TIME ZONE` syntax is syntactic sugar for the (two argument) `timezone` function listed above:

```sql
SELECT TIMESTAMP '2001-02-16 20:38:40' AT TIME ZONE 'America/Denver' AS ts;
```

```text
2001-02-16 19:38:40-08
```

```sql
SELECT TIMESTAMP WITH TIME ZONE '2001-02-16 20:38:40-05' AT TIME ZONE 'America/Denver' AS ts;
```

```text
2001-02-16 18:38:40
```

Note that numeric timezones are not allowed:

```sql
SELECT TIMESTAMP '2001-02-16 20:38:40-05' AT TIME ZONE '0200' AS ts;
```

```console
Not implemented Error: Unknown TimeZone '0200'
```

## Infinities

Functions applied to infinite dates will either return the same infinite dates
(e.g., `greatest`) or `NULL` (e.g., `date_part`) depending on what “makes sense”.
In general, if the function needs to examine the parts of the infinite temporal value,
the result will be `NULL`.

## Calendars

The ICU extension also supports [non-Gregorian calendars]({% link docs/stable/sql/data_types/timestamp.md %}#calendar-support).
If such a calendar is current, then the display and binning operations will use that calendar.
