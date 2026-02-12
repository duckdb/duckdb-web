---
layout: post
title: "Fast Hypothetical Updates Evaluation"
author: "Haneen Mohammed, Alexander Yao, Charlie Summers, Hongbin Zhong, Gromit Yeuk-Yin Chan, Subrata Mitra, Lampros Flokas, Eugene Wu"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "PW 25"
---

[Paper (PDF)](https://dl.acm.org/doi/pdf/10.1145/3736229.3736254)

Venue: ProvenanceWeek 2025

## Abstract

We demonstrate FaDE, a DuckDB extension that supports fast hypothetical deletions and scaling updates for Select-Project-Join-Aggregate-Union (SPJAU) queries, achieving low latency and high throughput (>1M hypothetical deletions or scaling updates per second)—orders of magnitude higher throughput than any prior approach. To showcase the expressiveness of FaDE’s API, we explore two data-driven applications. First, we use FaDE’s whatif() API to update linked visualizations by modeling updates as hypothetical deletions, effectively removing the influence of non-selected tuples. Second, we use FaDE to build an interactive explanation engine that uses the whatif() API to apply a set of hypothetical updates (12.7K interventions in <2ms) to find the best predicates that explain a set of outliers with just a few lines of code. Finally, explanations vary in the base query, metric, and space of candidate predicates. To demonstrate FaDE’s versatility, participants can use FaDE as a DuckDB extension through a Python Notebook, reuse workload from previous applications, and explore FaDE’s  whatif() API.
