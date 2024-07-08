---
layout: community_extension
title: lindel
excerpt: |
  DuckDB Community Extensions
  Linearization/Delinearization, Z-Order, Hilbert and Morton Curves

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

docs:
  hello_world: |
    SELECT hilbert_encode([1, 2, 3]::tinyint[3]);
  extended_description: |
    This `lindel` extension adds functions for the linearization and
    delinearization of numeric arrays in DuckDB. It allows you to order
    multi-dimensional data using space-filling curves.

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

| function_name  | function_type |                           description                           | comment |                           example                           |
|----------------|---------------|-----------------------------------------------------------------|---------|-------------------------------------------------------------|
| hilbert_encode | scalar        | Encode an array of values using the Hilbert space filling curve |         | select hilbert_encode([43, 3]::integer[2]);                 |
| hilbert_decode | scalar        | Decode a Hilbert encoded set of values                          |         | select hilbert_decode(7::uint16, 2, false, true) as values; |
| morton_encode  | scalar        | Encode an array of values using Morton encoding                 |         | select morton_encode([43, 3]::integer[2]);                  |
| morton_decode  | scalar        | Decode an array of values using Morton encoding                 |         | select morton_decode(7::uint16, 2, false, true) as values;  |



---

