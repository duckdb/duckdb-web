---
layout: docu
title: Timestamp Functions
selected: Documentation/Functions/Timestamp Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating `TIMESTAMP` values.

## Timestamp Operators
The table below shows the available mathematical operators for `TIMESTAMP` types.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `+` | addition of an `INTERVAL` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `-` | subtraction of `TIMESTAMP`s | `TIMESTAMP '1992-03-27' - TIMESTAMP '1992-03-22'` | `5 days` |
| `-` | subtraction of an `INTERVAL` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |

Adding to or subtracting from [infinite values](../../sql/data_types/timestamp#special-values) produces the same infinite value.

## Timestamp Functions
The table below shows the available scalar functions for `TIMESTAMP` values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `age(`*`timestamp`*`, `*`timestamp`*`)` | Subtract arguments, resulting in the time difference between the two timestamps | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20')` | `8 years 6 months 20 days` |
| `age(`*`timestamp`*`)` | Subtract from current_date | `age(TIMESTAMP '1992-09-20')` | `29 years 1 month 27 days 12:39:00.844` |
| `century(`*`timestamp`*`)` | Extracts the century of a timestamp | `century(TIMESTAMP '1992-03-22')` | `20` |
| `date_diff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `date_diff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `2` |
| `datediff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_diff. The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `datediff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `2` |
| `date_part(`*`part`*`, `*`timestamp`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIMESTAMP '1992-09-20 20:38:40')` | `38` |
| `datepart(`*`part`*`, `*`timestamp`*`)` | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `datepart('minute', TIMESTAMP '1992-09-20 20:38:40')` | `38` |
| `date_part([`*`part`*`, ...], `*`timestamp`*`)` | Get the listed [subfields](../../sql/functions/datepart) as a `struct`. The list must be constant. | `date_part(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` | `{year: 1992, month: 9, day: 20}` |
| `datepart([`*`part`*`, ...], `*`timestamp`*`)` | Alias of date_part. Get the listed [subfields](../../sql/functions/datepart) as a `struct`. The list must be constant. | `datepart(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` | `{year: 1992, month: 9, day: 20}` |
| `date_sub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `date_sub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `1` |
| `datesub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `datesub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `1` |
| `date_trunc(`*`part`*`, `*`timestamp`*`)` | Truncate to specified [precision](../../sql/functions/datepart) | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | `1992-09-20 20:00:00` |
| `datetrunc(`*`part`*`, `*`timestamp`*`)` | Alias of date_trunc. Truncate to specified [precision](../../sql/functions/datepart) | `datetrunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | `1992-09-20 20:00:00` |
| `dayname(`*`timestamp`*`)` | The (English) name of the weekday | `dayname(TIMESTAMP '1992-03-22')` | `Sunday` |
| `epoch(`*`timestamp`*`)` | Converts a timestamp to the seconds since the epoch | `epoch('2022-11-07 08:43:04'::TIMESTAMP);` | `1667810584` |
| `epoch_ms(`*`ms`*`)` | Converts ms since epoch to a timestamp | `epoch_ms(701222400000)` | `1992-03-22 00:00:00` |
| `extract(`*`field`* `from` *`timestamp`*`)` | Get [subfield](../../sql/functions/datepart) from a timestamp | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` | `20` |
| `greatest(`*`timestamp`*`, `*`timestamp`*`)` | The later of two timestamps | `greatest(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-09-20 20:38:48` |
| `isfinite(`*`timestamp`*`)` | Returns true if the timestamp is finite, false otherwise | `isfinite(TIMESTAMP '1992-03-07')` | true |
| `isinf(`*`timestamp`*`)` | Returns true if the timestamp is infinite, false otherwise | `isinf(TIMESTAMP '-infinity')` | true |
| `last_day(`*`timestamp`*`)` | The last day of the month. | `last_day(TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-03-31` |
| `least(`*`timestamp`*`, `*`timestamp`*`)` | The earlier of two timestamps | `least(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-03-22 01:02:03.1234` |
| `make_timestamp(`*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`double`*`)` | The timestamp for the given parts | `make_timestamp(1992, 9, 20, 13, 34, 27.123456)` | `1992-09-20 13:34:27.123456` |
| `monthname(`*`timestamp`*`)` | The (English) name of the month. | `monthname(TIMESTAMP '1992-09-20')` | `September` |
| `strftime(`*`timestamp`*`, `*`format`*`)` | Converts timestamp to string according to the [format string](../../sql/functions/dateformat) | `strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` | `Wed, 1 January 1992 - 08:38:40 PM` |
| `strptime(`*`text`*`, `*`format`*`)` | Converts string to timestamp according to the [format string](../../sql/functions/dateformat) | `strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` | `1992-01-01 20:38:40` |
| `time_bucket(`*`bucket_width`*`, `*`timestamp`*`[, `*`origin`*`])` | Truncate `timestamp` by the specified interval `bucket_width`. Buckets are aligned relative to `origin` timestamp. `origin` defaults to 2000-01-03 00:00:00 for buckets that don't include a month or year interval, and to 2000-01-01 00:00:00 for month and year buckets. | `time_bucket(INTERVAL '2 weeks', TIMESTAMP '1992-04-20 15:26:00', TIMESTAMP '1992-04-01 00:00:00')` | `1992-04-15 00:00:00` |
| `time_bucket(`*`bucket_width`*`, `*`timestamp`*`[, `*`offset`*`])` | Truncate `timestamp` by the specified interval `bucket_width`. Buckets are offset by `offset` interval. | `time_bucket(INTERVAL '10 minutes', TIMESTAMP '1992-04-20 15:26:00-07', INTERVAL '5 minutes')` | `1992-04-20 15:25:00` |
| `to_timestamp(`*`sec`*`)` | Converts sec since epoch to a timestamp | `to_timestamp(701222400)` | `1992-03-22 00:00:00` |

There are also dedicated extraction functions to get the [subfields](../../sql/functions/datepart).

Functions applied to infinite dates will either return the same infinite dates
(e.g, `greatest`) or `NULL` (e.g., `date_part`) depending on what "makes sense".
In general, if the function needs to examine the parts of the infinite date, the result will be `NULL`.

## Timestamp Table Functions
The table below shows the available table functions for `TIMESTAMP` types.

| Function | Description | Example |
|:---|:---|:---|:---|
| `generate_series(`*`timestamp`*`, `*`timestamp`*`, `*`interval`*`)` | Generate a table of timestamps in the closed range, stepping by the interval | `generate_series(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)`
| `range(`*`timestamp`*`, `*`timestamp`*`, `*`interval`*`)` | Generate a table of timestamps in the half open range, stepping by the interval | `range(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)`

Infinite values are not allowed as table function bounds.
