---
layout: docu
redirect_from:
- /docs/sql/statements/update_extensions
title: UPDATE EXTENSIONS
---

The `UPDATE EXTENSIONS` statement allows to sychronize the local installed extension state with the repository that published a given extension.

This statement is the recommended way to keep up to date with new feature or bug fixed being rolled out by extension developers.

## Updating All Extensions

Say you want to automatically check for updates for all extensions (for the current DuckDB version and platform) currently installed in the `extension_directory`.

```sql
UPDATE EXTENSIONS;
```

This will iterate over the extensions, and inform user on which ones have been bumped.

`UPDATE EXTENSIONS` will use the information about where a given extension has been sourced, and try to fetch it only from there.

## Updating Selected Extensions

You can provide a list of extension names to be updated. This allow more fine grained control:

```sql
UPDATE EXTENSIONS (name_a, name_b, name_c);
```

## How It Works

`UPDATE EXTENSIONS` is implemented by storing, if available, the [ETag](https://en.wikipedia.org/wiki/HTTP_ETag) information, and sending a GET request conditional on the fact that the remote extension is different (using the ETag as proxy) than the local available one. This ensures that `UPDATE EXTENSIONS` on consecutive instructions (if the remote state has not changed) is rather inexpensive.

If a change is found for a given extension, DuckDB performs the following operation. For example, if `name_a` and `name_c` changed, then:

```sql
UPDATE EXTENSIONS (name_a, name_b, name_c);
```

will result in the following commands:

```sql
FORCE INSTALL name_a;
FORCE INSTALL name_c;
```