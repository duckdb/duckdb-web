This section describes functions and operators for examining and manipulating time values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| `date_part(`*`part`*`, `*`time`*`)` | Get subfield (equivalent to *extract*) | `date_part('minute', TIME '14:21:13')` | 21 |
| `extract(`*`part`* `from` *`time`*`)` | Get subfield from a date | `extract('hour' FROM TIME '14:21:13')` | 14 |

The only date parts that are defined for times are `epoch`, `hours`, `minutes`, `seconds`, `milliseconds` and `microseconds`.
