---
layout: docu
title: Aggregate Functions
selected: Documentation/Aggregates
railroad: expressions/aggregate.js
---
<div id="rrdiagram"></div>

Aggregates are functions that *combine* multiple rows into a single value. Aggregates are different from scalar functions and window functions because they change the cardinality of the result. As such, aggregates can only be used in the `SELECT` and `HAVING` clauses of a SQL query.

When the `DISTINCT` clause is provided, only distinct values are considered in the computation of the aggregate. This is typically used in combination with the `COUNT` aggregate to get the number of distinct elements; but it can be used together with any aggregate function in the system.

When the `ORDER BY` clause is provided, the values being aggregated are sorted before applying the function.
Usually this is not important, but there are some order-sensitive aggregates that can have indeterminate results
(e.g., `first`, `last`, `list` and `string_agg`). These can be made deterministic by ordering the arguments.
For order-insensitive aggregates, this clause is parsed but ignored.

## General Aggregate Functions
The table below shows the available general aggregate functions.

| Function | Description | Example | Alias(es) |
|:---|:---|:---|:---|
| `arg_max(arg,val)` |Calculates the arg value for a maximum val value. | `arg_max(A,B)` | `argMax(A,B)`, `max_by(A,b)` |
| `arg_min(arg,val)` |Calculates the arg value for a minimum val value. | `arg_min(A,B)` | `argMin(A,B)`, `min_by(A,B)` |
| `avg(arg)` |Calculates the average value for all tuples in arg. | `avg(A)` | - |
| `bit_and(arg)` |Returns the bitwise AND of all bits in a given expression . | `bit_and(A)` | - |
| `bit_or(arg)` |Returns the bitwise OR of all bits in a given expression.  | `bit_or(A)` | - |
| `bit_xor(arg)` |Returns the bitwise XOR of all bits in a given expression. | `bit_xor(A)` | - |
| `bool_and(arg)` |Returns TRUE if every input value is TRUE, otherwise FALSE. | `bool_and(A)` | - |
| `bool_or(arg)` |Returns TRUE if any input value is TRUE, otherwise FALSE. | `bool(A)` | - |
| `count(arg)` |Calculates the number of tuples tuples in arg. | `count(A)` | - |
| `favg(arg)` |Calculates the average using a more accurate floating point summation (Kahan Sum). | `favg(A)` | - |
| `first(arg)` |Returns the first value of a column. | `first(A)` |`arbitrary(A)` |
| `fsum(arg)` |Calculates the sum using a more accurate floating point summation (Kahan Sum). | `fsum(A)` | `sumKahan`, `kahan_sum` |
| `histogram(arg)` |Returns a `LIST` of `STRUCT`s with the fields `bucket` and `count`. | `histogram(A)` | - |
| `last(arg)` |Returns the last value of a column. | `last(A)` | - |
| `list(arg)` |Returns a `LIST` containing all the values of a column. | `list(A)` |`array_agg` |
| `max(arg)` |Returns the maximum value present in arg. | `max(A)` | - |
| `min(arg)` | Returns the minumum value present in arg. | `min(A)` | - |
| `product(arg)` |Calculates the product of all tuples in arg | `product(A)` | - |
| `string_agg(arg, sep)` |Concatenates the column string values with a separator | `string_agg(S, ',')` | `group_concat` |
| `sum(arg)` |Calculates the sum value for all tuples in arg. | `sum(A)` | - |

## Approximate Aggregates
The table below shows the available approximate aggregate functions.

| Function | Description | Example |
|:---|:---|:---|
| `approx_count_distinct(x)` | Gives the approximate count of distintinct elements using HyperLogLog. | `approx_count_distinct(A)` |
| `approx_quantile(x,pos)` | Gives the approximate quantile using T-Digest. | `approx_quantile(A,0.5)` |
| `reservoir_quantile(x,quantile,sample_size=8192)` | Gives the approximate quantile using reservoir sampling, the sample size is optional and uses 8192 as a default size. | `reservoir_quantile(A,0.5,1024)` |

