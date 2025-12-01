---
layout: post
title: "Announcing DuckDB 1.4.3 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-3-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-3-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.3."
tags: ["release"]
---

In this blog post, we highlight a few important fixes and convenience improvements in DuckDB v1.4.3, the second bugfix release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.3).

To install the new version, please visit the [installation page]({% link install/index.html %}).


## Windows ARM64

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

### Python Wheel Distribution for Windows ARM64

We now distribute Python wheels for Windows ARM64. This means that you take e.g. a Copilot+ laptop and run:

```bash
pip install duckdb
```
