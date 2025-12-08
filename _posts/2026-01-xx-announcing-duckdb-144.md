---
layout: post
title: "Announcing DuckDB 1.4.4 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-4-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-4-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.4."
tags: ["release"]
---

### Extension Distribution for Windows ARM64

We are introducing beta support for Windows ARM64. You can now install core extensions now on this platform:

```sql
PRAGMA platform;
```

```text
┌───────────────┐
│   platform    │
│    varchar    │
├───────────────┤
│ windows_arm64 │
└───────────────┘
```

```sql
INSTALL spatial;
LOAD spatial;
SELECT ST_Area(ST_GeomFromText('POLYGON((0 0, 4 0, 4 3, 0 3, 0 0))')) AS area;
```

```text
┌────────┐
│  area  │
│ double │
├────────┤
│  12.0  │
└────────┘
```

