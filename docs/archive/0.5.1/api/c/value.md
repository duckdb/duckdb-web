---
layout: docu
title: C API - Values
selected: Values
---

The value class represents a single value of any type.

## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_value">duckdb_destroy_value</a></span>(<span class="kt">duckdb_value</span> *<span class="k">value</span>);
<span class="kt">duckdb_value</span> <span class="nf"><a href="#duckdb_create_varchar">duckdb_create_varchar</a></span>(<span class="kt">const</span> <span class="kt">char</span> *<span class="k">text</span>);
<span class="kt">duckdb_value</span> <span class="nf"><a href="#duckdb_create_varchar_length">duckdb_create_varchar_length</a></span>(<span class="kt">const</span> <span class="kt">char</span> *<span class="k">text</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_value</span> <span class="nf"><a href="#duckdb_create_int64">duckdb_create_int64</a></span>(<span class="kt">int64_t</span> <span class="k">val</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_get_varchar">duckdb_get_varchar</a></span>(<span class="kt">duckdb_value</span> <span class="k">value</span>);
<span class="kt">int64_t</span> <span class="nf"><a href="#duckdb_get_int64">duckdb_get_int64</a></span>(<span class="kt">duckdb_value</span> <span class="k">value</span>);
</code></pre></div></div>
### **duckdb_destroy_value**
---
Destroys the value and de-allocates all memory allocated for that type.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_value</span>(<span class="k">
</span>  <span class="kt">duckdb_value</span> *<span class="k">value
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `value`

The value to destroy.

<br>

### **duckdb_create_varchar**
---
Creates a value from a null-terminated string

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="k">duckdb_create_varchar</span>(<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">text
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `value`

The null-terminated string
* `returns`

The value. This must be destroyed with `duckdb_destroy_value`.

<br>

### **duckdb_create_varchar_length**
---
Creates a value from a string

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="k">duckdb_create_varchar_length</span>(<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">text</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `value`

The text
* `length`

The length of the text
* `returns`

The value. This must be destroyed with `duckdb_destroy_value`.

<br>

### **duckdb_create_int64**
---
Creates a value from an int64

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_value</span> <span class="k">duckdb_create_int64</span>(<span class="k">
</span>  <span class="kt">int64_t</span> <span class="k">val
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `value`

The bigint value
* `returns`

The value. This must be destroyed with `duckdb_destroy_value`.

<br>

### **duckdb_get_varchar**
---
Obtains a string representation of the given value.
The result must be destroyed with `duckdb_free`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_get_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_value</span> <span class="k">value
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `value`

The value
* `returns`

The string value. This must be destroyed with `duckdb_free`.

<br>

### **duckdb_get_int64**
---
Obtains an int64 of the given value.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int64_t</span> <span class="k">duckdb_get_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_value</span> <span class="k">value
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `value`

The value
* `returns`

The int64 value, or 0 if no conversion is possible

<br>

