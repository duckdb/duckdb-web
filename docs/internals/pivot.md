---
layout: docu
title: Pivot Internals
---

## `PIVOT`

[Pivoting]({% link docs/sql/statements/pivot.md %}) is implemented as a combination of SQL query re-writing and a dedicated `PhysicalPivot` operator for higher performance.
Each `PIVOT` is implemented as set of aggregations into lists and then the dedicated `PhysicalPivot` operator converts those lists into column names and values.
Additional pre-processing steps are required if the columns to be created when pivoting are detected dynamically (which occurs when the `IN` clause is not in use).

DuckDB, like most SQL engines, requires that all column names and types be known at the start of a query.
In order to automatically detect the columns that should be created as a result of a `PIVOT` statement, it must be translated into multiple queries.
[`ENUM` types]({% link docs/sql/data_types/enum.md %}) are used to find the distinct values that should become columns.
Each `ENUM` is then injected into one of the `PIVOT` statement's `IN` clauses.

After the `IN` clauses have been populated with `ENUM`s, the query is re-written again into a set of aggregations into lists.

For example:

```sql
PIVOT cities
ON year
USING sum(population);
```

is initially translated into:

```sql
CREATE TEMPORARY TYPE __pivot_enum_0_0 AS ENUM (
    SELECT DISTINCT
        year::VARCHAR
    FROM cities
    ORDER BY
        year
    );
PIVOT cities
ON year IN __pivot_enum_0_0
USING sum(population);
```

and finally translated into:

```sql
SELECT country, name, list(year), list(population_sum)
FROM (
    SELECT country, name, year, sum(population) AS population_sum
    FROM cities
    GROUP BY ALL
)
GROUP BY ALL;
```

This produces the result:


| country |     name      |    list("year")    | list(population_sum) |
|---------|---------------|--------------------|----------------------|
| NL      | Amsterdam     | [2000, 2010, 2020] | [1005, 1065, 1158]   |
| US      | Seattle       | [2000, 2010, 2020] | [564, 608, 738]      |
| US      | New York City | [2000, 2010, 2020] | [8015, 8175, 8772]   |

The `PhysicalPivot` operator converts those lists into column names and values to return this result:


| country |     name      | 2000 | 2010 | 2020 |
|---------|---------------|-----:|-----:|-----:|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |

## `UNPIVOT`

### Internals

Unpivoting is implemented entirely as rewrites into SQL queries.
Each `UNPIVOT` is implemented as set of `unnest` functions, operating on a list of the column names and a list of the column values.
If dynamically unpivoting, the `COLUMNS` expression is evaluated first to calculate the column list.

For example:

```sql
UNPIVOT monthly_sales
ON jan, feb, mar, apr, may, jun
INTO
    NAME month
    VALUE sales;
```

is translated into:

```sql
SELECT
    empid,
    dept,
    unnest(['jan', 'feb', 'mar', 'apr', 'may', 'jun']) AS month,
    unnest(["jan", "feb", "mar", "apr", "may", "jun"]) AS sales
FROM monthly_sales;
```

Note the single quotes to build a list of text strings to populate `month`, and the double quotes to pull the column values for use in `sales`.
This produces the same result as the initial example:


| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | jan   | 1     |
| 1     | electronics | feb   | 2     |
| 1     | electronics | mar   | 3     |
| 1     | electronics | apr   | 4     |
| 1     | electronics | may   | 5     |
| 1     | electronics | jun   | 6     |
| 2     | clothes     | jan   | 10    |
| 2     | clothes     | feb   | 20    |
| 2     | clothes     | mar   | 30    |
| 2     | clothes     | apr   | 40    |
| 2     | clothes     | may   | 50    |
| 2     | clothes     | jun   | 60    |
| 3     | cars        | jan   | 100   |
| 3     | cars        | feb   | 200   |
| 3     | cars        | mar   | 300   |
| 3     | cars        | apr   | 400   |
| 3     | cars        | may   | 500   |
| 3     | cars        | jun   | 600   |
