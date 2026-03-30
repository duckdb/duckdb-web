---
layout: docu
redirect_from:
  - /docs/sql/statements/update_extensions
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
│ icu            │ core         │ NO_UPDATE_AVAILABLE │ v1.2.1           │ v1.2.1          │
│ autocomplete   │ core         │ NO_UPDATE_AVAILABLE │ v1.2.1           │ v1.2.1          │
│ httpfs         │ core_nightly │ NO_UPDATE_AVAILABLE │ cf3584b          │ cf3584b         │
│ json           │ core         │ NO_UPDATE_AVAILABLE │ v1.2.1           │ v1.2.1          │
│ aws            │ core_nightly │ NO_UPDATE_AVAILABLE │ d3c5013          │ d3c5013         │
└────────────────┴──────────────┴─────────────────────┴──────────────────┴─────────────────┘
```

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
