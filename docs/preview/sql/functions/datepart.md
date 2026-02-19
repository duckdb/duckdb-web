---
layout: docu
title: Date Part Functions
---

<!-- markdownlint-disable MD001 -->

The `date_part`, `date_trunc` and `date_diff` functions can be used to extract or manipulate parts of temporal types such as [`TIMESTAMP`]({% link docs/preview/sql/data_types/timestamp.md %}), [`TIMESTAMPTZ`]({% link docs/preview/sql/data_types/timestamp.md %}), [`DATE`]({% link docs/preview/sql/data_types/date.md %}) and [`INTERVAL`]({% link docs/preview/sql/data_types/interval.md %}).

The parts to be extracted or manipulated are specified by one of the strings in the tables below.
The example column provides the corresponding parts of the timestamp `2021-08-03 11:59:44.123456`.
Only the entries of the first table can be extracted from `INTERVAL`s or used to construct them.

> Except for `julian` and `epoch`, which return `DOUBLE`s, all parts are extracted as integers. Since there are no infinite integer values in DuckDB, `NULL`s are returned for infinite timestamps.

## Part Specifiers Usable as Date Part Specifiers and in Intervals

| Specifier | Description | Synonyms | Example |
|:--|:--|:---|--:|
| `century` | Gregorian century | `cent`, `centuries`, `c` | `21` |
| `day` | Gregorian day | `days`, `d`, `dayofmonth` | `3` |
| `decade` | Gregorian decade | `dec`, `decades`, `decs` | `202` |
| `hour` | Hours | `hr`, `hours`, `hrs`, `h` | `11` |
| `microseconds` | Sub-minute microseconds | `microsecond`, `us`, `usec`, `usecs`, `usecond`, `useconds` | `44123456` |
| `millennium` | Gregorian millennium | `mil`, `millenniums`, `millenia`, `mils`, `millenium` | `3` |
| `milliseconds` | Sub-minute milliseconds | `millisecond`, `ms`, `msec`, `msecs`, `msecond`, `mseconds` | `44123` |
| `minute` | Minutes | `min`, `minutes`, `mins`, `m` | `59` |
| `month` | Gregorian month | `mon`, `months`, `mons` | `8` |
| `quarter` | Quarter of the year (1-4) | `quarters` | `3` |
| `second` | Seconds | `sec`, `seconds`, `secs`, `s` | `44` |
| `year` | Gregorian year | `yr`, `y`, `years`, `yrs` | `2021` |

## Part Specifiers Only Usable as Date Part Specifiers

| Specifier | Description | Synonyms | Example |
|:--|:--|:---|--:|
| `dayofweek` | Day of the week (Sunday = 0, Saturday = 6) | `weekday`, `dow` | `2` |
| `dayofyear` | Day of the year (1-365/366) | `doy` | `215` |
| `epoch` | Seconds since 1970-01-01 | | `1760465850.6698709` |
| `era` | Gregorian era (CE/AD, BCE/BC) | | `1` |
| `isodow` | ISO day of the week (Monday = 1, Sunday = 7) | | `2` |
| `isoyear` | ISO Year number (Starts on Monday of week containing Jan 4th) | | `2021` |
| `julian` | Julian Day number. | | `2459430.4998162435` |
| `timezone_hour` | Time zone offset hour portion | | `0` |
| `timezone_minute` | Time zone offset minute portion | | `0` |
| `timezone` | Time zone offset in seconds | | `0` |
| `week` | Week number | `weeks`, `w` | `31` |
| `yearweek` | ISO year and week number in `YYYYWW` format | | `202131` |

Note that the time zone parts are all zero unless a time zone extension such as [ICU]({% link docs/preview/core_extensions/icu.md %})
has been installed to support `TIMESTAMP WITH TIME ZONE`.

## Part Functions

There are dedicated extraction functions to get certain subfields:

