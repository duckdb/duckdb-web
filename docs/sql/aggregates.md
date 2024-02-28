---
layout: docu
title: Aggregate Functions
railroad: expressions/aggregate.js
---

## Examples

```sql
-- produce a single row containing the sum of the "amount" column
SELECT sum(amount) FROM sales;
-- produce one row per unique region, containing the sum of "amount" for each group
SELECT region, sum(amount) FROM sales GROUP BY region;
-- return only the regions that have a sum of "amount" higher than 100
SELECT region FROM sales GROUP BY region HAVING sum(amount) > 100;
-- return the number of unique values in the "region" column
SELECT count(DISTINCT region) FROM sales;
-- return two values, the total sum of "amount" and the sum of "amount" minus columns where the region is "north"
SELECT sum(amount), sum(amount) FILTER (region != 'north') FROM sales;
-- returns a list of all regions in order of the "amount" column
SELECT list(region ORDER BY amount DESC) FROM sales;
-- returns the amount of the first sale using the first() aggregate function
SELECT first(amount ORDER BY date ASC) FROM sales;
```

## Syntax

<div id="rrdiagram"></div>

Aggregates are functions that *combine* multiple rows into a single value. Aggregates are different from scalar functions and window functions because they change the cardinality of the result. As such, aggregates can only be used in the `SELECT` and `HAVING` clauses of a SQL query.

### `DISTINCT` Clause in Aggregate Functions

When the `DISTINCT` clause is provided, only distinct values are considered in the computation of the aggregate. This is typically used in combination with the `count` aggregate to get the number of distinct elements; but it can be used together with any aggregate function in the system.

### `ORDER BY` Clause in Aggregate Functions

An `ORDER BY` clause can be provided after the last argument of the function call. Note the lack of the comma separator before the clause.

```sql
SELECT ⟨aggregate_function⟩(⟨arg⟩, ⟨sep⟩ ORDER BY ⟨ordering_criteria⟩);
```

This clause ensures that the values being aggregated are sorted before applying the function.
Most aggregate functions are order-insensitive, therefore, this clause is parsed and applied, which is inefficient, but has on effect on the results.
However, there are some order-sensitive aggregates that can have non-deterministic results without ordering, e.g., `first`, `last`, `list` and `string_agg` / `group_concat` / `listagg`.
These can be made deterministic by ordering the arguments.

For example:

```sql
CREATE TABLE tbl AS SELECT s FROM range(1, 4) r(s);
SELECT string_agg(s, ', ' ORDER BY s DESC) AS countdown FROM tbl;
```
```text
┌───────────┐
│ countdown │
│  varchar  │
├───────────┤
│ 3, 2, 1   │
└───────────┘
```

## General Aggregate Functions

The table below shows the available general aggregate functions.

