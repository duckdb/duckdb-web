---
layout: post
title:  "The Return of the H2oai Benchmark"
author: Tom Ebergen
excerpt_separator: <!--more-->
---

*TL;DR: We re-ran the h2oai db-benchmarks with up-to-date libraries and DuckDB is consistently a top performer.*


[Skip directly to the results](#results)

The H2O.ai [DB benchmark](https://h2oai.github.io/db-benchmark/) is a well-known benchmark in the data analytics and R community. The benchmark measures the groupby and join performance of various analytical tools like data.table, polars, dplyr, clickhouse, duckdb and more. Since July 2nd 2021, the benchmark has been dormant, with no result updates or maintenance. Many of the analytical systems measured in the benchmark have since undergone substantial improvements, leaving many of the maintainers curious as to where their analytical tool ranks on the benchmark.

DuckDB has decided to give the H2O.ai benchmark new life and maintain it for the foreseeable future. One reason for DuckDB labs' decision to maintain the benchmark is that duckdb has had 4 new minor releases since the most recent published results on July 2nd, 2021. After managing to run parts of the benchmark on a r3-8xlarge AWS box, DuckDB ranked as a top performer on the benchmark. Therefore, the decision was made to fork the benchmark, modernize underlying dependencies and run the benchmark on the latest versions of the included systems. You can find the repository [here](https://github.com/duckdb/h2oai-db-benchmark).

The results of the new benchmark are very interesting, but first a quick summary of the benchmark and what updates took place.

## The H2O AI benchmark
There are 5 basic grouping tests and 5 advanced grouping tests. The 10 grouping queries all focus on a combination of the following
- Low cardinality (a few big groups)
- High cardinality (lots of very small groups)
- Grouping integer types
- Grouping string types

Each query is run only twice with both results being reported. This way we can see the performance of a cold run and any effects data caching may have. The idea is to avoid reporting any potential "best" results on a hot system. Data analysts only need to run a query once to get their answer. No one drives to the store a second time to get another litre of milk faster.

The time reported is the sum of the time it takes to run all 5 queries twice.

More information about the specific queries can be found below.

#### The Data and Queries

The queries have not changed since the benchmark went dormant. The data is generated in a rather simple manner. Inspecting the datagen files you can see that the columns are generated with small, medium, and large groups of char and int values. Similar generation logic applies to the join data generation.

| Query | SQL |  Objective |
|-----------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| groupby #1  |   `SELECT id1, sum(v1) AS v1 FROM tbl GROUP BY id1` |  Sum over large cardinality groups, grouped by varchar                                                                                          |
| groupby #2  |   `SELECT id1, id2, sum(v1) AS v1 FROM tbl GROUP BY id1, id2` | Sum over medium cardinality groups, grouped by varchars                                                                               |
| groupby #3  |   `SELECT id3, sum(v1) AS v1, mean(v3) AS v3 FROM tbl GROUP BY id3`                 |      Sum and mean over many small cardinality groups, grouped by varchar                   |
| groupby #4  |   `SELECT id4, mean(v1) AS v1, mean(v2) AS v2, mean(v3) AS v3 FROM tbl GROUP BY id4`|      Mean over many large cardinality groups, grouped by integer                                              |
| groupby #5  |   `SELECT id6, sum(v1) AS v1, sum(v2) AS v2, sum(v3) AS v3 FROM tbl GROUP BY id6`   |      Sum over many small groups, grouped by integer                                                           |
| advanced groupby #1  |   `SELECT id4, id5, quantile_cont(v3, 0.5) AS median_v3, stddev(v3) AS sd_v3 FROM tbl GROUP BY id4, id5`  | `quantile_cont` over medium cardinality group, grouped by integers                                        |
| advanced groupby #2  |   `SELECT id3, max(v1)-min(v2) AS range_v1_v2 FROM tbl GROUP BY id3`                |      Range selection over small cardinality groups, grouped by integer                                          |
| advanced groupby #3  |   `SELECT id6, v3 AS largest2_v3 FROM (SELECT id6, v3, row_number() OVER (PARTITION BY id6 ORDER BY v3 DESC) AS order_v3 FROM x WHERE v3 IS NOT NULL) sub_query WHERE order_v3 <= 2` |Advanced group by query         |
| advanced groupby #4  |   `SELECT id2, id4, pow(corr(v1, v2), 2) AS r2 FROM tbl GROUP BY id2, id4`          |      Arithmetic over medium sized groups, grouped by varchar, integer.                                                         |
| advanced groupby #5 |   `SELECT id1, id2, id3, id4, id5, id6, sum(v3) AS v3, count(*) AS count FROM tbl GROUP BY id1, id2, id3, id4, id5, id6`  | Many many small groups, the number of groups is the cardinality of the dataset           |
| join #1 |`SELECT x.*, small.id4 AS small_id4, v2 FROM x JOIN small USING (id1)`                                                                           |   Joining a large table (x) with a small-sized table on integer type   |
| join #2 |`SELECT x.*, medium.id1 AS medium_id1, medium.id4 AS medium_id4, medium.id5 AS medium_id5, v2 FROM x JOIN medium USING (id2)`                    |   Joining a large table (x) with a medium-sized table on integer type  |
| join #3 |`SELECT x.*, medium.id1 AS medium_id1, medium.id4 AS medium_id4, medium.id5 AS medium_id5, v2 FROM x LEFT JOIN medium USING (id2)`               |   Left join a large table (x) with a medium-sized table on integer type|
| join #4 |`SELECT x.*, medium.id1 AS medium_id1, medium.id2 AS medium_id2, medium.id4 AS medium_id4, v2 FROM x JOIN medium USING (id5)`                    |   Join a large table (x) with a medium table on varchar type           |
| join #5 |`SELECT x.*, big.id1 AS big_id1, big.id2 AS big_id2, big.id4 AS big_id4, big.id5 AS big_id5, big.id6 AS big_id6, v2 FROM x JOIN big USING (id3)` |   Join a large table (x) with a large table on integer type.           |


### Modifications to the Benchmark & Hardware
No modifications have been made to the queries or the data generation. Some scripts required minor modifications so that the current version of the library could be run. The hardware used is slightly different as the exact AWS offering the benchmark previously used is no longer available. Base libraries have been updated as well. GPU libraries were not tested. 


AWS is a [m4.10xlarge](https://aws.amazon.com/ec2/instance-types/)

- CPU model: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz 
- CPU cores: 40 
- RAM model: Unknown 
- Memory: 160GB 
- NO GPU specifications 
- R upgraded, 4.0.0 -> 4.2.2 
- Python upgraded 3.\[6\|7\] -> 3.10 

### Changes made to install scripts of other systems
Pandas, Polars, Dask, and Clickhouse required changes to their setup/install scripts. The changes were relatively minor consisting mostly of syntax updates and data ingestion updates. Data ingestion did not affect the reporting timing results.


## RESULTS

<div style="position:relative; padding-bottom:10%; width: 100%; height:500px">
	<iframe src="https://tmonster.github.io/h2oai-db-benchmark/"  title="h2o db benchmmark" style="width: 100%; height:100%"></iframe>
</div>

You can also look at the results [here](https://duckdb.github.io/h2oai-db-benchmark/). Hopefully you immediately notice that DuckDB ranks first in all of the queries (I mean, why else would we be writing a blog post about it 😜?). A major contributor to our increased performance is [parallel grouped aggregation](https://duckdb.org/2022/03/07/aggregate-hashtable.html) which was merged in March 2022. In addition, DuckDB now supports [enum types](https://duckdb.org/2021/11/26/duck-enum.html), which makes DuckDB `group by` aggregation even faster. [Improvements to the out-of-core hash join](https://github.com/duckdb/duckdb/pull/4970) were merged as well, further improving the performance of our joins.


## Questions about certain results?

Some solutions may report internal errors for some queries. This will be updated soon to give more detail into the error. Feel free to file an issue to know more. In addition, there are many areas in the code where certain tests are automatically nullified. If you believe that is the case for a test case for your system or if you have any other questions, feel free to file an issue here (<- issue tracker for duckdb h2oai benchmark.)

# Maintenance plan
DuckDB will continue to maintain this benchmark for the forseeable future. The process for re-running the benchmarks must still be decided.

Do you have any other questions? Would you like to have your system added to the benchmark? Please feel free to read the ReadMe.md in the [repository](https://github.com/duckdb/h2oai-db-benchmark), and if you still have questions, you can reach out to me at tom@duckdb.com or on our [Discord](https://discord.com/invite/tcvwpjfnZx)!
