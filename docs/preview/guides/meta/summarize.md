---
layout: docu
title: Summarize
---

The `SUMMARIZE` command can be used to easily compute a number of aggregates over a table or a query.
The `SUMMARIZE` command launches a query that computes a number of aggregates over all columns (`min`, `max`, `approx_unique`, `avg`, `std`, `q25`, `q50`, `q75`, `count`), and return these along the column name, column type, and the percentage of `NULL` values in the column.
Note that the quantiles and percentiles are **approximate values**.

## Usage

To summarize the contents of a table, use `SUMMARIZE` followed by the table name.

```sql
SUMMARIZE tbl;
```

To summarize a query, prepend `SUMMARIZE` to a query.

```sql
SUMMARIZE SELECT * FROM tbl;
```

## Example

Below is an example of `SUMMARIZE` on the `lineitem` table of TPC-H `SF1` table, generated using the [`tpch` extension]({% link docs/preview/core_extensions/tpch.md %}).

```sql
INSTALL tpch;
LOAD tpch;
CALL dbgen(sf = 1);
```

```sql
SUMMARIZE lineitem;
```

|   column_name   |  column_type  |     min     |         max         | approx_unique |         avg         |         std          |   q25   |   q50   |   q75   |  count  | null_percentage |
|-----------------|---------------|-------------|---------------------|---------------|---------------------|----------------------|---------|---------|---------|---------|-----------------|
| l_orderkey      | INTEGER       | 1           | 6000000             | 1508227       | 3000279.604204982   | 1732187.8734803519   | 1509447 | 2989869 | 4485232 | 6001215 | 0.0%            |
| l_partkey       | INTEGER       | 1           | 200000              | 202598        | 100017.98932999402  | 57735.69082650496    | 49913   | 99992   | 150039  | 6001215 | 0.0%            |
| l_suppkey       | INTEGER       | 1           | 10000               | 10061         | 5000.602606138924   | 2886.9619987306114   | 2501    | 4999    | 7500    | 6001215 | 0.0%            |
| l_linenumber    | INTEGER       | 1           | 7                   | 7             | 3.0005757167506912  | 1.7324314036519328   | 2       | 3       | 4       | 6001215 | 0.0%            |
| l_quantity      | DECIMAL(15,2) | 1.00        | 50.00               | 50            | 25.507967136654827  | 14.426262537016918   | 13      | 26      | 38      | 6001215 | 0.0%            |
| l_extendedprice | DECIMAL(15,2) | 901.00      | 104949.50           | 923139        | 38255.138484656854  | 23300.43871096221    | 18756   | 36724   | 55159   | 6001215 | 0.0%            |
| l_discount      | DECIMAL(15,2) | 0.00        | 0.10                | 11            | 0.04999943011540163 | 0.03161985510812596  | 0       | 0       | 0       | 6001215 | 0.0%            |
| l_tax           | DECIMAL(15,2) | 0.00        | 0.08                | 9             | 0.04001350893110812 | 0.025816551798842728 | 0       | 0       | 0       | 6001215 | 0.0%            |
| l_returnflag    | VARCHAR       | A           | R                   | 3             | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_linestatus    | VARCHAR       | F           | O                   | 2             | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_shipdate      | DATE          | 1992-01-02  | 1998-12-01          | 2516          | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_commitdate    | DATE          | 1992-01-31  | 1998-10-31          | 2460          | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_receiptdate   | DATE          | 1992-01-04  | 1998-12-31          | 2549          | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_shipinstruct  | VARCHAR       | COLLECT COD | TAKE BACK RETURN    | 4             | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_shipmode      | VARCHAR       | AIR         | TRUCK               | 7             | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |
| l_comment       | VARCHAR       |  Tiresias   | zzle? furiously iro | 3558599       | NULL                | NULL                 | NULL    | NULL    | NULL    | 6001215 | 0.0%            |

## Using `SUMMARIZE` in a Subquery

`SUMMARIZE` can be used as a subquery. This allows creating a table from the summary, for example:

```sql
CREATE TABLE tbl_summary AS SELECT * FROM (SUMMARIZE tbl);
```

## Summarizing Remote Tables

It is possible to summarize remote tables via the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) using the `SUMMARIZE TABLE` statement. For example:

```sql
SUMMARIZE TABLE 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv';
```
