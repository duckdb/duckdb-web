---
layout: post
title: "Can Learned Query Optimizers Adapt Across DBMS Architectures? A Case Study with Balsa and DuckDB"
author: "Wangshu Hong, Ryan Marcus"
tags: ["Paper"]
thirdparty: true
category: community
excerpt: ""
pill: "AIDB@VLDB 2026"
---

|-------|-------|
| **Paper** | [Can Learned Query Optimizers Adapt Across DBMS Architectures? A Case Study with Balsa and DuckDB (PDF)](https://vldb.org/2026/Workshops/VLDB-Workshops-2026/AIDB/aidb26_9.pdf) |
| **Implementation** | [Code](https://github.com/winstonhong15/balsa) |
| **Venue** | AIDB workshop at VLDB 2026 (Applied AI for Database Systems and Applications) |

## Abstract

Learned query optimizers such as Balsa have demonstrated strong performance on PostgreSQL-style database systems, but their portability to modern analytical engines remains unclear. This work adapts Balsa to DuckDB, a vectorized analytical database that lacks both plan hinting and statement-level timeout support. To enable reinforcement-learning-based optimization in this setting, we introduce lightweight portability mechanisms based on SQL-level plan forcing and timeout management for safe exploration. We further incorporate censored-observation training to improve stability during reinforcement-learning-based exploration. Experiments on the Join Order Benchmark (JOB) and JOB-Complex benchmarks show that Balsa can learn competitive query plans on DuckDB without modifying the underlying optimizer or execution engine. These results suggest that learned query optimizers can adapt to substantially different DBMS architectures using lightweight integration mechanisms.
