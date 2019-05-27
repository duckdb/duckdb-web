
## Date Type

| Name | Aliases | Description |
|:---|:---|:---|
| date |   | calendar date (year, month day) |

A date specifies a combination of year, month and day. DuckDB follows the SQL standard's lead by counting dates exclusively in the Gregorian calendar, even for years before that calendar was in use. Dates can be created using the `DATE` keyword, where the data must be formatted according to the ISO 8601 format (YYYY-MM-DD).

```sql
-- 20 September, 1992
SELECT DATE '1992-09-20';
```

## Functions
See [Date Functions and Operators](https://www.duckdb.org/docs/sql/functions/date_functions)