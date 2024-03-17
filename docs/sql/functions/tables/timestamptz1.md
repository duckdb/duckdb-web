| Function | Description | Example | Result |
|:--|:--|:---|:--|
| `current_timestamp` | Current date and time (start of current transaction) | `current_timestamp` | `2022-10-08 12:44:46.122-07` |
| `get_current_timestamp()` | Current date and time (start of current transaction) | `get_current_timestamp()` | `2022-10-08 12:44:46.122-07` |
| `greatest(`*`timestamptz`*`, `*`timestamptz`*`)` | The later of two timestamps | `greatest(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` | `1992-09-20 20:38:48-07` |
| `isfinite(`*`timestamptz`*`)` | Returns true if the timestamp with time zone is finite, false otherwise | `isfinite(TIMESTAMPTZ '1992-03-07')` | `true` |
| `isinf(`*`timestamptz`*`)` | Returns true if the timestamp with time zone is infinite, false otherwise | `isinf(TIMESTAMPTZ '-infinity')` | `true` |
| `least(`*`timestamptz`*`, `*`timestamptz`*`)` | The earlier of two timestamps | `least(TIMESTAMPTZ '1992-09-20 20:38:48', TIMESTAMPTZ '1992-03-22 01:02:03.1234')` | `1992-03-22 01:02:03.1234-08` |
| `now()` | Current date and time (start of current transaction) | `now()` | `2022-10-08 12:44:46.122-07`|
| `transaction_timestamp()` | Current date and time (start of current transaction) | `transaction_timestamp()` | `2022-10-08 12:44:46.122-07`|
