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
| `century(`*`timestamp`*`)` | Extracts the century of a timestamp | `century(TIMESTAMP '1992-03-22')` | 20 |
| `current_date` | Current date (start of current transaction) | | |
| `current_time` | Current time (start of current transaction) | | |
| `current_timestamp` | Current date and time (start of current transaction) | | |
| `date_trunc(`*`part`*`, `*`timestamp`*`)` | Truncate to specified precision | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | 1992-09-20 20:00:00 |
| `day(`*`timestamp`*`)` | Extracts the day of a timestamp | `day(TIMESTAMP '1992-03-22')` | 22 |
| `dayofweek(`*`timestamp`*`)` | Extracts the day of the week of a timestamp (0-6, 0 = Sunday, 6 = Saturday) | `dayofweek(TIMESTAMP '1992-03-22')` | 0 |
| `dayofyear(`*`timestamp`*`)` | Extracts the day of the year of a timestamp (1-366) | `dayofyear(TIMESTAMP '1992-03-22')` | 81 |
| `decade(`*`timestamp`*`)` | Extracts the decade of a timestamp | `decade(TIMESTAMP '1992-03-22')` | 199 |
| `epoch(`*`timestamp`*`)` | Extracts the epoch of a timestamp in seconds | `epoch(TIMESTAMP '1992-03-22')` | 701222400 |
| `epoch_ms(ms)` | Converts ms since epoch to a timestamp | `epoch_ms(701222400000)` | 1992-03-22 00:00:00 |
| `extract(`*`field`* `from` *`timestamp`*`)` | Get subfield from a timestamp | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` | 20 |
| `hour(`*`timestamp`*`)` | Extracts the hour component of a timestamp | `hour(TIMESTAMP '1992-03-22 01:02:03.1234')` | 1 |
| `isodow(`*`timestamp`*`)` | Extracts the ISO day of the week of a timestamp (1-7, 1 = Monday, 7 = Sunday) | `isodow(TIMESTAMP '1992-03-22')` | 7 |
| `microsecond(`*`timestamp`*`)` | Extracts the sub-minute component of a timestamp in microseconds | `microsecond(TIMESTAMP '1992-03-22 01:02:03.1234')` | 3123400 |
| `millisecond(`*`timestamp`*`)` | Extracts the sub-minute component of a timestamp in milliseconds | `millisecond(TIMESTAMP '1992-03-22 01:02:03.1234')` | 3123 |
| `millenium(`*`timestamp`*`)` | Extracts the millenium of a timestamp | `millenium(TIMESTAMP '1992-03-22')` | 2 |
| `minute(`*`timestamp`*`)` | Extracts the minute component of a timestamp | `minute(TIMESTAMP '1992-03-22 01:02:03.1234')` | 2 |
| `month(`*`timestamp`*`)` | Extracts the month of a timestamp | `month(TIMESTAMP '1992-03-22')` | 3 |
| `now()` | Current date and time (start of current transaction) | | |
| `quarter(`*`timestamp`*`)` | Extracts the quarter of a timestamp | `quarter(TIMESTAMP '1992-03-22')` | 1 |
| `second(`*`timestamp`*`)` | Extracts the second component of a timestamp | `second(TIMESTAMP '1992-03-22 01:02:03.1234')` | 3 |
| `strftime(timestamp, format)` | Converts timestamp to string according to format (see [Date Format](/docs/sql/functions/dateformat)) | `strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` | Wed, 1 January 1992 - 08:38:40 PM |
| `strptime(text, format)` | Converts string to timestamp according to format (see [Date Format](/docs/sql/functions/dateformat)) | `strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` | 1992-01-01 20:38:40 |
| `to_timestamp(sec)` | Converts sec since epoch to a timestamp | `to_timestamp(701222400)` | 1992-03-22 00:00:00 |
| `week(`*`timestamp`*`)` | Extracts the week number of a timestamp (1-53) | `week(TIMESTAMP '1992-03-22')` | 12 |
| `year(`*`timestamp`*`)` | Extracts the year of a timestamp | `year(TIMESTAMP '1992-03-22')` | 1992|
