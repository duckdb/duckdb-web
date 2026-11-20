---
layout: post
title: "The 6th normal form using UNPIVOT and VARIANT"
authors:
  - Roland Bouman
thumb: /images/blog/thumbs/6th-normal-form.svg
image: /images/blog/thumbs/6th-normal-form.png
excerpt: "Transform any tabular data set to the 6th normal form using UNPIVOT and VARIANT."
tag: sql
---

NOTE: this is in a  "solution looking for a problem" stage.
The idea is to show off a few things using DuckDB's modern SQL dialect
- UNPIVOT
- PIVOT
- COLUMNS star expression
- VARIANT data type

What it does is: 
1) turn an arbitrary relational dataset into a Entity-Attribute-Value format using UNPIVOT.
   VARIANT is useful here to allow every column from the original relational result to be projected into a generic value column
2) pivot the unpivoted data again into a relational format.
   The neat thing here is that we can truly dynamically (using a query) select the columns.
   This is something that is hithertoo impossible in plain DuckDB: COLUMNS can select from a static list, but not from a subquery, while PIVOT allows a subquery in the ON-clause.

possible real world use cases where this might make sense:
- ingesting a data set that is prone to schema drift. 
  of course, a schema where everything can drift is not a schema at all; 
  what this allows is drift of the data type, not of the column identity
- anchor modeling uses 6NF storage structures. It feels as if the unpivoting step could help solve part of this.
- ...?   

~~~sql
with data as (
    select row_number() over () as row_id
    ,      *
    from   promotion
)
, unpivoted as (
    unpivot data 
    on columns( lambda x, i: i > 1 )::variant
    into name col_name
        value col_value
)
pivot unpivoted
on col_name -- IN ( select * from (values('column1', 'column2')) )
using first( col_value )
group by row_id
;
~~~