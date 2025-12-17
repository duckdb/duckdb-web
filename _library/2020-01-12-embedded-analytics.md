---
layout: post
title: "Data Management for Data Science Towards Embedded Analytics"
author: "Hannes Mühleisen, Mark Raasveldt"
thumb: "/images/science/thumbs/cidr-2020.svg"
image: "/images/science/thumbs/cidr-2020.png"
tags: ["Paper"]
thirdparty: false
---

[Paper (PDF)](https://hannes.muehleisen.org/publications/CIDR2020-raasveldt-muehleisen-duckdb.pdf)

Venue: CIDR 2020

## Abstract

The rise of Data Science has caused an influx of new users in need of data management solutions. However, instead of utilizing existing RDBMS solutions they are opting to use a stack of independent solutions for data storage and processing glued together by scripting languages. This is not because they do not need the functionality that an integrated RDBMS provides, but rather because existing RDBMS implementations do not cater to their use case. To solve these issues, we propose a new class of data management systems: embedded analytical systems. These systems are tightly integrated with analytical tools, and provide fast and efficient access to the data stored within them. In this work, we describe the unique challenges and opportunities w.r.t. workloads, resilience and cooperation that are faced by this new class of systems and the steps we have taken towards addressing them in the DuckDB system.
