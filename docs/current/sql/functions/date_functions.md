---
layout: default
title: Date Functions
selected: Documentation/Functions/Date Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating date values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| date_part(*part*, *date*) | Get subfield (equivalent to *extract*) | date_part('year', DATE '1992-09-20') | 1992 |
| extract(*part* from *date*) | Get subfield from a date | extract('year' FROM DATE '1992-09-20') | 1992 |
