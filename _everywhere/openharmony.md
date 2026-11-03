---
layout: post
title: "Huawei MateBook (OpenHarmony, Arm64)"
date: 2026-10-27
authors:
  - springmin
thumb: "/images/everywhere/thumbs/huawei-matebook.png"
image: "/images/everywhere/thumbs/huawei-matebook.png"
excerpt: "DuckDB builds and runs natively on OpenHarmony arm64 devices."
tag: other
category: community
---

DuckDB runs natively on OpenHarmony (OHOS) arm64 devices.
We tested it on a HarmonyOS device (arm64, 20 cores, HongMeng kernel 1.13.0) with the
OpenHarmony SDK 26.0.0.18: the CLI builds natively, reports the platform as
`openharmony_arm64`, and passes 8,315 of 8,316 test cases in the DuckDB test suite.

```sql
PRAGMA platform;
```

```text
┌───────────────────┐
│     platform      │
│      varchar      │
├───────────────────┤
│ openharmony_arm64 │
└───────────────────┘
```

The build is documented on the
[OpenHarmony build page]({% link docs/2.0/dev/building/openharmony.md %}), and a
cross-compilation CI job uses the official OpenHarmony 7.0 Linux x64 SDK.
See [duckdb/duckdb#27882](https://github.com/duckdb/duckdb/pull/27882) for the build support.
