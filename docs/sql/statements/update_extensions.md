---
layout: docu
title: UPDATE EXTENSIONS
---

## `UPDATE EXTENSIONS`

The `UPDATE EXTENSIONS` allows to syncronize local installed extension state with the repository that published a given extension.

`UPDATE EXTENSIONS` is implemented by storing, if available, the Etag information, and sending a GET download request conditional on the fact that the remote extension is different (using Etag as proxy) than the local available one.

This makes so that update extensions is on consecutive instructions (if no remote state has changed) somewhat inexpensive.

This statement is the reccomened way to keep up to date with new feature or bug fixed being rolled out by extension developers.

### Examples

Say you want to automatically check for updates for all extensions (for the current DuckDB version and platform) currently installed in the `extension_directory`.
```
UPDATE EXTENSIONS;
```
Will iterate over the extensions, and inform user on which ones have been bumped

Update extensions will use the information about where a given extension has been sourced, and try to fetch it only from there.

## `UPDATE EXTENSIONS (name_a, name_b, name_c)

You can provide a list of extension names to be updated. This allow more fine grained control

### Examples

```sql
INSTALL spatial;
```
Then say that a week pass by, what if some improvements (deemed to be at the same level of stability) are rolled out?

```
UPDATE EXTENSIONS (spatial);
```
Will either be equivalent to `FORCE INSTALL spatial` if changes are detected, or no change the local extension directory.
