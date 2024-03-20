| Function | Description | Example | Result |
|:--|:--|:---|:--|
| `current_time`/`get_current_time()` | Current time (start of current transaction) | `get_current_time()` | `10:31:58.578` |
| `date_diff(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | The number of [partition](../../sql/functions/datepart) boundaries between the times | `date_diff('hour', TIME '01:02:03', TIME '06:01:03')` | `5` |
| `date_part(`*`part`*`, `*`time`*`)` | Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `date_part('minute', TIME '14:21:13')` | `21` |
| `date_sub(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | The number of complete [partitions](../../sql/functions/datepart) between the times | `date_sub('hour', TIME '01:02:03', TIME '06:01:03')` | `4` |
| `datediff(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | Alias of `date_diff`. The number of [partition](../../sql/functions/datepart) boundaries between the times | `datediff('hour', TIME '01:02:03', TIME '06:01:03')` | `5` |
| `datepart(`*`part`*`, `*`time`*`)` | Alias of date_part. Get [subfield](../../sql/functions/datepart) (equivalent to *extract*) | `datepart('minute', TIME '14:21:13')` | `21` |
| `datesub(`*`part`*`, `*`starttime`*`, `*`endtime`*`)` | Alias of date_sub. The number of complete [partitions](../../sql/functions/datepart) between the times | `datesub('hour', TIME '01:02:03', TIME '06:01:03')` | `4` |
| `extract(`*`part`* `FROM` *`time`*`)` | Get subfield from a time | `extract('hour' FROM TIME '14:21:13')` | `14` |
| `make_time(`*`bigint`*`, `*`bigint`*`, `*`double`*`)` | The time for the given parts | `make_time(13, 34, 27.123456)` | `13:34:27.123456` |
