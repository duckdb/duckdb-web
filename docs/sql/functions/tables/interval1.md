| Operator | Description | Example | Result |
|:-|:--|:----|:--|
| `+` | addition of an `INTERVAL` | `INTERVAL 1 HOUR + INTERVAL 5 HOUR` | `INTERVAL 6 HOUR` |
| `+` | addition to a `DATE` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27` |
| `+` | addition to a `TIMESTAMP` | `TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY` | `1992-03-27 01:02:03` |
| `+` | addition to a `TIME` | `TIME '01:02:03' + INTERVAL 5 HOUR` | `06:02:03` |
| `-` | subtraction of an `INTERVAL` | `INTERVAL 5 HOUR - INTERVAL 1 HOUR` | `INTERVAL 4 HOUR` |
| `-` | subtraction from a `DATE` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22` |
| `-` | subtraction from a `TIMESTAMP` | `TIMESTAMP '1992-03-27 01:02:03' - INTERVAL 5 DAY` | `1992-03-22 01:02:03` |
| `-` | subtraction from a `TIME` | `TIME '06:02:03' - INTERVAL 5 HOUR` | `01:02:03` |
