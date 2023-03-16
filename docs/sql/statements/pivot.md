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

### Examples
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

Use the `PIVOT` statement below to create a separate column for each year and calculate the total population in each.
The `ON` clause specifies which column(s) to split into separate columns.
It is equivalent to the columns parameter in a spreadsheet pivot table.

The `USING` clause determines how to aggregate the values that are split into separate columns.
This is equivalent to the values parameter in a spreadsheet pivot table.
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


Multiple columns can be specified in the `ON` and `GROUP BY` clauses, and multiple aggregate expressions can be included in the `USING` clause.

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



To only create a separate column for specific values within a column in the `ON` clause, add an `IN` clause.
Let's say for example that we wanted to forget about the year 2020 for no particular reason...
```sql
PIVOT Cities ON Year IN (2000, 2010) USING SUM(Population) GROUP BY Country;
```

| Country | 2000 | 2010 |
|---------|------|------|
| NL      | 1005 | 1065 |
| US      | 8579 | 8783 |



### Simplified Pivot Full Syntax Diagram
Below is the full syntax diagram of the `PIVOT` statement. 

<div id="rrdiagram"></div>


## SQL Standard Pivot Syntax
The full syntax diagram is below, but the SQL Standard `PIVOT` syntax can be summarized as:
```sql
FROM [dataset] 
PIVOT (
    [aggregate_expression(s)]
    FOR 
        [pivot_column_1] IN ([in-list])
        [pivot_column_2] IN ([in-list])
        ...
    GROUP BY [group_by_expression(s)]
)
```