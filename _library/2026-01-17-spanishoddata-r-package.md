---
layout: post
title: "spanishoddata: A package for accessing and working with Spanish Open Mobility Big Data"
author: "Egor Kotov, Eugeni Vidal-Tortosa, Oliva G. Cantú-Ros, Javier Burrieza-Galán, Ricardo Herranz, Tania Gullón Muñoz-Repiso, Robin Lovelace"
thumb: "/images/library/thumbs/paper.svg"
image: "/images/library/thumbs/paper.png"
tags: ["Paper"]
thirdparty: true
excerpt: ""
pill: "EPB 2026"
---

[Paper (Open Access)](https://doi.org/10.1177/23998083251415040)

[Supplementary Materials (PDF)](https://journals.sagepub.com/doi/suppl/10.1177/23998083251415040/suppl_file/sj-pdf-1-epb-10.1177_23998083251415040.pdf)

[Reproducible R code and data](https://doi.org/10.5281/zenodo.15289979)

Venue: Environment and Planning B: Urban Analytics and City Science (2026)

## Abstract

We present [spanishoddata](https://ropenspain.github.io/spanishoddata/), an R package that enables fast and efficient access to Spain’s open, high-resolution origin-destination human mobility datasets, derived from anonymized mobile-phone records and released by the Ministry of Transport and Sustainable Mobility. The package directly addresses challenges of data accessibility, reproducibility and efficient processing identified in prior studies. Using DuckDB, spanishoddata automates retrieval from the official source, performs file and schema validation, and converts the data to efficient, analysis-ready formats (DuckDB and Parquet) that enable multi-month and multi-year analysis on consumer-grade hardware. The interface handles complexities associated with these datasets, enabling a wide range of people – from data science beginners to experienced practitioners with domain expertise – to start using the data with just a few lines of code. We demonstrate the utility of the package with example applications in urban transport planning, such as assessing cycling potential or understanding mobility patterns by activity type. By simplifying data access and promoting reproducible workflows, spanishoddata lowers the barrier to entry for researchers, policymakers, transport planners or anyone seeking to leverage mobility datasets.

## Implementation

The spanishoddata R package leverages DuckDB as a backend to handle massive mobility datasets. It utilizes the underlying [DuckDB R package](https://r.duckdb.org/) and its compatibility with the [tidyverse](https://tidyverse.org/) to provide a user-friendly and opinionated interface for data manipulation and analysis.

*   [GitHub Repository](https://github.com/rOpenSpain/spanishoddata)

*   [CRAN R package repository](https://CRAN.R-project.org/package=spanishoddata)

## Educational Resources

To complement the package, we have developed educational resources to help users get started with the package and the data:

*   [Workshop: Analysing massive open human mobility data using spanishoddata, duckdb and flowmaps](https://www.ekotov.pro/agit-2025-spanishoddata/) (AGIT 2025)

*   [Tutorial: Mobility Flows and Accessibility Using R and Big Open Data](https://www.ekotov.pro/spanish-open-mobility-workshop-ic2s2-2025/) (IC2S2 2025)
