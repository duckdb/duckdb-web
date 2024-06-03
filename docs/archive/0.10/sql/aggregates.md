---
layout: docu
railroad: expressions/aggregate.js
title: Aggregate Functions
---

## Examples

Produce a single row containing the sum of the `amount` column:

```sql
SELECT sum(amount) FROM sales;
```

Produce one row per unique region, containing the sum of `amount` for each group:

```sql
SELECT region, sum(amount) FROM sales GROUP BY region;
```

Return only the regions that have a sum of `amount` higher than 100:

```sql
SELECT region FROM sales GROUP BY region HAVING sum(amount) > 100;
```

Return the number of unique values in the `region` column:

```sql
SELECT count(DISTINCT region) FROM sales;
```

Return two values, the total sum of `amount` and the sum of `amount` minus columns where the region is `north`:

```sql
SELECT sum(amount), sum(amount) FILTER (region != 'north') FROM sales;
```

Returns a list of all regions in order of the `amount` column:

```sql
SELECT list(region ORDER BY amount DESC) FROM sales;
```

Returns the amount of the first sale using the `first()` aggregate function:

```sql
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
Most aggregate functions are order-insensitive, and for them this clause is parsed and discarded.
However, there are some order-sensitive aggregates that can have non-deterministic results without ordering, e.g., `first`, `last`, `list` and `string_agg` / `group_concat` / `listagg`.
These can be made deterministic by ordering the arguments.

For example:

```sql
CREATE TABLE tbl AS SELECT s FROM range(1, 4) r(s);
SELECT string_agg(s, ', ' ORDER BY s DESC) AS countdown FROM tbl;
```

| countdown |
|-----------|
| 3, 2, 1   |

## General Aggregate Functions

The table below shows the available general aggregate functions.

| Function | Description |
|:--|:--------|
| [`any_value(arg)`](#any_valuearg) | Returns the first non-null value from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arbitrary(arg)`](#arbitraryarg) | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_max(arg, val)`](#arg_maxarg-val) | Finds the row with the maximum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_min(arg, val)`](#arg_minarg-val) | Finds the row with the minimum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`array_agg(arg)`](#array_aggarg) | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`avg(arg)`](#avgarg) | Calculates the average value for all tuples in `arg`. |
| [`bit_and(arg)`](#bit_andarg) | Returns the bitwise AND of all bits in a given expression. |
| [`bit_or(arg)`](#bit_orarg) | Returns the bitwise OR of all bits in a given expression. |
| [`bit_xor(arg)`](#bit_xorarg) | Returns the bitwise XOR of all bits in a given expression. |
| [`bitstring_agg(arg)`](#bitstring_aggarg) | Returns a bitstring with bits set for each distinct value. |
| [`bool_and(arg)`](#bool_andarg) | Returns `true` if every input value is `true`, otherwise `false`. |
| [`bool_or(arg)`](#bool_orarg) | Returns `true` if any input value is `true`, otherwise `false`. |
| [`count(arg)`](#countarg) | Calculates the number of tuples in `arg`. |
| [`favg(arg)`](#favgarg) | Calculates the average using a more accurate floating point summation (Kahan Sum). |
| [`first(arg)`](#firstarg) | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`fsum(arg)`](#fsumarg) | Calculates the sum using a more accurate floating point summation (Kahan Sum). |
| [`geomean(arg)`](#geomeanarg) | Calculates the geometric mean for all tuples in `arg`. |
| [`histogram(arg)`](#histogramarg) | Returns a `MAP` of key-value pairs representing buckets and counts. |
| [`last(arg)`](#lastarg) | Returns the last value of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`list(arg)`](#listarg) | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`max(arg)`](#maxarg) | Returns the maximum value present in `arg`. |
| [`max_by(arg, val)`](#max_byarg-val) | Finds the row with the maximum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`min(arg)`](#minarg) | Returns the minimum value present in `arg`. |
| [`min_by(arg, val)`](#min_byarg-val) | Finds the row with the minimum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`product(arg)`](#productarg) | Calculates the product of all tuples in `arg`. |
| [`string_agg(arg, sep)`](#string_aggarg-sep) | Concatenates the column string values with a separator. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`sum(arg)`](#sumarg) | Calculates the sum value for all tuples in `arg`. |
| [`sum_no_overflow(arg)`](#sum_no_overflowarg) | Calculates the sum value for all tuples in `arg` without [overflow](https://en.wikipedia.org/wiki/Integer_overflow) checks. Unlike `sum`, which works on floating-point values, `sum_no_overflow` only accepts `INTEGER` and `DECIMAL` values. |

### `any_value(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the first non-null value from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `any_value(A)` |
| **Alias(es)** | - |

### `arbitrary(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arbitrary(A)` |
| **Alias(es)** | `first(A)` |

### `arg_max(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the maximum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_max(A, B)` |
| **Alias(es)** | `argMax(arg, val)`, `max_by(arg, val)` |

### `arg_min(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the minimum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_min(A, B)` |
| **Alias(es)** | `argMin(arg, val)`, `min_by(arg, val)` |

### `array_agg(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `array_agg(A)` |
| **Alias(es)** | `list` |

### `avg(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the average value for all tuples in `arg`. |
| **Example** | `avg(A)` |
| **Alias(es)** | `mean` |

### `bit_and(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise `AND` of all bits in a given expression. |
| **Example** | `bit_and(A)` |
| **Alias(es)** | - |

### `bit_or(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise `OR` of all bits in a given expression. |
| **Example** | `bit_or(A)` |
| **Alias(es)** | - |

### `bit_xor(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise `XOR` of all bits in a given expression. |
| **Example** | `bit_xor(A)` |
| **Alias(es)** | - |

### `bitstring_agg(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a bitstring with bits set for each distinct value. |
| **Example** | `bitstring_agg(A)` |
| **Alias(es)** | - |

### `bool_and(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if every input value is `true`, otherwise `false`. |
| **Example** | `bool_and(A)` |
| **Alias(es)** | - |

### `bool_or(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if any input value is `true`, otherwise `false`. |
| **Example** | `bool_or(A)` |
| **Alias(es)** | - |

### `count(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the number of tuples in `arg`. |
| **Example** | `count(A)` |
| **Alias(es)** | - |

### `favg(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the average using a more accurate floating point summation (Kahan Sum). |
| **Example** | `favg(A)` |
| **Alias(es)** | - |

### `first(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `first(A)` |
| **Alias(es)** | `arbitrary(A)` |

### `fsum(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the sum using a more accurate floating point summation (Kahan Sum). |
| **Example** | `fsum(A)` |
| **Alias(es)** | `sumKahan`, `kahan_sum` |

### `geomean(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the geometric mean for all tuples in `arg`. |
| **Example** | `geomean(A)` |
| **Alias(es)** | `geometric_mean(A)` |

### `histogram(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a `MAP` of key-value pairs representing buckets and counts. |
| **Example** | `histogram(A)` |
| **Alias(es)** | - |

### `last(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the last value of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `last(A)` |
| **Alias(es)** | - |

### `list(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `list(A)` |
| **Alias(es)** | `array_agg` |

### `max(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the maximum value present in `arg`. |
| **Example** | `max(A)` |
| **Alias(es)** | - |

### `max_by(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the maximum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `max_by(A, B)` |
| **Alias(es)** | `argMax(arg, val)`, `arg_max(arg, val)` |

### `min(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the minimum value present in `arg`. |
| **Example** | `min(A)` |
| **Alias(es)** | - |

### `min_by(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the minimum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `min_by(A, B)` |
| **Alias(es)** | `argMin(arg, val)`, `arg_min(arg, val)` |

### `product(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the product of all tuples in `arg`. |
| **Example** | `product(A)` |
| **Alias(es)** | - |

### `string_agg(arg, sep)`

<div class="nostroke_table"></div>

| **Description** | Concatenates the column string values with a separator. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `string_agg(S, ',')` |
| **Alias(es)** | `group_concat(arg, sep)`, `listagg(arg, sep)` |

### `sum(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the sum value for all tuples in `arg`. |
| **Example** | `sum(A)` |
| **Alias(es)** | - |

### `sum_no_overflow(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the sum value for all tuples in `arg` without [overflow](https://en.wikipedia.org/wiki/Integer_overflow) checks. Unlike `sum`, which works on floating-point values, `sum_no_overflow` only accepts `INTEGER` and `DECIMAL` values. |
| **Example** | `sum_no_overflow(A)` |
| **Alias(es)** | - |

## Approximate Aggregates

The table below shows the available approximate aggregate functions.

| Function | Description | Example |
|:---|:---|:---|
| `approx_count_distinct(x)` | Gives the approximate count of distinct elements using HyperLogLog. | `approx_count_distinct(A)` |
| `approx_quantile(x, pos)` | Gives the approximate quantile using T-Digest. | `approx_quantile(A, 0.5)` |
| `reservoir_quantile(x, quantile, sample_size = 8192)` | Gives the approximate quantile using reservoir sampling, the sample size is optional and uses 8192 as a default size. | `reservoir_quantile(A, 0.5, 1024)` |

## Statistical Aggregates

The table below shows the available statistical aggregate functions.

| Function | Description |
|:--|:--------|
| [`corr(y, x)`](#corry-x) | Returns the correlation coefficient for non-null pairs in a group. |
| [`covar_pop(y, x)`](#covar_popy-x) | Returns the population covariance of input values. |
| [`covar_samp(y, x)`](#covar_sampy-x) | Returns the sample covariance for non-null pairs in a group. |
| [`entropy(x)`](#entropyx) | Returns the log-2 entropy of count input-values. |
| [`kurtosis_pop(x)`](#kurtosis_popx) | Returns the excess kurtosis (Fisher's definition) of all input values. Bias correction is not applied. |
| [`kurtosis(x)`](#kurtosisx) | Returns the excess kurtosis (Fisher's definition) of all input values, with a bias correction according to the sample size. |
| [`mad(x)`](#madx) | Returns the median absolute deviation for the values within x. NULL values are ignored. Temporal types return a positive `INTERVAL`. |
| [`median(x)`](#medianx) | Returns the middle value of the set. NULL values are ignored. For even value counts, quantitative values are averaged and ordinal values return the lower value. |
| [`mode(x)`](#modex)| Returns the most frequent value for the values within x. NULL values are ignored. |
| [`quantile_cont(x, pos)`](#quantile_contx-pos) | Returns the interpolated `pos`-quantile of `x` for `0 <= pos <= 1`, i.e., orders the values of `x` and returns the `pos * (n_nonnull_values - 1)`th (zero-indexed) element (or an interpolation between the adjacent elements if the index is not an integer). If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding interpolated quantiles. |
| [`quantile_disc(x, pos)`](#quantile_discx-pos) | Returns the discrete `pos`-quantile of `x` for `0 <= pos <= 1`, i.e., orders the values of `x` and returns the `floor(pos * (n_nonnull_values - 1))`th (zero-indexed) element. If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding discrete quantiles. |
| [`regr_avgx(y, x)`](#regr_avgxy-x) | Returns the average of the independent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. |
| [`regr_avgy(y, x)`](#regr_avgyy-x) | Returns the average of the dependent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. |
| [`regr_count(y, x)`](#regr_county-x) | Returns the number of non-null number pairs in a group. |
| [`regr_intercept(y, x)`](#regr_intercepty-x) | Returns the intercept of the univariate linear regression line for non-null pairs in a group. |
| [`regr_r2(y, x)`](#regr_r2y-x) | Returns the coefficient of determination for non-null pairs in a group. |
| [`regr_slope(y, x)`](#regr_slopey-x) | Returns the slope of the linear regression line for non-null pairs in a group. |
| [`regr_sxx(y, x)`](#regr_sxxy-x) | - |
| [`regr_sxy(y, x)`](#regr_sxyy-x) | Returns the population covariance of input values. |
| [`regr_syy(y, x)`](#regr_syyy-x) | - |
| [`skewness(x)`](#skewnessx) | Returns the skewness of all input values. |
| [`stddev_pop(x)`](#stddev_popx) | Returns the population standard deviation. |
| [`stddev_samp(x)`](#stddev_sampx) | Returns the sample standard deviation. |
| [`var_pop(x)`](#var_popx) | Returns the population variance. |
| [`var_samp(x)`](#var_sampx) | Returns the sample variance of all input values. |


### `corr(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the correlation coefficient for non-`NULL` pairs in a group.
| **Formula** | `covar_pop(y, x) / (stddev_pop(x) * stddev_pop(y))` |
| **Alias(es)** | - |

### `covar_pop(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the population covariance of input values. |
| **Formula** | `(sum(x*y) - sum(x) * sum(y) / count(*)) / count(*)` |
| **Alias(es)** | - |

### `covar_samp(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the sample covariance for non-`NULL` pairs in a group. |
| **Formula** | `(sum(x*y) - sum(x) * sum(y) / count(*)) / (count(*) - 1)` |
| **Alias(es)** | - |

### `entropy(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the log-2 entropy of count input-values. |
| **Formula** | - |
| **Alias(es)** | - |

### `kurtosis_pop(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the excess kurtosis (Fisher's definition) of all input values. Bias correction is not applied. |
| **Formula** | - |
| **Alias(es)** | - |

### `kurtosis(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the excess kurtosis (Fisher's definition) of all input values, with a bias correction according to the sample size. |
| **Formula** | - |
| **Alias(es)** | - |

### `mad(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the median absolute deviation for the values within x. `NULL` values are ignored. Temporal types return a positive `INTERVAL`. |
| **Formula** | `median(abs(x - median(x)))` |
| **Alias(es)** | - |

### `median(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the middle value of the set. `NULL` values are ignored. For even value counts, quantitative values are averaged and ordinal values return the lower value. |
| **Formula** | `quantile_cont(x, 0.5)` |
| **Alias(es)** | - |

### `mode(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the most frequent value for the values within x. `NULL` values are ignored. |
| **Formula** | - |
| **Alias(es)** | - |

### `quantile_cont(x, pos)`

<div class="nostroke_table"></div>

| **Description** | Returns the interpolated `pos`-quantile of `x` for `0 <= pos <= 1`, i.e., orders the values of `x` and returns the `pos * (n_nonnull_values - 1)`th (zero-indexed) element (or an interpolation between the adjacent elements if the index is not an integer). If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding interpolated quantiles. |
| **Formula** | - |
| **Alias(es)** | - |

### `quantile_disc(x, pos)`

<div class="nostroke_table"></div>

| **Description** | Returns the discrete `pos`-quantile of `x` for `0 <= pos <= 1`, i.e., orders the values of `x` and returns the `floor(pos * (n_nonnull_values - 1))`th (zero-indexed) element. If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding discrete quantiles. |
| **Formula** | - |
| **Alias(es)** | `quantile` |

### `regr_avgx(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the average of the independent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

### `regr_avgy(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the average of the dependent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

### `regr_count(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the number of non-null number pairs in a group. |
| **Formula** | `(sum(x*y) - sum(x) * sum(y) / count(*)) / count(*)` |
| **Alias(es)** | - |

### `regr_intercept(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the intercept of the univariate linear regression line for non-null pairs in a group. |
| **Formula** | `avg(y) - regr_slope(y, x) * avg(x)` |
| **Alias(es)** | - |

### `regr_r2(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the coefficient of determination for non-null pairs in a group. |
| **Formula** | - |
| **Alias(es)** | - |

### `regr_slope(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the slope of the linear regression line for non-null pairs in a group. |
| **Formula** | `covar_pop(x, y) / var_pop(x)` |
| **Alias(es)** | - |

### `regr_sxx(y, x)`

<div class="nostroke_table"></div>

| **Description** | - |
| **Formula** | `regr_count(y, x) * var_pop(x)` |
| **Alias(es)** | - |

### `regr_sxy(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the population covariance of input values. |
| **Formula** | `regr_count(y, x) * covar_pop(y, x)` |
| **Alias(es)** | - |

### `regr_syy(y, x)`

<div class="nostroke_table"></div>

| **Description** | - |
| **Formula** | `regr_count(y, x) * var_pop(y)` |
| **Alias(es)** | - |

### `skewness(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the skewness of all input values. |
| **Formula** | - |
| **Alias(es)** | - |

### `stddev_pop(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the population standard deviation. |
| **Formula** | `sqrt(var_pop(x))` |
| **Alias(es)** | - |

### `stddev_samp(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the sample standard deviation. |
| **Formula** | `sqrt(var_samp(x))`|
| **Alias(es)** | `stddev(x)`|

### `var_pop(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the population variance. |
| **Formula** | - |
| **Alias(es)** | - |

### `var_samp(x)`

<div class="nostroke_table"></div>

| **Description** | Returns the sample variance of all input values. |
| **Formula** | `(sum(x^2) - sum(x)^2 / count(x)) / (count(x) - 1)` |
| **Alias(es)** | `variance(arg, val)` |

## Ordered Set Aggregate Functions

The table below shows the available "ordered set" aggregate functions.
These functions are specified using the `WITHIN GROUP (ORDER BY sort_expression)` syntax,
and they are converted to an equivalent aggregate function that takes the ordering expression
as the first argument.

| Function | Equivalent |
|:---|:---|
| <code>mode() WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>mode(column ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_cont(fraction) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_cont(column, fraction ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_cont(fractions) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_cont(column, fractions ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_disc(fraction) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_disc(column, fraction ORDER BY column [(ASC&#124;DESC)])</code> |
| <code>percentile_disc(fractions) WITHIN GROUP (ORDER BY column [(ASC&#124;DESC)])</code> | <code>quantile_disc(column, fractions ORDER BY column [(ASC&#124;DESC)])</code> |

## Miscellaneous Aggregate Functions

| Function | Description | Alias |
|:--|:---|:--|
| `grouping()` | For queries with `GROUP BY` and either [`ROLLUP` or `GROUPING SETS`](query_syntax/grouping_sets#identifying-grouping-sets-with-grouping_id): Returns an integer identifying which of the argument expressions where used to group on to create the current supper-aggregate row. | `grouping_id()` |