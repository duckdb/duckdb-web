---
layout: docu
title: Command Line Arguments
---

The shell offers context-aware auto-complete of SQL queries. Auto-complete is triggered by pressing `Tab`.

Multiple auto-complete suggestions can be present. You can cycle forwards through the suggestions by repeatedly pressing `Tab`, or `Shift+Tab` to cycle backwards. Auto-completion can be reverted by pressing `ESC` twice. 

The shell auto-completes four different groups:

* Keywords
* Table names & Table functions
* Column names + scalar functions
* File names

The shell looks at the position in the SQL statement to determine which of these auto-completions to trigger. For example:

```sql
SELECT s -> student_id

SELECT student_id F -> FROM

SELECT student_id FROM g -> grades

SELECT student_id FROM 'd -> data/

SELECT student_id FROM 'data/ -> data/grades.csv
```
