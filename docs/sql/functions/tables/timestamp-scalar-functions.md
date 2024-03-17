| Function | Description | Example | Result |
|:--|:--|:---|:--|
| `age(`*`timestamp`*`, `*`timestamp`*`)` | Subtract arguments, resulting in the time difference between the two timestamps | `age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20')` | `8 years 6 months 20 days` |
| `age(`*`timestamp`*`)` | Subtract from current_date | `age(TIMESTAMP '1992-09-20')` | `29 years 1 month 27 days 12:39:00.844` |
| `century(`*`timestamp`*`)` | Extracts the century of a timestamp | `century(TIMESTAMP '1992-03-22')` | `20` |
| `date_diff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `date_diff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `2` |
| `date_part([`*`part`*`, ...], `*`timestamp`*`)` | Get the listed [subfields](../../sql/functions/datepart) as a `struct`. The list must be constant. | `date_part(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` | `{year: 1992, month: 9, day: 20}` |
| `date_part(`*`part`*`, `*`timestamp`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIMESTAMP '1992-09-20 20:38:40')` | `38` |
| `date_sub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `date_sub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `1` |
| `date_trunc(`*`part`*`, `*`timestamp`*`)` | Truncate to specified [precision](../../sql/functions/datepart) | `date_trunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | `1992-09-20 20:00:00` |
| `datediff(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_diff. The number of [partition](../../sql/functions/datepart) boundaries between the timestamps | `datediff('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `2` |
| `datepart([`*`part`*`, ...], `*`timestamp`*`)` | Alias of date_part. Get the listed [subfields](../../sql/functions/datepart) as a `struct`. The list must be constant. | `datepart(['year', 'month', 'day'], TIMESTAMP '1992-09-20 20:38:40')` | `{year: 1992, month: 9, day: 20}` |
| `datepart(`*`part`*`, `*`timestamp`*`)` | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `datepart('minute', TIMESTAMP '1992-09-20 20:38:40')` | `38` |
| `datesub(`*`part`*`, `*`startdate`*`, `*`enddate`*`)` | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the timestamps | `datesub('hour', TIMESTAMP '1992-09-30 23:59:59', TIMESTAMP '1992-10-01 01:58:00')` | `1` |
| `datetrunc(`*`part`*`, `*`timestamp`*`)` | Alias of date_trunc. Truncate to specified [precision](../../sql/functions/datepart) | `datetrunc('hour', TIMESTAMP '1992-09-20 20:38:40')` | `1992-09-20 20:00:00` |
| `dayname(`*`timestamp`*`)` | The (English) name of the weekday | `dayname(TIMESTAMP '1992-03-22')` | `Sunday` |
| `epoch_ms(`*`ms`*`)` | Converts ms since epoch to a timestamp | `epoch_ms(701222400000)` | `1992-03-22 00:00:00` |
| `epoch_ms(`*`timestamp`*`)` | Converts a timestamp to milliseconds since the epoch | `epoch_ms('2022-11-07 08:43:04.123456'::TIMESTAMP);` | `1667810584123` |
| `epoch_ms(`*`timestamp`*`)` | Return the total number of milliseconds since the epoch | `epoch_ms(timestamp '2021-08-03 11:59:44.123456')` | `1627991984123` |
| `epoch_ns(`*`timestamp`*`)` | Return the total number of nanoseconds since the epoch | `epoch_ns(timestamp '2021-08-03 11:59:44.123456')` | `1627991984123456000` |
| `epoch_us(`*`timestamp`*`)` | Return the total number of microseconds since the epoch | `epoch_ms(timestamp '2021-08-03 11:59:44.123456')` | `1627991984123456` |
| `epoch(`*`timestamp`*`)` | Converts a timestamp to seconds since the epoch | `epoch('2022-11-07 08:43:04'::TIMESTAMP);` | `1667810584` |
| `extract(`*`field`* `from` *`timestamp`*`)` | Get [subfield](../../sql/functions/datepart) from a timestamp | `extract('hour' FROM TIMESTAMP '1992-09-20 20:38:48')` | `20` |
| `greatest(`*`timestamp`*`, `*`timestamp`*`)` | The later of two timestamps | `greatest(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-09-20 20:38:48` |
| `isfinite(`*`timestamp`*`)` | Returns true if the timestamp is finite, false otherwise | `isfinite(TIMESTAMP '1992-03-07')` | `true` |
| `isinf(`*`timestamp`*`)` | Returns true if the timestamp is infinite, false otherwise | `isinf(TIMESTAMP '-infinity')` | `true` |
| `last_day(`*`timestamp`*`)` | The last day of the month. | `last_day(TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-03-31` |
| `least(`*`timestamp`*`, `*`timestamp`*`)` | The earlier of two timestamps | `least(TIMESTAMP '1992-09-20 20:38:48', TIMESTAMP '1992-03-22 01:02:03.1234')` | `1992-03-22 01:02:03.1234` |
| `make_timestamp(`*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`bigint`*`, `*`double`*`)` | The timestamp for the given parts | `make_timestamp(1992, 9, 20, 13, 34, 27.123456)` | `1992-09-20 13:34:27.123456` |
| `make_timestamp(`*`microseconds`*`)` | The timestamp for the given number of µs since the epoch | `make_timestamp(1667810584123456)` | `2022-11-07 08:43:04.123456` |
| `monthname(`*`timestamp`*`)` | The (English) name of the month. | `monthname(TIMESTAMP '1992-09-20')` | `September` |
| `strftime(`*`timestamp`*`, `*`format`*`)` | Converts timestamp to string according to the [format string](../../sql/functions/dateformat) | `strftime(timestamp '1992-01-01 20:38:40', '%a, %-d %B %Y - %I:%M:%S %p')` | `Wed, 1 January 1992 - 08:38:40 PM` |
| `strptime(`*`text`*`, `*`format-list`*`)` | Converts string to timestamp applying the [format strings](../../sql/functions/dateformat) in the list until one succeeds. Throws on failure. | `strptime('4/15/2023 10:56:00', ['%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'])` | `2023-04-15 10:56:00` |
| `strptime(`*`text`*`, `*`format`*`)` | Converts string to timestamp according to the [format string](../../sql/functions/dateformat). Throws on failure. | `strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` | `1992-01-01 20:38:40` |
| `time_bucket(`*`bucket_width`*`, `*`timestamp`*`[, `*`offset`*`])` | Truncate `timestamp` by the specified interval `bucket_width`. Buckets are offset by `offset` interval. | `time_bucket(INTERVAL '10 minutes', TIMESTAMP '1992-04-20 15:26:00-07', INTERVAL '5 minutes')` | `1992-04-20 15:25:00` |
| `time_bucket(`*`bucket_width`*`, `*`timestamp`*`[, `*`origin`*`])` | Truncate `timestamp` by the specified interval `bucket_width`. Buckets are aligned relative to `origin` timestamp. `origin` defaults to 2000-01-03 00:00:00 for buckets that don't include a month or year interval, and to 2000-01-01 00:00:00 for month and year buckets. | `time_bucket(INTERVAL '2 weeks', TIMESTAMP '1992-04-20 15:26:00', TIMESTAMP '1992-04-01 00:00:00')` | `1992-04-15 00:00:00` |
| `to_timestamp(`*`double`*`)` | Converts seconds since the epoch to a timestamp with time zone | `to_timestamp(1284352323.5)` | `2010-09-13 04:32:03.5+00` |
| `try_strptime(`*`text`*`, `*`format-list`*`)` | Converts string to timestamp applying the [format strings](../../sql/functions/dateformat) in the list until one succeeds. Returns `NULL` on failure. | `try_strptime('4/15/2023 10:56:00', ['%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'])` | `2023-04-15 10:56:00` |
| `try_strptime(`*`text`*`, `*`format`*`)` | Converts string to timestamp according to the [format string](../../sql/functions/dateformat). Returns `NULL` on failure. | `try_strptime('Wed, 1 January 1992 - 08:38:40 PM', '%a, %-d %B %Y - %I:%M:%S %p')` | `1992-01-01 20:38:40` |
