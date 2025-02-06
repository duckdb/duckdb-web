---
layout: docu
title: Aggregate Functions
railroad: expressions/aggregate.js
redirect_from:
  - docs/sql/aggregates
---

<!-- markdownlint-disable MD001 -->

## Examples

Produce a single row containing the sum of the `amount` column:

```sql
SELECT sum(amount)
FROM sales;
```

Produce one row per unique region, containing the sum of `amount` for each group:

```sql
SELECT region, sum(amount)
FROM sales
GROUP BY region;
```

Return only the regions that have a sum of `amount` higher than 100:

```sql
SELECT region
FROM sales
GROUP BY region
HAVING sum(amount) > 100;
```

Return the number of unique values in the `region` column:

```sql
SELECT count(DISTINCT region)
FROM sales;
```

Return two values, the total sum of `amount` and the sum of `amount` minus columns where the region is `north` using the [`FILTER` clause]({% link docs/sql/query_syntax/filter.md %}):

```sql
SELECT sum(amount), sum(amount) FILTER (region != 'north')
FROM sales;
```

Returns a list of all regions in order of the `amount` column:

```sql
SELECT list(region ORDER BY amount DESC)
FROM sales;
```

Returns the amount of the first sale using the `first()` aggregate function:

```sql
SELECT first(amount ORDER BY date ASC)
FROM sales;
```

## Syntax

<div id="rrdiagram"></div>

Aggregates are functions that *combine* multiple rows into a single value. Aggregates are different from scalar functions and window functions because they change the cardinality of the result. As such, aggregates can only be used in the `SELECT` and `HAVING` clauses of a SQL query.

### `DISTINCT` Clause in Aggregate Functions

When the `DISTINCT` clause is provided, only distinct values are considered in the computation of the aggregate. This is typically used in combination with the `count` aggregate to get the number of distinct elements; but it can be used together with any aggregate function in the system.
There are some aggregates that are insensitive to duplicate values (e.g., `min` and `max`) and for them this clause is parsed and ignored.

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
CREATE TABLE tbl AS
    SELECT s FROM range(1, 4) r(s);

