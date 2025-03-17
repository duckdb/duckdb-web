---
blurb: The UNPIVOT statement allows columns to be stacked into rows that indicate
  the prior column name and value.
layout: docu
railroad: statements/unpivot.js
redirect_from:
- /docs/sql/statements/unpivot
title: UNPIVOT Statement
---

The `UNPIVOT` statement allows multiple columns to be stacked into fewer columns.
In the basic case, multiple columns are stacked into two columns: a `NAME` column (which contains the name of the source column) and a `VALUE` column (which contains the value from the source column).

DuckDB implements both the SQL Standard `UNPIVOT` syntax and a simplified `UNPIVOT` syntax.
Both can utilize a [`COLUMNS` expression]({% link docs/stable/sql/expressions/star.md %}#columns) to automatically detect the columns to unpivot.
`PIVOT_LONGER` may also be used in place of the `UNPIVOT` keyword.

For details on how the `UNPIVOT` statement is implemented, see the [Pivot Internals site]({% link docs/stable/internals/pivot.md %}#unpivot).

> The [`PIVOT` statement]({% link docs/stable/sql/statements/pivot.md %}) is the inverse of the `UNPIVOT` statement.

## Simplified `UNPIVOT` Syntax

The full syntax diagram is below, but the simplified `UNPIVOT` syntax can be summarized using spreadsheet pivot table naming conventions as:

```sql
UNPIVOT ⟨dataset⟩
ON ⟨column(s)⟩
INTO
    NAME ⟨name_column_name⟩
    VALUE ⟨value_column_name(s)⟩
ORDER BY ⟨column(s)_with_order_direction(s)⟩
LIMIT ⟨number_of_rows⟩;
```

### Example Data

All examples use the dataset produced by the queries below:

```sql
CREATE OR REPLACE TABLE monthly_sales
    (empid INTEGER, dept TEXT, Jan INTEGER, Feb INTEGER, Mar INTEGER, Apr INTEGER, May INTEGER, Jun INTEGER);
INSERT INTO monthly_sales VALUES
    (1, 'electronics', 1, 2, 3, 4, 5, 6),
    (2, 'clothes', 10, 20, 30, 40, 50, 60),
    (3, 'cars', 100, 200, 300, 400, 500, 600);
```

```sql
FROM monthly_sales;
```

| empid |    dept     | Jan | Feb | Mar | Apr | May | Jun |
|------:|-------------|----:|----:|----:|----:|----:|----:|
| 1     | electronics | 1   | 2   | 3   | 4   | 5   | 6   |
| 2     | clothes     | 10  | 20  | 30  | 40  | 50  | 60  |
| 3     | cars        | 100 | 200 | 300 | 400 | 500 | 600 |

<!--
    Easiest is to just unpivot all months into their own name/value pair manually.
    Then show the columns-expr version.
    Can also show the quarterly example. -->

### `UNPIVOT` Manually

The most typical `UNPIVOT` transformation is to take already pivoted data and re-stack it into a column each for the name and value.
In this case, all months will be stacked into a `month` column and a `sales` column.

```sql
UNPIVOT monthly_sales
ON jan, feb, mar, apr, may, jun
INTO
    NAME month
    VALUE sales;
```

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | Jan   | 1     |
| 1     | electronics | Feb   | 2     |
| 1     | electronics | Mar   | 3     |
| 1     | electronics | Apr   | 4     |
| 1     | electronics | May   | 5     |
| 1     | electronics | Jun   | 6     |
| 2     | clothes     | Jan   | 10    |
| 2     | clothes     | Feb   | 20    |
| 2     | clothes     | Mar   | 30    |
| 2     | clothes     | Apr   | 40    |
| 2     | clothes     | May   | 50    |
| 2     | clothes     | Jun   | 60    |
| 3     | cars        | Jan   | 100   |
| 3     | cars        | Feb   | 200   |
| 3     | cars        | Mar   | 300   |
| 3     | cars        | Apr   | 400   |
| 3     | cars        | May   | 500   |
| 3     | cars        | Jun   | 600   |

### `UNPIVOT` Dynamically Using Columns Expression

In many cases, the number of columns to unpivot is not easy to predetermine ahead of time.
In the case of this dataset, the query above would have to change each time a new month is added.
The [`COLUMNS` expression]({% link docs/stable/sql/expressions/star.md %}#columns-expression) can be used to select all columns that are not `empid` or `dept`.
This enables dynamic unpivoting that will work regardless of how many months are added.
The query below returns identical results to the one above.

```sql
UNPIVOT monthly_sales
ON COLUMNS(* EXCLUDE (empid, dept))
INTO
    NAME month
    VALUE sales;
```

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | Jan   | 1     |
| 1     | electronics | Feb   | 2     |
| 1     | electronics | Mar   | 3     |
| 1     | electronics | Apr   | 4     |
| 1     | electronics | May   | 5     |
| 1     | electronics | Jun   | 6     |
| 2     | clothes     | Jan   | 10    |
| 2     | clothes     | Feb   | 20    |
| 2     | clothes     | Mar   | 30    |
| 2     | clothes     | Apr   | 40    |
| 2     | clothes     | May   | 50    |
| 2     | clothes     | Jun   | 60    |
| 3     | cars        | Jan   | 100   |
| 3     | cars        | Feb   | 200   |
| 3     | cars        | Mar   | 300   |
| 3     | cars        | Apr   | 400   |
| 3     | cars        | May   | 500   |
| 3     | cars        | Jun   | 600   |

### `UNPIVOT` into Multiple Value Columns

The `UNPIVOT` statement has additional flexibility: more than 2 destination columns are supported.
This can be useful when the goal is to reduce the extent to which a dataset is pivoted, but not completely stack all pivoted columns.
To demonstrate this, the query below will generate a dataset with a separate column for the number of each month within the quarter (month 1, 2, or 3), and a separate row for each quarter.
Since there are fewer quarters than months, this does make the dataset longer, but not as long as the above.

To accomplish this, multiple sets of columns are included in the `ON` clause.
The `q1` and `q2` aliases are optional.
The number of columns in each set of columns in the `ON` clause must match the number of columns in the `VALUE` clause.

```sql
UNPIVOT monthly_sales
    ON (jan, feb, mar) AS q1, (apr, may, jun) AS q2
    INTO
        NAME quarter
        VALUE month_1_sales, month_2_sales, month_3_sales;
```

| empid |    dept     | quarter | month_1_sales | month_2_sales | month_3_sales |
|------:|-------------|---------|--------------:|--------------:|--------------:|
| 1     | electronics | q1      | 1             | 2             | 3             |
| 1     | electronics | q2      | 4             | 5             | 6             |
| 2     | clothes     | q1      | 10            | 20            | 30            |
| 2     | clothes     | q2      | 40            | 50            | 60            |
| 3     | cars        | q1      | 100           | 200           | 300           |
| 3     | cars        | q2      | 400           | 500           | 600           |

### Using `UNPIVOT` within a `SELECT` Statement

The `UNPIVOT` statement may be included within a `SELECT` statement as a CTE ([a Common Table Expression, or WITH clause]({% link docs/stable/sql/query_syntax/with.md %})), or a subquery.
This allows for an `UNPIVOT` to be used alongside other SQL logic, as well as for multiple `UNPIVOT`s to be used in one query.

No `SELECT` is needed within the CTE, the `UNPIVOT` keyword can be thought of as taking its place.

```sql
WITH unpivot_alias AS (
    UNPIVOT monthly_sales
    ON COLUMNS(* EXCLUDE (empid, dept))
    INTO
        NAME month
        VALUE sales
)
SELECT * FROM unpivot_alias;
```

An `UNPIVOT` may be used in a subquery and must be wrapped in parentheses.
Note that this behavior is different than the SQL Standard Unpivot, as illustrated in subsequent examples.

```sql
SELECT *
FROM (
    UNPIVOT monthly_sales
    ON COLUMNS(* EXCLUDE (empid, dept))
    INTO
        NAME month
        VALUE sales
) unpivot_alias;
```

### Expressions within `UNPIVOT` Statements

DuckDB allows expressions within the `UNPIVOT` statements, provided that they only involve a single column. These can be used to perform computations as well as [explicit casts]({% link docs/stable/sql/data_types/typecasting.md %}#explicit-casting). For example:

```sql
UNPIVOT
    (SELECT 42 AS col1, 'woot' AS col2)
    ON
        (col1 * 2)::VARCHAR,
        col2;
```

| name | value |
|------|-------|
| col1 | 84    |
| col2 | woot  |

### Simplified `UNPIVOT` Full Syntax Diagram

Below is the full syntax diagram of the `UNPIVOT` statement.

<div id="rrdiagram"></div>

## SQL Standard `UNPIVOT` Syntax

The full syntax diagram is below, but the SQL Standard `UNPIVOT` syntax can be summarized as:

```sql
FROM [dataset]
UNPIVOT [INCLUDE NULLS] (
    [value-column-name(s)]
    FOR [name-column-name] IN [column(s)]
);
```

Note that only one column can be included in the `name-column-name` expression.

### SQL Standard `UNPIVOT` Manually

To complete the basic `UNPIVOT` operation using the SQL standard syntax, only a few additions are needed.

```sql
FROM monthly_sales UNPIVOT (
    sales
    FOR month IN (jan, feb, mar, apr, may, jun)
);
```

| empid |    dept     | month | sales |
|------:|-------------|-------|------:|
| 1     | electronics | Jan   | 1     |
| 1     | electronics | Feb   | 2     |
| 1     | electronics | Mar   | 3     |
| 1     | electronics | Apr   | 4     |
| 1     | electronics | May   | 5     |
| 1     | electronics | Jun   | 6     |
| 2     | clothes     | Jan   | 10    |
| 2     | clothes     | Feb   | 20    |
| 2     | clothes     | Mar   | 30    |
| 2     | clothes     | Apr   | 40    |
| 2     | clothes     | May   | 50    |
| 2     | clothes     | Jun   | 60    |
| 3     | cars        | Jan   | 100   |
| 3     | cars        | Feb   | 200   |
| 3     | cars        | Mar   | 300   |
| 3     | cars        | Apr   | 400   |
| 3     | cars        | May   | 500   |
| 3     | cars        | Jun   | 600   |

### SQL Standard `UNPIVOT` Dynamically Using the `COLUMNS` Expression

The [`COLUMNS` expression]({% link docs/stable/sql/expressions/star.md %}#columns) can be used to determine the `IN` list of columns dynamically.
This will continue to work even if additional `month` columns are added to the dataset.
It produces the same result as the query above.

```sql
FROM monthly_sales UNPIVOT (
    sales
    FOR month IN (columns(* EXCLUDE (empid, dept)))
);
```

### SQL Standard `UNPIVOT` into Multiple Value Columns

The `UNPIVOT` statement has additional flexibility: more than 2 destination columns are supported.
This can be useful when the goal is to reduce the extent to which a dataset is pivoted, but not completely stack all pivoted columns.
To demonstrate this, the query below will generate a dataset with a separate column for the number of each month within the quarter (month 1, 2, or 3), and a separate row for each quarter.
Since there are fewer quarters than months, this does make the dataset longer, but not as long as the above.

To accomplish this, multiple columns are included in the `value-column-name` portion of the `UNPIVOT` statement.
Multiple sets of columns are included in the `IN` clause.
The `q1` and `q2` aliases are optional.
The number of columns in each set of columns in the `IN` clause must match the number of columns in the `value-column-name` portion.

```sql
FROM monthly_sales
UNPIVOT (
    (month_1_sales, month_2_sales, month_3_sales)
    FOR quarter IN (
        (jan, feb, mar) AS q1,
        (apr, may, jun) AS q2
    )
);
```

| empid |    dept     | quarter | month_1_sales | month_2_sales | month_3_sales |
|------:|-------------|---------|--------------:|--------------:|--------------:|
| 1     | electronics | q1      | 1             | 2             | 3             |
| 1     | electronics | q2      | 4             | 5             | 6             |
| 2     | clothes     | q1      | 10            | 20            | 30            |
| 2     | clothes     | q2      | 40            | 50            | 60            |
| 3     | cars        | q1      | 100           | 200           | 300           |
| 3     | cars        | q2      | 400           | 500           | 600           |

### SQL Standard `UNPIVOT` Full Syntax Diagram

Below is the full syntax diagram of the SQL Standard version of the `UNPIVOT` statement.

<div id="rrdiagram2"></div>
