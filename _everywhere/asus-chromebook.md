---
layout: post
title: "Asus Chromebook CM3001DM2"
date: 2026-03-02
author: "Ladislav Dvorak"
thumb: "/images/everywhere/thumbs/asus-chromebook.jpg"
image: "/images/everywhere/thumbs/asus-chromebook.jpg"
excerpt: "DuckDB can complete all TPC-H SF100 queries on the Asus Chromebook CM3001DM2, an ARM-based Chromebook with 8 GB of RAM, running via ChromeOS's Linux container environment."
tags: ["PCs"]
thirdparty: true
---

DuckDB can complete all [TPC-H]({% link docs/current/core_extensions/tpch.md %}) SF100 queries on the [Asus Chromebook CM30 Detachable (CM3001)](https://www.asus.com/laptops/for-home/chromebook/asus-chromebook-cm30-detachable-cm3001/techspec/), running via Crostini, ChromeOS's built-in Linux container environment.

The laptop is powered by the MediaTek Kompanio 520 (MT8186), which features 2 Arm Cortex-A76 performance cores (up to 2.2 GHz) and 6 Arm Cortex-A55 efficiency cores (up to 2.0 GHz), with a 256 KB L2 cache per CPU package. The machine ships with 8 GB of LPDDR4X RAM soldered to the board and 128 GB of eMMC storage.

The benchmark was run using DuckDB v1.5.1, downloaded as a pre-compiled binary — compiling DuckDB from source was not feasible due to the limited RAM available in the Crostini container (approximately 6.5 GB). We could not test TPC-H SF300 dataset because the 128 GB eMMC storage was insufficient to hold the database file.

![Asus Chromebook CM3001DM2 running TPC-H queries with DuckDB]({% link images/everywhere/asus_chromebook_running_tpch_duckdb.jpg %})
