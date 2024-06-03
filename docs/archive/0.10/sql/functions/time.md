---
layout: docu
title: Time Functions
---

This section describes functions and operators for examining and manipulating `TIME` values.

## Time Operators

The table below shows the available mathematical operators for `TIME` types.

<div class="narrow_table"></div>

| Operator | Description | Example | Result |
|:-|:---|:----|:--|
| `+` | addition of an `INTERVAL` | `TIME '01:02:03' + INTERVAL 5 HOUR` | `06:02:03` |
| `-` | subtraction of an `INTERVAL` | `TIME '06:02:03' - INTERVAL 5 HOUR'` | `01:02:03` |

## Time Functions

The table below shows the available scalar functions for `TIME` types.

| Name | Description |
|:--|:-------|
| [`current_time`](#current_time) | Current time (start of current transaction). |
| [`date_diff(part, starttime, endtime)`](#date_diffpart-starttime-endtime) | The number of [partition](../../sql/functions/datepart) boundaries between the times. |
| [`date_part(part, time)`](#date_partpart-time) | Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| [`date_sub(part, starttime, endtime)`](#date_subpart-starttime-endtime) | The number of complete [partitions](../../sql/functions/datepart) between the times. |
| [`datediff(part, starttime, endtime)`](#datediffpart-starttime-endtime) | Alias of `date_diff`. The number of [partition](../../sql/functions/datepart) boundaries between the times. |
| [`datepart(part, time)`](#datepartpart-time) | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| [`datesub(part, starttime, endtime)`](#datesubpart-starttime-endtime) | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the times. |
| [`extract(part FROM time)`](#extractpart-from-time) | Get subfield from a time. |
| [`get_current_time()`](#get_current_time) | Current time (start of current transaction). |
| [`make_time(bigint, bigint, double)`](#make_timebigint-bigint-double) | The time for the given parts. |

The only [date parts](../../sql/functions/datepart) that are defined for times are `epoch`, `hours`, `minutes`, `seconds`, `milliseconds` and `microseconds`.

### `current_time`

<div class="nostroke_table"></div>

| **Description** | Current time (start of current transaction). Note that parentheses should be omitted. |
| **Example** | `current_time` |
| **Result** | `10:31:58.578` |
| **Alias** | `get_current_time()` |

### `date_diff(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **Description** | The number of [partition](../../sql/functions/datepart) boundaries between the times. |
| **Example** | `date_diff('hour', TIME '01:02:03', TIME '06:01:03')` |
| **Result** | `5` |

### `date_part(part, time)`

<div class="nostroke_table"></div>

| **Description** | Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| **Example** | `date_part('minute', TIME '14:21:13')` |
| **Result** | `21` |

### `date_sub(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **Description** | The number of complete [partitions](../../sql/functions/datepart) between the times. |
| **Example** | `date_sub('hour', TIME '01:02:03', TIME '06:01:03')` |
| **Result** | `4` |

### `datediff(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **Description** | Alias of `date_diff`. The number of [partition](../../sql/functions/datepart) boundaries between the times. |
| **Example** | `datediff('hour', TIME '01:02:03', TIME '06:01:03')` |
| **Result** | `5` |

### `datepart(part, time)`

<div class="nostroke_table"></div>

| **Description** | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to `extract`). |
| **Example** | `datepart('minute', TIME '14:21:13')` |
| **Result** | `21` |

### `datesub(part, starttime, endtime)`

<div class="nostroke_table"></div>

| **Description** | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the times. |
| **Example** | `datesub('hour', TIME '01:02:03', TIME '06:01:03')` |
| **Result** | `4` |

### `extract(part FROM time)`

<div class="nostroke_table"></div>

| **Description** | Get subfield from a time. |
| **Example** | `extract('hour' FROM TIME '14:21:13')` |
| **Result** | `14` |

### `get_current_time()`

<div class="nostroke_table"></div>

| **Description** | Current time (start of current transaction). |
| **Example** | `get_current_time()` |
| **Result** | `10:31:58.578` |
| **Alias** | `current_time` |

### `make_time(bigint, bigint, double)`

<div class="nostroke_table"></div>

| **Description** | The time for the given parts. |
| **Example** | `make_time(13, 34, 27.123456)` |
| **Result** | `13:34:27.123456` |