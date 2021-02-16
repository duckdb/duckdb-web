---
layout: docu
title: Aggregate Functions
selected: Documentation/Aggregates
railroad: expressions/aggregate.js
---
<div id="rrdiagram"></div>

Aggregates are functions that *combine* multiple rows into a single value. Aggregates are different from scalar functions and window functions because they change the cardinality of the result. As such, aggregates can only be used in the `SELECT` and `HAVING` clauses of a SQL query.

When the `DISTINCT` clause is provided, only distinct values are considered in the computation of the aggregate. This is typically used in combination with the `COUNT` aggregate to get the number of distinct elements; but it can be used together with any aggregate function in the system.

## General Aggregate Functions
argMin
argMax
variance (alias for var_samp)

## Approximate Aggregates
The table below shows the available approximate aggregations.
| Function | Description | Example |
|:---|:---|:---|
| `approx_count_distinct(x)` | Gives the approximate count of distintinct elements using HyperLogLog | `approx_count_distinct(A)` |
| `approx_quantile(x,quantile)` | Gives the approximate quantile using T-Digest | `approx_quantile(A,0.5)` |
| `reservoir_quantile(x,quantile,sample_size=8192)` | Gives the approximate quantile using reservoir sampling, the sample size is optional and uses 8192 as a default size | `reservoir_quantile(A,0.5,1024)` |

approx_count_distinct

## Statistical Aggregates
| Function | Description | Formula | Alias |
|:---|:---|:---|:---|
| `corr(y,x)` | Returns the correlation coefficient for non-null pairs in a group. | `COVAR_POP(y, x) / (STDDEV_POP(x) * STDDEV_POP(y))`| - |
| `covar_pop(y,x)` | Returns the population covariance of input values. | `(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*) ` | - |
| `stddev_pop(y,x)` | Returns the population standard deviation (square root of variance) of non-NULL values. | - | - |
| `covar_pop(y,x)` | Returns the population covariance of input values. | `(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*) ` | - |
| `regr_avgx(y,x)` | Returns the average of the independent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. | - | - |
| `regr_avgy(y,x)` | Returns the average of the dependent variable for non-null pairs in a group, where x is the independent variable and y is the dependent variable. | - | - |
| `regr_count(y,x)` | Returns the number of non-null number pairs in a group. | `(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*) ` | - |
| `regr_intercept(y,x)` | Returns the intercept of the univariate linear regression line for non-null pairs in a group. | `AVG(y)-REGR_SLOPE(y,x)*AVG(x)` | - |
| `regr_r2(y,x)` | Returns the coefficient of determination for non-null pairs in a group. | - | - |
| `regr_slope(y,x)` | Returns the slope of the linear regression line for non-null pairs in a group.| `COVAR_POP(x,y) / VAR_POP(x)` | - |
| `regr_sxx(y,x)` | -  | `REGR_COUNT(y, x) * VAR_POP(x)` | - |
| `regr_sxy(y,x)` | Returns the population covariance of input values. | `REGR_COUNT(y, x) * COVAR_POP(y, x) ` | - |
| `regr_syy(y,x)` | - | `REGR_COUNT(y, x) * VAR_POP(y) f` | - |
| `mode(x)` | Returns the most frequent value for the values within ${expr1}. NULL values are ignored. | - | - |
| `covar_pop(y,x)` | Returns the population covariance of input values. | `(SUM(x*y) - SUM(x) * SUM(y) / COUNT(*)) / COUNT(*) ` | - |

