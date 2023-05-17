---
layout: docu
title: Date Parts
selected: Documentation/Functions/Date Parts
expanded: Functions
---

The `date_part` and `date_diff` and `date_trunc` functions can be used to manipulate the fields of temporal types.
The fields are specified as strings that contain the part name of the field.

## Part Specifiers
Below is a full list of all available date part specifiers.
The examples are the corresponding parts of the timestamp `2021-08-03 11:59:44.123456`.

### Usable as Date Part Specifiers and in Intervals

| Specifier | Description | Synonyms | Example |
|:---|:---|:---|:---|
| `'century'` | Gregorian century | `'cent'`, `'centuries'`, `'c'` | 21 |
| `'day'` | Gregorian day | `'days'`, `'d'`, `'dayofmonth'` | 3 |
| `'decade'` | Gregorian decade | `'dec'`, `'decades'`, `'decs'` | 202 |
| `'hour'` | Hours | `'hr'`, `'hours'`, `'hrs'`, `'h'` | 11 |
| `'microseconds'` | Sub-minute microseconds | `'microsecond'`, `'us'`, `'usec'`, `'usecs'`, `'usecond'`, `'useconds'` | 44123456 |
| `'millennium'` | Gregorian millennium | `'mil'`, `'millenniums'`, `'millenia'`, `'mils'`, `'millenium'` | 3 |
| `'milliseconds'` | Sub-minute milliseconds | `'millisecond'`, `'ms'`, `'msec'`, `'msecs'`, `'msecond'`, `'mseconds'` | 44123 |
| `'minute'` | Minutes | `'min'`, `'minutes'`, `'mins'`, `'m'` | 59 |
| `'month'` | Gregorian month | `'mon'`, `'months'`, `'mons'` | 8 |
| `'quarter'` | Quarter of the year (1-4) | `'quarters'` | 3 |
| `'second'` | Seconds | `'sec'`, `'seconds'`, `'secs'`, `'s'` | 44 |
| `'year'` | Gregorian year | `'yr'`, `'y'`, `'years'`, `'yrs'` | 2021 |

### Usable in Date Part Specifiers Only

| Specifier | Description | Synonyms | Example |
|:---|:---|:---|:---|
| `'dayofweek'` | Day of the week (Sunday = 0, Saturday = 6) | `'weekday'`, `'dow'` | 2 |
| `'dayofyear'` | Day of the year (1-365/366) | `'doy'` | 215 |
| `'epoch'` | Seconds since 1970-01-01 | | 1627991984 |
| `'era'` | Gregorian era (CE/AD, BCE/BC) | | 1 |
| `'isodow'` | ISO day of the week (Monday = 1, Sunday = 7) | | 2 |
| `'isoyear'` | ISO Year number (Starts on Monday of week containing Jan 4th) | | 2021 |
| `'timezone'` | Time zone offset in seconds | | 0 |
| `'timezone_hour'` | Time zone offset hour portion | | 0 |
| `'timezone_minute'` | Time zone offset minute portion | | 0 |
| `'week'` | Week number | `'weeks'`, `'w'` | 31 |
| `'yearweek'` | ISO year and week number in `YYYYWW` format | | 202131 |

Note that the time zone parts are all zero unless a time zone plugin such as ICU
has been installed to support `TIMESTAMP WITH TIME ZONE`.

### Part Functions
There are dedicated extraction functions to get certain subfields:

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `century(`*`date`*`)` | Century | `century(date '1992-02-15')` | `20` |
| `day(`*`date`*`)` | Day | `day(date '1992-02-15')` | `15` |
| `dayofmonth(`*`date`*`)` | Day (synonym) | `dayofmonth(date '1992-02-15')` | `15` |
| `dayofweek(`*`date`*`)` | Numeric weekday (Sunday = 0, Saturday = 6) | `dayofweek(date '1992-02-15')` | `6` |
| `dayofyear(`*`date`*`)` | Numeric ISO weekday (Monday = 1, Sunday = 7) | `isodow(date '1992-02-15')` | `46` |
| `decade(`*`date`*`)` | Decade (year / 10) | `decade(date '1992-02-15')` | `199` |
| `epoch(`*`date`*`)` | Seconds since 1970-01-01 | `epoch(date '1992-02-15')` | `698112000` |
| `era(`*`date`*`)` | Calendar era | `era(date '0044-03-15 (BC)')` | `0` |
| `hour(`*`date`*`)` | Hours | `hour(timestamp '2021-08-03 11:59:44.123456')` | `11` |
| `isodow(`*`date`*`)` | Numeric ISO weekday (Monday = 1, Sunday = 7) | `isodow(date '1992-02-15')` | `6` |
| `isoyear(`*`date`*`)` | ISO Year number (Starts on Monday of week containing Jan 4th) | `isoyear(date '2022-01-01')` | `2021` |
| `microsecond(`*`date`*`)` | Sub-minute microseconds | `microsecond(timestamp '2021-08-03 11:59:44.123456')` | `44123456` |
| `millennium(`*`date`*`)` | Millennium | `millennium(date '1992-02-15')` | `2` |
| `millisecond(`*`date`*`)` | Sub-minute milliseconds | `millisecond(timestamp '2021-08-03 11:59:44.123456')` | `44123` |
| `minute(`*`date`*`)` | Minutes | `minute(timestamp '2021-08-03 11:59:44.123456')` | `59` |
| `month(`*`date`*`)` | Month | `month(date '1992-02-15')` | `2` |
| `quarter(`*`date`*`)` | Quarter | `quarter(date '1992-02-15')` | `1` |
| `second(`*`date`*`)` | Seconds | `second(timestamp '2021-08-03 11:59:44.123456')` | `44` |
| `timezone(`*`date`*`)` | Time Zone offset in minutes | `timezone(date '1992-02-15')` | `0` |
| `timezone_hour(`*`date`*`)` | Time zone offset hour portion | `timezone_hour(date '1992-02-15')` | `0` |
| `timezone_minute(`*`date`*`)` | Time zone offset minutes portion | `timezone_minute(date '1992-02-15')` | `0` |
| `week(`*`date`*`)` | ISO Week | `week(date '1992-02-15')` | `7` |
| `weekday(`*`date`*`)` | Numeric weekday synonym (Sunday = 0, Saturday = 6) | `weekday(date '1992-02-15')` | `6` |
| `weekofyear(`*`date`*`)` | ISO Week (synonym) | `weekofyear(date '1992-02-15')` | `7` |
| `year(`*`date`*`)` | Year | `year(date '1992-02-15')` | `1992` |
| `yearweek(`*`date`*`)` | `BIGINT` of combined ISO Year number and 2-digit version of ISO Week number | `yearweek(date '1992-02-15')` | `199207` |
