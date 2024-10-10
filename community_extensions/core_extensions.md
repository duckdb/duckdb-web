---
layout: community_extension_doc
title: Core Extensions
---

DuckDB's [Extension mechanism](https://duckdb.org/docs/extensions/overview) allows for easy extending of DuckDB functionality. Because ducks
are not averse to a little [dog food](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) once in a while, a significant part of DuckDB's 
core functionality is provided through this extension mechanism. These extension live in the `core` repository. This 
repository is the default extension repository meaning that extensions can be loaded either by specifically specifying the `core` repository:

```sql
INSTALL json FROM core;
LOAD json
```

or by simply omitting the repository altogether:

```sql
INSTALL json;
LOAD json
```

For an extensive list and documentation of all core DuckDB extensions check out the [main DuckDB docs](https://duckdb.org/docs/extensions/core_extensions.html).