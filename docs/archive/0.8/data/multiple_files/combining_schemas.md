---
layout: docu
title: Combining Schemas
---

### Examples

```sql
-- read a set of CSV files combining columns by position
SELECT * FROM read_csv_auto('flights*.csv')
-- read a set of CSV files combining columns by name 
SELECT * FROM read_csv_auto('flights*.csv', union_by_name=True)
```

### Combining Schemas

When reading from multiple files, we have to **combine schemas** from those files. That is because each file has its own schema that can differ from the other files. DuckDB offers two ways of unifying schemas of multiple files: **by column position** and **by column name**.

By default, DuckDB reads the schema of the first file provided, and then unifies columns in subsequent files by column position. This works correctly as long as all files have the same schema. If the schema of the files differs, you might want to use the `union_by_name` option  to allow DuckDB to construct the schema by reading all of the names instead.

Below is an example of how both methods work.

### Union By Position

By default, DuckDB unifies the columns of these different files **by position**. This means that the first column in each file is combined together, as well as the second column in each file, etc. For example, consider the following two files:

**flights1.csv**
```
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-01|AA|New York, NY|Los Angeles, CA
1988-01-02|AA|New York, NY|Los Angeles, CA
```

**flights2.csv**
```
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-03|AA|New York, NY|Los Angeles, CA
```

Reading the two files at the same time will produce the following result set:

| FlightDate | UniqueCarrier | OriginCityName |  DestCityName   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

This is equivalent to the SQL construct [`UNION ALL`](../../sql/query_syntax/setops#union-all).

### Union By Name

If you are processing multiple files that have different schemas, perhaps because columns have been added or renamed, it might be desirable to unify the columns of different files **by name** instead. This can be done by providing the `union_by_name` option. For example, consider the following two files, where `flights2.csv` has an extra column (`UniqueCarrier`):

**flights1.csv**
```
FlightDate|OriginCityName|DestCityName
1988-01-01|New York, NY|Los Angeles, CA
1988-01-02|New York, NY|Los Angeles, CA
```

**flights2.csv**
```
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-03|AA|New York, NY|Los Angeles, CA
```

Reading these when unifying column names **by position** results in an error - as the two files have a different number of columns. When specifying the `union_by_name` option, the columns are correctly unified, and any missing values are set to `NULL`. 

```sql
SELECT * FROM read_csv_auto(['flights1.csv', 'flights2.csv'], union_by_name=True)
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |
|------------|----------------|-----------------|---------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            |


This is equivalent to the SQL construct [`UNION ALL BY NAME`](../../sql/query_syntax/setops#union-all-by-name).
