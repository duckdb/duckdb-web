---
layout: post
title: "Generation of Adversarial Queries via Bayesian Optimization"
author: "Jeffrey Tao, Yimeng Zeng, Natalie Maus, Haydn Jones, Osbert Bastani, Jacob R. Gardner, Ryan Marcus"
tags: ["Paper"]
thirdparty: true
category: community
excerpt: ""
pill: "AIDB@VLDB 2026"
---

|-------|-------|
| **Paper** | [Generation of Adversarial Queries via Bayesian Optimization (PDF)](https://vldb.org/2026/Workshops/VLDB-Workshops-2026/AIDB/aidb26_14.pdf) |
| **Implementation** | [Code](https://github.com/Speculative/adversarial-queries) |
| **Venue** | AIDB workshop at VLDB 2026 (Applied AI for Database Systems and Applications) |

## Abstract

Benchmarks determine where the database community will direct its optimization efforts and directly shape the behaviors of learned systems. However, existing benchmarks are constructed to be realistic or difficult, with no guarantee that systems can actually improve on their queries. We argue that benchmarks should instead target headroom, the gap between how well a query currently executes and how well it could execute. By identifying queries which have optimization potential, headroom provides a clear signal of where a system is underperforming. To this end, we introduce Gremlin, a system for generating adversarial benchmarks of queries with high headroom. To do so, we apply Bayesian optimization to search the joint space of queries and witness plans, seeking query-plan pairs that maximize headroom, where each witness plan provides concrete evidence of how a system could have selected a better join order. We show that Gremlin is system and dataset-agnostic, demonstrating that the generation technique is generalizable and reusable. Comparing against existing benchmarks, we find that Gremlin-generated benchmarks have multiple orders of magnitude more headroom, with the median query having 34.2× headroom to JOB + JOB-Complex's 1.4×, and summed headroom at the benchmark level of over 8 hours compared to 12.4 seconds.
