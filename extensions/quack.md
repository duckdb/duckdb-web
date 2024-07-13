---
layout: community_extension
title: quack
excerpt: |
  DuckDB Community Extensions
  Provides a hello world example demo

extension:
  name: quack
  description: Provides a hello world example demo
  version: 0.0.1
  language: C++
  build: cmake
  # Note that quack doesn't actually need any extra toolchains, but they are added since quack is used to test community-extensions CI
  requires_toolchains: "rust"
  license: MIT
  maintainers:
    - hannes

repo:
  github: hannes/quack
  ref: 09680a975bcf9e93b5a2f46d3eeb68792d5239c6

docs:
  hello_world: |
    SELECT quack('world');
  extended_description: |
    The quack extension is based on DuckDB's [Extension Template](https://duckdb/extension_template/), and it's a great starting point to get started building more advanced extensions.

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

|     function_name     | function_type | description | comment | example |
|-----------------------|---------------|-------------|---------|---------|
| quack                 | scalar        |             |         |         |
| quack_openssl_version | scalar        |             |         |         |



---

