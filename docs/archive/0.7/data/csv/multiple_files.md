---
layout: docu
title: Reading Multiple CSV Files
---

DuckDB can read multiple CSV files at the same time using either the glob syntax, or by providing a list of files to read.

```sql
-- read all files with a name ending in ".csv" in the folder "dir"
SELECT * FROM 'dir/*.csv';
-- read all files with a name ending in ".csv", two directories deep
SELECT * FROM '*/*/*.csv';
-- read the CSV files 'flights1.csv' and 'flights2.csv'
SELECT * FROM read_csv_auto(['flights1.csv', 'flights2.csv'])
```

#### Union By Position

By default, DuckDB unifies the columns of these different files **by position**. For example, consider the following two files:

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

This works correctly, as long as all CSV files have the same schema. If the schema of the files differs, however, this no longer works. This might occur if columns have been added in later files, for example.

#### Union By Name

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


#### Filename

The `filename` argument can be used to add an extra `filename` column to the result that indicates which row came from which file. For example:

```sql
SELECT * FROM read_csv_auto(['flights1.csv', 'flights2.csv'], union_by_name=True, filename=True)
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |   filename   |
|------------|----------------|-----------------|---------------|--------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          | flights1.csv |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            | flights2.csv |
