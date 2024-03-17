| Operator | Description | Example | Result |
|:-|:--|:---|:--|
| `+` | addition of days (integers) | `DATE '1992-03-22' + 5` | `1992-03-27` |
| `+` | addition of an `INTERVAL` | `DATE '1992-03-22' + INTERVAL 5 DAY` | `1992-03-27` |
| `+` | addition of a variable `INTERVAL` | `SELECT DATE '1992-03-22' + INTERVAL (d.days) DAY FROM (VALUES (5), (11)) AS d(days)` | `1992-03-27` and `1992-04-02` |
| `-` | subtraction of `DATE`s | `DATE '1992-03-27' - DATE '1992-03-22'` | `5` |
| `-` | subtraction of an `INTERVAL` | `DATE '1992-03-27' - INTERVAL 5 DAY` | `1992-03-22` |
| `-` | subtraction of a variable `INTERVAL` | `SELECT DATE '1992-03-27' - INTERVAL (d.days) DAY FROM (VALUES (5), (11)) AS d(days)` | `1992-03-22` and `1992-03-16` |
