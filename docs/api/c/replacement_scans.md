---
layout: docu
title: C API - Replacement Scans
selected: Replacement Scans
---

The replacement scan API can be used to register a callback that is called when a table is read that does not exist in the catalog. For example, when a query such as `SELECT * FROM my_table` is executed and `my_table` does not exist, the replacement scan callback will be called with `my_table` as parameter. The replacement scan can then insert a table function with a specific parameter to replace the read of the table.

## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf"><a href="#duckdb_add_replacement_scan">duckdb_add_replacement_scan</a></span>(<span class="kt">duckdb_database</span> <span class="k">db</span>, <span class="k">duckdb_replacement_callback_t</span> <span class="k">replacement</span>, <span class="kt">void</span> *<span class="k">extra_data</span>, <span class="k">duckdb_delete_callback_t</span> <span class="k">delete_callback</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_replacement_scan_set_function_name">duckdb_replacement_scan_set_function_name</a></span>(<span class="kt">duckdb_replacement_scan_info</span> <span class="k">info</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">function_name</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_replacement_scan_add_parameter">duckdb_replacement_scan_add_parameter</a></span>(<span class="kt">duckdb_replacement_scan_info</span> <span class="k">info</span>, <span class="kt">duckdb_value</span> <span class="k">parameter</span>);
</code></pre></div></div>
### **duckdb_add_replacement_scan**
---
Add a replacement scan definition to the specified database

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_add_replacement_scan</span>(<span class="k">
</span>  <span class="kt">duckdb_database</span> <span class="k">db</span>,<span class="k">
</span>  <span class="k">duckdb_replacement_callback_t</span> <span class="k">replacement</span>,<span class="k">
</span>  <span class="kt">void</span> *<span class="k">extra_data</span>,<span class="k">
</span>  <span class="k">duckdb_delete_callback_t</span> <span class="k">delete_callback
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `db`

The database object to add the replacement scan to
* `replacement`

The replacement scan callback
* `extra_data`

Extra data that is passed back into the specified callback
* `delete_callback`

The delete callback to call on the extra data, if any

<br>

### **duckdb_replacement_scan_set_function_name**
---
Sets the replacement function name to use. If this function is called in the replacement callback,
the replacement scan is performed. If it is not called, the replacement callback is not performed.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_replacement_scan_set_function_name</span>(<span class="k">
</span>  <span class="kt">duckdb_replacement_scan_info</span> <span class="k">info</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">function_name
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `info`

The info object
* `function_name`

The function name to substitute.

<br>

### **duckdb_replacement_scan_add_parameter**
---
Adds a parameter to the replacement scan function.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_replacement_scan_add_parameter</span>(<span class="k">
</span>  <span class="kt">duckdb_replacement_scan_info</span> <span class="k">info</span>,<span class="k">
</span>  <span class="kt">duckdb_value</span> <span class="k">parameter
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `info`

The info object
* `parameter`

The parameter to add.

<br>

