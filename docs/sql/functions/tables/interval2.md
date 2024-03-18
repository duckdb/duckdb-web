| Function | Description | Example | Result |
|:--|:--|:---|:--|
| `date_part(`*`part`*`, `*`interval`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('year', INTERVAL '14 months')` | `1` |
| `datepart(`*`part`*`, `*`interval`*`)` | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `datepart('year', INTERVAL '14 months')` | `1` |
| `extract(`*`part`* `from` *`interval`*`)` | Get [subfield](../../sql/functions/datepart) from an interval | `extract('month' FROM INTERVAL '14 months')` | 2 |
| `epoch(`*`interval`*`)` | Get total number of seconds in interval | `epoch(INTERVAL 5 HOUR)` | `18000.0` |
| `to_centuries(`*`integer`*`)` | Construct a century interval | `to_centuries(5)` | `INTERVAL 500 YEAR` |
| `to_days(`*`integer`*`)` | Construct a day interval | `to_days(5)` | `INTERVAL 5 DAY` |
| `to_decades(`*`integer`*`)` | Construct a decade interval | `to_decades(5)` | `INTERVAL 50 YEAR` |
| `to_hours(`*`integer`*`)` | Construct a hour interval | `to_hours(5)` | `INTERVAL 5 HOUR` |
| `to_microseconds(`*`integer`*`)` | Construct a microsecond interval | `to_microseconds(5)` | `INTERVAL 5 MICROSECOND` |
| `to_millennia(`*`integer`*`)` | Construct a millenium interval | `to_millennia(5)` | `INTERVAL 5000 YEAR` |
| `to_milliseconds(`*`integer`*`)` | Construct a millisecond interval | `to_milliseconds(5)` | `INTERVAL 5 MILLISECOND` |
| `to_minutes(`*`integer`*`)` | Construct a minute interval | `to_minutes(5)` | `INTERVAL 5 MINUTE` |
| `to_months(`*`integer`*`)` | Construct a month interval | `to_months(5)` | `INTERVAL 5 MONTH` |
| `to_seconds(`*`integer`*`)` | Construct a second interval | `to_seconds(5)` | `INTERVAL 5 SECOND` |
| `to_weeks(`*`integer`*`)` | Construct a week interval | `to_weeks(5)` | `INTERVAL 35 DAY` |
| `to_years(`*`integer`*`)` | Construct a year interval | `to_years(5)` | `INTERVAL 5 YEAR` |
