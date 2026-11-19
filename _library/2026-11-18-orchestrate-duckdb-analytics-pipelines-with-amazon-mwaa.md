---
layout: post
title: "Orchestrate DuckDB Analytics Pipelines with Amazon MWAA"
authors:
  - Vinod Jayendra
  - Niko Oliveira
  - Suba Palanisamy
  - Varsha Gowda
tag: article
category: community
excerpt: ""
venue: "AWS Big Data Blog"
---

|-------|-------|
| **Article** | [Orchestrate DuckDB analytics pipelines with Amazon MWAA](https://aws.amazon.com/blogs/big-data/orchestrate-duckdb-analytics-pipelines-with-amazon-mwaa/) |
| **Publication** | [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/) |

A walkthrough of running DuckDB 2.0 inside Apache Airflow tasks on Amazon Managed Workflows for Apache Airflow (MWAA) using the Airflow DuckDB provider's `DuckDBExecuteQueryOperator`. The example builds a showback pipeline that transforms Parquet data from Amazon S3, publishes the results as Apache Iceberg tables in Amazon S3 Tables, and validates the output, all without a separate analytics cluster.