| Name | Description |
|:--|:-------|
| [`century(date)`](#centurydate) | Century. |
| [`day(date)`](#daydate) | Day. |
| [`dayofmonth(date)`](#dayofmonthdate) | Day (synonym). |
| [`dayofweek(date)`](#dayofweekdate) | Numeric weekday (Sunday = 0, Saturday = 6). |
| [`dayofyear(date)`](#dayofyeardate) | Day of the year (starts from 1, i.e., January 1 = 1). |
| [`decade(date)`](#decadedate) | Decade (year / 10). |
| [`epoch(date)`](#epochdate) | Seconds since 1970-01-01. |
| [`era(date)`](#eradate) | Calendar era. |
| [`hour(date)`](#hourdate) | Hours. |
| [`isodow(date)`](#isodowdate) | Numeric ISO weekday (Monday = 1, Sunday = 7). |
| [`isoyear(date)`](#isoyeardate) | ISO Year number (Starts on Monday of week containing Jan 4th). |
| [`julian(date)`](#juliandate) | `DOUBLE` Julian Day number. |
| [`microsecond(date)`](#microseconddate) | Sub-minute microseconds. |
| [`millennium(date)`](#millenniumdate) | Millennium. |
| [`millisecond(date)`](#milliseconddate) | Sub-minute milliseconds. |
| [`minute(date)`](#minutedate) | Minutes. |
| [`month(date)`](#monthdate) | Month. |
| [`quarter(date)`](#quarterdate) | Quarter. |
| [`second(date)`](#seconddate) | Seconds. |
| [`timezone_hour(date)`](#timezone_hourdate) | Time zone offset hour portion. |
| [`timezone_minute(date)`](#timezone_minutedate) | Time zone offset minutes portion. |
| [`timezone(date)`](#timezonedate) | Time zone offset in seconds. |
| [`week(date)`](#weekdate) | ISO Week. |
| [`weekday(date)`](#weekdaydate) | Numeric weekday synonym (Sunday = 0, Saturday = 6). |
| [`weekofyear(date)`](#weekofyeardate) | ISO Week (synonym). |
| [`year(date)`](#yeardate) | Year. |
| [`yearweek(date)`](#yearweekdate) | `BIGINT` of combined ISO Year number and 2-digit version of ISO Week number. |

#### `century(date)`

<div class="nostroke_table"></div>

| **Description** | Century. |
| **Example** | `century(DATE '1992-02-15')` |
| **Result** | `20` |

#### `day(date)`

<div class="nostroke_table"></div>

| **Description** | Day. |
| **Example** | `day(DATE '1992-02-15')` |
| **Result** | `15` |

#### `dayofmonth(date)`

<div class="nostroke_table"></div>

| **Description** | Day (synonym). |
| **Example** | `dayofmonth(DATE '1992-02-15')` |
| **Result** | `15` |

#### `dayofweek(date)`

<div class="nostroke_table"></div>

| **Description** | Numeric weekday (Sunday = 0, Saturday = 6). |
| **Example** | `dayofweek(DATE '1992-02-15')` |
| **Result** | `6` |

#### `dayofyear(date)`

<div class="nostroke_table"></div>

| **Description** | Day of the year (starts from 1, i.e., January 1 = 1). |
| **Example** | `dayofyear(DATE '1992-02-15')` |
| **Result** | `46` |

#### `decade(date)`

<div class="nostroke_table"></div>

| **Description** | Decade (year / 10). |
| **Example** | `decade(DATE '1992-02-15')` |
| **Result** | `199` |

#### `epoch(date)`

<div class="nostroke_table"></div>

| **Description** | Seconds since 1970-01-01. |
| **Example** | `epoch(DATE '1992-02-15')` |
| **Result** | `698112000` |

#### `era(date)`

<div class="nostroke_table"></div>

| **Description** | Calendar era. |
| **Example** | `era(DATE '0044-03-15 (BC)')` |
| **Result** | `0` |

#### `hour(date)`

<div class="nostroke_table"></div>

| **Description** | Hours. |
| **Example** | `hour(timestamp '2021-08-03 11:59:44.123456')` |
| **Result** | `11` |

#### `isodow(date)`

<div class="nostroke_table"></div>

| **Description** | Numeric ISO weekday (Monday = 1, Sunday = 7). |
| **Example** | `isodow(DATE '1992-02-15')` |
| **Result** | `6` |

#### `isoyear(date)`

<div class="nostroke_table"></div>

| **Description** | ISO Year number (Starts on Monday of week containing Jan 4th). |
| **Example** | `isoyear(DATE '2022-01-01')` |
| **Result** | `2021` |


#### `julian(date)`

<div class="nostroke_table"></div>

| **Description** | `DOUBLE` Julian Day number. |
| **Example** | `julian(DATE '1992-09-20')` |
| **Result** | `2448886.0` |


#### `microsecond(date)`

<div class="nostroke_table"></div>

| **Description** | Sub-minute microseconds. |
| **Example** | `microsecond(timestamp '2021-08-03 11:59:44.123456')` |
| **Result** | `44123456` |

#### `millennium(date)`

<div class="nostroke_table"></div>

| **Description** | Millennium. |
| **Example** | `millennium(DATE '1992-02-15')` |
| **Result** | `2` |

#### `millisecond(date)`

<div class="nostroke_table"></div>

| **Description** | Sub-minute milliseconds. |
| **Example** | `millisecond(timestamp '2021-08-03 11:59:44.123456')` |
| **Result** | `44123` |

#### `minute(date)`

<div class="nostroke_table"></div>

| **Description** | Minutes. |
| **Example** | `minute(timestamp '2021-08-03 11:59:44.123456')` |
| **Result** | `59` |

#### `month(date)`

<div class="nostroke_table"></div>

| **Description** | Month. |
| **Example** | `month(DATE '1992-02-15')` |
| **Result** | `2` |

#### `quarter(date)`

<div class="nostroke_table"></div>

| **Description** | Quarter. |
| **Example** | `quarter(DATE '1992-02-15')` |
| **Result** | `1` |

#### `second(date)`

<div class="nostroke_table"></div>

| **Description** | Seconds. |
| **Example** | `second(timestamp '2021-08-03 11:59:44.123456')` |
| **Result** | `44` |

#### `timezone_hour(date)`

<div class="nostroke_table"></div>

| **Description** | Time zone offset hour portion. |
| **Example** | `timezone_hour(DATE '1992-02-15')` |
| **Result** | `0` |

#### `timezone_minute(date)`

<div class="nostroke_table"></div>

| **Description** | Time zone offset minutes portion. |
| **Example** | `timezone_minute(DATE '1992-02-15')` |
| **Result** | `0` |

#### `timezone(date)`

<div class="nostroke_table"></div>

| **Description** | Time zone offset in minutes. |
| **Example** | `timezone(DATE '1992-02-15')` |
| **Result** | `0` |

#### `week(date)`

<div class="nostroke_table"></div>

| **Description** | ISO Week. |
| **Example** | `week(DATE '1992-02-15')` |
| **Result** | `7` |

#### `weekday(date)`

<div class="nostroke_table"></div>

| **Description** | Numeric weekday synonym (Sunday = 0, Saturday = 6). |
| **Example** | `weekday(DATE '1992-02-15')` |
| **Result** | `6` |

#### `weekofyear(date)`

<div class="nostroke_table"></div>

| **Description** | ISO Week (synonym). |
| **Example** | `weekofyear(DATE '1992-02-15')` |
| **Result** | `7` |

#### `year(date)`

<div class="nostroke_table"></div>

| **Description** | Year. |
| **Example** | `year(DATE '1992-02-15')` |
| **Result** | `1992` |

#### `yearweek(date)`

<div class="nostroke_table"></div>

| **Description** | `BIGINT` of combined ISO Year number and 2-digit version of ISO Week number. |
| **Example** | `yearweek(DATE '1992-02-15')` |
| **Result** | `199207` |
