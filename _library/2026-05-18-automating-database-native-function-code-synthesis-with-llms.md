---
layout: post
title: "Automating Database-Native Function Code Synthesis with LLMs"
author: "Wei Zhou, Xuanhe Zhou, Qikang He, Guoliang Li, Bingsheng He, Quanqing Xu, Fan Wu"
thumb: "/images/library/thumbs/sigmod.svg"
image: "/images/library/thumbs/sigmod.jpg"
tags: ["Paper"]
category: community
excerpt: ""
pill: "SIGMOD 2026"
---

| | |
|-------|-------|
| **Paper** | [Automating Database-Native Function Code Synthesis with LLMs (PDF)](https://dl.acm.org/doi/pdf/10.1145/3802018) |
| **Venue** | SIGMOD 2026 |

## Abstract

Database systems incorporate an ever-growing number of functions built in their kernels (a.k.a., database native functions) for scenarios like new application support and business migration. This growth causes an urgent demand for automatic database native function synthesis. While recent advances in LLM-based code generation (e.g., Claude Code) show promise, existing approaches are too generic for database-specific development. They often hallucinate or overlook critical context because database function synthesis is inherently complex and error-prone, where synthesizing a single database function may involve registering multiple function units (e.g., for different input types), placing code in the correct source files, linking internal references, and implementing logic correctly.

To this end, we propose DBCooker, an LLM-based system for automatically synthesizing database native functions. The system consists of three key components. First, the function characterization module aggregates multi-source declarations, identifies function units that require specialized coding through hierarchical analysis, and traces cross-unit dependencies via static analysis. Second, we design operations to address the main synthesis challenges: (1) a pseudo-code–based coding plan generator that constructs structured implementation skeletons by identifying key elements such as reusable referenced functions; (2) a hybrid fill-in-the-blank model guided by probabilistic priors and component awareness to integrate core logic with reusable routines; and (3) three-level progressive validation, including syntax checking, standards compliance, and LLM-guided semantic verification. Finally, an adaptive orchestration strategy unifies these operations with existing database tools and dynamically sequences them based on the orchestration history of similar functions. Results show that our system outperforms state-of-the-art methods on SQLite, PostgreSQL, and DuckDB (34.55% higher accuracy on average), and can synthesize four categories of new functions absent in the latest SQLite (v3.50). The code is available at [`https://github.com/weAIDB/DBCooker`](https://github.com/weAIDB/DBCooker).
