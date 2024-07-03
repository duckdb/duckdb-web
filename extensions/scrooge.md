---
layout: community_extension
title: scrooge
extension:
  name: scrooge
  description: Provides functionality for financial data-analysis
  version: 0.0.1
  language: C++
  build: cmake
  license: MIT
  maintainers:
    - pdet

repo:
  github: pdet/Scrooge-McDuck
  ref: 9520aeba138a6bb43f766ed4f78accac026bfae0

extension_star_count: 111
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

|   function_name    | function_type | description | comment | example |
|--------------------|---------------|-------------|---------|---------|
| first_s            | aggregate     |             |         |         |
| last_s             | aggregate     |             |         |         |
| portfolio_frontier | table         |             |         |         |
| read_eth           | table         |             |         |         |
| sma                | aggregate     |             |         |         |
| timebucket         | scalar        |             |         |         |
| volatility         | aggregate     |             |         |         |
| yahoo_finance      | table         |             |         |         |

### Added settings

|     name     |            description             | input_type | scope  |
|--------------|------------------------------------|------------|--------|
| eth_node_url | URL of Ethereum node to be queried | VARCHAR    | GLOBAL |


