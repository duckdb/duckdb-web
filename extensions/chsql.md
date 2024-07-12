---
layout: community_extension
title: chsql
excerpt: |
  DuckDB Community Extensions
  ClickHouse SQL Macros for DuckDB

extension:
  name: chsql
  description: ClickHouse SQL Macros for DuckDB
  version: 1.0.1
  language: SQL & C++
  build: cmake
  license: MIT
  maintainers:
    - lmangani

repo:
  github: lmangani/duckdb-extension-clickhouse-sql
  ref: 17c249ba08a9b88338e77c7f2d6e5dd2040b4590

docs:
  hello_world: |
    SELECT toString('world') as hello, toInt8OrZero('world') as zero;
  extended_description: |
    This extension provides a growing number of ClickHouse SQL Macros for DuckDB. 

extension_star_count: 5

---

### Installing and Loading
```sql
INSTALL {{ page.extension.name }} FROM community;
LOAD {{ page.extension.name }};
```

{% if page.docs.hello_world %}
### Example
```sql
{{ page.docs.hello_world }}```
{% endif %}

{% if page.docs.extended_description %}
### About {{ page.extension.name }}
{{ page.docs.extended_description }}
{% endif %}

### Added Functions

<div class="extension_functions_table"></div>

|     function_name     | function_type | description | comment | example |
|-----------------------|---------------|-------------|---------|---------|
| arrayExists           | macro         |             |         |         |
| arrayMap              | macro         |             |         |         |
| chsql                 | scalar        |             |         |         |
| chsql_openssl_version | scalar        |             |         |         |
| intDiv                | macro         |             |         |         |
| match                 | macro         |             |         |         |
| times_two             | macro         |             |         |         |
| times_two_table       | table_macro   |             |         |         |
| toFloat               | macro         |             |         |         |
| toFloatOrNull         | macro         |             |         |         |
| toFloatOrZero         | macro         |             |         |         |
| toInt128              | macro         |             |         |         |
| toInt128OrNull        | macro         |             |         |         |
| toInt128OrZero        | macro         |             |         |         |
| toInt16               | macro         |             |         |         |
| toInt16OrNull         | macro         |             |         |         |
| toInt16OrZero         | macro         |             |         |         |
| toInt256              | macro         |             |         |         |
| toInt256OrNull        | macro         |             |         |         |
| toInt256OrZero        | macro         |             |         |         |
| toInt32               | macro         |             |         |         |
| toInt32OrNull         | macro         |             |         |         |
| toInt32OrZero         | macro         |             |         |         |
| toInt64               | macro         |             |         |         |
| toInt64OrNull         | macro         |             |         |         |
| toInt64OrZero         | macro         |             |         |         |
| toInt8                | macro         |             |         |         |
| toInt8OrNull          | macro         |             |         |         |
| toInt8OrZero          | macro         |             |         |         |
| toString              | macro         |             |         |         |
| toUInt16              | macro         |             |         |         |
| toUInt16OrNull        | macro         |             |         |         |
| toUInt16OrZero        | macro         |             |         |         |
| toUInt32              | macro         |             |         |         |
| toUInt32OrNull        | macro         |             |         |         |
| toUInt32OrZero        | macro         |             |         |         |
| toUInt64              | macro         |             |         |         |
| toUInt64OrNull        | macro         |             |         |         |
| toUInt64OrZero        | macro         |             |         |         |
| toUInt8               | macro         |             |         |         |
| toUInt8OrNull         | macro         |             |         |         |
| toUInt8OrZero         | macro         |             |         |         |



---

