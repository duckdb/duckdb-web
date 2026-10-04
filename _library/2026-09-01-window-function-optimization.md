---
layout: post
title: "Window Function Optimization: Co-Evaluation and Other Techniques"
author: "Daniel Lindner, Felix Naumann, Alberto Lerner"
tags: ["Paper"]
thirdparty: true
category: community
excerpt: ""
pill: "VLDB 2026"
---

| | |
|-------|-------|
| **Paper** | [Window Function Optimization: Co-Evaluation and Other Techniques (PDF)](https://www.vldb.org/pvldb/vol19/p3525-lindner.pdf) |
| **Implementation** | [Code](https://github.com/HPI-Information-Systems/wf-optimization) |
| **Venue** | VLDB 2026 |

## Abstract

Window functions are among the most expressive features of modern SQL. Surprisingly, relatively little has been written about their optimization. Some techniques exist, such as pushing predicates through a window under ideal conditions, but known optimizations no longer apply when those conditions are even slightly unmet. We show that these limitations are not fundamental, but persist because a reasoning framework for window function optimization has been missing. We provide such a framework, introducing techniques we call Frame Analysis, Partition Analysis, and a new execution strategy called Co-Evaluation. These clarify when and how optimizations can be applied. Co-Evaluation, in particular, allows early evaluation of predicates even when they depend on the window function’s result. We present each technique and organize the results as a table of algebraic equivalences for window functions. We test these optimizations in an open-source engine, where they never hurt performance and make certain common queries up to 40.7× faster, with larger tables yielding larger gains.
