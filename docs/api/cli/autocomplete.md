---
layout: docu
title: Autocomplete
---

The shell offers context-aware autocomplete of SQL queries through the [`autocomplete` extension](../../extensions/autocomplete). autocomplete is triggered by pressing `Tab`.

Multiple autocomplete suggestions can be present. You can cycle forwards through the suggestions by repeatedly pressing `Tab`, or `Shift+Tab` to cycle backwards. autocompletion can be reverted by pressing `ESC` twice.

The shell autocompletes four different groups:

* Keywords
* Table names and table functions
* Column names and scalar functions
* File names

The shell looks at the position in the SQL statement to determine which of these autocompletions to trigger. For example:

```sql
SELECT s -> student_id
```

```sql
SELECT student_id F -> FROM
```

```sql
SELECT student_id FROM g -> grades
```

```sql
SELECT student_id FROM 'd -> data/
```

```sql
SELECT student_id FROM 'data/ -> data/grades.csv
```
