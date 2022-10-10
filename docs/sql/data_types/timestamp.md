---
layout: docu
title: Timestamp Type
selected: Documentation/Data Types/Timestamp
expanded: Data Types
blurb: A timestamp specifies a combination of a date (year, month, day) and a time (hour, minute, second, millisecond).
---
Timestamps represent points in absolute time, usually called *instants*.
DuckDB represents instants as the number of microseconds (µs) since `1970-01-01 00:00:00+00`.

| Name | Aliases | Description |
|:---|:---|:---|
| `TIMESTAMP` | datetime | time of day (ignores time zone) |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMPTZ` | time of day (uses time zone) |

A timestamp specifies a combination of `DATE` (year, month, day) and a `TIME` (hour, minute, second, millisecond). Timestamps can be created using the `TIMESTAMP` keyword, where the data must be formatted according to the ISO 8601 format (`YYYY-MM-DD hh:mm:ss[.zzzzzz][+-TT[:tt]]`).

```sql
-- 11:30 AM at 20 September, 1992 GMT
SELECT TIMESTAMP '1992-09-20 11:30:00';
-- 2:30 PM at 20 September, 1992 GMT
SELECT TIMESTAMP '1992-09-20 14:30:00';
```

## Special Values

There are also three special date values that can be used on input:

| Input String | Valid Types                       | Description                                    |
|:-------------|:----------------------------------|:-----------------------------------------------|
| epoch	       | timestamp, timestamptz            | 1970-01-01 00:00:00+00 (Unix system time zero) |
| infinity	   | timestamp, timestamptz            | later than all other time stamps               |
| -infinity	   | timestamp, timestamptz            | earlier than all other time stamps             |

The values `infinity` and `-infinity` are specially represented inside the system and will be displayed unchanged; 
but `epoch` is simply a notational shorthand that will be converted to the time stamp value when read.

```sql
SELECT '-infinity'::TIMESTAMP, 'epoch'::TIMESTAMP, 'infinity'::TIMESTAMP;
```

| Negative  | Epoch              | Positive |
|:----------|:-------------------|:---------|
| -infinity | 1970-01-01 00:00:00| infinity |

## Functions
See [Timestamp Functions](../../sql/functions/timestamp).

## Time Zones
The `TIMESTAMPTZ` type can be binned into calendar and clock bins using a suitable extension.
The built in ICU extension implements all the binning and arithmetic functions using the
[International Components for Unicode](https://icu.unicode.org) time zone and calendar functions.

<!-- 
    To find the ICU installation information, for Python and R look in CMakeLists.txt.
    For JDBC/ODBC, check the Github Actions CI workflows (duckdb/.github/workflows/). 
    For NodeJS, I couldn't find anything
-->
To set the time zone to use, first load the ICU extension. The ICU extension comes pre-bundled
with several DuckDB clients (including Python, R, JDBC, and ODBC), so this step can be skipped in those cases. In other cases you might first need to install and load the ICU extension.

```sql
INSTALL icu;
LOAD icu;
```

Next, use the `Set TimeZone` command:

```sql
Set TimeZone='America/Los_Angeles';
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

You can also find a reference table of available time zones [here](../../sql/data_types/timezones).

## Calendars
The ICU extension also supports non-Gregorian calendars using the `Set Calendar` command.
Note that the `require icu` step is only required if the DuckDB client does not bundle the
ICU extension. 

```sql
LOAD icu;

Set Calendar='japanese';
```

Time binning operations for `TIMESTAMPTZ` will then be implemented using the given calendar.
In  this example, the `era` part will now report the Japanese imperial era number.

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
