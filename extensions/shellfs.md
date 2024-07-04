---
layout: community_extension
title: shellfs
extension:
  name: shellfs
  description: Allow shell commands to be used for input and output
  version: 1.0.0
  language: C++
  build: cmake
  excluded_platforms: "wasm_mvp;wasm_eh;wasm_threads"
  license: MIT
  maintainers:
    - rustyconover

repo:
  github: rustyconover/duckdb-shellfs-extension
  ref: d01c73d211544f5f0ff62acb8263a9874f973ddd

extension_star_count: 14
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

### Added settings

|      name      |  description   | input_type | scope  |
|----------------|----------------|------------|--------|
| ignore_sigpipe | Ignore SIGPIPE | BOOLEAN    | GLOBAL |



---

