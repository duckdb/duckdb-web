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
| `+` | addition of an `INTERVAL` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | 1992-03-27 01:02:03 |
| `-` | subtraction of `TIMESTAMP`s | `TIMESTAMP '1992-03-27' - TIMESTAMP '1992-03-22'` | INTERVAL 5 DAY |
| `-` | subtraction of an `INTERVAL` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY'` | 1992-03-22 01:02:03 |

## Timestamp Functions
The table below shows the available scalar functions for `TIMESTAMP` types.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `age(`*`timestamp`*`, `*`timestamp`*`)` | Subtract arguments, resulting in the time difference between the two timestamps | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20'`) | 8 years 6 mons 20 days |
| `age(`*`timestamp`*`)` | Subtract from current_date | `age(TIMESTAMP '1992-09-20')` | 26 years 9 mons 9 days |
| `century(`*`timestamp`*`)` | Extracts the century of a timestamp | `century(TIMESTAMP '1992-03-22')` | 20 |
| `current_timestamp` | Current date and time (start of current transaction) | | |
| `date_diff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `date_diff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | 2 |
| `date_part(`*`part`*`, `*`timestamp`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIMESTAMP '1992-09-20 20:38:40')` | 38 |
| `date_sub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `date_sub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | 1 |
| `date_trunc(`*`part`*`, `*`timestamp`*`)` | Truncate to specified [precision](../../sql/functions/datepart) | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | 1992-09-20 20:00:00 |
| `day(`*`timestamp`*`)` | Extracts the day of a timestamp | `day(TIMESTAMP '1992-03-22')` | 22 |
| `dayname(`*`timestamp`*`)` | The (English) name of the weekday | `dayname(TIMESTAMP '1992-03-22')` | Sunday |
| `dayofweek(`*`timestamp`*`)` | Extracts the day of the week of a timestamp (0-6, 0 = Sunday, 6 = Saturday) | `dayofweek(TIMESTAMP '1992-03-22')` | 0 |
| `dayofyear(`*`timestamp`*`)` | Extracts the day of the year of a timestamp (1-366) | `dayofyear(TIMESTAMP '1992-03-22')` | 81 |
| `decade(`*`timestamp`*`)` | Extracts the decade of a timestamp | `decade(TIMESTAMP '1992-03-22')` | 199 |
| `epoch(`*`timestamp`*`)` | Extracts the epoch of a timestamp in seconds | `epoch(TIMESTAMP '1992-03-22')` | 701222400 |
| `epoch_ms(ms)` | Converts ms since epoch to a timestamp | `epoch_ms(701222400000)` | 1992-03-22 00:00:00 |
| `extract(`*`field`* `from` *`timestamp`*`)` | Get [subfield](../../sql/functions/datepart) from a timestamp | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` | 20 |
| `greatest(`*`timestamp`*`, `*`timestamp`*`)` | The later of two timestamps | `greatest(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-09-20 20:38:48` |
| `hour(`*`timestamp`*`)` | Extracts the hour component of a timestamp | `hour(TIMESTAMP '1992-03-22 01:02:03.1234')` | 1 |
| `isodow(`*`timestamp`*`)` | Extracts the ISO day of the week of a timestamp (1-7, 1 = Monday, 7 = Sunday) | `isodow(TIMESTAMP '1992-03-22')` | 7 |
| `last_day(`*`timestamp`*`)` | The last day of the month. | `last_day(TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-03-31` |
| `least(`*`timestamp`*`, `*`timestamp`*`)` | The earlier of two timestamps | `least(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-03-22 01:02:03.1234` |
| `microsecond(`*`timestamp`*`)` | Extracts the sub-minute component of a timestamp in microseconds | `microsecond(TIMESTAMP '1992-03-22 01:02:03.1234')` | 3123400 |
| `millisecond(`*`timestamp`*`)` | Extracts the sub-minute component of a timestamp in milliseconds | `millisecond(TIMESTAMP '1992-03-22 01:02:03.1234')` | 3123 |
| `millenium(`*`timestamp`*`)` | Extracts the millenium of a timestamp | `millenium(TIMESTAMP '1992-03-22')` | 2 |
| `minute(`*`timestamp`*`)` | Extracts the minute component of a timestamp | `minute(TIMESTAMP '1992-03-22 01:02:03.1234')` | 2 |
| `month(`*`timestamp`*`)` | Extracts the month of a timestamp | `month(TIMESTAMP '1992-03-22')` | 3 |
| `monthname(`*`timestamp`*`)` | The (English) name of the month. | `monthname(TIMESTAMP '1992-09-20')` | `March` |
| `now()` | Current date and time (start of current transaction) | | |
| `quarter(`*`timestamp`*`)` | Extracts the quarter of a timestamp | `quarter(TIMESTAMP '1992-03-22')` | 1 |
| `second(`*`timestamp`*`)` | Extracts the second component of a timestamp | `second(TIMESTAMP '1992-03-22 01:02:03.1234')` | 3 |
| `strftime(timestamp, format)` | Converts timestamp to string according to the [format string](../../sql/functions/dateformat) | `strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` | Wed, 1 January 1992 - 08:38:40 PM |
| `strptime(text, format)` | Converts string to timestamp according to the [format string](../../sql/functions/dateformat) | `strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` | 1992-01-01 20:38:40 |
| `to_timestamp(sec)` | Converts sec since epoch to a timestamp | `to_timestamp(701222400)` | 1992-03-22 00:00:00 |
| `week(`*`timestamp`*`)` | Extracts the week number of a timestamp (1-53) | `week(TIMESTAMP '1992-03-22')` | 12 |
| `year(`*`timestamp`*`)` | Extracts the year of a timestamp | `year(TIMESTAMP '1992-03-22')` | 1992 |

## Timestamp Table Functions
The table below shows the available scalar functions for `TIMESTAMP` types.

| Function | Description | Example |
|:---|:---|:---|:---|
| `generate_series(`*`timestamp`*`, `*`timestamp`*`, `*`interval`*`)` | Generate a table of timestamps in the closed range, stepping by the interval | `range(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)`
| `range(`*`timestamp`*`, `*`timestamp`*`, `*`interval`*`)` | Generate a table of timestamps in the half open range, stepping by the interval | `range(TIMESTAMP '2001-04-10', TIMESTAMP '2001-04-11', INTERVAL 30 MINUTE)`
