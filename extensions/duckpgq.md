---
layout: community_extension
title: duckpgq
excerpt: |
  DuckDB Community Extensions
  Extension that adds support for SQL/PGQ and graph algorithms

extension:
  name: duckpgq
  description: Extension that adds support for SQL/PGQ and graph algorithms
  version: 0.0.1
  language: C++
  build: cmake
  license: MIT
  maintainers:
    - Dtenwolde

repo:
  github: cwida/duckpgq-extension
  ref: 6c06589fb8fe3293bf3b31f5d8e89177504edf5f

docs:
  hello_world: |
    CREATE TABLE Person as select * from 'https://gist.githubusercontent.com/Dtenwolde/2b02aebbed3c9638a06fda8ee0088a36/raw/8c4dc551f7344b12eaff2d1438c9da08649d00ec/person-sf0.003.csv';
    CREATE TABLE Person_knows_person as select * from 'https://gist.githubusercontent.com/Dtenwolde/81c32c9002d4059c2c3073dbca155275/raw/8b440e810a48dcaa08c07086e493ec0e2ec6b3cb/person_knows_person-sf0.003.csv';

    CREATE PROPERTY GRAPH snb
      VERTEX sABLES (
        Person
      )
    EDGE TABLES (
      Person_knows_person 	SOURCE KEY (Person1Id) REFERENCES Person (id)
       DESTINATION KEY (Person2Id) REFERENCES Person (id)
       LABEL Knows
    );

    FROM GRAPH_TABLE (snb
      MATCH (a:Person)-[k:knows]->(b:Person)
      COLUMNS (a.id, b.id)
    )
    LIMIT 1;

    from local_clustering_coefficient(snb, person, knows);

    DROP PROPERTY GRAPH snb; 

  extended_description: |
    The DuckPGQ extension supports the SQL/PGQ syntax part of the official SQL:2023 standard developed by ISO. 
    Specifically, it introduces visual graph pattern matching and more concise syntax for path-finding.
    The extension is an ongoing research project and a work in progress.

extension_star_count: 33

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

|        function_name         | function_type | description | comment | example |
|------------------------------|---------------|-------------|---------|---------|
| cheapest_path_length         | scalar        |             |         |         |
| create_csr_edge              | scalar        |             |         |         |
| create_csr_vertex            | scalar        |             |         |         |
| create_property_graph        | table         |             |         |         |
| csr_get_w_type               | scalar        |             |         |         |
| delete_csr                   | scalar        |             |         |         |
| drop_property_graph          | table         |             |         |         |
| duckpgq                      | scalar        |             |         |         |
| duckpgq_match                | table         |             |         |         |
| get_csr_e                    | table         |             |         |         |
| get_csr_ptr                  | table         |             |         |         |
| get_csr_v                    | table         |             |         |         |
| get_csr_w                    | table         |             |         |         |
| get_pg_ecolnames             | table         |             |         |         |
| get_pg_etablenames           | table         |             |         |         |
| get_pg_vcolnames             | table         |             |         |         |
| get_pg_vtablenames           | table         |             |         |         |
| iterativelength              | scalar        |             |         |         |
| iterativelength2             | scalar        |             |         |         |
| iterativelengthbidirectional | scalar        |             |         |         |
| local_clustering_coefficient | table         |             |         |         |
| local_clustering_coefficient | scalar        |             |         |         |
| reachability                 | scalar        |             |         |         |
| shortestpath                 | scalar        |             |         |         |



---

