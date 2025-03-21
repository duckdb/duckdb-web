---
warning: DO NOT CHANGE THIS MANUALLY, THIS IS GENERATED BY https://github/duckdb/community-extensions repository, check README there
title: faiss
excerpt: |
  DuckDB Community Extensions
  Provides a subset of the faiss API to DuckDB

extension:
  name: faiss
  description: Provides a subset of the faiss API to DuckDB
  version: 0.9.0
  language: C++
  build: cmake
  license: MIT
  maintainers:
    - JAicewizard
    - arjenpdevries
  excluded_platforms: "wasm_mvp;wasm_eh;wasm_threads"
  requires_toolchains: "fortran;omp"
  vcpkg_url: "https://github.com/jaicewizard/vcpkg.git"
  vcpkg_commit: "4973a339118ad0e2455a7dad1348baa8c27bce16"

repo:
  github: arjenpdevries/faiss
  ref: ac09d01af7ce9711f74097012f4bff4b5275147f

docs:
  hello_world: |
    -- Generate semi-random input data and queries
    -- Note that the dimensionality of our data will be 5
    CREATE TABLE input AS SELECT i AS id, apply(generate_series(1, 5), j-> CAST(hash(i*1000+j) AS FLOAT)/18446744073709551615) AS data FROM generate_series(1, 1000) s(i);
    CREATE TABLE queries AS SELECT i AS id, apply(generate_series(1, 5), j-> CAST(hash(i*1000+j+8047329823) AS FLOAT)/18446744073709551615) AS data FROM generate_series(1, 10) s(i);
    -- Create the index and insert data into it
    CALL FAISS_CREATE('name', 5, 'IDMap,HNSW32');
    CALL FAISS_ADD((SELECT id, data FROM input), 'name');
    -- Get 10 results with uneven id
    SELECT id, UNNEST(FAISS_SEARCH_FILTER('name', 10, data, 'id%2==1', 'rowid', 'input')) FROM queries;
    -- Get 10 results with even id
    SELECT id, UNNEST(FAISS_SEARCH_FILTER('name', 10, data, 'id%2==0', 'rowid', 'input')) FROM queries;
    -- Get 10 results
    SELECT id, UNNEST(FAISS_SEARCH('name', 10, data)) FROM queries;
  extended_description: |
    The FAISS extension allows DuckDB users to store vector data in faiss, and query this data, making reliable vector search more accessible.

extension_star_count: 9
extension_star_count_pretty: 9
extension_download_count: 439
extension_download_count_pretty: 439
image: '/images/community_extensions/social_preview/preview_community_extension_faiss.png'
layout: community_extension_doc
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

|      function_name      | function_type | description | comment | example |
|-------------------------|---------------|-------------|---------|---------|
| __faiss_create_mask     | table         |             |         |         |
| faiss_add               | table         |             |         |         |
| faiss_create            | table         |             |         |         |
| faiss_create_params     | table         |             |         |         |
| faiss_destroy           | table         |             |         |         |
| faiss_load              | table         |             |         |         |
| faiss_manual_train      | table         |             |         |         |
| faiss_save              | table         |             |         |         |
| faiss_search            | scalar        |             |         |         |
| faiss_search_filter     | scalar        |             |         |         |
| faiss_search_filter_set | scalar        |             |         |         |


