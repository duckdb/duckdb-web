---
blurb: A timestamp specifies a combination of a date (year, month, day) and a time
  (hour, minute, second, microsecond).
layout: docu
redirect_from:
- docs/archive/0.9.2/sql/data_types/timestamp
title: Timestamp Types
---

Timestamps represent points in absolute time, usually called *instants*.
DuckDB represents instants as the number of microseconds (µs) since `1970-01-01 00:00:00+00`.

## Timestamp types

| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP_NS` | `TIMESTAMP`, `DATETIME`    | timestamp with nanosecond precision (ignores time zone)  |
| `TIMESTAMP_MS` |                            | timestamp with millisecond precision (ignores time zone) |
| `TIMESTAMP_S`  |                            | timestamp with second precision (ignores time zone)      |
| `TIMESTAMPTZ`  | `TIMESTAMP WITH TIME ZONE` | timestamp (uses time zone)                               |

A timestamp specifies a combination of [`DATE`](date) (year, month, day) and a [`TIME`](time) (hour, minute, second, microsecond). Timestamps can be created using the `TIMESTAMP` keyword, where the data must be formatted according to the ISO 8601 format (`YYYY-MM-DD hh:mm:ss[.zzzzzz][+-TT[:tt]]`).

```sql
SELECT TIMESTAMP_NS '1992-09-20 11:30:00.123456'; -- 1992-09-20 11:30:00.123456
SELECT TIMESTAMP    '1992-09-20 11:30:00.123456'; -- 1992-09-20 11:30:00.123456
SELECT DATETIME     '1992-09-20 11:30:00.123456'; -- 1992-09-20 11:30:00.123456
SELECT TIMESTAMP_MS '1992-09-20 11:30:00.123456'; -- 1992-09-20 11:30:00.123
SELECT TIMESTAMP_S  '1992-09-20 11:30:00.123456'; -- 1992-09-20 11:30:00
SELECT TIMESTAMPTZ  '1992-09-20 11:30:00.123456'; -- 1992-09-20 11:30:00.123456+00
SELECT TIMESTAMP WITH TIME ZONE '1992-09-20 11:30:00.123456';
-- 1992-09-20 11:30:00.123456+00
```

## Special Values

There are also three special date values that can be used on input:

<div class="narrow_table"></div>

| Input String | Valid Types                           | Description                                    |
|:-------------|:--------------------------------------|:-----------------------------------------------|
| epoch	       | `TIMESTAMP`, `TIMESTAMPTZ`            | 1970-01-01 00:00:00+00 (Unix system time zero) |
| infinity	   | `TIMESTAMP`, `TIMESTAMPTZ`            | later than all other time stamps               |
| -infinity	   | `TIMESTAMP`, `TIMESTAMPTZ`            | earlier than all other time stamps             |

The values `infinity` and `-infinity` are specially represented inside the system and will be displayed unchanged; 
but `epoch` is simply a notational shorthand that will be converted to the time stamp value when read.

```sql
SELECT '-infinity'::TIMESTAMP, 'epoch'::TIMESTAMP, 'infinity'::TIMESTAMP;
```

<div class="narrow_table"></div>

| Negative  | Epoch               | Positive |
|:----------|:--------------------|:---------|
| -infinity | 1970-01-01 00:00:00 | infinity |

## Functions

See [Timestamp Functions](../../sql/functions/timestamp).

## Time Zones

The `TIMESTAMPTZ` type can be binned into calendar and clock bins using a suitable extension.
The built-in [ICU extension](../../extensions/icu) implements all the binning and arithmetic functions using the
[International Components for Unicode](https://icu.unicode.org) time zone and calendar functions.

<!-- 
    To find the ICU installation information, for Python and R look in CMakeLists.txt.
    For JDBC/ODBC, check the GitHub Actions CI workflows (duckdb/.github/workflows/). 
    For NodeJS, I couldn't find anything
-->
To set the time zone to use, first load the ICU extension. The ICU extension comes pre-bundled with several DuckDB clients (including Python, R, JDBC, and ODBC), so this step can be skipped in those cases. In other cases you might first need to install and load the ICU extension.

```sql
INSTALL icu;
LOAD icu;
```

Next, use the `SET TimeZone` command:

```sql
SET TimeZone='America/Los_Angeles';
```

Time binning operations for `TIMESTAMPTZ` will then be implemented using the given time zone.

A list of available time zones can be pulled from the `pg_timezone_names()` table function:

```sql
SELECT 
    name,
    abbrev,
    utc_offset 
FROM pg_timezone_names() 
ORDER BY 
    name;
```

You can also find a reference table of [available time zones](../../sql/data_types/timezones).

## Calendars

The ICU extension also supports non-Gregorian calendars using the `SET Calendar` command.
Note that the `INSTALL` and `LOAD` steps are only required if the DuckDB client does not bundle the ICU extension.

```sql
INSTALL ICU;
LOAD icu;
SET Calendar='japanese';
```

Time binning operations for `TIMESTAMPTZ` will then be implemented using the given calendar.
In this example, the `era` part will now report the Japanese imperial era number.

A list of available calendars can be pulled from the `icu_calendar_names()` table function:

```sql
SELECT name FROM icu_calendar_names() ORDER BY 1;
```

## Settings

The current value of the `TimeZone` and `Calendar` settings are determined by ICU when it starts up.
They can be looked from in the `duckdb_settings()` table function:

```sql
SELECT * FROM duckdb_settings() WHERE name = 'TimeZone';
-- America/Los_Angeles
SELECT * FROM duckdb_settings() WHERE name = 'Calendar';
-- gregorian
```