---
layout: community_extension
title: evalexpr_rhai
excerpt: |
  DuckDB Community Extensions
  Evaluate the Rhai scripting language in DuckDB

extension:
  name: evalexpr_rhai
  description: Evaluate the Rhai scripting language in DuckDB
  version: 1.0.0
  language: C++
  build: cmake
  license: Apache-2.0
  maintainers:
    - rustyconover
  excluded_platforms: "windows_amd64_rtools;windows_amd64"

repo:
  github: rustyconover/duckdb-evalexpr-rhai-extension
  ref: 4acdf799b1b72d43af4c50659a2c859814140b33

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

### Added Functions

<div class="extension_functions_table"></div>

| function_name | function_type | description | comment | example |
|---------------|---------------|-------------|---------|---------|
| evalexpr_rhai | scalar        |             |         |         |



---

