
## Timestamp Type

| Name | Aliases | Description |
|:---|:---|:---|
| timestamp | datetime | time of day (no time zone) |

A timestamp specifies a combination of `DATE` (year, month, day) and a `TIME` (hour, minute, second, millisecond). Timestamps can be created using the `TIMESTAMP` keyword, where the data must be formatted according to the ISO 8601 format (YYYY-MM-DD hh:mm:ss).

```sql
-- 11:30 AM at 20 September, 1992
SELECT TIMESTAMP '1992-20-09 11:30:00';
-- 2:30 PM at 20 September, 1992
SELECT TIMESTAMP '1992-20-09 14:30:00';
```

## Functions
See [Timestamp Functions and Operators](https://www.duckdb.org/docs/sql/functions/timestamp_functions)