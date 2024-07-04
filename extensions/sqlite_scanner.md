---
layout: community_extension
title: sqlite_scanner
extension:
  name: sqlite_scanner
  description: Provides a SQLite scanner
  version: 0.0.1
  language: C++
  build: cmake
  license: MIT
  maintainers:
    - Mytherin

repo:
  github: duckdb/sqlite_scanner
  ref: ecdb82d436b7eb6e4d0e956401d1c7ed3d63e9e0

extension_star_count: 190
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
| sqlite_attach | table         |             |         |         |
| sqlite_scan   | table         |             |         |         |

### Added settings

|        name        |                description                 | input_type | scope  |
|--------------------|--------------------------------------------|------------|--------|
| sqlite_all_varchar | Load all SQLite columns as VARCHAR columns | BOOLEAN    | GLOBAL |



---

