---
layout: docu
title: Benchmark Suite
---

DuckDB has an extensive benchmark suite.
When making changes that have potential performance implications, it is important to run these benchmarks to detect potential performance regressions.

## Getting Started

To build the benchmark suite, run the following command in the [DuckDB repository](https://github.com/duckdb/duckdb):

```batch
BUILD_BENCHMARK=1 BUILD_EXTENSIONS='tpch' make
```

## Listing Benchmarks

To list all available benchmarks, run:

```batch
build/release/benchmark/benchmark_runner --list
```

## Running Benchmarks

### Running a Single Benchmark

To run a single benchmark, issue the following command:

```batch
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark
```

The output will be printed to `stdout` in CSV format, in the following format:

```text
name	run	timing
benchmark/micro/nulls/no_nulls_addition.benchmark	1	0.121234
benchmark/micro/nulls/no_nulls_addition.benchmark	2	0.121702
benchmark/micro/nulls/no_nulls_addition.benchmark	3	0.122948
benchmark/micro/nulls/no_nulls_addition.benchmark	4	0.122534
benchmark/micro/nulls/no_nulls_addition.benchmark	5	0.124102
```

You can also specify an output file using the `--out` flag. This will write only the timings (delimited by newlines) to that file.

```batch
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark --out=timings.out
```

The output will contain the following:

```text
0.182472
0.185027
0.184163
0.185281
0.182948
```

### Running Multiple Benchmarks Using a Regular Expression

You can also use a regular expression to specify which benchmarks to run.
Be careful of shell expansion of certain regex characters (e.g., `*` will likely be expanded by your shell, hence this requires proper quoting or escaping).

```batch
build/release/benchmark/benchmark_runner "benchmark/micro/nulls/.*"
```

#### Running All Benchmarks

Not specifying any argument will run all benchmarks.

```batch
build/release/benchmark/benchmark_runner
```

#### Other Options

The `--info` flag gives you some other information about the benchmark.

```batch
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark --info
```

```text
display_name:NULL Addition (no nulls)
group:micro
subgroup:nulls
```

The `--query` flag will print the query that is run by the benchmark.

```sql
SELECT min(i + 1) FROM integers;
```

The `--profile` flag will output a query tree.

## Creating Benchmarks

Some development work is around performance,
and including a benchmark along with the other tests not only validates any improvements,
but also prevents future performance regressions in the feature.

### Benchmark Example

To illustrate how to create a benchmark file, we can look at the benchmark for the `FILL` window function.
(The `FILL` function linearly interpolates missing values in an ordered partition.)

Benchmarks are similar to unit test files, and have the same type of header.

```python
# name: benchmark/micro/window/window_fill.benchmark
# description: Measure the performance of FILL
# group: [window]
```
The `make format-head` command can ensure that the header has the expected structure and prevent tidy check errors.

Below this header, there are a set of keywords summarizing the benchmark.

```text
name FillPerformance
group micro
subgroup window
```

While some benchmarks run a single query,
it can often be useful to _parameterize_ a benchmark using the `argument` keyword.
This allows the benchmark to be run with different settings, such as data volume.
For the `FILL` benchmark, there are three arguments:

```text
argument sf 10
argument errors 0.1
argument keys 4
```

For `FILL` these are
* The scale factor (millions of rows per partition)
* The error rate (fraction of the values that are missing)
* The number of partitions.

Benchmarks generally require some data preparation before running the query.
Data preparation is done in the `load` section of the benchmark file.
For the `FILL` benchmark, we create a table using the parameters and a random number generator.

```sql
load
select setseed(0.8675309);
create or replace table data as (
	select
		k::TINYINT as k,
		(case when random() > ${errors} then m - 1704067200000 else null end) as v,
		m,
	from range(1704067200000, 1704067200000 + ${sf} * 1_000_000 * 10, 10) times(m)
	cross join range(${keys}) keys(k)
);
```

The `argument` parameters are expanded in the query,
similar to the way that `foreach` values are expanded in unit tests.
Note that we can issue multiple SQL statements in the `load` section.

Once the data is prepared, we are finally ready to specify the query we will benchmark!
This is done in the `run` section, and the restrictions are the same as for a unit test
(e.g., no blank lines, etc.)
For the `FILL` benchmark, we want to find all places where the interpolation fails:

```sql
run
SELECT
	m,
	k,
	fill(v) OVER (PARTITION BY k ORDER BY m) as v
FROM
	data
qualify v <> m - 1704067200000;
```

If the interpolation is correct, then we will have no output, no matter the scale.
We can check this with the final `result` clause,
which has the same syntax as a unit test:

```text
result III
```

By providing no output rows, we can check the correctness of the query as well as its performance.

There are many other examples in the top level `benchmark/` directory,
and you may want to have a look to discover some other techniques.
