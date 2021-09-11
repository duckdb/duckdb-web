---
layout: docu
title: C API - Complete API
selected: API Reference
---

## **API Reference**
### **Open/Connect**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_open">duckdb_open</a></span>(<span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>, <span class="kt">duckdb_database</span> *<span class="k">out_database</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_open_ext">duckdb_open_ext</a></span>(<span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>, <span class="kt">duckdb_database</span> *<span class="k">out_database</span>, <span class="kt">duckdb_config</span> <span class="k">config</span>, <span class="kt">char</span> **<span class="k">out_error</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_close">duckdb_close</a></span>(<span class="kt">duckdb_database</span> *<span class="k">database</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_connect">duckdb_connect</a></span>(<span class="kt">duckdb_database</span> <span class="k">database</span>, <span class="kt">duckdb_connection</span> *<span class="k">out_connection</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_disconnect">duckdb_disconnect</a></span>(<span class="kt">duckdb_connection</span> *<span class="k">connection</span>);
</code></pre></div></div>
### **Configuration**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_create_config">duckdb_create_config</a></span>(<span class="kt">duckdb_config</span> *<span class="k">out_config</span>);
<span class="kt">size_t</span> <span class="nf"><a href="#duckdb_config_count">duckdb_config_count</a></span>();
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_get_config_flag">duckdb_get_config_flag</a></span>(<span class="kt">size_t</span> <span class="k">index</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="k">out_name</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="k">out_description</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_set_config">duckdb_set_config</a></span>(<span class="kt">duckdb_config</span> <span class="k">config</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">name</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">option</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_config">duckdb_destroy_config</a></span>(<span class="kt">duckdb_config</span> *<span class="k">config</span>);
</code></pre></div></div>
### **Query Execution**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_query">duckdb_query</a></span>(<span class="kt">duckdb_connection</span> <span class="k">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>, <span class="kt">duckdb_result</span> *<span class="k">out_result</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_result">duckdb_destroy_result</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_column_name">duckdb_column_name</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_column_type">duckdb_column_type</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_column_count">duckdb_column_count</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_row_count">duckdb_row_count</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_rows_changed">duckdb_rows_changed</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">void</span> *<span class="nf"><a href="#duckdb_column_data">duckdb_column_data</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">bool</span> *<span class="nf"><a href="#duckdb_nullmask_data">duckdb_nullmask_data</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_result_error">duckdb_result_error</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
</code></pre></div></div>
### **Result Functions**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nf"><a href="#duckdb_value_boolean">duckdb_value_boolean</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int8_t</span> <span class="nf"><a href="#duckdb_value_int8">duckdb_value_int8</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int16_t</span> <span class="nf"><a href="#duckdb_value_int16">duckdb_value_int16</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int32_t</span> <span class="nf"><a href="#duckdb_value_int32">duckdb_value_int32</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int64_t</span> <span class="nf"><a href="#duckdb_value_int64">duckdb_value_int64</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_hugeint</span> <span class="nf"><a href="#duckdb_value_hugeint">duckdb_value_hugeint</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint8_t</span> <span class="nf"><a href="#duckdb_value_uint8">duckdb_value_uint8</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint16_t</span> <span class="nf"><a href="#duckdb_value_uint16">duckdb_value_uint16</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint32_t</span> <span class="nf"><a href="#duckdb_value_uint32">duckdb_value_uint32</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint64_t</span> <span class="nf"><a href="#duckdb_value_uint64">duckdb_value_uint64</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">float</span> <span class="nf"><a href="#duckdb_value_float">duckdb_value_float</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">double</span> <span class="nf"><a href="#duckdb_value_double">duckdb_value_double</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_date</span> <span class="nf"><a href="#duckdb_value_date">duckdb_value_date</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_time</span> <span class="nf"><a href="#duckdb_value_time">duckdb_value_time</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_timestamp</span> <span class="nf"><a href="#duckdb_value_timestamp">duckdb_value_timestamp</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_interval</span> <span class="nf"><a href="#duckdb_value_interval">duckdb_value_interval</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_value_varchar">duckdb_value_varchar</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_value_varchar_internal">duckdb_value_varchar_internal</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_blob</span> <span class="nf"><a href="#duckdb_value_blob">duckdb_value_blob</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">bool</span> <span class="nf"><a href="#duckdb_value_is_null">duckdb_value_is_null</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
</code></pre></div></div>
### **Helpers**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nf"><a href="#duckdb_malloc">duckdb_malloc</a></span>(<span class="kt">size_t</span> <span class="k">size</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_free">duckdb_free</a></span>(<span class="kt">void</span> *<span class="k">ptr</span>);
</code></pre></div></div>
### **Date/Time/Timestamp Helpers**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="nf"><a href="#duckdb_from_date">duckdb_from_date</a></span>(<span class="kt">duckdb_date</span> <span class="k">date</span>);
<span class="kt">duckdb_date</span> <span class="nf"><a href="#duckdb_to_date">duckdb_to_date</a></span>(<span class="kt">duckdb_date_struct</span> <span class="k">date</span>);
<span class="kt">duckdb_time_struct</span> <span class="nf"><a href="#duckdb_from_time">duckdb_from_time</a></span>(<span class="kt">duckdb_time</span> <span class="k">time</span>);
<span class="kt">duckdb_time</span> <span class="nf"><a href="#duckdb_to_time">duckdb_to_time</a></span>(<span class="kt">duckdb_time_struct</span> <span class="k">time</span>);
<span class="kt">duckdb_timestamp_struct</span> <span class="nf"><a href="#duckdb_from_timestamp">duckdb_from_timestamp</a></span>(<span class="kt">duckdb_timestamp</span> <span class="k">ts</span>);
<span class="kt">duckdb_timestamp</span> <span class="nf"><a href="#duckdb_to_timestamp">duckdb_to_timestamp</a></span>(<span class="kt">duckdb_timestamp_struct</span> <span class="k">ts</span>);
</code></pre></div></div>
### **Hugeint Helpers**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nf"><a href="#duckdb_hugeint_to_double">duckdb_hugeint_to_double</a></span>(<span class="kt">duckdb_hugeint</span> <span class="k">val</span>);
<span class="kt">duckdb_hugeint</span> <span class="nf"><a href="#duckdb_double_to_hugeint">duckdb_double_to_hugeint</a></span>(<span class="kt">double</span> <span class="k">val</span>);
</code></pre></div></div>
### **Prepared Statements**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_prepare">duckdb_prepare</a></span>(<span class="kt">duckdb_connection</span> <span class="k">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>, <span class="kt">duckdb_prepared_statement</span> *<span class="k">out_prepared_statement</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_prepare">duckdb_destroy_prepare</a></span>(<span class="kt">duckdb_prepared_statement</span> *<span class="k">prepared_statement</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_prepare_error">duckdb_prepare_error</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_nparams">duckdb_nparams</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_param_type">duckdb_param_type</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_boolean">duckdb_bind_boolean</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">bool</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int8">duckdb_bind_int8</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int8_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int16">duckdb_bind_int16</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int16_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int32">duckdb_bind_int32</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int32_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int64">duckdb_bind_int64</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int64_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_hugeint">duckdb_bind_hugeint</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_hugeint</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint8">duckdb_bind_uint8</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint8_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint16">duckdb_bind_uint16</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint16_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint32">duckdb_bind_uint32</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint32_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint64">duckdb_bind_uint64</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint64_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_float">duckdb_bind_float</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">float</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_double">duckdb_bind_double</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">double</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_date">duckdb_bind_date</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_date</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_time">duckdb_bind_time</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_time</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_timestamp">duckdb_bind_timestamp</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_timestamp</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_interval">duckdb_bind_interval</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_interval</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_varchar">duckdb_bind_varchar</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_varchar_length">duckdb_bind_varchar_length</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_blob">duckdb_bind_blob</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">const</span> <span class="kt">void</span> *<span class="k">data</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_null">duckdb_bind_null</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_execute_prepared">duckdb_execute_prepared</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">duckdb_result</span> *<span class="k">out_result</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_execute_prepared_arrow">duckdb_execute_prepared_arrow</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">duckdb_arrow</span> *<span class="k">out_result</span>);
</code></pre></div></div>
### **Appender**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_appender_create">duckdb_appender_create</a></span>(<span class="kt">duckdb_connection</span> <span class="k">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">schema</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">table</span>, <span class="kt">duckdb_appender</span> *<span class="k">out_appender</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_appender_error">duckdb_appender_error</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_appender_flush">duckdb_appender_flush</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_appender_close">duckdb_appender_close</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_appender_destroy">duckdb_appender_destroy</a></span>(<span class="kt">duckdb_appender</span> *<span class="k">appender</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_appender_begin_row">duckdb_appender_begin_row</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_appender_end_row">duckdb_appender_end_row</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_bool">duckdb_append_bool</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">bool</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_int8">duckdb_append_int8</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">int8_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_int16">duckdb_append_int16</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">int16_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_int32">duckdb_append_int32</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">int32_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_int64">duckdb_append_int64</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">int64_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_hugeint">duckdb_append_hugeint</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">duckdb_hugeint</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_uint8">duckdb_append_uint8</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">uint8_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_uint16">duckdb_append_uint16</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">uint16_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_uint32">duckdb_append_uint32</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">uint32_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_uint64">duckdb_append_uint64</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">uint64_t</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_float">duckdb_append_float</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">float</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_double">duckdb_append_double</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">double</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_date">duckdb_append_date</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">duckdb_date</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_time">duckdb_append_time</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">duckdb_time</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_timestamp">duckdb_append_timestamp</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">duckdb_timestamp</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_interval">duckdb_append_interval</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">duckdb_interval</span> <span class="k">value</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_varchar">duckdb_append_varchar</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_varchar_length">duckdb_append_varchar_length</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_blob">duckdb_append_blob</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>, <span class="kt">const</span> <span class="kt">void</span> *<span class="k">data</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_append_null">duckdb_append_null</a></span>(<span class="kt">duckdb_appender</span> <span class="k">appender</span>);
</code></pre></div></div>
### **Arrow Interface**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_query_arrow">duckdb_query_arrow</a></span>(<span class="kt">duckdb_connection</span> <span class="k">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>, <span class="kt">duckdb_arrow</span> *<span class="k">out_result</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_query_arrow_schema">duckdb_query_arrow_schema</a></span>(<span class="kt">duckdb_arrow</span> <span class="k">result</span>, <span class="kt">duckdb_arrow_schema</span> *<span class="k">out_schema</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_query_arrow_array">duckdb_query_arrow_array</a></span>(<span class="kt">duckdb_arrow</span> <span class="k">result</span>, <span class="kt">duckdb_arrow_array</span> *<span class="k">out_array</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_arrow_column_count">duckdb_arrow_column_count</a></span>(<span class="kt">duckdb_arrow</span> <span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_arrow_row_count">duckdb_arrow_row_count</a></span>(<span class="kt">duckdb_arrow</span> <span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_arrow_rows_changed">duckdb_arrow_rows_changed</a></span>(<span class="kt">duckdb_arrow</span> <span class="k">result</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_query_arrow_error">duckdb_query_arrow_error</a></span>(<span class="kt">duckdb_arrow</span> <span class="k">result</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_arrow">duckdb_destroy_arrow</a></span>(<span class="kt">duckdb_arrow</span> *<span class="k">result</span>);
</code></pre></div></div>
### **duckdb_open**
---
Creates a new database or opens an existing database file stored at the the given path.
If no path is given a new in-memory database is created instead.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_open</span>(<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>,<span class="k">
</span>  <span class="kt">duckdb_database</span> *<span class="k">out_database
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `path`

Path to the database file on disk, or `nullptr` or `:memory:` to open an in-memory database.
* `out_database`

The result database object.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_open_ext**
---
Extended version of duckdb_open. Creates a new database or opens an existing database file stored at the the given path.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_open_ext</span>(<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">path</span>,<span class="k">
</span>  <span class="kt">duckdb_database</span> *<span class="k">out_database</span>,<span class="k">
</span>  <span class="kt">duckdb_config</span> <span class="k">config</span>,<span class="k">
</span>  <span class="kt">char</span> **<span class="k">out_error
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `path`

Path to the database file on disk, or `nullptr` or `:memory:` to open an in-memory database.
* `out_database`

The result database object.
* `config`

(Optional) configuration used to start up the database system.
* `out_error`

If set and the function returns DuckDBError, this will contain the reason why the start-up failed.
Note that the error must be freed using `duckdb_free`.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_close**
---
Closes the specified database and de-allocates all memory allocated for that database.
This should be called after you are done with any database allocated through `duckdb_open`.
Note that failing to call `duckdb_close` (in case of e.g. a program crash) will not cause data corruption.
Still it is recommended to always correctly close a database object after you are done with it.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_close</span>(<span class="k">
</span>  <span class="kt">duckdb_database</span> *<span class="k">database
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `database`

The database object to shut down.

<br>

### **duckdb_connect**
---
Opens a connection to a database. Connections are required to query the database, and store transactional state
associated with the connection.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_connect</span>(<span class="k">
</span>  <span class="kt">duckdb_database</span> <span class="k">database</span>,<span class="k">
</span>  <span class="kt">duckdb_connection</span> *<span class="k">out_connection
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `database`

The database file to connect to.
* `out_connection`

The result connection object.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_disconnect**
---
Closes the specified connection and de-allocates all memory allocated for that connection.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_disconnect</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> *<span class="k">connection
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `connection`

The connection to close.

<br>

### **duckdb_create_config**
---
Initializes an empty configuration object that can be used to provide start-up options for the DuckDB instance
through `duckdb_open_ext`.

This will always succeed unless there is a malloc failure.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_create_config</span>(<span class="k">
</span>  <span class="kt">duckdb_config</span> *<span class="k">out_config
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `out_config`

The result configuration object.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_config_count**
---
This returns the total amount of configuration options available for usage with `duckdb_get_config_flag`.

This should not be called in a loop as it internally loops over all the options.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">size_t</span> <span class="k">duckdb_config_count</span>(<span class="k">
</span>  <span class="k">
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The amount of config options available.

<br>

### **duckdb_get_config_flag**
---
Obtains a human-readable name and description of a specific configuration option. This can be used to e.g.
display configuration options. This will succeed unless `index` is out of range (i.e. `>= duckdb_config_count`).

The result name or description MUST NOT be freed.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_get_config_flag</span>(<span class="k">
</span>  <span class="kt">size_t</span> <span class="k">index</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="k">out_name</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="k">out_description
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `index`

The index of the configuration option (between 0 and `duckdb_config_count`)
* `out_name`

A name of the configuration flag.
* `out_description`

A description of the configuration flag.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_set_config**
---
Sets the specified option for the specified configuration. The configuration option is indicated by name.
To obtain a list of config options, see `duckdb_get_config_flag`.

In the source code, configuration options are defined in `config.cpp`.

This can fail if either the name is invalid, or if the value provided for the option is invalid.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_set_config</span>(<span class="k">
</span>  <span class="kt">duckdb_config</span> <span class="k">config</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">name</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">option
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `duckdb_config`

The configuration object to set the option on.
* `name`

The name of the configuration flag to set.
* `option`

The value to set the configuration flag to.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_destroy_config**
---
Destroys the specified configuration option and de-allocates all memory allocated for the object.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_config</span>(<span class="k">
</span>  <span class="kt">duckdb_config</span> *<span class="k">config
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `config`

The configuration object to destroy.

<br>

### **duckdb_query**
---
Executes a SQL query within a connection and stores the full (materialized) result in the out_result pointer.
If the query fails to execute, DuckDBError is returned and the error message can be retrieved by calling
`duckdb_result_error`.

Note that after running `duckdb_query`, `duckdb_destroy_result` must be called on the result object even if the
query fails, otherwise the error stored within the result will not be freed correctly.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_query</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> <span class="k">connection</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>,<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `connection`

The connection to perform the query in.
* `query`

The SQL query to run.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_destroy_result**
---
Closes the result and de-allocates all memory allocated for that connection.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_result</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result to destroy.

<br>

### **duckdb_column_name**
---
Returns the column name of the specified column. The result should not need be freed; the column names will
automatically be destroyed when the result is destroyed.

Returns `NULL` if the column is out of range.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_column_name</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object to fetch the column name from.
* `col`

The column index.
* `returns`

The column name of the specified column.

<br>

### **duckdb_column_type**
---
Returns the column type of the specified column.

Returns `DUCKDB_TYPE_INVALID` if the column is out of range.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_column_type</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object to fetch the column type from.
* `col`

The column index.
* `returns`

The column type of the specified column.

<br>

### **duckdb_column_count**
---
Returns the number of columns present in a the result object.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_column_count</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object.
* `returns`

The number of columns present in the result object.

<br>

### **duckdb_row_count**
---
Returns the number of rows present in a the result object.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_row_count</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object.
* `returns`

The number of rows present in the result object.

<br>

### **duckdb_rows_changed**
---
Returns the number of rows changed by the query stored in the result. This is relevant only for INSERT/UPDATE/DELETE
queries. For other queries the rows_changed will be 0.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_rows_changed</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object.
* `returns`

The number of rows changed.

<br>

### **duckdb_column_data**
---
Returns the data of a specific column of a result in columnar format. This is the fastest way of accessing data in a
query result, as no conversion or type checking must be performed (outside of the original switch). If performance
is a concern, it is recommended to use this API over the `duckdb_value` functions.

The function returns a dense array which contains the result data. The exact type stored in the array depends on the
corresponding duckdb_type (as provided by `duckdb_column_type`). For the exact type by which the data should be
accessed, see the comments in [the types section](types) or the `DUCKDB_TYPE` enum.

For example, for a column of type `DUCKDB_TYPE_INTEGER`, rows can be accessed in the following manner:
```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
printf("Data for row %d: %d\n", row, data[row]);
```

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="k">duckdb_column_data</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object to fetch the column data from.
* `col`

The column index.
* `returns`

The column data of the specified column.

<br>

### **duckdb_nullmask_data**
---
Returns the nullmask of a specific column of a result in columnar format. The nullmask indicates for every row
whether or not the corresponding row is `NULL`. If a row is `NULL`, the values present in the array provided
by `duckdb_column_data` are undefined.

```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
bool *nullmask = duckdb_nullmask_data(&result, 0);
if (nullmask[row]) {
printf("Data for row %d: NULL\n", row);
} else {
printf("Data for row %d: %d\n", row, data[row]);
}
```

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> *<span class="k">duckdb_nullmask_data</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object to fetch the nullmask from.
* `col`

The column index.
* `returns`

The nullmask of the specified column.

<br>

### **duckdb_result_error**
---
Returns the error message contained within the result. The error is only set if `duckdb_query` returns `DuckDBError`.

The result of this function must not be freed. It will be cleaned up when `duckdb_destroy_result` is called.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_result_error</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object to fetch the nullmask from.
* `returns`

The error of the result.

<br>

### **duckdb_value_boolean**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_value_boolean</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The boolean value at the specified location, or false if the value cannot be converted.

<br>

### **duckdb_value_int8**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int8_t</span> <span class="k">duckdb_value_int8</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int8_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_int16**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int16_t</span> <span class="k">duckdb_value_int16</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int16_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_int32**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int32_t</span> <span class="k">duckdb_value_int32</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int32_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_int64**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int64_t</span> <span class="k">duckdb_value_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int64_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_hugeint**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="k">duckdb_value_hugeint</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_hugeint value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint8**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="k">duckdb_value_uint8</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint8_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint16**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint16_t</span> <span class="k">duckdb_value_uint16</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint16_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint32**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint32_t</span> <span class="k">duckdb_value_uint32</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint32_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint64**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> <span class="k">duckdb_value_uint64</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint64_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_float**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">float</span> <span class="k">duckdb_value_float</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The float value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_double**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_value_double</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The double value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_date**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="k">duckdb_value_date</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_date value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_time**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="k">duckdb_value_time</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_time value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_timestamp**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="k">duckdb_value_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_timestamp value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_interval**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_interval</span> <span class="k">duckdb_value_interval</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_interval value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_varchar**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_value_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The char* value at the specified location, or nullptr if the value cannot be converted.
The result must be freed with `duckdb_free`.

<br>

### **duckdb_value_varchar_internal**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_value_varchar_internal</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The char* value at the specified location. ONLY works on VARCHAR columns and does not auto-cast.
If the column is NOT a VARCHAR column this function will return NULL.

The result must NOT be freed.

<br>

### **duckdb_value_blob**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_blob</span> <span class="k">duckdb_value_blob</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_blob value at the specified location. Returns a blob with blob.data set to nullptr if the
value cannot be converted. The resulting "blob.data" must be freed with `duckdb_free.`

<br>

### **duckdb_value_is_null**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_value_is_null</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

Returns true if the value at the specified index is NULL, and false otherwise.

<br>

### **duckdb_malloc**
---
Allocate `size` bytes of memory using the duckdb internal malloc function. Any memory allocated in this manner
should be freed using `duckdb_free`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="k">duckdb_malloc</span>(<span class="k">
</span>  <span class="kt">size_t</span> <span class="k">size
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `size`

The number of bytes to allocate.
* `returns`

A pointer to the allocated memory region.

<br>

### **duckdb_free**
---
Free a value returned from `duckdb_malloc`, `duckdb_value_varchar` or `duckdb_value_blob`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_free</span>(<span class="k">
</span>  <span class="kt">void</span> *<span class="k">ptr
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `ptr`

The memory region to de-allocate.

<br>

### **duckdb_from_date**
---
Decompose a `duckdb_date` object into year, month and date (stored as `duckdb_date_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="k">duckdb_from_date</span>(<span class="k">
</span>  <span class="kt">duckdb_date</span> <span class="k">date
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `date`

The date object, as obtained from a `DUCKDB_TYPE_DATE` column.
* `returns`

The `duckdb_date_struct` with the decomposed elements.

<br>

### **duckdb_to_date**
---
Re-compose a `duckdb_date` from year, month and date (`duckdb_date_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="k">duckdb_to_date</span>(<span class="k">
</span>  <span class="kt">duckdb_date_struct</span> <span class="k">date
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `date`

The year, month and date stored in a `duckdb_date_struct`.
* `returns`

The `duckdb_date` element.

<br>

### **duckdb_from_time**
---
Decompose a `duckdb_time` object into hour, minute, second and microsecond (stored as `duckdb_time_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_struct</span> <span class="k">duckdb_from_time</span>(<span class="k">
</span>  <span class="kt">duckdb_time</span> <span class="k">time
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `time`

The time object, as obtained from a `DUCKDB_TYPE_TIME` column.
* `returns`

The `duckdb_time_struct` with the decomposed elements.

<br>

### **duckdb_to_time**
---
Re-compose a `duckdb_time` from hour, minute, second and microsecond (`duckdb_time_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="k">duckdb_to_time</span>(<span class="k">
</span>  <span class="kt">duckdb_time_struct</span> <span class="k">time
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `time`

The hour, minute, second and microsecond in a `duckdb_time_struct`.
* `returns`

The `duckdb_time` element.

<br>

### **duckdb_from_timestamp**
---
Decompose a `duckdb_timestamp` object into a `duckdb_timestamp_struct`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp_struct</span> <span class="k">duckdb_from_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_timestamp</span> <span class="k">ts
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `ts`

The ts object, as obtained from a `DUCKDB_TYPE_TIMESTAMP` column.
* `returns`

The `duckdb_timestamp_struct` with the decomposed elements.

<br>

### **duckdb_to_timestamp**
---
Re-compose a `duckdb_timestamp` from a duckdb_timestamp_struct.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="k">duckdb_to_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_timestamp_struct</span> <span class="k">ts
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `ts`

The de-composed elements in a `duckdb_timestamp_struct`.
* `returns`

The `duckdb_timestamp` element.

<br>

### **duckdb_hugeint_to_double**
---
Converts a duckdb_hugeint object (as obtained from a `DUCKDB_TYPE_HUGEINT` column) into a double.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_hugeint_to_double</span>(<span class="k">
</span>  <span class="kt">duckdb_hugeint</span> <span class="k">val
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `val`

The hugeint value.
* `returns`

The converted `double` element.

<br>

### **duckdb_double_to_hugeint**
---
Converts a double value to a duckdb_hugeint object.

If the conversion fails because the double value is too big the result will be 0.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="k">duckdb_double_to_hugeint</span>(<span class="k">
</span>  <span class="kt">double</span> <span class="k">val
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `val`

The double value.
* `returns`

The converted `duckdb_hugeint` element.

<br>

### **duckdb_prepare**
---
Create a prepared statement object from a query.

Note that after calling `duckdb_prepare`, the prepared statement should always be destroyed using
`duckdb_destroy_prepare`, even if the prepare fails.

If the prepare fails, `duckdb_prepare_error` can be called to obtain the reason why the prepare failed.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_prepare</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> <span class="k">connection</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>,<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> *<span class="k">out_prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `connection`

The connection object
* `query`

The SQL query to prepare
* `out_prepared_statement`

The resulting prepared statement object
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_destroy_prepare**
---
Closes the prepared statement and de-allocates all memory allocated for that connection.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_prepare</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> *<span class="k">prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to destroy.

<br>

### **duckdb_prepare_error**
---
Returns the error message associated with the given prepared statement.
If the prepared statement has no error message, this returns `nullptr` instead.

The error message should not be freed. It will be de-allocated when `duckdb_destroy_prepare` is called.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_prepare_error</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to obtain the error from.
* `returns`

The error message, or `nullptr` if there is none.

<br>

### **duckdb_nparams**
---
Returns the number of parameters that can be provided to the given prepared statement.

Returns 0 if the query was not successfully prepared.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_nparams</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to obtain the number of parameters for.

<br>

### **duckdb_param_type**
---
Returns the parameter type for the parameter at the given index.

Returns `DUCKDB_TYPE_INVALID` if the parameter index is out of range or the statement was not successfully prepared.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_param_type</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement.
* `param_idx`

The parameter index.
* `returns`

The parameter type

<br>

### **duckdb_bind_boolean**
---
Binds a bool value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_boolean</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">bool</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int8**
---
Binds an int8_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int8</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int8_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int16**
---
Binds an int16_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int16</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int16_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int32**
---
Binds an int32_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int32</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int32_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int64**
---
Binds an int64_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int64_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_hugeint**
---
Binds an duckdb_hugeint value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_hugeint</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_hugeint</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint8**
---
Binds an uint8_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint8</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint16**
---
Binds an uint16_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint16</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint16_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint32**
---
Binds an uint32_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint32</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint32_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint64**
---
Binds an uint64_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint64</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint64_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_float**
---
Binds an float value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_float</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">float</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_double**
---
Binds an double value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_double</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">double</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_date**
---
Binds a duckdb_date value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_date</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_date</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_time**
---
Binds a duckdb_time value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_time</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_time</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_timestamp**
---
Binds a duckdb_timestamp value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_timestamp</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_interval**
---
Binds a duckdb_interval value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_interval</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_interval</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_varchar**
---
Binds a null-terminated varchar value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_varchar_length**
---
Binds a varchar value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_varchar_length</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_blob**
---
Binds a blob value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_blob</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">void</span> *<span class="k">data</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_null**
---
Binds a NULL value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_null</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx
</span>);
</code></pre></div></div>
<br>

### **duckdb_execute_prepared**
---
Executes the prepared statement with the given bound parameters, and returns a materialized query result.

This method can be called multiple times for each prepared statement, and the parameters can be modified
between calls to this function.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_execute_prepared</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to execute.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_execute_prepared_arrow**
---
Executes the prepared statement with the given bound parameters, and returns an arrow query result.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_execute_prepared_arrow</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">duckdb_arrow</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to execute.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_appender_create**
---
Creates an appender object.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_appender_create</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> <span class="k">connection</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">schema</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">table</span>,<span class="k">
</span>  <span class="kt">duckdb_appender</span> *<span class="k">out_appender
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `connection`

The connection context to create the appender in.
* `schema`

The schema of the table to append to, or `nullptr` for the default schema.
* `table`

The table name to append to.
* `out_appender`

The resulting appender object.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_appender_error**
---
Returns the error message associated with the given appender.
If the appender has no error message, this returns `nullptr` instead.

The error message should be freed using `duckdb_free`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_appender_error</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `appender`

The appender to get the error from.
* `returns`

The error message, or `nullptr` if there is none.

<br>

### **duckdb_appender_flush**
---
Flush the appender to the table, forcing the cache of the appender to be cleared and the data to be appended to the
base table.

This should generally not be used unless you know what you are doing. Instead, call `duckdb_appender_destroy` when you
are done with the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_appender_flush</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `appender`

The appender to flush.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_appender_close**
---
Close the appender, flushing all intermediate state in the appender to the table and closing it for further appends.

This is generally not necessary. Call `duckdb_appender_destroy` instead.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_appender_close</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `appender`

The appender to flush and close.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_appender_destroy**
---
Close the appender and destroy it. Flushing all intermediate state in the appender to the table, and de-allocating
all memory associated with the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_appender_destroy</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> *<span class="k">appender
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `appender`

The appender to flush, close and destroy.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_appender_begin_row**
---
A nop function, provided for backwards compatibility reasons. Does nothing. Only `duckdb_appender_end_row` is required.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_appender_begin_row</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender
</span>);
</code></pre></div></div>
<br>

### **duckdb_appender_end_row**
---
Finish the current row of appends. After end_row is called, the next row can be appended.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_appender_end_row</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `appender`

The appender.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_append_bool**
---
Append a bool value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_bool</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">bool</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_int8**
---
Append an int8_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_int8</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">int8_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_int16**
---
Append an int16_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_int16</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">int16_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_int32**
---
Append an int32_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_int32</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">int32_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_int64**
---
Append an int64_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">int64_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_hugeint**
---
Append a duckdb_hugeint value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_hugeint</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">duckdb_hugeint</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_uint8**
---
Append a uint8_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_uint8</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_uint16**
---
Append a uint16_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_uint16</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">uint16_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_uint32**
---
Append a uint32_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_uint32</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">uint32_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_uint64**
---
Append a uint64_t value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_uint64</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">uint64_t</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_float**
---
Append a float value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_float</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">float</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_double**
---
Append a double value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_double</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">double</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_date**
---
Append a duckdb_date value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_date</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">duckdb_date</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_time**
---
Append a duckdb_time value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_time</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">duckdb_time</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_timestamp**
---
Append a duckdb_timestamp value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">duckdb_timestamp</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_interval**
---
Append a duckdb_interval value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_interval</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">duckdb_interval</span> <span class="k">value
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_varchar**
---
Append a varchar value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_varchar_length**
---
Append a varchar value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_varchar_length</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_blob**
---
Append a blob value to the appender.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_blob</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">void</span> *<span class="k">data</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
<br>

### **duckdb_append_null**
---
Append a NULL value to the appender (of any type).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_append_null</span>(<span class="k">
</span>  <span class="kt">duckdb_appender</span> <span class="k">appender
</span>);
</code></pre></div></div>
<br>

### **duckdb_query_arrow**
---
Executes a SQL query within a connection and stores the full (materialized) result in an arrow structure.
If the query fails to execute, DuckDBError is returned and the error message can be retrieved by calling
`duckdb_query_arrow_error`.

Note that after running `duckdb_query_arrow`, `duckdb_destroy_arrow` must be called on the result object even if the
query fails, otherwise the error stored within the result will not be freed correctly.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_query_arrow</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> <span class="k">connection</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>,<span class="k">
</span>  <span class="kt">duckdb_arrow</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `connection`

The connection to perform the query in.
* `query`

The SQL query to run.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_query_arrow_schema**
---
Fetch the internal arrow schema from the arrow result.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_query_arrow_schema</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> <span class="k">result</span>,<span class="k">
</span>  <span class="kt">duckdb_arrow_schema</span> *<span class="k">out_schema
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result to fetch the schema from.
* `out_schema`

The output schema.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_query_arrow_array**
---
Fetch an internal arrow array from the arrow result.

This function can be called multiple time to get next chunks, which will free the previous out_array.
So consume the out_array before calling this function again.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_query_arrow_array</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> <span class="k">result</span>,<span class="k">
</span>  <span class="kt">duckdb_arrow_array</span> *<span class="k">out_array
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result to fetch the array from.
* `out_array`

The output array.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_arrow_column_count**
---
Returns the number of columns present in a the arrow result object.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_arrow_column_count</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> <span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object.
* `returns`

The number of columns present in the result object.

<br>

### **duckdb_arrow_row_count**
---
Returns the number of rows present in a the arrow result object.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_arrow_row_count</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> <span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object.
* `returns`

The number of rows present in the result object.

<br>

### **duckdb_arrow_rows_changed**
---
Returns the number of rows changed by the query stored in the arrow result. This is relevant only for
INSERT/UPDATE/DELETE queries. For other queries the rows_changed will be 0.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_arrow_rows_changed</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> <span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object.
* `returns`

The number of rows changed.

<br>

### **duckdb_query_arrow_error**
---
Returns the error message contained within the result. The error is only set if `duckdb_query_arrow` returns
`DuckDBError`.

The result should be freed using `duckdb_free`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_query_arrow_error</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> <span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result object to fetch the nullmask from.
* `returns`

The error of the result.

<br>

### **duckdb_destroy_arrow**
---
Closes the result and de-allocates all memory allocated for the arrow result.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_arrow</span>(<span class="k">
</span>  <span class="kt">duckdb_arrow</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `result`

The result to destroy.

<br>