| Function | Description | Example | Alias(es) |
|:--|:---|:--|:--|
| `any_value(arg)` |Returns the first non-null value from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). | `any_value(A)` | |
| `arbitrary(arg)` |Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). | `arbitrary(A)` | `first(A)` |
| `arg_max(arg, val)` |Finds the row with the maximum `val`. Calculates the `arg` expression at that row. | `arg_max(A, B)` | `argMax(arg, val)`, `max_by(arg, val)` |
| `arg_min(arg, val)` |Finds the row with the minimum `val`. Calculates the `arg` expression at that row. | `arg_min(A, B)` | `argMin(arg, val)`, `min_by(arg, val)` |
| `avg(arg)` |Calculates the average value for all tuples in `arg`. | `avg(A)` | `mean` |
| `bit_and(arg)` |Returns the bitwise AND of all bits in a given expression. | `bit_and(A)` | - |
| `bit_or(arg)` |Returns the bitwise OR of all bits in a given expression.  | `bit_or(A)` | - |
| `bit_xor(arg)` |Returns the bitwise XOR of all bits in a given expression. | `bit_xor(A)` | - |
| `bitstring_agg(arg)` |Returns a bitstring with bits set for each distinct value. | `bitstring_agg(A)` | - |
| `bool_and(arg)` |Returns `true` if every input value is `true`, otherwise `false`. | `bool_and(A)` | - |
| `bool_or(arg)` |Returns `true` if any input value is `true`, otherwise `false`. | `bool_or(A)` | - |
| `count(arg)` |Calculates the number of tuples in `arg`. | `count(A)` | - |
| `favg(arg)` |Calculates the average using a more accurate floating point summation (Kahan Sum). | `favg(A)` | - |
| `first(arg)` |Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). | `first(A)` | `arbitrary(A)` |
| `fsum(arg)` |Calculates the sum using a more accurate floating point summation (Kahan Sum). | `fsum(A)` | `sumKahan`, `kahan_sum` |
| `geomean(arg)` |Calculates the geometric mean for all tuples in `arg`. | `geomean(A)` | `geometric_mean(A)` |
| `histogram(arg)` |Returns a `MAP` of key-value pairs representing buckets and counts. | `histogram(A)` | - |
| `last(arg)` |Returns the last value of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). | `last(A)` | - |
| `list(arg)` |Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). | `list(A)` |`array_agg` |
| `max(arg)` |Returns the maximum value present in `arg`. | `max(A)` | - |
| `min(arg)` |Returns the minimum value present in `arg`. | `min(A)` | - |
| `product(arg)` |Calculates the product of all tuples in `arg`. | `product(A)` | - |
| `string_agg(arg, sep)` |Concatenates the column string values with a separator. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). | `string_agg(S, ',')` | `group_concat(arg, sep)`, `listagg(arg, sep)` |
| `sum(arg)` |Calculates the sum value for all tuples in `arg`. | `sum(A)` | - |
| `sum_no_overflow(arg)` |Calculates the sum value for all tuples in `arg` without [overflow](https://en.wikipedia.org/wiki/Integer_overflow) checks. Unlike `sum`, which works on floating-point values, `sum_no_overflow` only accepts `INTEGER` and `DECIMAL` values.| `sum_no_overflow(A)` | - |

## Approximate Aggregates

The table below shows the available approximate aggregate functions.

| Function | Description | Example |
|:---|:---|:---|
| `approx_count_distinct(x)` | Gives the approximate count of distinct elements using HyperLogLog. | `approx_count_distinct(A)` |
| `approx_quantile(x, pos)` | Gives the approximate quantile using T-Digest. | `approx_quantile(A, 0.5)` |
| `reservoir_quantile(x, quantile, sample_size = 8192)` | Gives the approximate quantile using reservoir sampling, the sample size is optional and uses 8192 as a default size. | `reservoir_quantile(A, 0.5, 1024)` |

## Statistical Aggregates

The table below shows the available statistical aggregate functions.

| Function | Description | Formula | Alias |
|:--|:---|:--|:-|
| `corr(y, x)` | Returns the correlation coefficient for non-null pairs in a group. | `covar_pop(y, x) / (stddev_pop(x) * stddev_pop(y))`| - |
| `covar_pop(y, x)` | Returns the population covariance of input values. | `(sum(x*y) - sum(x) * sum(y) / count(*)) / count(*)` | - |
| `covar_samp(y, x)` | Returns the sample covariance for non-null pairs in a group. | `(sum(x*y) - sum(x) * sum(y) / count(*)) / (count(*) - 1)` | - |
| `entropy(x)` | Returns the log-2 entropy of count input-values. | - | - |
| `kurtosis_pop(x)` | Returns the excess kurtosis (Fisher's definition) of all input values. Bias correction is not applied. | - | - |
| `kurtosis(x)` | Returns the excess kurtosis (Fisher's definition) of all input values, with a bias correction according to the sample size. | - | - |
| `mad(x)` | Returns the median absolute deviation for the values within x. NULL values are ignored. Temporal types return a positive `INTERVAL`. | `median(abs(x - median(x)))` | - |
| `median(x)` | Returns the middle value of the set. NULL values are ignored. For even value counts, quantitative values are averaged and ordinal values return the lower value. | `quantile_cont(x, 0.5)` | - |
| `mode(x)` | Returns the most frequent value for the values within x. NULL values are ignored. | - | - |
| `quantile_cont(x, pos)` | Returns the interpolated quantile number between 0 and 1 . If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding interpolated quantiles. | - | - |
| `quantile_disc(x, pos)` | Returns the exact quantile number between 0 and 1 . If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding exact quantiles. | - | `quantile` |
| `regr_avgx(y, x)` | Returns the average of the independent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. | - | - |
| `regr_avgy(y, x)` | Returns the average of the dependent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. | - | - |
| `regr_count(y, x)` | Returns the number of non-null number pairs in a group. | `(sum(x*y) - sum(x) * sum(y) / count(*)) / count(*)` | - |
| `regr_intercept(y, x)` | Returns the intercept of the univariate linear regression line for non-null pairs in a group. | `avg(y) - regr_slope(y, x) * avg(x)` | - |
| `regr_r2(y, x)` | Returns the coefficient of determination for non-null pairs in a group. | - | - |
| `regr_slope(y, x)` | Returns the slope of the linear regression line for non-null pairs in a group.| `covar_pop(x, y) / var_pop(x)` | - |
| `regr_sxx(y, x)` | -  | `regr_count(y, x) * var_pop(x)` | - |
| `regr_sxy(y, x)` | Returns the population covariance of input values. | `regr_count(y, x) * covar_pop(y, x)` | - |
| `regr_syy(y, x)` | - | `regr_count(y, x) * var_pop(y)` | - |
| `skewness(x)` | Returns the skewness of all input values. | - | - |
| `stddev_pop(x)` | Returns the population standard deviation.  | `sqrt(var_pop(x))` | - |
| `stddev_samp(x)` | Returns the sample standard deviation. | `sqrt(var_samp(x))` | `stddev(x)` |
| `var_pop(x)` | Returns the population variance. | - | - |
| `var_samp(x)` | Returns the sample variance of all input values. | `(sum(x^2) - sum(x)^2 / count(x)) / (count(x) - 1)` | `variance(arg, val)` |

## Ordered Set Aggregate Functions

The table below shows the available "ordered set" aggregate functions.
These functions are specified using the `WITHIN GROUP (ORDER BY sort_expression)` syntax,
and they are converted to an equivalent aggregate function that takes the ordering expression
as the first argument.

| Function | Equivalent |
|:---|:---|
| `mode() WITHIN GROUP (ORDER BY sort_expression)` | `mode(sort_expression)` |
| `percentile_cont(fraction) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_cont(sort_expression, fraction)` |
| `percentile_cont(fractions) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_cont(sort_expression, fractions)` |
| `percentile_disc(fraction) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_disc(sort_expression, fraction)` |
| `percentile_disc(fractions) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_disc(sort_expression, fractions)` |

## Miscellaneous Aggregate Functions

| Function | Description | Alias |
|:--|:---|:--|
| `grouping()` | For queries with `GROUP BY` and either [`ROLLUP` or `GROUPING SETS`](query_syntax/grouping_sets#identifying-grouping-sets-with-grouping_id): Returns an integer identifying which of the argument expressions where used to group on to create the current supper-aggregate row. | `grouping_id()` |

