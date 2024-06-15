---
layout: docu
title: Glossary of Terms
---

This page contains a glossary of a few common terms used in DuckDB.

## Terms

### In-Process Database Management System

The DBMS runs in the client application's process instead of running as a separate process, which is common in the traditional client–server setup. An alterative term is **embeddable** database management system. In general, the term _"embedded database management system"_ should be avoided, as it can be confused with DBMSs targeting _embedded systems_ (which run on e.g. microcontrollers).

### Replacement Scan

In DuckDB, replacement scans are used when a table name used by a query does not exist in the catalog. These scans can substitute another data source intead of the table. Using replacement scans allows DuckDB to, e.g., seamlessly read [Pandas DataFrames](../guides/python/sql_on_pandas) or read input data from remote sources without explicitly invoking the functions that perform this (e.g., [reading Parquet files from https](../guides/network_cloud_storage/http_import)). For details, see the [C API - Replacement Scans page](../api/c/replacement_scans).

### Extension

DuckDB has a flexible extension mechanism that allows for dynamically loading extensions. These may extend DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality. For details, see the [Extensions page](../extensions/overview).

### Platform

The platform is a combination of the operating system (e.g., Linux, macOS, Windows), system architecture (e.g., AMD64, ARM64), and, optionally, the compiler used (e.g., GCC4). Platforms are used to distributed DuckDB binaries and [extension packages](../extensions/working_with_extensions#platforms).
