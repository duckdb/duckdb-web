---
layout: docu
title: Pivot Statement
selected: Documentation/SQL/Pivot
expanded: SQL
railroad: statements/pivot.js
blurb: The PIVOT statement allows values within a column to be separated into their own columns.
---
<!-- 
TODO: 
    Add to menu 
    Build RR diagram
    Document Pivot
        Short form syntax
        Long form syntax
    Document UnPivot
        Separate document?
        Short
        Long
-->

The `PIVOT` statement allows distinct values within a column to be separated into their own columns.
The values within those new columns are calculated using an aggregate function on the subset of rows that match each distinct value.

DuckDB implements both the SQL Standard `PIVOT` syntax and a simplified `PIVOT` syntax that automatically detects the columns to create while pivoting. 
`PIVOT_WIDER` may also be used in place of the `PIVOT` keyword.

## Simplified Pivot Syntax

The full syntax diagram is below, but the simplified `PIVOT` syntax can be summarized using spreadsheet pivot table naming conventions as:
```sql
PIVOT [dataset] 
ON [column(s)] 
USING [value(s)] 
GROUP BY [row(s)]
```
The `ON`, `USING`, and `GROUP BY` clauses are each optional, but they may not all be omitted.

### Example Data
All examples use the dataset produced by the queries below:
```sql
CREATE TABLE Cities(Country VARCHAR, Name VARCHAR, Year INT, Population INT);
INSERT INTO Cities VALUES ('NL', 'Amsterdam', 2000, 1005);
INSERT INTO Cities VALUES ('NL', 'Amsterdam', 2010, 1065);
INSERT INTO Cities VALUES ('NL', 'Amsterdam', 2020, 1158);
INSERT INTO Cities VALUES ('US', 'Seattle', 2000, 564);
INSERT INTO Cities VALUES ('US', 'Seattle', 2010, 608);
INSERT INTO Cities VALUES ('US', 'Seattle', 2020, 738);
INSERT INTO Cities VALUES ('US', 'New York City', 2000, 8015);
INSERT INTO Cities VALUES ('US', 'New York City', 2010, 8175);
INSERT INTO Cities VALUES ('US', 'New York City', 2020, 8772);
```
```sql
FROM Cities;
```

| Country |     Name      | Year | Population |
|---------|---------------|------|------------|
| NL      | Amsterdam     | 2000 | 1005       |
| NL      | Amsterdam     | 2010 | 1065       |
| NL      | Amsterdam     | 2020 | 1158       |
| US      | Seattle       | 2000 | 564        |
| US      | Seattle       | 2010 | 608        |
| US      | Seattle       | 2020 | 738        |
| US      | New York City | 2000 | 8015       |
| US      | New York City | 2010 | 8175       |
| US      | New York City | 2020 | 8772       |

### PIVOT ON and USING

Use the `PIVOT` statement below to create a separate column for each year and calculate the total population in each.
The `ON` clause specifies which column(s) to split into separate columns.
It is equivalent to the columns parameter in a spreadsheet pivot table.

The `USING` clause determines how to aggregate the values that are split into separate columns.
This is equivalent to the values parameter in a spreadsheet pivot table.
If the `USING` clause is not included, it defaults to `COUNT(*)`.

```sql
PIVOT Cities ON Year USING SUM(Population);
```

| Country |     Name      | 2000 | 2010 | 2020 |
|---------|---------------|------|------|------|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |

In the above example, the `SUM` aggregate is always operating on a single value. 
If we only want to change the orientation of how the data is displayed without aggregating, use the `FIRST` aggregate function.
In this example, we are pivoting numeric values, but the `FIRST` function works very well for pivoting out a text column.
(This is something that is difficult to do in an spreadsheet pivot table, but easy in DuckDB!)

This query produces a result that is identical to the one above:
```sql
PIVOT Cities ON Year USING FIRST(Population);
```

### PIVOT ON, USING, and GROUP BY
By default, the `PIVOT` statement retains all columns not specified in the `ON` or `USING` clauses. 
To include only certain columns and further aggregate, specify columns in the `GROUP BY` clause. 
This is equivalent to the rows parameter of a spreadsheet pivot table.

