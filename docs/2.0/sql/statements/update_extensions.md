---
layout: docu
redirect_from:
- /docs/sql/statements/update_extensions
- /docs/stable/sql/statements/update_extensions
- /docs/current/sql/statements/update_extensions
- /docs/lts/sql/statements/update_extensions
- /docs/preview/sql/statements/update_extensions
title: UPDATE EXTENSIONS
---

The `UPDATE EXTENSIONS` statement allows synchronizing the locally installed extension state with the repository that published a given extension.
This statement is the recommended way to keep up to date with new features or bug fixes being rolled out by extension developers.

Note that DuckDB extensions cannot be reloaded during runtime, therefore `UPDATE EXTENSIONS` does not reload the updated extensions.
To use the updated extensions, restart the process running DuckDB.

## Updating All Extensions

To update all extensions installed for the DuckDB version of your client:

```sql
UPDATE EXTENSIONS;
```

This will iterate over the extensions and return their repositories and the update result:

```text
┌────────────────┬──────────────┬─────────────────────┬──────────────────┬─────────────────┐
│ extension_name │  repository  │    update_result    │ previous_version │ current_version │
│    varchar     │   varchar    │       varchar       │     varchar      │     varchar     │
├────────────────┼──────────────┼─────────────────────┼──────────────────┼─────────────────┤
│ iceberg        │ core_nightly │ UPDATED             │ 6386ab5          │ b3ec51a         │
│ tpch           │ core         │ NO_UPDATE_AVAILABLE │ v2.0.0           │ v2.0.0          │
│ httpfs         │ core         │ NO_UPDATE_AVAILABLE │ 77392a7          │ 77392a7         │
│ spatial        │ core         │ NO_UPDATE_AVAILABLE │ 4e066c1          │ 4e066c1         │
│ aws            │ core_nightly │ NO_UPDATE_AVAILABLE │ d3c5013          │ d3c5013         │
└────────────────┴──────────────┴─────────────────────┴──────────────────┴─────────────────┘
```

Extensions that are statically linked into the DuckDB binary, such as `json`, `parquet`, and `icu` in the official DuckDB builds, are not updated by this statement.

Extensions installed from a [custom extension repository]({% link docs/2.0/extensions/extension_repositories.md %}) are not updated either: `UPDATE EXTENSIONS` skips them, and naming one in the list of extensions fails with an error. To upgrade such an extension, run `FORCE INSTALL ⟨extension_name⟩ FROM ⟨repository_name⟩;`{:.language-sql .highlight}.

## Updating Selected Extensions

For more fine-grained control, you can also provide a list of extension names to be updated:

```sql
UPDATE EXTENSIONS (name_a, name_b, name_c);
```

## How It Works

`UPDATE EXTENSIONS` is implemented by storing, if available, the [ETag](https://en.wikipedia.org/wiki/HTTP_ETag) information, and sending a GET request conditional on the fact that the remote extension is different (using the ETag as proxy) than the local available one.
This ensures that subsequent `UPDATE EXTENSIONS` calls – if the remote state has not changed – are inexpensive.

If a change is found for a given extension, DuckDB performs the following operation. For example, if `name_a` and `name_c` changed, then:

```sql
UPDATE EXTENSIONS (name_a, name_b, name_c);
```

This will result in the following commands:

```sql
FORCE INSTALL name_a;
FORCE INSTALL name_c;
```
