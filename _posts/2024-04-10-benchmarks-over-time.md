---
layout: post
title: "Benchmarking Ourselves Over Time at DuckDB"
author: Alex Monahan
excerpt: "In the last 3 years, DuckDB has become 3 - 25x faster and can analyze ~10x larger datasets."
---
<!-- <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> -->
<script src="{{ site.baseurl }}/js/plotly-1.58.5.min.js"></script>

A big part of DuckDB's focus is on the developer experience of working with data.
However, performance is an important consideration when investigating data management systems. 
Fairly comparing data processing systems using benchmarks is [very difficult](https://mytherin.github.io/papers/2018-dbtest.pdf). 
Whoever creates the benchmark is likely to know one system better than the rest, influencing benchmark selection, how much time is spent tuning parameters, and more. 

Instead, this post focuses on benchmarking *our own* performance over time. 
(Of course, we encourage you to conduct your own benchmarks and welcome your feedback!)
This approach avoids many comparison pitfalls, but also provides several valuable data points to consider when selecting a system.

#### How fast is it improving? 
When you select a data processing system, it is important to think about the future. 
The best way to predict the future is to look at the past!
Learning a new tool is an investment, in addition to the time spent integrating it into your workflows.
If a tool improves quickly over time, a simple version update can speed up your analysis.

When choosing an analytical engine, you also want to consider the situation where your data sizes could grow substantially.
If the system is improving rapidly, then the system can scale as your data scales, with lower chances for a migration in the future.
Plus, if you haven't experimented with a tool in a while, you can see how much faster it has become since you last checked!

#### What is it especially good at?
The choice of benchmark is an indicator of what types of workloads a tool is useful for. 
The higher the variety of analyses in the benchmark, the more broadly useful the tool can be.

#### What scale of data can it handle?
Many benchmarks are deliberately smaller than typical workloads. 
This allows the benchmark to complete in a reasonable amount of time when run with many configurations. 
However, an important question to answer when selecting a system is whether the size of your data can be handled within the size of your compute resources.

### Limitations of benchmarking over time
There are some limitations when looking at the performance of a system over time.
If a feature is brand new, there is no prior performance to compare to!
As a result, this post focuses on fundamental workloads rather than DuckDB's ever-increasing set of integrations with different data formats and cloud services.

The code used to run the benchmark also avoids many of DuckDB's Friendlier SQL additions, as those have also been added more recently. 
(When writing these queries, it felt like going back in time!)

<!-- Is this too formal? Maybe I can just say that DuckDB has been hard at work making the system faster and let's see how it has been going.  Maybe I should just let the beautiful charts do the talking for me...?-->
<!-- 
What are the takeaways I want people to have?
    - DuckDB is getting faster very fast
    - DuckDB is focused on all aspects of performance
    - DuckDB can handle larger datasets

Benchmark overview
    Performance over time
    Scale over time
    Why H2O.ai
    Why we trimmed the benchmark
        Only the middle size for the performance tests just for speed
        Testing multiple sizes for scale
    Why we added more to the benchmark
        Adding scanning of other formats
        Adding data export
        Adding Window functions
    Computing resources (M1 16GB)
    Python client 
        Note that we still used R to generate the data, for consistency
        Most popular
        Also allows for timing integrations with other formats like Pandas and Arrow
    Persistent DuckDB file
    Writing results back to that persistent file
    Default settings 

Performance over time
    Overall chart in terms of seconds
        DuckDB Version
        Over time

    Workload type aggregated area chart over time, scaled to relative performance
        Group by
        Join
        Window functions

        CSV Import 
        Parquet Export

        Scanning other formats
            Pandas vs. Arrow vs. parquet over time 
                Plot them all
                Just Arrow vs. Pandas: Pick the winner over time

Scale over time
    Can it run y/n
    Stitched together over multiple runs as older versions would sometimes run indefinitely 




 --> 
## Benchmark design

### Summary
* H2O.ai, plus import/export and window function tests
* 5GB scale for everything, plus 50GB scale for group bys and joins
* Python instead of R
* Using a Macbook Pro M1 with 16GB RAM
* Median of 3 runs
* DuckDB Versions 0.2.7 through 1.0.0
    * Nearly 3 years, from 2021-06-14 to 2024-06-03


### H2O.ai as the foundation
This post measures DuckDB's performance over time on the H2O.ai benchmark for both joins and group by queries.
Please see our previous [blog](https://duckdb.org/2023/04/14/h2oai.html) [posts](https://duckdb.org/2023/11/03/db-benchmark-update.html) for details on why we believe the H2O.ai benchmark is a good approach!

The result of each H2O.ai query is written to a table in a persistent DuckDB file.
This does require additional work when compared with an in-memory workflow (especially the burden on the SSD rather than RAM), but improves scalability and is a common approach for larger analyses.

### Import, Export, and Replacement Scans
However, we now extend this benchmark in several important ways. 
In addition to considering raw query performance, we measure import and export performance to several formats, as well as DuckDB's replacement scan functionality. 
Replacement scans allow DuckDB to read other formats like Pandas and Apache Arrow without a prior import step. 

### Import and Export Formats
Over time, DuckDB has added support for reading and writing multiple dataframe formats, including Pandas and Apache Arrow in the Python client. 
We measured the performance in both cases, but when summarizing the total performance, we chose the best performing format at the time.
This likely mirrored the behavior of performance-sensitive users (as they would likely not write to both formats!).
In version 0.5.1, DuckDB's performance when writing to and reading from the Apache Arrow format surpassed Pandas. 
As a result, versions 0.2.7 to 0.4.0 use Pandas, and 0.5.1 onward uses Arrow. 

### Python Client
To measure these common use cases, we have used Python rather than R (used by H2O.ai) for this analysis.
We do continue to use R for the data generation step for consistency with the benchmark.
Python is DuckDB's most popular client, so this is the most representative of real world performance.

### Window Functions
We also added an entire series of Window function benchmarks. 
Window functions are a critical workload in real world data analysis scenarios, and can stress test a system in other ways.
DuckDB has implemented state of the art algorithms to quickly process even the most complex window functions.
We use the largest table from the join benchmark as the raw data for these new tests to help with comparability to the rest of the benchmark. 
Window function benchmarks are much less common than more traditional joins and aggregations, and we were unable to find a suitable suite off the shelf. 
These queries were designed to showcase the variety of uses for window functions, but there are certainly more that could be added.
We are open to your suggestions for queries to add, and hope these queries could prove useful for other systems!

### Workload size
We test only the middle 5GB dataset size for the workloads mentioned thus far, primarily because some import and export operations to external formats like Pandas must fit in memory (and we used a Macbook Pro M1 with only 16GB of RAM). 
Additionally, running the tests for 3 year's of DuckDB versions was time-intensive even at that scale, due to the performance of older versions.

### Scale tests
However, using only 5GB of data does not answer our second key question: "What scale of data can it handle?"!
We also ran only the group by and join related operations (avoiding in-memory imports and exports) at the 5GB and the 50GB scale. 
Older versions of DuckDB could not handle the 50GB dataset when joining or aggregating, but modern versions can handle both, even on a memory-constrained 16GB RAM laptop.

### Computing resources
All tests use a 16GB Macbook Pro M1 with 16GB of RAM.
In 2024, this is far from state of the art! 
If you have more powerful hardware, you will see both improved performance and scalability.

### DuckDB Versions
Version 0.2.7 was the first version to include a Python client compiled for arm64, so it was the first version that could easily run on the benchmarking compute resources. 
Version 1.0.0 is the latest available at the time of publication, although we also provide a sneak preview of an in-development feature branch.

## Overall Benchmark Results
The latest DuckDB can complete one run of the full benchmark suite in under 35 seconds, while version 0.2.7 requires nearly 500 seconds for the same task. 
**That is 14 times faster, in only 3 years!**

### Performance Over Time
<div id="overall_results_by_time" style="width:100%;height:400px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/perf_over_time_overall_results_by_time.json')
        .then(res => res.json())
        .then(parsed_json => {
            let overall_results_by_time = document.getElementById('overall_results_by_time');
            parsed_json.layout = {...parsed_json.layout, "title": "Benchmark results over time"};
            Plotly.plot( overall_results_by_time, parsed_json.data, parsed_json.layout );
            });
</script>

The above plot shows the median runtime in seconds for all tests. 
Due to the variety of uses for window functions, and their relative algorithmic complexity, the 16 window function tests require the most time of any category.

<div id="overall_results_by_time_relative" style="width:100%;height:400px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/perf_over_time_overall_results_by_time_relative.json')
        .then(res => res.json())
        .then(parsed_json => {
            let overall_results_by_time_relative = document.getElementById('overall_results_by_time_relative');
            parsed_json.layout = {...parsed_json.layout, "title": "Relative benchmark results over time"};
            Plotly.plot( overall_results_by_time_relative, parsed_json.data, parsed_json.layout );
            });
</script>

This plot normalizes performance to the latest version of DuckDB to show relative improvements over time. 
If you look at the point in time when you most recently measured DuckDB performance, that number will show you how many times faster DuckDB is now!

> Note These graphs are interactive, thanks to [Plotly.js](https://plotly.com/javascript/)!
> Feel free to filter the various series (single click to hide, double click to show only that series) and click-and-drag to zoom in. 
> Individual benchmark results are visible on hover. 
> The color pallete used is the Tableau 10. 

A portion of the overall improvement is DuckDB's addition of multi-threading, which became the default in version 0.3.1. 
DuckDB also moved to a push-based execution model in that version for additional gains.
Parallel data loading boosted performance in 0.6.1, as did improvements to the core `JOIN` algorithm. 
We will explore other improvements in detail later in the post.

However, we see that all aspects of the system have seen improvements, not just raw query performance!
DuckDB focuses on the entire data analysis workflow, not just aggregate or join performance.
CSV parsing has seen significant gains, import and export have improved significantly, and Window functions have improved the most of all.

What was the slight regression from December 2022 to June 2023? 
Window functions received additional capabilities and experienced a slight performance degradation in the process.
However, from version 0.9.0 onward we see substantial performance improvement across the board for window functions. 
If window functions are filtered out of the chart, we see more consistent gains. 

You may also notice that starting with version 0.9 in September 2023, the performance appears to plateau. 
What is happening here? 
The DuckDB Labs team focused on scalability by developing algorithms that support larger than memory calculations. 
We will see the fruits of those labors in the scale section later on!
In addition, DuckDB focused exclusively on bug fixes for all versions beyond 0.10.0 in preparation for an especially robust DuckDB 1.0. 
The pre-0.9 trend is a better indicator for the future now that those two major milestones were accomplished!


### Performance by Version
We can also recreate the overall plot by version rather than by time.
This demonstrates that DuckDB has been doing more frequent releases recently. 

<div id="overall_results_by_version" style="width:100%;height:400px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/perf_over_time_overall_results_by_version.json')
        .then(res => res.json())
        .then(parsed_json => {
            let overall_results_by_version = document.getElementById('overall_results_by_version');
            parsed_json.layout = {...parsed_json.layout, "title": "Benchmark results by version"};
            Plotly.plot( overall_results_by_version, parsed_json.data, parsed_json.layout );
            });
</script>

If you remember the version that you last tested, you can compare how much faster things are now with 1.0!

<div id="overall_results_by_version_relative" style="width:100%;height:400px;"></div>
<script>
    fetch('{{ site.baseurl }}/data/perf_over_time_overall_results_by_version_relative.json')
        .then(res => res.json())
        .then(parsed_json => {
            let overall_results_by_version_relative = document.getElementById('overall_results_by_version_relative');
            parsed_json.layout = {...parsed_json.layout, "title": "Relative benchmark results by version"};
            Plotly.plot( overall_results_by_version_relative, parsed_json.data, parsed_json.layout );
            });
</script>

## Results by Workload

### CSV Parsing
DuckDB has invested substantially in building a [fast and robust CSV parser](https://duckdb.org/2023/10/27/csv-sniffer.html).
This is often the first task in a data analysis workload, and it tends to be under valued and under-benchmarked. 
DuckDB has improved csv reader performance by nearly 3x, while adding the ability to handle many more csv file formats automatically.

### Group By
Group by or aggregation operations are a critical OLAP workload, and have therefore received substantial focus in DuckDB, improving over 12x in the last 3 years.
In version 0.3.1, multithreaded aggregation was enabled by default, providing a significant speedup.

In 0.6.1, data loads into tables were parallelized.
This is another example of improving the entire data workflow, as this group by benchmark actually stressed the insertion performance substantially. 
Inserting the results was taking the majority of the time!

Enums were also used in place of strings for categorical columns in version 0.6.1. 
This means that DuckDB was able to use integers rather than strings when operating on those columns, further boosting performance.

Despite the performance plateau, aggregations have received significant attention in the most recent versions to enable larger than memory aggregations.
You can see that this was achieved without reducing performance for the smaller-than-memory case.


### Join
Join operations are another area of focus for analytical databases, and DuckDB in particular.
Join speeds have improved by 4x in the last 3 years! 

Version 0.6.1 introduced improvements to the out of core hash join that actually improved the smaller-than-memory case as well.
Parallel data loading from 0.6.1 also helps in this benchmark as well, as some results are the same size as the input table. 

In recent versions, they have also been upgraded to support larger than memory capabilities. 
This focus has also benefitted the smaller-than-memory case and has led to the improvements in 0.10. 

### Window Functions
<!-- TODO: Research why things got faster at various points -->

### Export
Often DuckDB is not the final step in a workflow, so export performance has an impact. 
Until recently, the DuckDB format was not backward compatible, so the recommended long term persistence format was Parquet.
Parquet is also critical to interoperability with many other systems, especially data lakes. 
DuckDB works well as a workflow engine, so exporting to other in memory formats is quite common as well.

In version 0.5.1 we see significant improvements driven by switching from Pandas to Apache Arrow as the recommended in-memory export format.
DuckDB's underlying data types share many similarities with Arrow, so data transfer is quite quick.

Exports to parquet have also improved dramatically in version 0.10.2. 
<!-- TODO: Why are parquet exports better in 0.10.2? -->


### Scan Other Formats
In some use cases, DuckDB does not need to store the raw data, but instead should simply read and analyze it. 
This allows DuckDB to fit seamlessly into other workflows. 
This benchmark measures how fast DuckDB can scan and aggregate various data formats. 
To enable comparisons over time, we switch from Pandas to Arrow at version 0.5.1 as mentioned.
DuckDB is nearly 7x faster in this situation, and the absolute time required is very short. 
DuckDB is a great fit for this type of work!


## Scale tests

### 50GB Group By

### 50GB Join


<!-- TODO: Fix the hover text of the DuckDB version for the export data points -->
