| Function | Description | Example | Result |
|:--|:--|:---|:-|
| `century(`*`date`*`)` | Century | `century(date '1992-02-15')` | `20` |
| `day(`*`date`*`)` | Day | `day(date '1992-02-15')` | `15` |
| `dayofmonth(`*`date`*`)` | Day (synonym) | `dayofmonth(date '1992-02-15')` | `15` |
| `dayofweek(`*`date`*`)` | Numeric weekday (Sunday = 0, Saturday = 6) | `dayofweek(date '1992-02-15')` | `6` |
| `dayofyear(`*`date`*`)` | Day of the year (starts from 1, i.e., January 1 = 1) | `dayofyear(date '1992-02-15')` | `46` |
| `decade(`*`date`*`)` | Decade (year / 10) | `decade(date '1992-02-15')` | `199` |
| `epoch(`*`date`*`)` | Seconds since 1970-01-01 | `epoch(date '1992-02-15')` | `698112000` |
| `era(`*`date`*`)` | Calendar era | `era(date '0044-03-15 (BC)')` | `0` |
| `hour(`*`date`*`)` | Hours | `hour(timestamp '2021-08-03 11:59:44.123456')` | `11` |
| `isodow(`*`date`*`)` | Numeric ISO weekday (Monday = 1, Sunday = 7) | `isodow(date '1992-02-15')` | `6` |
| `isoyear(`*`date`*`)` | ISO Year number (Starts on Monday of week containing Jan 4th) | `isoyear(date '2022-01-01')` | `2021` |
| `microsecond(`*`date`*`)` | Sub-minute microseconds | `microsecond(timestamp '2021-08-03 11:59:44.123456')` | `44123456` |
| `millennium(`*`date`*`)` | Millennium | `millennium(date '1992-02-15')` | `2` |
| `millisecond(`*`date`*`)` | Sub-minute milliseconds | `millisecond(timestamp '2021-08-03 11:59:44.123456')` | `44123` |
| `minute(`*`date`*`)` | Minutes | `minute(timestamp '2021-08-03 11:59:44.123456')` | `59` |
| `month(`*`date`*`)` | Month | `month(date '1992-02-15')` | `2` |
| `quarter(`*`date`*`)` | Quarter | `quarter(date '1992-02-15')` | `1` |
| `second(`*`date`*`)` | Seconds | `second(timestamp '2021-08-03 11:59:44.123456')` | `44` |
| `timezone_hour(`*`date`*`)` | Time zone offset hour portion | `timezone_hour(date '1992-02-15')` | `0` |
| `timezone_minute(`*`date`*`)` | Time zone offset minutes portion | `timezone_minute(date '1992-02-15')` | `0` |
| `timezone(`*`date`*`)` | Time Zone offset in minutes | `timezone(date '1992-02-15')` | `0` |
| `week(`*`date`*`)` | ISO Week | `week(date '1992-02-15')` | `7` |
| `weekday(`*`date`*`)` | Numeric weekday synonym (Sunday = 0, Saturday = 6) | `weekday(date '1992-02-15')` | `6` |
| `weekofyear(`*`date`*`)` | ISO Week (synonym) | `weekofyear(date '1992-02-15')` | `7` |
| `year(`*`date`*`)` | Year | `year(date '1992-02-15')` | `1992` |
| `yearweek(`*`date`*`)` | `BIGINT` of combined ISO Year number and 2-digit version of ISO Week number | `yearweek(date '1992-02-15')` | `199207` |
