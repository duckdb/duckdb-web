---
layout: post
title:  "Updates to the H2O.ai db-benchmark!"
author: Tom Ebergen
excerpt: The H2O.ai db-benchmark has been updated with new results. In addition, the AWS EC2 instance used for benchmarking has been changed to a c6id.metal for improved repeatability and fairness across libraries. DuckDB is the fastest library for both join and group by queries at almost every data size.
---

[Skip directly to the results](#results)

## The Benchmark Has Been Updated!

In April, DuckDB Labs published a [blog post reporting updated H2O.ai db-benchmark results](https://duckdb.org/2023/04/14/h2oai.html). Since then, the results haven't been updated. The original plan was to update the results with every DuckDB release. DuckDB 0.9.1 was recently released, and DuckDB Labs has updated the benchmark. While updating the benchmark, however, we noticed that our initial setup did not lend itself to being fair to all solutions. The machine used had network storage and could suffer from noisy neighbors. To avoid these issues, the whole benchmark was re-run on a c6id.metal machine.

## New Benchmark Environment: c6id.metal Instance

Initially, updating the results to the benchmark showed strange results. Even using the same library versions from the prior update, some solutions regressed and others improved. We believe this variance came from the AWS EC2 instance we chose: an m4.10xlarge. The m4.10xlarge has 40 virtual CPUs and EBS storage. EBS storage is highly available network block storage for EC2 instances. When running compute-heavy benchmarks, a machine like the m4.10xlarge can suffer from the following issues: 

* **Network storage** is an issue for benchmarking solutions that interact with storage frequently. For the 500MB and 5GB workloads, network storage was not an issue on the m4.10xlarge since all solutions could execute the queries in memory. For the 50GB workload, however, network storage was an issue for the solutions that could not execute queries in memory. While the m4.10xlarge has dedicated EBS bandwidth, any read/write from storage is still happening over the network, which is usually slower than physically mounted storage. Solutions that frequently read and write to storage for the 50GB queries end up doing this over the network. This network time becomes a chunk of the execution time of the query. If the network has variable performance, the query performance is then also variable.

* **Noisy neighbors** is a common issue when benchmarking on virtual CPUs. The previous machine most likely shared its compute hardware with other (neighboring) AWS EC2 instances. If these neighbors are also running compute heavy workloads, the physical CPU caches are repeatedly invalidated/flushed by the neighboring instance and the benchmark instance. When the CPU cache is shared between two workloads on two instances, both workloads require extra reads from memory for data that would already be in CPU cache on a non-virtual machine.

In order to be fair to all solutions, we decided to change the instance type to a metal instance with local storage. Metal instance types negate any noisy neighbor problems because the hardware is physical and not shared with any other AWS users/instances. Network storage problems are also fixed because solutions can read and write data to the local instance storage, which is physically mounted on the hardware.

Another benefit of the the c6id.metal box is that it stresses parallel performance. There are 128 cores on the c6id.metal. Performance differences between solutions that can effectively use every core and solutions that cannot are clearly visible.

See the [updated settings](#updated-settings) section on how settings were change for each solution when run on the new machine.

## Updating the Benchmark

Moving forward we will update the benchmark when PRs with new performance numbers are provided. The PR should include a description of the changes to a solution script or a version update and new entries in the `time.csv` and `logs.csv` files. These entries will be verified using a different c6id.metal instance, and if there is limited variance, the PR will be merged and the results will be updated!

### Updated Settings

1. ClickHouse
	* Storage: Any data this gets spilled to disk also needs to be on the NVMe drive. This has been changed in the new `format_and_mount.sh` script and the `clickhouse/clickhouse-mount-config.xml` file.
2. Julia (juliadf & juliads)
	* Threads: The threads were hardcoded for juliadf/juliads to 20/40 threads. Now the max number of threads are used. No option was given to spill to disk, so this was not changed/researched.
3. DuckDB
	* Storage: The DuckDB database file was specified to run on the NVMe mount.
4. Spark
	* Storage: There is an option to spill to disk. I was unsure of how to modify the storage location so that it was on the NVMe drive. Open to a PR with storage location changes and improved results!

Many solutions do not spill to disk, so they did not require any modification to use the instance storage. Other solutions use `parallel::ncores()` or default to a maximum number of cores for parallelism. Solution scripts were run in their current form on [github.com/duckdblabs/db-benchmark](https://github.com/duckdblabs/db-benchmark). Please read the [Updating the Benchmark](https://github.com/duckdblabs/db-benchmark#updating-the-benchmark) section on how to re-run your solution.


### Results

The first results you see are the 50GB group by results. The benchmark runs every query twice per solution, and both runtimes are reported. The "first time" can be considered a cold run, and the "second time" can be considered a hot run. DuckDB and DuckDB-latest perform very well among all dataset sizes and variations. 

The team at DuckDB Labs has been hard at work improving the performance of the out-of-core hash aggregates and joins. The most notable improvement is the performance of query 5 in the advanced group by queries. The cold run is almost an order of magnitude better than every other solution! DuckDB is also one of only two solutions to finish the 50GB join query. Some solutions are experiencing timeouts on the 50GB datasets. Solutions running the 50GB group by queries are killed after running for 180 minutes, meaning all 10 group by queries need to finish within the 180 minutes. Solutions running the 50GB join queries are killed after running for 360 minutes.

[Link to result page](https://DuckDBlabs.github.io/db-benchmark/)
<iframe src="https://DuckDBlabs.github.io/db-benchmark/"  title="h2oai db benchmmark" height=500 width=600></iframe>
