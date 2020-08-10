---
layout: docu
title: Timestamp Functions
selected: Documentation/Functions/Timestamp Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating timestamp values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `age(`*`timestamp`*`, `*`timestamp`*`)` | Subtract arguments, resulting in the time difference between the two timestamps | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20'`) | 8 years 6 mons 20 days |
| `age(`*`timestamp`*`)` | Subtract from current_date | `age(TIMESTAMP '1992-09-20')` | 26 years 9 mons 9 days |
| `current_date` | Current date (start of current transaction) | | |
| `current_time` | Current time (start of current transaction) | | |
| `current_timestamp` | Current date and time (start of current transaction) | | |
| `date_trunc(`*`part`*`, `*`timestamp`*`)` | Truncate to specified precision | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | 1992-09-20 20:00:00 |
| `epoch_ms(ms)` | Converts ms since epoch to a timestamp | `epoch(0)` | 1970-01-01 00:00:00 |
| `extract(`*`field`* `from` *`timestamp`*`)` | Get subfield from a timestamp | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` | 20 |
| `now()` | Current date and time (start of current transaction) | | |
| `strftime(timestamp, format)` | Converts timestamp to string according to format (see [Date Format](/docs/sql/functions/dateformat)) | strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p') | Wed, 1 January 1992 - 08:38:40 PM |
| `strptime(text, format)` | Converts string to timestamp according to format (see [Date Format](/docs/sql/functions/dateformat)) | strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p') | 1992-01-01 20:38:40 |
