---
layout: default
title: Timestamp Functions
selected: Documentation/Functions/Timestamp Functions
expanded: Functions
---
This section describes functions and operators for examining and manipulating timestamp values.

| Function | Description | Example | Result |
|:---|:---|:---|:---|
| age(*timestamp*, *timestamp*) | Subtract arguments, resulting in the time difference between the two timestamps | age(TIMESTAMP '2001-04-10', TIMESTAMP '1992-09-20') | 8 years 6 mons 20 days |
| age(*timestamp*) | Subtract from current_date | age(TIMESTAMP '1992-09-20') | 26 years 9 mons 9 days |
