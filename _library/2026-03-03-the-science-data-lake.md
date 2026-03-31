---
layout: post
title: "The Science Data Lake: A Unified Open Infrastructure Integrating 293 Million Papers Across Eight Scholarly Sources with Embedding-Based Ontology Alignment"
author: "Jonas Wilinski"
thumb: "/images/library/thumbs/arxiv.svg"
image: "/images/library/thumbs/arxiv.jpg"
tags: ["Paper"]
category: community
excerpt: ""
pill: "arXiv"
---

|-------|-------|
| **Paper** | [The Science Data Lake: A Unified Open Infrastructure Integrating 293 Million Papers Across Eight Scholarly Sources with Embedding-Based Ontology Alignment (Preprint PDF)](https://arxiv.org/pdf/2603.03126.pdf) |
| **Implementation** | [GitHub](https://github.com/J0nasW/science-datalake) |
| **Dataset** | [HuggingFace](https://huggingface.co/datasets/J0nasW/science-datalake) |
| **Published** | arXiv, 2026 |

## Abstract

Scholarly data are largely fragmented across siloed databases with divergent metadata and missing linkages among them. We present the Science Data Lake, a locally-deployable infrastructure built on DuckDB and simple Parquet files that unifies eight open sources – Semantic Scholar, OpenAlex, SciSciNet, Papers with Code, Retraction Watch, Reliance on Science, a preprint-to-published mapping, and Crossref – via DOI normalization while preserving source-level schemas. The resulting resource comprises approximately 960 GB of Parquet files spanning 293 million uniquely identifiable papers, with SQL views that expose cross-source joins without redundant data copies. To bridge the heterogeneous subject taxonomies of these sources, we introduce an embedding-based ontology alignment method that maps over 4,500 OpenAlex topics to thirteen established scientific ontologies, achieving an F1 of 0.77 at recommended thresholds. We validate integration quality through automated checks, cross-source citation analysis, and manual annotation, and demonstrate several analyses infeasible with any single database. All code, data, and documentation are released as an open-source, locally deployable resource with remote query support and LLM-ready documentation.
