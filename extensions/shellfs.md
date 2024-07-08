---
layout: community_extension
title: shellfs
excerpt: |
  DuckDB Community Extensions
  Allow shell commands to be used for input and output

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

docs:
  hello_world: |
    SELECT * FROM read_csv('seq 1 100 | grep 2 |');
  extended_description: |
    The `shellfs` extension for DuckDB enables the use of Unix pipes for input and output.
    By appending a pipe character `|` to a filename, DuckDB will treat it as a series of commands
    to execute and capture the output. Conversely, if you prefix a filename with `|`, DuckDB will
    treat it as an output pipe.

extension_star_count:  34

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

### Added Settings

<div class="extension_settings_table"></div>

|      name      |  description   | input_type | scope  |
|----------------|----------------|------------|--------|
| ignore_sigpipe | Ignore SIGPIPE | BOOLEAN    | GLOBAL |



---

