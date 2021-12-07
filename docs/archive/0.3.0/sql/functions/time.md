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
| `date_diff(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | The number of [partition](/docs/sql/functions/datepart) boundaries between the times | `date_diff('hour', TIME '01:02:03', TIME '06:01:03')` | 5 |
| `date_part(`*`part`*`, `*`time`*`)` | Get [subfield](/docs/sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIME '14:21:13')` | 21 |
| `date_sub(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | The number of complete [partitions](/docs/sql/functions/datepart) between the times | `date_sub('hour', TIME '01:02:03', TIME '06:01:03')` | 4 |
| `epoch(`*`time`*`)` | The number of seconds since midnight| `epoch(TIME '14:21:13')` | 51673 |
| `extract(`*`part`* `from` *`time`*`)` | Get subfield from a date | `extract('hour' FROM TIME '14:21:13')` | 14 |
| `hour(`*`time`*`)` | Extracts the hour component of a time | `hour(TIME '01:02:03.1234')` | 1 |
| `microsecond(`*`time`*`)` | Extracts the sub-minute component of a time in microseconds | `microsecond(TIME '01:02:03.1234')` | 3123400 |
| `millisecond(`*`time`*`)` | Extracts the sub-minute component of a time in milliseconds | `millisecond(TIME '01:02:03.1234')` | 3123 |
| `minute(`*`time`*`)` | Extracts the minute component of a time | `minute(TIME '01:02:03.1234')` | 2 |
| `second(`*`time`*`)` | Extracts the second component of a time | `second(TIME '01:02:03.1234')` | 3 |

The only [date parts](/docs/sql/functions/datepart) that are defined for times are `epoch`, `hours`, `minutes`, `seconds`, `milliseconds` and `microseconds`.
