---
layout: docu
title: Unpivot Statement
selected: Documentation/SQL/Unpivot
expanded: SQL
railroad: statements/unpivot.js
blurb: The UNPIVOT statement allows columns to be stacked into rows that indicate the prior column name and value.
---

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



<!-- Maybe we swap to using monthly sales as an example? -->



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


### PIVOT ON, USING, and GROUP BY

### IN filter for ON clause


### Multiple expressions per clause


#### Multiple ON columns and ON expressions

#### Multiple USING expressions

#### Multiple GROUP BY columns


### Using PIVOT within a SELECT statement


#### Multiple Pivots


### Internals
Pivoting is implemented entirely as rewrites into SQL queries. 
Each `PIVOT` is implemented as set of aggregations with `FILTER` clauses.
Additional pre-processing steps are required if the columns to be created when pivoting are detected dynamically (which occurs when the `IN` clause is not in use).

DuckDB, like most SQL engines, requires that all column names and types be known at the start of a query.
In order to automatically detect the columns that should be created as a result of a `PIVOT` statement, it must be translated into multiple queries.
[`ENUM` types](../data_types/enum) are used to find the distinct values that should become columns. 
Each `ENUM` is then injected into one of the `PIVOT` statement's `IN` clauses.

After the `IN` clauses have been populated with `ENUM`s, the query is re-written again into a set of aggregations with `FILTER` clauses.

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
Unlike the simplified syntax, the `IN` clause must be specified for each column to be pivoted.
If you are interested in dynamic pivoting, the simplified syntax is recommended.

Note that no commas separate the expressions in the `FOR` clause, but that `value` and `GROUP BY` expressions must be comma-separated!

### Examples


### SQL Standard Pivot Full Syntax Diagram
Below is the full syntax diagram of the SQL Standard version of the `PIVOT` statement. 

<div id="rrdiagram2"></div>
