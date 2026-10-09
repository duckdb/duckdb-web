---
layout: post
title: "iPhone 17 Pro vs. Databricks"
date: 2026-10-07
authors:
  - George Fraser
thumb: "/images/everywhere/thumbs/iphone-17-pro.png"
image: "/images/everywhere/thumbs/iphone-17-pro.png"
excerpt: "An iPhone 17 Pro running DuckDB outperforms Databricks Serverless SQL clusters on TPC-H at most scale factors up to SF200."
tag: phones
category: community
---

George Fraser, CEO of Fivetran, benchmarked an iPhone 17 Pro (6 CPU cores, 12 GB RAM) running DuckDB against Databricks Serverless SQL clusters (XS, S and M, with up to 80 CPUs and 448 GB of memory) on the [TPC-H]({% link docs/current/core_extensions/tpch.md %}) benchmark at scale factors 25, 50, 100 and 200.
The iPhone beat every Databricks cluster at all scales except SF200, where it was still close – with the help of an ice pack to avoid thermal throttling.

See the [“I benchmarked Databricks against my iPhone” blog post](https://www.fivetran.com/blog/i-benchmarked-databricks-against-my-iphone) and the [`fivetran/iphone_benchmark` repository](https://github.com/fivetran/iphone_benchmark) for details.