## Statistical Aggregates
The table below shows the available statistical aggregate functions.

| Function | Description | Formula | Alias |
|:---|:---|:---|:---|
| `corr(y,x)` | Returns the correlation coefficient for non-null pairs in a group. | `COVAR_POP(y, x) / (STDDEV_POP(x) * STDDEV_POP(y))`| - |
| `covar_pop(y,x)` | Returns the population covariance of input values. | `(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*) ` | - |
| `entropy(x)` | Returns the log-2 entropy of count input-values. | - | - |
| `kurtosis(x)` | Returns the excess kurtosis of all input values. | - | - |
| `mad(x)` | Returns the median absolute deviation for the values within x. NULL values are ignored. Temporal types return a positive `INTERVAL`. | `MEDIAN(ABS(x-MEDIAN(x)))` | - |
| `median(x)` | Returns the middle value of the set. NULL values are ignored. For even value counts, quantitiative values are averaged and ordinal values return the lower value. | `QUANTILE_CONT(x, 0.5)` | - |
| `mode(x)` | Returns the most frequent value for the values within x. NULL values are ignored. | - | - |
| `quantile_cont(x,pos)` | Returns the intepolated quantile number between 0 and 1 . If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding intepolated quantiles. | - | - |
| `quantile_disc(x,pos)` | Returns the exact quantile number between 0 and 1 . If `pos` is a `LIST` of `FLOAT`s, then the result is a `LIST` of the corresponding exact quantiles. | - | `quantile` |
| `regr_avgx(y,x)` | Returns the average of the independent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. | - | - |
| `regr_avgy(y,x)` | Returns the average of the dependent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. | - | - |
| `regr_count(y,x)` | Returns the number of non-null number pairs in a group. | `(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*)` | - |
| `regr_intercept(y,x)` | Returns the intercept of the univariate linear regression line for non-null pairs in a group. | `AVG(y)-REGR_SLOPE(y,x)*AVG(x)` | - |
| `regr_r2(y,x)` | Returns the coefficient of determination for non-null pairs in a group. | - | - |
| `regr_slope(y,x)` | Returns the slope of the linear regression line for non-null pairs in a group.| `COVAR_POP(x,y) / VAR_POP(x)` | - |
| `regr_sxx(y,x)` | -  | `REGR_COUNT(y, x) * VAR_POP(x)` | - |
| `regr_sxy(y,x)` | Returns the population covariance of input values. | `REGR_COUNT(y, x) * COVAR_POP(y, x) ` | - |
| `regr_syy(y,x)` | - | `REGR_COUNT(y, x) * VAR_POP(y) f` | - |
| `skewness(x)` | Returns the skewness of all input values. | - | - |
| `stddev_pop(x)` | Returns the population standard deviation.  | `sqrt(var_pop(x))` | - |
| `stddev_samp(x)` | Returns the sample standard deviation. | `sqrt(var_samp(x))` | `stddev(x)` |
| `var_pop(x)` | Returns the population variance. | - | - |
| `var_samp(x)` | Returns the sample variance of all input values. | `(SUM(x^2) - SUM(x)^2 / COUNT(x)) / (COUNT(x) - 1)` | `variance(arg,val)` |

## Ordered Set Aggregate Functions
The table below shows the available "ordered set" aggregate functions.
These functions are specified using the `WITHIN GROUP(ORDER BY sort_expression)` syntax,
and they are converted to an equivalent aggregate function that takes the ordering expression
as the first argument.

| Function | Equivalent |
|:---|:---|
| `mode() WITHIN GROUP (ORDER BY sort_expression)` | `mode(sort_expression)` |
| `percentile_cont(fraction) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_cont(sort_expression, fraction)` |
| `percentile_cont(fractions) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_cont(sort_expression, fractions)` |
| `percentile_disc(fraction) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_disc(sort_expression, fraction)` |
| `percentile_disc(fractions) WITHIN GROUP (ORDER BY sort_expression)` | `quantile_disc(sort_expression, fractions)` |

