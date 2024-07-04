---
layout: community_extension
title: lindel
extension:
  name: lindel
  description: Linearization/Delinearization, Z-Order, Hilbert and Morton Curves
  version: 1.0.0
  language: C++
  build: cmake
  license: Apache-2.0
  maintainers:
    - rustyconover

repo:
  github: rustyconover/duckdb-lindel-extension
  ref: 76f5bc78e8bfd1a7953c8cc4c284209b65626216

extension_star_count: 2
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

| function_name  | function_type | description | comment | example |
|----------------|---------------|-------------|---------|---------|
| hilbert_decode | scalar        |             |         |         |
| hilbert_encode | scalar        |             |         |         |
| morton_decode  | scalar        |             |         |         |
| morton_encode  | scalar        |             |         |         |



---