SELECT string_agg(s, ', ' ORDER BY s DESC) AS countdown
FROM tbl;
```

| countdown |
|-----------|
| 3, 2, 1   |

### Handling `NULL` Values

All general aggregate functions except for [`list`](#listarg) and [`first`](#firstarg) (and their aliases [`array_agg`](#array_aggarg) and [`arbitrary`](#arbitraryarg), respectively) ignore `NULL`s.
To exclude `NULL`s from `list`, you can use a [`FILTER` clause]({% link docs/sql/query_syntax/filter.md %}).
To ignore `NULL`s from `first`, you can use the [`any_value` aggregate](#any_valuearg).

All general aggregate functions except [`count`](#countarg) return `NULL` on empty groups.
In particular, [`list`](#listarg) does *not* return an empty list, [`sum`](#sumarg) does *not* return zero, and [`string_agg`](#string_aggarg-sep) does *not* return an empty string in this case.

## General Aggregate Functions

The table below shows the available general aggregate functions.

| Function | Description |
|:--|:--------|
| [`any_value(arg)`](#any_valuearg) | Returns the first non-null value from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arbitrary(arg)`](#arbitraryarg) | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_max(arg, val)`](#arg_maxarg-val) | Finds the row with the maximum `val` and calculates the `arg` expression at that row. Rows where the value of the `arg` or `val` expression is `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_max(arg, val, n)`](#arg_maxarg-val-n) | The generalized case of [`arg_max`](#arg_maxarg-val) for `n` values: returns a `LIST` containing the `arg` expressions for the top `n` rows ordered by `val` descending. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_max_null(arg, val)`](#arg_max_nullarg-val) | Finds the row with the maximum `val` and calculates the `arg` expression at that row. Rows where the `val` expression evaluates to `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_min(arg, val)`](#arg_minarg-val) | Finds the row with the minimum `val` and calculates the `arg` expression at that row. Rows where the value of the `arg` or `val` expression is `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_min(arg, val, n)`](#arg_minarg-val-n) | Returns a `LIST` containing the `arg` expressions for the "bottom" `n` rows ordered by `val` ascending. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`arg_min_null(arg, val)`](#arg_min_nullarg-val) | Finds the row with the minimum `val` and calculates the `arg` expression at that row. Rows where the `val` expression evaluates to `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`array_agg(arg)`](#array_aggarg) | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`avg(arg)`](#avgarg) | Calculates the average of all non-null values in `arg`. |
| [`bit_and(arg)`](#bit_andarg) | Returns the bitwise AND of all bits in a given expression. |
| [`bit_or(arg)`](#bit_orarg) | Returns the bitwise OR of all bits in a given expression. |
| [`bit_xor(arg)`](#bit_xorarg) | Returns the bitwise XOR of all bits in a given expression. |
| [`bitstring_agg(arg)`](#bitstring_aggarg) | Returns a bitstring whose length corresponds to the range of the non-null (integer) values, with bits set at the location of each (distinct) value. |
| [`bool_and(arg)`](#bool_andarg) | Returns `true` if every input value is `true`, otherwise `false`. |
| [`bool_or(arg)`](#bool_orarg) | Returns `true` if any input value is `true`, otherwise `false`. |
| [`count()`](#countarg) | Returns the number of rows in a group. |
| [`count(arg)`](#countarg) | Returns the number of non-null values in `arg`. |
| [`favg(arg)`](#favgarg) | Calculates the average using a more accurate floating point summation (Kahan Sum). |
| [`first(arg)`](#firstarg) | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`fsum(arg)`](#fsumarg) | Calculates the sum using a more accurate floating point summation (Kahan Sum). |
| [`geomean(arg)`](#geomeanarg) | Calculates the geometric mean of all non-null values in `arg`. |
| [`histogram(arg)`](#histogramarg) | Returns a `MAP` of key-value pairs representing buckets and counts. |
| [`histogram(arg, boundaries)`](#histogramarg-boundaries) | Returns a `MAP` of key-value pairs representing the provided upper `boundaries` and counts of elements in the corresponding left-open and right-closed partition of the datatype. A boundary at the largest value of the datatype is automatically added when elements larger than all provided `boundaries` appear, see [`is_histogram_other_bin`]({% link docs/sql/functions/utility.md %}#is_histogram_other_binarg). Boundaries may be provided, e.g., via [`equi_width_bins`]({% link docs/sql/functions/utility.md %}#equi_width_binsminmaxbincountnice). |
| [`histogram_exact(arg, elements)`](#histogram_exactarg-elements) | Returns a `MAP` of key-value pairs representing the requested elements and their counts. A catch-all element specific to the data-type is automatically added to count other elements when they appear, see [`is_histogram_other_bin`]({% link docs/sql/functions/utility.md %}#is_histogram_other_binarg). |
| [`last(arg)`](#lastarg) | Returns the last value of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`list(arg)`](#listarg) | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`max(arg)`](#maxarg) | Returns the maximum value present in `arg`. This function is [unaffected by distinctness](#distinct-clause-in-aggregate-functions). |
| [`max(arg, n)`](#maxarg-n) | Returns a `LIST` containing the `arg` values for the "top" `n` rows ordered by `arg` descending. |
| [`max_by(arg, val)`](#max_byarg-val) | Finds the row with the maximum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`max_by(arg, val, n)`](#max_byarg-val-n) | Returns a `LIST` containing the `arg` expressions for the "top" `n` rows ordered by `val` descending. |
| [`min(arg)`](#minarg) | Returns the minimum value present in `arg`. This function is [unaffected by distinctness](#distinct-clause-in-aggregate-functions). |
| [`min(arg, n)`](#minarg-n) | Returns a `LIST` containing the `arg` values for the "bottom" `n` rows ordered by `arg` ascending. |
| [`min_by(arg, val)`](#min_byarg-val) | Finds the row with the minimum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`min_by(arg, val, n)`](#min_byarg-val-n) | Returns a `LIST` containing the `arg` expressions for the "bottom" `n` rows ordered by `val` ascending. |
| [`product(arg)`](#productarg) | Calculates the product of all non-null values in `arg`. |
| [`string_agg(arg, sep)`](#string_aggarg-sep) | Concatenates the column string values with a separator. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`sum(arg)`](#sumarg) | Calculates the sum of all non-null values in `arg` / counts `true` values when `arg` is boolean. |
| [`weighted_avg(arg, weight)`](#weighted_avgarg-weight) | Calculates the weighted average all non-null values in `arg`, where each value is scaled by its corresponding `weight`. If `weight` is `NULL`, the corresponding `arg` value will be skipped. |

#### `any_value(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the first non-`NULL` value from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `any_value(A)` |
| **Alias(es)** | - |

#### `arbitrary(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the first value (`NULL` or non-`NULL`) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arbitrary(A)` |
| **Alias(es)** | `first(A)` |

#### `arg_max(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the maximum `val` and calculates the `arg` expression at that row. Rows where the value of the `arg` or `val` expression is `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_max(A, B)` |
| **Alias(es)** | `argMax(arg, val)`, `max_by(arg, val)` |

#### `arg_max(arg, val, n)`

<div class="nostroke_table"></div>

| **Description** | The generalized case of [`arg_max`](#arg_maxarg-val) for `n` values: returns a `LIST` containing the `arg` expressions for the top `n` rows ordered by `val` descending. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_max(A, B, 2)` |
| **Alias(es)** | `argMax(arg, val, n)`, `max_by(arg, val, n)` |

#### `arg_max_null(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the maximum `val` and calculates the `arg` expression at that row. Rows where the `val` expression evaluates to `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_max_null(A, B)` |
| **Alias(es)** | - |

#### `arg_min(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the minimum `val` and calculates the `arg` expression at that row. Rows where the value of the `arg` or `val` expression is `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_min(A, B)` |
| **Alias(es)** | `argmin(arg, val)`, `min_by(arg, val)` |

#### `arg_min(arg, val, n)`

<div class="nostroke_table"></div>

| **Description** | The generalized case of [`arg_min`](#arg_minarg-val) for `n` values: returns a `LIST` containing the `arg` expressions for the top `n` rows ordered by `val` descending. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_min(A, B, 2)` |
| **Alias(es)** | `argmin(arg, val, n)`, `min_by(arg, val, n)` |

#### `arg_min_null(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the minimum `val` and calculates the `arg` expression at that row. Rows where the `val` expression evaluates to `NULL` are ignored. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `arg_min_null(A, B)` |
| **Alias(es)** | - |

#### `array_agg(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `array_agg(A)` |
| **Alias(es)** | `list` |

#### `avg(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the average of all non-null values in `arg`. |
| **Example** | `avg(A)` |
| **Alias(es)** | `mean` |

#### `bit_and(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise `AND` of all bits in a given expression. |
| **Example** | `bit_and(A)` |
| **Alias(es)** | - |

#### `bit_or(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise `OR` of all bits in a given expression. |
| **Example** | `bit_or(A)` |
| **Alias(es)** | - |

#### `bit_xor(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the bitwise `XOR` of all bits in a given expression. |
| **Example** | `bit_xor(A)` |
| **Alias(es)** | - |

#### `bitstring_agg(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a bitstring whose length corresponds to the range of the non-null (integer) values, with bits set at the location of each (distinct) value. |
| **Example** | `bitstring_agg(A)` |
| **Alias(es)** | - |

#### `bool_and(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if every input value is `true`, otherwise `false`. |
| **Example** | `bool_and(A)` |
| **Alias(es)** | - |

#### `bool_or(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns `true` if any input value is `true`, otherwise `false`. |
| **Example** | `bool_or(A)` |
| **Alias(es)** | - |

#### `count()`

<div class="nostroke_table"></div>

| **Description** | Returns the number of rows in a group.|
| **Example** | `count()` |
| **Alias(es)** | `count(*)` |

#### `count(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the number of non-null values in `arg`. |
| **Example** | `count(A)` |
| **Alias(es)** | - |

#### `favg(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the average using a more accurate floating point summation (Kahan Sum). |
| **Example** | `favg(A)` |
| **Alias(es)** | - |

#### `first(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the first value (null or non-null) from `arg`. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `first(A)` |
| **Alias(es)** | `arbitrary(A)` |

#### `fsum(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the sum using a more accurate floating point summation (Kahan Sum). |
| **Example** | `fsum(A)` |
| **Alias(es)** | `sumKahan`, `kahan_sum` |

#### `geomean(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the geometric mean of all non-null values in `arg`. |
| **Example** | `geomean(A)` |
| **Alias(es)** | `geometric_mean(A)` |

#### `histogram(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a `MAP` of key-value pairs representing buckets and counts. |
| **Example** | `histogram(A)` |
| **Alias(es)** | - |

#### `histogram(arg, boundaries)`

<div class="nostroke_table"></div>

| **Description** | Returns a `MAP` of key-value pairs representing the provided upper `boundaries` and counts of elements in the corresponding left-open and right-closed partition of the datatype. A boundary at the largest value of the datatype is automatically added when elements larger than all provided `boundaries` appear, see [`is_histogram_other_bin`]({% link docs/sql/functions/utility.md %}#is_histogram_other_binarg). Boundaries may be provided, e.g., via [`equi_width_bins`]({% link docs/sql/functions/utility.md %}#equi_width_binsminmaxbincountnice). |
| **Example** | `histogram(A, [0, 1, 10])` |
| **Alias(es)** | - |

#### `histogram_exact(arg, elements)`

<div class="nostroke_table"></div>

| **Description** | Returns a `MAP` of key-value pairs representing the requested elements and their counts. A catch-all element specific to the data-type is automatically added to count other elements when they appear, see [`is_histogram_other_bin`]({% link docs/sql/functions/utility.md %}#is_histogram_other_binarg). |
| **Example** | `histogram_exact(A, [0, 1, 10])` |
| **Alias(es)** | - |

#### `last(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the last value of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `last(A)` |
| **Alias(es)** | - |

#### `list(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing all the values of a column. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `list(A)` |
| **Alias(es)** | `array_agg` |

#### `max(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the maximum value present in `arg`. This function is [unaffected by distinctness](#distinct-clause-in-aggregate-functions). |
| **Example** | `max(A)` |
| **Alias(es)** | - |

#### `max(arg, n)`

<div class="nostroke_table"></div>

| **Description** |  Returns a `LIST` containing the `arg` values for the "top" `n` rows ordered by `arg` descending. |
| **Example** | `max(A, 2)` |
| **Alias(es)** | - |

#### `max_by(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the maximum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `max_by(A, B)` |
| **Alias(es)** | `argMax(arg, val)`, `arg_max(arg, val)` |

#### `max_by(arg, val, n)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing the `arg` expressions for the "top" `n` rows ordered by `val` descending. |
| **Example** | `max_by_n(A, B, 2)` |
| **Alias(es)** | `argMax(arg, val, n)`, `arg_max(arg, val, n)` |

#### `min(arg)`

<div class="nostroke_table"></div>

| **Description** | Returns the minimum value present in `arg`. This function is [unaffected by distinctness](#distinct-clause-in-aggregate-functions). |
| **Example** | `min(A)` |
| **Alias(es)** | - |

#### `min(arg, n)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing the `arg` values for the "bottom" `n` rows ordered by `arg` ascending. |
| **Example** | `min(A, 2)` |
| **Alias(es)** | - |

#### `min_by(arg, val)`

<div class="nostroke_table"></div>

| **Description** | Finds the row with the minimum `val`. Calculates the `arg` expression at that row. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `min_by(A, B)` |
| **Alias(es)** | `argMin(arg, val)`, `arg_min(arg, val)` |

#### `min_by(arg, val, n)`

<div class="nostroke_table"></div>

| **Description** | Returns a `LIST` containing the `arg` expressions for the "bottom" `n` rows ordered by `val` ascending. |
| **Example** | `min_by(A, B, 2)` |
| **Alias(es)** | `argMin(arg, val, n)`, `arg_min(arg, val, n)` |

#### `product(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the product of all non-null values in `arg`. |
| **Example** | `product(A)` |
| **Alias(es)** | - |

#### `string_agg(arg, sep)`

<div class="nostroke_table"></div>

| **Description** | Concatenates the column string values with a separator. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Example** | `string_agg(S, ',')` |
| **Alias(es)** | `group_concat(arg, sep)`, `listagg(arg, sep)` |

#### `sum(arg)`

<div class="nostroke_table"></div>

| **Description** | Calculates the sum of all non-null values in `arg` / counts `true` values when `arg` is boolean. |
| **Example** | `sum(A)` |
| **Alias(es)** | - |

#### `weighted_avg(arg, weight)`

<div class="nostroke_table"></div>

| **Description** | Calculates the weighted average of all non-null values in `arg`, where each value is scaled by its corresponding `weight`. If `weight` is `NULL`, the value will be skipped. |
| **Example** | `weighted_avg(A, W)` |
| **Alias(es)** | `wavg(arg, weight)` |

## Approximate Aggregates

The table below shows the available approximate aggregate functions.

| Function | Description | Example |
|:---|:---|:---|
| `approx_count_distinct(x)` | Gives the approximate count of distinct elements using HyperLogLog. | `approx_count_distinct(A)` |
| `approx_quantile(x, pos)` | Gives the approximate quantile using T-Digest. | `approx_quantile(A, 0.5)` |
| `reservoir_quantile(x, quantile, sample_size = 8192)` | Gives the approximate quantile using reservoir sampling, the sample size is optional and uses 8192 as a default size. | `reservoir_quantile(A, 0.5, 1024)` |

## Statistical Aggregates

The table below shows the available statistical aggregate functions.
They all ignore `NULL` values (in the case of a single input column `x`), or pairs where either input is `NULL` (in the case of two input columns `y` and `x`).

| Function | Description |
|:--|:--------|
| [`corr(y, x)`](#corry-x) | The correlation coefficient. |
| [`covar_pop(y, x)`](#covar_popy-x) | The population covariance, which does not include bias correction. |
| [`covar_samp(y, x)`](#covar_sampy-x) | The sample covariance, which includes Bessel's bias correction. |
| [`entropy(x)`](#entropyx) | The log-2 entropy. |
| [`kurtosis_pop(x)`](#kurtosis_popx) | The excess kurtosis (Fisher’s definition) without bias correction. |
| [`kurtosis(x)`](#kurtosisx) | The excess kurtosis (Fisher's definition) with bias correction according to the sample size. |
| [`mad(x)`](#madx) | The median absolute deviation. Temporal types return a positive `INTERVAL`. |
| [`median(x)`](#medianx) | The middle value of the set. For even value counts, quantitative values are averaged and ordinal values return the lower value. |
| [`mode(x)`](#modex)| The most frequent value. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| [`quantile_cont(x, pos)`](#quantile_contx-pos) | The interpolated `pos`-quantile of `x` for `0 <= pos <= 1`. Returns the `pos * (n_nonnull_values - 1)`th (zero-indexed, in the specified order) value of `x` or an interpolation between the adjacent values if the index is not an integer. Intuitively, arranges the values of `x` as equispaced *points* on a line, starting at 0 and ending at 1, and returns the (interpolated) value at `pos`. If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding interpolated quantiles. |
| [`quantile_disc(x, pos)`](#quantile_discx-pos) | The discrete `pos`-quantile of `x` for `0 <= pos <= 1`. Returns  the `greatest(ceil(pos * n_nonnull_values) - 1, 0)`th (zero-indexed, in the specified order) value of `x`. Intuitively, assigns to each value of `x` an equisized *sub-interval* (left-open and right-closed except for the initial interval) of the interval `[0, 1]`, and picks the value of the sub-interval that contains `pos`. If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding discrete quantiles. |
| [`regr_avgx(y, x)`](#regr_avgxy-x) | The average of the independent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| [`regr_avgy(y, x)`](#regr_avgyy-x) | The average of the dependent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| [`regr_count(y, x)`](#regr_county-x) | The number of non-`NULL` pairs. |
| [`regr_intercept(y, x)`](#regr_intercepty-x) | The intercept of the univariate linear regression line, where x is the independent variable and y is the dependent variable. |
| [`regr_r2(y, x)`](#regr_r2y-x) | The squared Pearson correlation coefficient between y and x. Also: The coefficient of determination in a linear regression, where x is the independent variable and y is the dependent variable. |
| [`regr_slope(y, x)`](#regr_slopey-x) | The slope of the linear regression line, where x is the independent variable and y is the dependent variable. |
| [`regr_sxx(y, x)`](#regr_sxxy-x) | The population variance, which includes Bessel's bias correction, of the independent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| [`regr_sxy(y, x)`](#regr_sxyy-x) | The population covariance, which includes Bessel's bias correction. |
| [`regr_syy(y, x)`](#regr_syyy-x) | The population variance, which includes Bessel's bias correction, of the dependent variable for non-`NULL` pairs , where x is the independent variable and y is the dependent variable. |
| [`skewness(x)`](#skewnessx) | The skewness. |
| [`stddev_pop(x)`](#stddev_popx) | The population standard deviation. |
| [`stddev_samp(x)`](#stddev_sampx) | The sample standard deviation. |
| [`var_pop(x)`](#var_popx) | The population variance, which does not include bias correction. |
| [`var_samp(x)`](#var_sampx) | The sample variance, which includes Bessel's bias correction. |

#### `corr(y, x)`

<div class="nostroke_table"></div>

| **Description** | The correlation coefficient.
| **Formula** | `covar_pop(y, x) / (stddev_pop(x) * stddev_pop(y))` |
| **Alias(es)** | - |

#### `covar_pop(y, x)`

<div class="nostroke_table"></div>

| **Description** | The population covariance, which does not include bias correction. |
| **Formula** | `(sum(x*y) - sum(x) * sum(y) / regr_count(y, x)) / regr_count(y, x)`, `covar_samp(y, x) * (1 - 1 / regr_count(y, x))` |
| **Alias(es)** | - |

#### `covar_samp(y, x)`

<div class="nostroke_table"></div>

| **Description** | The sample covariance, which includes Bessel's bias correction. |
| **Formula** | `(sum(x*y) - sum(x) * sum(y) / regr_count(y, x)) / (regr_count(y, x) - 1)`, `covar_pop(y, x) / (1 - 1 / regr_count(y, x))` |
| **Alias(es)** | `regr_sxy(y, x)` |

#### `entropy(x)`

<div class="nostroke_table"></div>

| **Description** | The log-2 entropy. |
| **Formula** | - |
| **Alias(es)** | - |

#### `kurtosis_pop(x)`

<div class="nostroke_table"></div>

| **Description** | The excess kurtosis (Fisher’s definition) without bias correction. |
| **Formula** | - |
| **Alias(es)** | - |

#### `kurtosis(x)`

<div class="nostroke_table"></div>

| **Description** | The excess kurtosis (Fisher's definition) with bias correction according to the sample size. |
| **Formula** | - |
| **Alias(es)** | - |

#### `mad(x)`

<div class="nostroke_table"></div>

| **Description** | The median absolute deviation. Temporal types return a positive `INTERVAL`. |
| **Formula** | `median(abs(x - median(x)))` |
| **Alias(es)** | - |

#### `median(x)`

<div class="nostroke_table"></div>

| **Description** | The middle value of the set. For even value counts, quantitative values are averaged and ordinal values return the lower value. |
| **Formula** | `quantile_cont(x, 0.5)` |
| **Alias(es)** | - |

#### `mode(x)`

<div class="nostroke_table"></div>

| **Description** | The most frequent value. This function is [affected by ordering](#order-by-clause-in-aggregate-functions). |
| **Formula** | - |
| **Alias(es)** | - |

#### `quantile_cont(x, pos)`

<div class="nostroke_table"></div>

| **Description** | The interpolated `pos`-quantile of `x` for `0 <= pos <= 1`. Returns the `pos * (n_nonnull_values - 1)`th (zero-indexed, in the specified order) value of `x` or an interpolation between the adjacent values if the index is not an integer. Intuitively, arranges the values of `x` as equispaced *points* on a line, starting at 0 and ending at 1, and returns the (interpolated) value at `pos`. If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding interpolated quantiles. |
| **Formula** | - |
| **Alias(es)** | - |

#### `quantile_disc(x, pos)`

<div class="nostroke_table"></div>

| **Description** | The discrete `pos`-quantile of `x` for `0 <= pos <= 1`. Returns  the `greatest(ceil(pos * n_nonnull_values) - 1, 0)`th (zero-indexed, in the specified order) value of `x`. Intuitively, assigns to each value of `x` an equisized *sub-interval* (left-open and right-closed except for the initial interval) of the interval `[0, 1]`, and picks the value of the sub-interval that contains `pos`. If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding discrete quantiles.  |
| **Formula** | - |
| **Alias(es)** | `quantile` |

#### `regr_avgx(y, x)`

<div class="nostroke_table"></div>

| **Description** | The average of the independent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

#### `regr_avgy(y, x)`

<div class="nostroke_table"></div>

| **Description** | The average of the dependent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

#### `regr_count(y, x)`

<div class="nostroke_table"></div>

| **Description** | The number of non-`NULL` pairs. |
| **Formula** | - |
| **Alias(es)** | - |

#### `regr_intercept(y, x)`

<div class="nostroke_table"></div>

| **Description** | The intercept of the univariate linear regression line, where x is the independent variable and y is the dependent variable. |
| **Formula** | `regr_avgy(y, x) - regr_slope(y, x) * regr_avgx(y, x)` |
| **Alias(es)** | - |

#### `regr_r2(y, x)`

<div class="nostroke_table"></div>

| **Description** | The squared Pearson correlation coefficient between y and x. Also: The coefficient of determination in a linear regression, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

#### `regr_slope(y, x)`

<div class="nostroke_table"></div>

| **Description** | Returns the slope of the linear regression line, where x is the independent variable and y is the dependent variable. |
| **Formula** | `regr_sxy(y, x) / regr_sxx(y, x)` |
| **Alias(es)** | - |

#### `regr_sxx(y, x)`

<div class="nostroke_table"></div>

| **Description** | The population variance, which includes Bessel's bias correction, of the independent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

#### `regr_sxy(y, x)`

<div class="nostroke_table"></div>

| **Description** | The population covariance, which includes Bessel's bias correction. |
| **Formula** | - |
| **Alias(es)** | - |

#### `regr_syy(y, x)`

<div class="nostroke_table"></div>

| **Description** | The population variance, which includes Bessel's bias correction, of the dependent variable for non-`NULL` pairs, where x is the independent variable and y is the dependent variable. |
| **Formula** | - |
| **Alias(es)** | - |

#### `skewness(x)`

<div class="nostroke_table"></div>

| **Description** | The skewness. |
| **Formula** | - |
| **Alias(es)** | - |

#### `stddev_pop(x)`

<div class="nostroke_table"></div>

| **Description** | The population standard deviation. |
| **Formula** | `sqrt(var_pop(x))` |
| **Alias(es)** | - |

#### `stddev_samp(x)`

<div class="nostroke_table"></div>

| **Description** | The sample standard deviation. |
| **Formula** | `sqrt(var_samp(x))`|
| **Alias(es)** | `stddev(x)`|

#### `var_pop(x)`

<div class="nostroke_table"></div>

| **Description** | The population variance, which does not include bias correction. |
| **Formula** | `(sum(x^2) - sum(x)^2 / count(x)) / count(x)`, `var_samp(y, x) * (1 - 1 / count(x))` |
| **Alias(es)** | - |

#### `var_samp(x)`

<div class="nostroke_table"></div>

| **Description** | The sample variance, which includes Bessel's bias correction. |
| **Formula** | `(sum(x^2) - sum(x)^2 / count(x)) / (count(x) - 1)`, `var_pop(y, x) / (1 - 1 / count(x))` |
| **Alias(es)** | `variance(arg, val)` |

## Ordered Set Aggregate Functions

The table below shows the available “ordered set” aggregate functions.
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
| `grouping()` | For queries with `GROUP BY` and either [`ROLLUP` or `GROUPING SETS`]({% link docs/sql/query_syntax/grouping_sets.md %}#identifying-grouping-sets-with-grouping_id): Returns an integer identifying which of the argument expressions where used to group on to create the current supper-aggregate row. | `grouping_id()` |
