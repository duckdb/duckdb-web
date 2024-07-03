---
layout: community_extension
title: crypto
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

extension_star_count: 1
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

### Added functions

| function_name | function_type | description | comment | example |
|---------------|---------------|-------------|---------|---------|
| crypto_hash   | scalar        |             |         |         |
| crypto_hmac   | scalar        |             |         |         |


