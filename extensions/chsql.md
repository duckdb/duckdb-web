---
layout: community_extension
title: chsql
excerpt: |
  DuckDB Community Extensions
  ClickHouse SQL Macros for DuckDB

extension:
  name: chsql
  description: ClickHouse SQL Macros for DuckDB
  version: 1.0.2
  language: SQL & C++
  build: cmake
  license: MIT
  maintainers:
    - lmangani

repo:
  github: lmangani/duckdb-extension-clickhouse-sql
  ref: 3a81f48b9ea4262eaaa5c40076ad4e6202065472

docs:
  hello_world: |
    SELECT toString('world') as hello, toInt8OrZero('world') as zero;
  extended_description: |
    This extension provides a growing number of ClickHouse SQL Macros for DuckDB. 
    For a list of supported functions, please refer to [latest release notes](https://github.com/lmangani/duckdb-extension-clickhouse-sql/releases).

extension_star_count: 7

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
| IPv4NumToString       | macro         |             |         |         |
| IPv4StringToNum       | macro         |             |         |         |
| arrayExists           | macro         |             |         |         |
| arrayJoin             | macro         |             |         |         |
| arrayMap              | macro         |             |         |         |
| bitCount              | macro         |             |         |         |
| chsql                 | scalar        |             |         |         |
| chsql_openssl_version | scalar        |             |         |         |
| domain                | macro         |             |         |         |
| empty                 | macro         |             |         |         |
| extractAllGroups      | macro         |             |         |         |
| formatDateTime        | macro         |             |         |         |
| generateUUIDv4        | macro         |             |         |         |
| ifNull                | macro         |             |         |         |
| intDiv                | macro         |             |         |         |
| intDivOZero           | macro         |             |         |         |
| intDivOrNull          | macro         |             |         |         |
| leftPad               | macro         |             |         |         |
| lengthUTF8            | macro         |             |         |         |
| match                 | macro         |             |         |         |
| minus                 | macro         |             |         |         |
| modulo                | macro         |             |         |         |
| moduloOrZero          | macro         |             |         |         |
| notEmpty              | macro         |             |         |         |
| numbers               | table_macro   |             |         |         |
| parseURL              | macro         |             |         |         |
| path                  | macro         |             |         |         |
| plus                  | macro         |             |         |         |
| protocol              | macro         |             |         |         |
| rightPad              | macro         |             |         |         |
| splitByChar           | macro         |             |         |         |
| tableMultiply         | table_macro   |             |         |         |
| toDayOfMonth          | macro         |             |         |         |
| toFixedString         | macro         |             |         |         |
| toFloat               | macro         |             |         |         |
| toFloatOrNull         | macro         |             |         |         |
| toFloatOrZero         | macro         |             |         |         |
| toHour                | macro         |             |         |         |
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
| toMinute              | macro         |             |         |         |
| toMonth               | macro         |             |         |         |
| toSecond              | macro         |             |         |         |
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
| toYYYYMM              | macro         |             |         |         |
| toYYYYMMDD            | macro         |             |         |         |
| toYYYYMMDDhhmmss      | macro         |             |         |         |
| toYear                | macro         |             |         |         |
| topLevelDomain        | macro         |             |         |         |
| tupleConcat           | macro         |             |         |         |
| tupleDivide           | macro         |             |         |         |
| tupleDivideByNumber   | macro         |             |         |         |
| tupleIntDiv           | macro         |             |         |         |
| tupleIntDivByNumber   | macro         |             |         |         |
| tupleMinus            | macro         |             |         |         |
| tupleModulo           | macro         |             |         |         |
| tupleModuloByNumber   | macro         |             |         |         |
| tupleMultiply         | macro         |             |         |         |
| tupleMultiplyByNumber | macro         |             |         |         |
| tuplePlus             | macro         |             |         |         |



---

