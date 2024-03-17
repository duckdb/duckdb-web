| Function | Description | Example | Result |
|:--|:--|:---|:--|
| `current_localtime()` | Returns a `TIME` whose GMT bin values correspond to local time in the current time zone. | `current_localtime()` | `08:47:56.497` |
| `current_localtimestamp()` | Returns a `TIMESTAMP` whose GMT bin values correspond to local date and time in the current time zone. | `current_localtimestamp()` | `2022-12-17 08:47:56.497` |
| `localtime` | Synonym for the `current_localtime()` function call. | `localtime` | `08:47:56.497` |
| `localtimestamp` | Synonym for the `current_localtimestamp()` function call. | `localtimestamp` | `2022-12-17 08:47:56.497` |
| `timezone(`*`text`*`, `*`timestamp`*`)` | Use the [date parts](../../sql/functions/datepart) of the timestamp in GMT to construct a timestamp in the given time zone. Effectively, the argument is a "local" time. | `timezone('America/Denver', TIMESTAMP '2001-02-16 20:38:40')` | `2001-02-16 19:38:40-08` |
| `timezone(`*`text`*`, `*`timestamptz`*`)` | Use the [date parts](../../sql/functions/datepart) of the timestamp in the given time zone to construct a timestamp. Effectively, the result is a "local" time. | `timezone('America/Denver', TIMESTAMPTZ '2001-02-16 20:38:40-05')` | `2001-02-16 18:38:40` |
