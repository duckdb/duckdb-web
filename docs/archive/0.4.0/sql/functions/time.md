---
layout: docu
title: Time Functions
selected: Documentation/Functions/Time Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating `TIME` values.

## Time Operators
The table below shows the available mathematical operators for `TIME` types.

| Operator | Description | Example | Result |
|:---|:---|:---|:---|
| `+` | addition of an `INTERVAL` | `TIME '01:02:03' + INTERVAL 5 HOUR` | 06:02:03 |
| `-` | subtraction of an `INTERVAL` | `TIME '06:02:03' - INTERVAL 5 HOUR'` | 01:02:03 |

## Time Functions
The table below shows the available scalar functions for `TIME` types.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `current_time` | Current time (start of current transaction) | | |
| `date_diff(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the times | `date_diff('hour', TIME '01:02:03', TIME '06:01:03')` | 5 |
| `date_part(`*`part`*`, `*`time`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIME '14:21:13')` | 21 |
| `date_sub(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the times | `date_sub('hour', TIME '01:02:03', TIME '06:01:03')` | 4 |
| `extract(`*`part`* `from` *`time`*`)` | Get subfield from a time | `extract('hour' FROM TIME '14:21:13')` | 14 |
| `make_time(`*`bigint`*`, `*`bigint`*`, `*`double`*`)` | The time for the given parts | `make_time(13, 34, 27.123456)` | `13:34:27.123456` |

The only [date parts](../../sql/functions/datepart) that are defined for times are `epoch`, `hours`, `minutes`, `seconds`, `milliseconds` and `microseconds`.
