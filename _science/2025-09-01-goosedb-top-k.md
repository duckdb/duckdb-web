---
layout: post
title: "GooseDB: A Database Engine that Optimally Refines Top-𝑘 Queries to Satisfy Representation Constraints"
author: "Zixuan Chen, Jinyang Li, H. V. Jagadish, Mirek Riedewald"
thumb: "/images/science/thumbs/vldb-2025.svg"
image: "/images/science/thumbs/vldb-2025.png"
excerpt: ""
tags: ["Paper"]
---

[Paper (PDF)](https://www.vldb.org/pvldb/vol18/p5351-chen.pdf)

Venue: VLDB 2025

## Abstract

In many applications, from university rankings to the selection of candidates for a job interview, there exist various “reasonable” ways to filter the data and generate a ranking. When the initial choice lacks certain desirable properties, we want to identify a minimally modified alternative that has those properties. To this end, we demonstrate GooseDB, a database engine that combines DuckDB with an MILP solver. Given an SQL query, constraints on the output, and modification preferences, GooseDB returns a minimally modified SQL query that satisfies the constraints. This demo focuses on representation constraints for top-𝑘 queries, i.e., count constraints over groups of tuples, such as the gender distribution of the top-𝑘 job candidates. GooseDB significantly generalizes previous work in two directions. First, it supports more general modifications of the selection condition and the scoring function. Second, it is the first solution to holistically optimize for both at the same time, as well as for alternative values of limit 𝑘. Conference attendees will be able to interactively refine queries from easy-to-understand applications, observing the impact of their choices.
