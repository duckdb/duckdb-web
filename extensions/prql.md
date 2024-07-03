---
layout: community_extension
title: prql
extension:
  name: prql
  description: Support for PRQL, the Pipelined Relational Query Language
  version: 1.0.0
  language: C++
  build: cmake
  license: MIT
  excluded_platforms: ""
  maintainers:
    - ywelsch

repo:
  github: ywelsch/duckdb-prql
  ref: 60854f0f1c90a3e90786ff353b0ac99629e26300

extension_star_count: 224
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


