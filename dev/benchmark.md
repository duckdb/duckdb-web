---
layout: docu
title: Benchmark Suite
---

DuckDB has an extensive benchmark suite.
When making changes that have potential performance implications, it is important to run these benchmarks to detect potential performance regressions.

## Getting Started

To build the benchmark suite, run:

```bash
git clone https://github.com/duckdb/duckdb
cd duckdb
BUILD_BENCHMARK=1 BUILD_TPCH=1 make
```

## Listing Benchmarks

To list all available benchmarks, run:

```bash
build/release/benchmark/benchmark_runner --list
```

## Running Benchmarks

### Running a Single Benchmark

To run a single benchmark, issue the following command:

```bash
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

```bash
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

### Running Multiple Benchmark Using a Regular Expression

You can also use a regular expression to specify which benchmarks to run. Be careful of shell expansion of certain regex characters (e.g. `*` will likely be expanded by your shell, hence this requires proper quoting or escaping).

```bash
build/release/benchmark/benchmark_runner "benchmark/micro/nulls/.*"
```

#### Running All Benchmarks

Not specifying any argument will run all benchmarks.

```bash
build/release/benchmark/benchmark_runner
```

#### Other Options

The `--info` flag gives you some other information about the benchmark.

```bash
build/release/benchmark/benchmark_runner benchmark/micro/nulls/no_nulls_addition.benchmark --info
```

```text
display_name:NULL Addition (no nulls)
group:micro
subgroup:nulls
```

The `--query` flag will print the query that is run by the benchmark.

```sql
SELECT MIN(i + 1) FROM integers
```

The `--profile` flag will output a query tree.
