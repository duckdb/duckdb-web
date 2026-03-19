---
layout: post
title: "BananaPi F3 (RISC-V)"
date: 2026-03-19
author: "Bruno Verachten"
thumb: "/images/everywhere/thumbs/bananapi-f3.jpg"
image: "/images/everywhere/thumbs/bananapi-f3.jpg"
excerpt: ""
tags: ["Single-board computers"]
thirdparty: true
---

DuckDB runs natively on the BananaPi F3, a $100 RISC-V single-board computer powered by the SpacemiT K1 SoC (8 cores @ 1.6 GHz, rv64gc, 16 GB RAM).

The build takes approximately 2 hours with `make -j8`, and the resulting binary passes SQL queries — from simple selects to aggregations over generated datasets.

```sql
SELECT count(*) AS cnt, round(avg(value), 2) AS avg_val
FROM (SELECT range * 3.14 AS value FROM range(1000));
```

```text
┌───────┬─────────┐
│  cnt  │ avg_val │
│ int64 │ double  │
├───────┼─────────┤
│  1000 │ 1568.43 │
└───────┴─────────┘
```

The DuckDB Python package also builds from source on riscv64.
See the [build instructions]({% link docs/current/dev/building/unofficial_and_unsupported_platforms.md %}#native-build-recommended) for details.