In the below example, the Name column is no longer included in the output, and the data is aggregated up to the Country level.
```sql
PIVOT Cities ON Year USING SUM(Population) GROUP BY Country;
```

| Country | 2000 | 2010 | 2020 |
|---------|------|------|------|
| NL      | 1005 | 1065 | 1158 |
| US      | 8579 | 8783 | 9510 |


### IN filter for ON clause
To only create a separate column for specific values within a column in the `ON` clause, use an optional `IN` expression.
Let's say for example that we wanted to forget about the year 2020 for no particular reason...
```sql
PIVOT Cities ON Year IN (2000, 2010) USING SUM(Population) GROUP BY Country;
```

| Country | 2000 | 2010 |
|---------|------|------|
| NL      | 1005 | 1065 |
| US      | 8579 | 8783 |


### Multiple expressions per clause
Multiple columns can be specified in the `ON` and `GROUP BY` clauses, and multiple aggregate expressions can be included in the `USING` clause.

#### Multiple ON columns and ON expressions
Multiple columns can be pivoted out into their own columns. 
DuckDB will find the distinct values in each `ON` clause column and create one new column for all combinations of those values (a cartesian product).

In the below example, all combinations of unique countries and unique cities receive their own column. 
Some combinations may not be present in the underlying data, so those columns are populated with `NULL` values.
```sql
PIVOT Cities on Country, Name USING SUM(Population);
```

| Year | NL_Amsterdam | NL_New York City | NL_Seattle | US_Amsterdam | US_New York City | US_Seattle |
|------|--------------|------------------|------------|--------------|------------------|------------|
| 2000 | 1005         | NULL             | NULL       | NULL         | 8015             | 564        |
| 2010 | 1065         | NULL             | NULL       | NULL         | 8175             | 608        |
| 2020 | 1158         | NULL             | NULL       | NULL         | 8772             | 738        |

To pivot only the combinations of values that are present in the underlying data, use an expression in the `ON` clause.
Multiple expressions and/or columns may be provided.

Here, Country and Name are concatenated together and the resulting concatenations each receive their own column.
Any arbitrary non-aggregating expression may be used.
In this case, concatenating with an underscore is used to imitate the naming convention the `PIVOT` clause uses when multiple `ON` columns are provided (like in the prior example).
```sql
PIVOT Cities on Country || '_' || Name USING SUM(Population);
```

| Year | NL_Amsterdam | US_New York City | US_Seattle |
|------|--------------|------------------|------------|
| 2000 | 1005         | 8015             | 564        |
| 2010 | 1065         | 8175             | 608        |
| 2020 | 1158         | 8772             | 738        |


#### Multiple USING expressions
An alias may also be included for each expression in the `USING` clause. 
It will be appended to the generated column names after an underscore (`_`).
This makes the column naming convention much cleaner when multiple expressions are included in the `USING` clause.

In this example, both the `SUM` and `MAX` of the Population column are calculated for each year and are split into separate columns.
```sql
PIVOT Cities ON Year USING SUM(Population) as total, MAX(Population) as max GROUP BY Country;
```

| Country | 2000_total | 2000_max | 2010_total | 2010_max | 2020_total | 2020_max |
|---------|------------|----------|------------|----------|------------|----------|
| NL      | 1005       | 1005     | 1065       | 1065     | 1158       | 1158     |
| US      | 8579       | 8015     | 8783       | 8175     | 9510       | 8772     |


#### Multiple GROUP BY columns
Multiple `GROUP BY` columns may also be provided. 
Note that column names must be used rather than column positions (1, 2, etc.), and that expressions are not supported in the `GROUP BY` clause.

```sql
PIVOT Cities on Year USING SUM(Population) GROUP BY Country, Name;
```

| Country |     Name      | 2000 | 2010 | 2020 |
|---------|---------------|------|------|------|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |


### Using PIVOT within a SELECT statement
The `PIVOT` statement may be included within a SELECT statement as a CTE ([a Common Table Expression, or WITH clause](../query_syntax/with)), or a subquery.
This allows for a `PIVOT` to be used alongside other SQL logic, as well as for multiple `PIVOT`s to be used in one query.

