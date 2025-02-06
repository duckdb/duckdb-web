---
layout: docu
title: Combining Schemas
---

<!-- markdownlint-disable MD036 -->

## Examples

Read a set of CSV files combining columns by position:

```sql
SELECT * FROM read_csv('flights*.csv');
```

Read a set of CSV files combining columns by name:

```sql
SELECT * FROM read_csv('flights*.csv', union_by_name = true);
```

## Combining Schemas

When reading from multiple files, we have to **combine schemas** from those files. That is because each file has its own schema that can differ from the other files. DuckDB offers two ways of unifying schemas of multiple files: **by column position** and **by column name**.

By default, DuckDB reads the schema of the first file provided, and then unifies columns in subsequent files by column position. This works correctly as long as all files have the same schema. If the schema of the files differs, you might want to use the `union_by_name` option  to allow DuckDB to construct the schema by reading all of the names instead.

Below is an example of how both methods work.

## Union by Position

By default, DuckDB unifies the columns of these different files **by position**. This means that the first column in each file is combined together, as well as the second column in each file, etc. For example, consider the following two files.

[`flights1.csv`](/data/flights1.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-01|AA|New York, NY|Los Angeles, CA
1988-01-02|AA|New York, NY|Los Angeles, CA
```

[`flights2.csv`](/data/flights2.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-03|AA|New York, NY|Los Angeles, CA
```

Reading the two files at the same time will produce the following result set:

| FlightDate | UniqueCarrier | OriginCityName |  DestCityName   |
|------------|---------------|----------------|-----------------|
| 1988-01-01 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-02 | AA            | New York, NY   | Los Angeles, CA |
| 1988-01-03 | AA            | New York, NY   | Los Angeles, CA |

This is equivalent to the SQL construct [`UNION ALL`]({% link docs/archive/1.1/sql/query_syntax/setops.md %}#union-all).

## Union by Name

If you are processing multiple files that have different schemas, perhaps because columns have been added or renamed, it might be desirable to unify the columns of different files **by name** instead. This can be done by providing the `union_by_name` option. For example, consider the following two files, where `flights4.csv` has an extra column (`UniqueCarrier`).

[`flights3.csv`](/data/flights3.csv):

```csv
FlightDate|OriginCityName|DestCityName
1988-01-01|New York, NY|Los Angeles, CA
1988-01-02|New York, NY|Los Angeles, CA
```

[`flights4.csv`](/data/flights4.csv):

```csv
FlightDate|UniqueCarrier|OriginCityName|DestCityName
1988-01-03|AA|New York, NY|Los Angeles, CA
```

Reading these when unifying column names **by position** results in an error – as the two files have a different number of columns. When specifying the `union_by_name` option, the columns are correctly unified, and any missing values are set to `NULL`.

```sql
SELECT * FROM read_csv(['flights3.csv', 'flights4.csv'], union_by_name = true);
```

| FlightDate | OriginCityName |  DestCityName   | UniqueCarrier |
|------------|----------------|-----------------|---------------|
| 1988-01-01 | New York, NY   | Los Angeles, CA | NULL          |
| 1988-01-02 | New York, NY   | Los Angeles, CA | NULL          |
| 1988-01-03 | New York, NY   | Los Angeles, CA | AA            |

This is equivalent to the SQL construct [`UNION ALL BY NAME`]({% link docs/archive/1.1/sql/query_syntax/setops.md %}#union-all-by-name).

> Using the `union_by_name` option increases memory consumption.