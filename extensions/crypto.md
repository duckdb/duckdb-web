---
layout: community_extension
title: crypto
excerpt: |
  DuckDB Community Extensions
  Cryptographic hash functions and HMAC

extension:
  name: crypto
  description: Cryptographic hash functions and HMAC
  version: 1.0.0
  language: C++
  build: cmake
  license: Apache-2.0
  excluded_platforms: "windows_amd64_rtools;windows_amd64"
  maintainers:
    - rustyconover

repo:
  github: rustyconover/duckdb-crypto-extension
  ref: b6ccda3451d4fac8a2c0ae5ab2bca5216f22424c

docs:
  hello_world: |
    SELECT * from read_csv('seq 1 100 | grep 2 |');
  extended_description: |
    This extension, `crypto`, adds cryptographic hash functions and
    the ability to calculate a HMAC to DuckDB's SQL engine.
extension_star_count: 3

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

| function_name | function_type |              description               | comment |                             example                             |
|---------------|---------------|----------------------------------------|---------|-----------------------------------------------------------------|
| crypto_hash   | scalar        | Calculate the value of a hash function |         | select crypto_hash('md5', 'test');                              |
| crypto_hmac   | scalar        | Calculate a HMAC value                 |         | select crypto_hmac('sha2-256', 'secret key', 'secret message'); |



---

