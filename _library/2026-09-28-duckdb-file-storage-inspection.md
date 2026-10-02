---
layout: post
title: "DuckDB File Storage Inspection"
author: "dentiny"
tags: ["Website"]
thirdparty: true
category: community
excerpt: ""
---

|-------|-------|
| **Implementation** | [Code](https://github.com/dentiny/DuckDB_file_storage_inspection) |

A browser-based viewer that visualizes the physical layout of a DuckDB database file, inspired by Parquet X-ray. It mounts the file read-only in DuckDB-Wasm and shows headers, metadata, row groups, column segments, free and index blocks, as well as the contents of the write-ahead log (WAL). It also handles truncated or corrupted files, marking missing blocks and flagging incomplete WAL entries.