No `SELECT` is needed within the CTE, the `PIVOT` keyword can be thought of as taking its place.
```sql
WITH pivot_alias AS (
    PIVOT Cities on Year USING SUM(Population) GROUP BY Country
) 
SELECT * FROM pivot_alias;
```

A `PIVOT` may be used in a subquery and must be wrapped in parentheses. 
Note that this behavior is different than the SQL Standard Pivot, as illustrated in subsequent examples.
```sql
SELECT 
    * 
FROM (
    PIVOT Cities on Year USING SUM(Population) GROUP BY Country
) pivot_alias;
```

#### Multiple Pivots
Each `PIVOT` can be treated as if it were a `SELECT` node, so they can be joined together or manipulated in other ways.

For example, if two `PIVOT` statments share the same `GROUP BY` expression, they can be joined together using the columns in the `GROUP BY` clause into a wider pivot.
```sql
FROM
    (PIVOT Cities ON Year USING SUM(Population) GROUP BY Country) year_pivot
JOIN
    (PIVOT Cities ON Name USING SUM(Population) GROUP BY Country) name_pivot
USING (Country);
```

| Country | 2000 | 2010 | 2020 | Amsterdam | New York City | Seattle |
|---------|------|------|------|-----------|---------------|---------|
| NL      | 1005 | 1065 | 1158 | 3228      | NULL          | NULL    |
| US      | 8579 | 8783 | 9510 | NULL      | 24962         | 1910    |


### Internals
Pivoting is implemented entirely as rewrites into SQL queries. 
Each `PIVOT` is implemented as set of aggregations with `FILTER` clauses.
Additional pre-processing steps are required if the columns to be created when pivoting are detected dynamically (which occurs when the `IN` clause is not in use).

DuckDB, like most SQL engines, requires that all column names and types be known at the start of a query.
In order to automatically detect the columns that should be created as a result of a `PIVOT` statement, it must be translated into multiple queries.
[`ENUM` types](../data_types/enum) are used to find the distinct values that should become columns. 
Each `ENUM` is then injected into one of the `PIVOT` statement's `IN` clauses.

After the `IN` clauses has been populated with `ENUM`s, the query is re-written again into a set of aggregations with `FILTER` clauses.

For example:
```sql
PIVOT Cities ON Year USING SUM(Population);
```

is initially translated into:
```sql
CREATE TEMPORARY TYPE __pivot_enum_0_0 AS ENUM (
    SELECT DISTINCT 
        Year::VARCHAR 
    FROM Cities 
    ORDER BY 
        Year
    );
PIVOT Cities ON Year IN __pivot_enum_0_0 USING SUM(Population);
```

and finally translated into:
```sql
SELECT 
    Country,
    Name,
    SUM(Population) FILTER (Year=2000) AS "2000",
    SUM(Population) FILTER (Year=2010) AS "2010",
    SUM(Population) FILTER (Year=2020) AS "2020"
FROM Cities
GROUP BY ALL;
```

This produces the result:

| Country |     Name      | 2000 | 2010 | 2020 |
|---------|---------------|------|------|------|
| NL      | Amsterdam     | 1005 | 1065 | 1158 |
| US      | Seattle       | 564  | 608  | 738  |
| US      | New York City | 8015 | 8175 | 8772 |


### Simplified Pivot Full Syntax Diagram
Below is the full syntax diagram of the `PIVOT` statement. 

<div id="rrdiagram"></div>


## SQL Standard Pivot Syntax
The full syntax diagram is below, but the SQL Standard `PIVOT` syntax can be summarized as:
```sql
FROM [dataset] 
PIVOT (
    [values(s)]
    FOR 
        [column_1] IN ([in_list])
        [column_2] IN ([in_list])
        ...
    GROUP BY [rows(s)]
)
```
Note that no commas separate the expressions in the `FOR` clause!


### SQL Standard Pivot Full Syntax Diagram
Below is the full syntax diagram of the SQL Standard version of the `PIVOT` statement. 

<div id="rrdiagram2"></div>