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
| `'year'` | Gregorian year | `'y'`, `'years'` | 2021 |
| `'month'` | Gregorian month | `'mon'`, `'months'`, `'mons'` | 8 |
| `'day'` | Gregorian day | `'days'`, `'d'`, `'dayofmonth'` | 3 |
| `'decade'` | Gregorian decade | `'decades'` | 202 |
| `'century'` | Gregorian century | `'centuries'` | 21 |
| `'millennium'` | Gregorian millennium | `'millenia'`, `'millenium'` | 3 |
| `'quarter'` | Quarter of the year (1-4) | `'quarters'` | 3 |
| `'microseconds'` | Sub-minute microseconds | `'microsecond'` | 44123456 |
| `'milliseconds'` | Sub-minute milliseconds | `'millisecond'`, `'ms'`, `'msec'`, `'msecs'` | 44123 |
| `'second'` | Seconds | `'seconds'`, `'s'` | 44 |
| `'minute'` | Minutes | `'minutes'`, `'m'` | 59 |
| `'hour'` | Hours | `'hours'`, `'h'` | 11 |

### Usable in Date Part Specifiers Only

| Specifier | Description | Synonyms | Example |
|:---|:---|:---|:---|
| `'epoch'` | Seconds since 1970-01-01 | | 1627991984 |
| `'dayofweek'` | Day of the week (Sunday = 0, Saturday = 6) | `'weekday'`, `'dow'` | 2 |
| `'isodow'` | ISO day of the week (Monday = 1, Sunday = 7) | | 2 |
| `'isoyear'` | ISO Year number (Starts on Monday of week containing Jan 4th) | | 2021 |
| `'week'` | Week number | `'weeks'`, `'w'` | 31 |
| `'yearweek'` | ISO year and week number in `YYYYWW` format | | 202131 |
| `'dayofyear'` | Day of the year (1-365/366) | `'doy'` | 215 |
| `'era'` | Gregorian era (CE/AD, BCE/BC) | | 1 |
| `'timezone'` | Time zone offset in seconds | | 0 |
| `'timezone_hour'` | Time zone offset hour portion | | 0 |
| `'timezone_minute'` | Time zone offset minute portion | | 0 |

Note that the time zone parts are all zero unless a time zone plugin such as ICU
has been installed to support `TIMESTAMP WITH TIME ZONE`.

### Part Functions
There are dedicated extraction functions to get certain subfields:

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `year(`*`date`*`)` | Year | `year(date '1992-02-15')` | `1992` |
| `month(`*`date`*`)` | Month | `month(date '1992-02-15')` | `2` |
| `day(`*`date`*`)` | Day | `day(date '1992-02-15')` | `15` |
| `dayofmonth(`*`date`*`)` | Day (synonym) | `dayofmonth(date '1992-02-15')` | `15` |
| `decade(`*`date`*`)` | Decade (year / 10) | `decade(date '1992-02-15')` | `199` |
| `century(`*`date`*`)` | Century | `century(date '1992-02-15')` | `20` |
| `millennium(`*`date`*`)` | Millennium | `millennium(date '1992-02-15')` | `2` |
| `quarter(`*`date`*`)` | Quarter | `quarter(date '1992-02-15')` | `1` |
| `microsecond(`*`date`*`)` | Sub-minute microseconds | `microsecond(timestamp '2021-08-03 11:59:44.123456')` | `44123456` |
| `millisecond(`*`date`*`)` | Sub-minute milliseconds | `millisecond(timestamp '2021-08-03 11:59:44.123456')` | `44123` |
| `second(`*`date`*`)` | Seconds | `second(timestamp '2021-08-03 11:59:44.123456')` | `44` |
| `minute(`*`date`*`)` | Minutes | `minute(timestamp '2021-08-03 11:59:44.123456')` | `59` |
| `hour(`*`date`*`)` | Hours | `hour(timestamp '2021-08-03 11:59:44.123456')` | `11` |
| `epoch(`*`date`*`)` | Seconds since 1970-01-01 | `epoch(date '1992-02-15')` | `698112000` |
| `dayofweek(`*`date`*`)` | Numeric weekday (Sunday = 0, Saturday = 6) | `dayofweek(date '1992-02-15')` | `6` |
| `weekday(`*`date`*`)` | Numeric weekday synonym (Sunday = 0, Saturday = 6) | `weekday(date '1992-02-15')` | `6` |
| `isodow(`*`date`*`)` | Numeric ISO weekday (Monday = 1, Sunday = 7) | `isodow(date '1992-02-15')` | `6` |
| `isoyear(`*`date`*`)` | ISO Year number (Starts on Monday of week containing Jan 4th) | `isoyear(date '2022-01-01')` | `2021` |
| `week(`*`date`*`)` | ISO Week | `week(date '1992-02-15')` | `7` |
| `weekofyear(`*`date`*`)` | ISO Week (synonym) | `weekofyear(date '1992-02-15')` | `7` |
| `dayofyear(`*`date`*`)` | Numeric ISO weekday (Monday = 1, Sunday = 7) | `isodow(date '1992-02-15')` | `46` |
| `quarter(`*`date`*`)` | Quarter | `quarter(date '1992-02-15')` | `1` |
| `era(`*`date`*`)` | Calendar era | `era(date '0044-03-15 (BC)')` | `0` |
| `timezone(`*`date`*`)` | Time Zone offset in minutes | `timezone(date '1992-02-15')` | `0` |
| `timezone_hour(`*`date`*`)` | Time zone offset hour portion | `timezone_hour(date '1992-02-15')` | `0` |
| `timezone_minute(`*`date`*`)` | Time zone offset minutes portion | `timezone_minute(date '1992-02-15')` | `0` |
