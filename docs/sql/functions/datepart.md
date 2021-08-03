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

| Specifier | Description | Synonyms | Example |
|:---|:---|:---|:---|
| `'year'` | Gregorian year | `'y'`, `'years'` | 2021 |
| `'month'` | Gregorian month | `'mon'`, `'months'`, `'mons'` | 8 |
| `'day'` | Gregorian day | `'days'`, `'d'` | 3 |
| `'decade'` | Gregorian decade | `'decades'` | 202 |
| `'century'` | Gregorian century | `'centuries'` | 21 |
| `'millennium'` | Gregorian millennium | `'millenia'` | 3 |
| `'microseconds'` | Sub-minute microseconds | `'microsecond'` | 44123456 |
| `'milliseconds'` | Sub-minute milliseconds | `'millisecond'`, `'ms'`, `'msec'`, `'msecs'` | 44123 |
| `'second'` | Seconds | `'seconds'`, `'s'` | 44 |
| `'minute'` | Minutes | `'minutes'`, `'m'` | 59 |
| `'hour'` | Hours | `'hours'`, `'h'` | 11 |
| `'epoch'` | Seconds since 1970-01-01 | | 1627991984 |
| `'dow'` | Day of the week (Sunday = 0, Saturday = 6) | | 2 |
| `'isodow'` | ISO day of the week (Monday = 1, Sunday = 7) | | 2 |
| `'week'` | Week number | `'weeks'`, `'w'` | 31 |
| `'dayofyear'` | Day of the year (1-365/366) | `'doy'` | 215 |
| `'quarter'` | Quarter of the year (1-4) | `'quarters'` | 3 |

The parts above `'epoch'` are also used to specify `INTERVAL` types.
