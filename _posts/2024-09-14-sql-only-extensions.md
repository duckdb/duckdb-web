---
layout: post
title: "Using a SQL-Only Extension for Excel-Style Pivoting in DuckDB"
author: "Alex Monahan"
excerpt: "Now you can easily create sharable extensions using only SQL MACROs that can apply to any table and any columns. We demonstrate the power of this capability with the pivot_table extension that provides Excel-style pivoting"
---
<!-- 

The vision
    Shareable helper libraries, built entirely in SQL
    Usable across all client languages supported by DuckDB
    Now with version 1.1, DuckDB supports dynamic table names as well as dynamic column names
        so any TABLE FUNCTION can be used on any table
    A powerful way to contribute to the DuckDB community if you are a SQL expert and not a C++ expert
    Allows for direct parameterization from your host language to ensure safety
    This can scale up to significant complexity (and therefore significant community value!), as we will demonstrate with the pivot_table extension

Capabilities of the pivot_table extension
    The pivot_table extension supports advanced pivoting functionality that was previously only available in spreadsheets, dataframe libraries, or custom host language functions.
    Supports the Excel pivoting API: values, rows, columns, filters
    It accepts arbitrary combinations of these parameters and can handle as many inputs as desired
    Plus advanced options like subtotals and grand totals
    If multiple values are in use, there is an option to create a separate column per value or a separate row per value

    Why was this hard for SQL in the past? The query syntax used to handle groupings and the syntax used to handle pivots is very different, and the Excel API supports both use cases.
        If no columns parameter is supplied, then a group by should be used. 
        Otherwise, a PIVOT is required

Operate on any table with query_table

Create SQL dynamically with query 
    Since this is really just operating on strings, we can modularize this
    It is also safe since it does not allow DDL statements (CREATE, UPDATE, and DELETE are disallowed)

Do valuable dynamic work thanks to list lambdas
    One way to operate on user-specified columns

Operate on user-specified columns with the columns expression

How to create your own
    Extension template
    Cover the exact C++ syntax so that it isn't intimidating

The pivot_table example
    Maybe a diagram of the various functions in use and how they call each other?
        Maybe just a list or table instead, with a quick description
        Start with the broadest function (root function)
    



-->
