---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
redirect_from:
- /docs/api/python/reference/index
- /docs/clients/python/reference/index
- /docs/stable/clients/python/reference/index
- /docs/current/clients/python/reference/index
- /docs/lts/clients/python/reference/index
- /docs/preview/clients/python/reference/index
title: Python Client API
---
<div class="documentwrapper">
<div class="bodywrapper">
<div class="body" role="main">

<section id="connection">
<h2>Connection<a class="headerlink" href="#connection" title="Link to this heading">&#182;</a>
</h2>
<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Appender">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Appender</span></span><a class="headerlink" href="#duckdb.Appender" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Appender.append_row">
<span class="sig-name descname"><span class="pre">append_row</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Appender.append_row" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Buffer one row, one value per column, each converted as an executemany parameter would be</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Appender.append_rows">
<span class="sig-name descname"><span class="pre">append_rows</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Appender.append_rows" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Buffer each row of an iterable of sequences, stopping at the first bad row and keeping the rows before it</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Appender.clear">
<span class="sig-name descname"><span class="pre">clear</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Appender.clear" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Drop the buffered rows</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Appender.flush">
<span class="sig-name descname"><span class="pre">flush</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Appender.flush" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Apply the rows buffered since the last flush with one statement on the appender&#8217;s connection</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyConnection</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.abort">
<span class="sig-name descname"><span class="pre">abort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.abort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Cancel the rest of the result of execute(); a statement that may write fails an open transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.append">
<span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">by_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.append" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Append the passed DataFrame to the named table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.appender">
<span class="sig-name descname"><span class="pre">appender</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">table</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">action</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'insert'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Appender" title="_duckdb.Appender"><span class="pre">_duckdb.Appender</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.appender" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an appender that buffers rows and inserts, upserts, updates or deletes them in the named table at each flush</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.array_type">
<span class="sig-name descname"><span class="pre">array_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.array_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.begin">
<span class="sig-name descname"><span class="pre">begin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.begin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Start a new transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.checkpoint">
<span class="sig-name descname"><span class="pre">checkpoint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.checkpoint" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Synchronizes data in the write-ahead log (WAL) to the database data file (no-op for in-memory connections)</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Close the connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.commit">
<span class="sig-name descname"><span class="pre">commit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.commit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Commit changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.complete">
<span class="sig-name descname"><span class="pre">complete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.complete" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the result of execute() to its end without reading its rows</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.create_function">
<span class="sig-name descname"><span class="pre">create_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">collections.abc.Callable</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">return_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">PythonUDFType</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">PythonUDFType.NATIVE</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_handling</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">FunctionNullHandling</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">FunctionNullHandling.DEFAULT</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exception_handling</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.PythonExceptionHandling" title="duckdb.PythonExceptionHandling"><span class="pre">PythonExceptionHandling</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">PythonExceptionHandling.DEFAULT</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">side_effects</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.create_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB function out of the passing in Python function so it can be used in queries</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.cursor">
<span class="sig-name descname"><span class="pre">cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.cursor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.decimal_type">
<span class="sig-name descname"><span class="pre">decimal_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.decimal_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a decimal type with &#8216;width&#8217; and &#8216;scale&#8217;</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.description">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set attributes, mainly column names</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.disable_profiling">
<span class="sig-name descname"><span class="pre">disable_profiling</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.disable_profiling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Disable profiling for subsequent queries</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.dtype">
<span class="sig-name descname"><span class="pre">dtype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.dtype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.duplicate">
<span class="sig-name descname"><span class="pre">duplicate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.duplicate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.enable_profiling">
<span class="sig-name descname"><span class="pre">enable_profiling</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.enable_profiling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Enable profiling for subsequent queries</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.enum_type">
<span class="sig-name descname"><span class="pre">enum_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.enum_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an enum type of underlying &#8216;type&#8217;, consisting of the list of &#8216;values&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given SQL query, optionally using prepared statements with parameters set. A query runs until its first rows are ready, so an error there raises here; every other statement runs to its end</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.executemany">
<span class="sig-name descname"><span class="pre">executemany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.executemany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given prepared statement multiple times using the list of parameter sets in parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.extract_statements">
<span class="sig-name descname"><span class="pre">extract_statements</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.extract_statements" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Parse the query string and extract the Statement object(s) produced</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df">
<span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df_chunk">
<span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df_chunk" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of the result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as list of NumPy arrays following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.filesystem_is_registered">
<span class="sig-name descname"><span class="pre">filesystem_is_registered</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.filesystem_is_registered" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Check if a filesystem with the provided name is currently registered</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_arrow">
<span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_csv_auto">
<span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_csv_auto" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_df">
<span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the DataFrame in df.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_parquet">
<span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">binary_as_string</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Parquet path(s) or file-like object(s) in &#8216;path_or_buffer&#8217;.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_query">
<span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. A statement that only reads returns a relation that runs the query each time it is read, parameter values bound at every run. Any other statement runs once, now, and gives a relation over what it returned. Statements before the last one run immediately.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_profiling_information">
<span class="sig-name descname"><span class="pre">get_profiling_information</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'json'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_profiling_information" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get profiling information for a query</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_table_names">
<span class="sig-name descname"><span class="pre">get_table_names</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">qualified</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">set</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_table_names" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the required table names from a query</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.install_extension">
<span class="sig-name descname"><span class="pre">install_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">force_install</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">repository</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">repository_url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">version</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.install_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Install an extension by name, with an optional version and/or repository to get the extension from</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.interrupt">
<span class="sig-name descname"><span class="pre">interrupt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.interrupt" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Interrupt pending operations</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.list_filesystems">
<span class="sig-name descname"><span class="pre">list_filesystems</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.list_filesystems" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>List registered filesystems, including builtin ones</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.list_type">
<span class="sig-name descname"><span class="pre">list_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.list_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a list type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.load_extension">
<span class="sig-name descname"><span class="pre">load_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.load_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Load an installed extension</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.map_type">
<span class="sig-name descname"><span class="pre">map_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.map_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a map type object from &#8216;key_type&#8217; and &#8216;value_type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. A statement that only reads returns a relation that runs the query each time it is read, parameter values bound at every run. Any other statement runs once, now, and gives a relation over what it returned. Statements before the last one run immediately.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query_appender">
<span class="sig-name descname"><span class="pre">query_appender</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dml</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">source</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Appender" title="_duckdb.Appender"><span class="pre">_duckdb.Appender</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query_appender" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an appender that buffers rows of the declared columns and runs the DML over them at each flush</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query_progress">
<span class="sig-name descname"><span class="pre">query_progress</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query_progress" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Query progress of pending operation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_csv">
<span class="sig-name descname"><span class="pre">read_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_json">
<span class="sig-name descname"><span class="pre">read_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the JSON file in &#8216;name&#8217;.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_parquet">
<span class="sig-name descname"><span class="pre">read_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">binary_as_string</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Parquet path(s) or file-like object(s) in &#8216;path_or_buffer&#8217;.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register">
<span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">python_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register the passed Python Object value for querying with a view</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register_filesystem">
<span class="sig-name descname"><span class="pre">register_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filesystem</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register a fsspec compliant filesystem</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.remove_function">
<span class="sig-name descname"><span class="pre">remove_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.remove_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Remove a previously created function</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rollback">
<span class="sig-name descname"><span class="pre">rollback</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rollback" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Roll back changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.row_type">
<span class="sig-name descname"><span class="pre">row_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.row_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rowcount">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">rowcount</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rowcount" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set row count</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.sql">
<span class="sig-name descname"><span class="pre">sql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.sql" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. A statement that only reads returns a relation that runs the query each time it is read, parameter values bound at every run. Any other statement runs once, now, and gives a relation over what it returned. Statements before the last one run immediately.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.sqltype">
<span class="sig-name descname"><span class="pre">sqltype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.sqltype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.string_type">
<span class="sig-name descname"><span class="pre">string_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.string_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a string type with an optional collation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.struct_type">
<span class="sig-name descname"><span class="pre">struct_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.struct_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table">
<span class="sig-name descname"><span class="pre">table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the named table.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table_function">
<span class="sig-name descname"><span class="pre">table_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the named table function with given parameters.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.tf">
<span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.to_arrow_reader">
<span class="sig-name descname"><span class="pre">to_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.to_arrow_reader" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A reader over every row the pending result still holds.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.to_arrow_table">
<span class="sig-name descname"><span class="pre">to_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.to_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Every row the pending result still holds, as an Arrow Table.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.torch">
<span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.type">
<span class="sig-name descname"><span class="pre">type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.union_type">
<span class="sig-name descname"><span class="pre">union_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">members</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.union_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a union type object from &#8216;members&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister">
<span class="sig-name descname"><span class="pre">unregister</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister the view name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister_filesystem">
<span class="sig-name descname"><span class="pre">unregister_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister a filesystem</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.values">
<span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.values" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the passed values.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.view">
<span class="sig-name descname"><span class="pre">view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the named view.</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Statement">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Statement</span></span><a class="headerlink" href="#duckdb.Statement" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.expected_result_type">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">expected_result_type</span></span><a class="headerlink" href="#duckdb.Statement.expected_result_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the expected type of result produced by this statement, actual type may vary depending on the statement.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.named_parameters">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">named_parameters</span></span><a class="headerlink" href="#duckdb.Statement.named_parameters" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the map of named parameters this statement has.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.query">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">query</span></span><a class="headerlink" href="#duckdb.Statement.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the query equivalent to this statement.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.type">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">type</span></span><a class="headerlink" href="#duckdb.Statement.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the type of the statement.</p>
</dd>
</dl>

</dd>
</dl>

</section>
<section id="relation">
<h2>Relation<a class="headerlink" href="#relation" title="Link to this heading">&#182;</a>
</h2>
<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyRelation</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DuckDBPyRelation" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>A query built a step at a time; it runs only when a method reads its rows, and runs again on every read.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}">Relational API page</a>.</div>
<br><dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.aggregate">
<span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.aggregate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#aggregate">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.alias">
<span class="sig-name descname"><span class="pre">alias</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the name of the current alias.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#alias">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.any_value">
<span class="sig-name descname"><span class="pre">any_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.any_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the first non-null value from a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#any_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.apply">
<span class="sig-name descname"><span class="pre">apply</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">function_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_parameter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.apply" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the function of a single column or a list of columns by the optional groups on the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#apply">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arg_max">
<span class="sig-name descname"><span class="pre">arg_max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arg_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arg_max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Finds the row with the maximum value for a value column and returns the value of that row for an argument column.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#arg_max">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arg_min">
<span class="sig-name descname"><span class="pre">arg_min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arg_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arg_min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Finds the row with the minimum value for a value column and returns the value of that row for an argument column.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#arg_min">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Alias of to_arrow_reader(). We recommend using to_arrow_reader() instead.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#arrow">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.avg">
<span class="sig-name descname"><span class="pre">avg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.avg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average of a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#avg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_and">
<span class="sig-name descname"><span class="pre">bit_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise AND of all bits present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#bit_and">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_or">
<span class="sig-name descname"><span class="pre">bit_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise OR of all bits present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#bit_or">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_xor">
<span class="sig-name descname"><span class="pre">bit_xor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_xor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise XOR of all bits present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#bit_xor">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bitstring_agg">
<span class="sig-name descname"><span class="pre">bitstring_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">min</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bitstring_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes a bitstring with bits set for each distinct value in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#bitstring_agg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bool_and">
<span class="sig-name descname"><span class="pre">bool_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bool_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the logical AND of all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#bool_and">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bool_or">
<span class="sig-name descname"><span class="pre">bool_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bool_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the logical OR of all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#bool_or">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Does nothing: a relation holds no result.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#close">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.columns">
<span class="sig-name descname"><span class="pre">columns</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.columns" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the names of the columns of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#columns">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.count">
<span class="sig-name descname"><span class="pre">count</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.count" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the number of elements present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#count">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object.</p>
<p>The name is table, schema.table or catalog.schema.table, and a part may be double quoted; a name of more than
three parts needs SQL (CREATE TABLE AS) for now.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#create">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create_view">
<span class="sig-name descname"><span class="pre">create_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create_view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#create_view">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cross">
<span class="sig-name descname"><span class="pre">cross</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cross" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create cross/cartesian product of two relational objects.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#cross">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cume_dist">
<span class="sig-name descname"><span class="pre">cume_dist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cume_dist" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the cumulative distribution within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#cume_dist">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dense_rank">
<span class="sig-name descname"><span class="pre">dense_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dense_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the dense rank within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#dense_rank">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.describe">
<span class="sig-name descname"><span class="pre">describe</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.describe" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Gives basic statistics (e.g., min, max) and if NULL exists for each column of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#describe">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.description">
<span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return the description of the result.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#description">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#df">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.distinct">
<span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">on</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve distinct rows from this relation object, or the first row of each distinct value of <cite>on</cite>.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#distinct">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.drop">
<span class="sig-name descname"><span class="pre">drop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.drop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Remove columns.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#drop">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dtypes">
<span class="sig-name descname"><span class="pre">dtypes</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dtypes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the types of the columns of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#dtypes">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.except_">
<span class="sig-name descname"><span class="pre">except_</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.except_" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set except of this relation object with another relation object in other_rel.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#except_">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.explain">
<span class="sig-name descname"><span class="pre">explain</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">ExplainType.STANDARD</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">analyze</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.explain" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The plan the engine runs for this relation, as text; under Jupyter the default is shown as HTML.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#explain">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.favg">
<span class="sig-name descname"><span class="pre">favg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.favg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average of all values present in a given expression using a more accurate floating point summation (Kahan Sum).</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#favg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_arrow_reader">
<span class="sig-name descname"><span class="pre">fetch_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_arrow_reader" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Deprecated: use to_arrow_reader() instead.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fetch_arrow_reader">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Deprecated: use to_arrow_table() instead.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fetch_arrow_table">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_record_batch">
<span class="sig-name descname"><span class="pre">fetch_record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Deprecated: use to_arrow_reader() instead.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fetch_record_batch">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">Any</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="p"><span class="pre">...</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a list of tuples.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fetchall">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fetchdf">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Python dict mapping each column to one numpy arrays.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fetchnumpy">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.filter">
<span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.filter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the relation object by the filter in filter_expr.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#filter">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.first">
<span class="sig-name descname"><span class="pre">first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the first value of a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#first">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.first_value">
<span class="sig-name descname"><span class="pre">first_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.first_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the first value within the group or partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#first_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fsum">
<span class="sig-name descname"><span class="pre">fsum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fsum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sum of all values present in a given expression using a more accurate floating point summation (Kahan Sum).</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#fsum">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.geomean">
<span class="sig-name descname"><span class="pre">geomean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.geomean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the geometric mean over all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#geomean">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.group_by">
<span class="sig-name descname"><span class="pre">group_by</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">GroupedRelation</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.group_by" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Begin a grouped aggregation; continue with <cite>.agg(&#8230;)</cite>.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#group_by">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.head">
<span class="sig-name descname"><span class="pre">head</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">5</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.head" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first <cite>n</cite> rows.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#head">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.histogram">
<span class="sig-name descname"><span class="pre">histogram</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.histogram" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the histogram over all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#histogram">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert">
<span class="sig-name descname"><span class="pre">insert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the given values into the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#insert">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert_into">
<span class="sig-name descname"><span class="pre">insert_into</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert_into" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the relation object into an existing table named table_name.</p>
<p>The name is table, schema.table or catalog.schema.table, and a part may be double quoted; a name of more than
three parts needs SQL (INSERT INTO) for now.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#insert_into">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.intersect">
<span class="sig-name descname"><span class="pre">intersect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.intersect" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set intersection of this relation object with another relation object in other_rel.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#intersect">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.iter_rows">
<span class="sig-name descname"><span class="pre">iter_rows</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1024</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Iterator</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">Any</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="p"><span class="pre">...</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.iter_rows" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Every row, a batch at a time, over one run of the relation.</p>
<p>The rows are read once into the engine&#8217;s memory, so every batch comes from the same run and the connection
is free between batches; the caller holds one batch at a time rather than the whole result.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#iter_rows">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.join">
<span class="sig-name descname"><span class="pre">join</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">how</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'inner'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">suffix</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.join" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Join the relation object with another relation object in other_rel.</p>
<p>The condition is SQL text, a column name or a list of them for a USING join, an Expression, or a function of
the two sides. Types supported are &#8216;inner&#8217;, &#8216;left&#8217;, &#8216;right&#8217;, &#8216;outer&#8217;, &#8216;full&#8217;, &#8216;semi&#8217;, &#8216;anti&#8217;, &#8216;cross&#8217;,
&#8216;positional&#8217;, &#8216;natural&#8217; and &#8216;asof&#8217;. With <cite>suffix</cite>, a column of the right side whose name the left side
already has is renamed with the suffix appended.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#join">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.lag">
<span class="sig-name descname"><span class="pre">lag</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'NULL'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.lag" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the lag within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#lag">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.last">
<span class="sig-name descname"><span class="pre">last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the last value of a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#last">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.last_value">
<span class="sig-name descname"><span class="pre">last_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.last_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the last value within the group or partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#last_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.lead">
<span class="sig-name descname"><span class="pre">lead</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'NULL'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.lead" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the lead within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#lead">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.limit">
<span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.limit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Only retrieve the first n rows from this relation object, starting at offset.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#limit">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.list" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns a list containing all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#list">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.map">
<span class="sig-name descname"><span class="pre">map</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">map_function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="p"><span class="pre">[</span></span><span class="p"><span class="pre">...</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.map" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Calls the passed function on the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#map">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.materialize">
<span class="sig-name descname"><span class="pre">materialize</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.materialize" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute once and return a relation over the rows, held in client memory.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#materialize">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.max">
<span class="sig-name descname"><span class="pre">max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the maximum value present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#max">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mean">
<span class="sig-name descname"><span class="pre">mean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average of a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#mean">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.median">
<span class="sig-name descname"><span class="pre">median</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.median" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the median over all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#median">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.min">
<span class="sig-name descname"><span class="pre">min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the minimum value present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#min">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mode">
<span class="sig-name descname"><span class="pre">mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the mode over all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#mode">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.n_tile">
<span class="sig-name descname"><span class="pre">n_tile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">num_buckets</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.n_tile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Divides the partition as equally as possible into num_buckets.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#n_tile">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.nth_value">
<span class="sig-name descname"><span class="pre">nth_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.nth_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the nth value within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#nth_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.offset">
<span class="sig-name descname"><span class="pre">offset</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.offset" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Skip <cite>n</cite> rows.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#offset">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.order">
<span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.order" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by order_expr, which is SQL order text or an expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#order">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.percent_rank">
<span class="sig-name descname"><span class="pre">percent_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.percent_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the relative rank within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#percent_rank">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.pivot">
<span class="sig-name descname"><span class="pre">pivot</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Iterable</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregate</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.pivot" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Turn the given values of <cite>column</cite> into columns holding <cite>aggregate</cite>; the values are explicit.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#pivot">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.pl">
<span class="sig-name descname"><span class="pre">pl</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">lazy</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.pl" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Polars DataFrame.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#pl">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.preview">
<span class="sig-name descname"><span class="pre">preview</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">limit</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">10</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.preview" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first <cite>limit</cite> rows drawn as a table, with the footer <cite>__repr__</cite> prints for the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#preview">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.product">
<span class="sig-name descname"><span class="pre">product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the product of all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#product">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.project">
<span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.project" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#project">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile">
<span class="sig-name descname"><span class="pre">quantile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the exact quantile value for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#quantile">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile_cont">
<span class="sig-name descname"><span class="pre">quantile_cont</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile_cont" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the interpolated quantile value for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#quantile_cont">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile_disc">
<span class="sig-name descname"><span class="pre">quantile_disc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile_disc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the exact quantile value for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#quantile_disc">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object.</p>
<p>The name is this query&#8217;s own: it is a common table expression over the relation, and a catalog entry for the
length of the call, so a table function or a query that defines the name itself can bind against it. Nothing
of it is left afterwards. A statement that does not only read, which includes a SELECT whose common table
expression writes, runs at the call and the relation holds what it returned.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#query-1">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rank">
<span class="sig-name descname"><span class="pre">rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the rank within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#rank">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rank_dense">
<span class="sig-name descname"><span class="pre">rank_dense</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rank_dense" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the dense rank within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#rank_dense">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rename">
<span class="sig-name descname"><span class="pre">rename</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rename" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Rename columns, given as old=new.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#rename">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.row_number">
<span class="sig-name descname"><span class="pre">row_number</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.row_number" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the row number within the partition.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#row_number">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sample">
<span class="sig-name descname"><span class="pre">sample</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">percent</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seed</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">method</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sample" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A random subset: <cite>n</cite> rows, or <cite>percent</cite> of them, with <cite>seed</cite> repeating a draw.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#sample">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select">
<span class="sig-name descname"><span class="pre">select</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#select">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select_dtypes">
<span class="sig-name descname"><span class="pre">select_dtypes</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select_dtypes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Select columns from the relation, by filtering based on type(s).</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#select_dtypes">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select_types">
<span class="sig-name descname"><span class="pre">select_types</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select_types" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Select columns from the relation, by filtering based on type(s).</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#select_types">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.set_alias">
<span class="sig-name descname"><span class="pre">set_alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.set_alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Rename the relation object to new alias.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#set_alias">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.shape">
<span class="sig-name descname"><span class="pre">shape</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.shape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Tuple of # of rows, # of columns in relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#shape">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_rows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_col_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">render_mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.show" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Display a summary of the data.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#show">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sort">
<span class="sig-name descname"><span class="pre">sort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by the provided expressions.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#sort">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sql_query">
<span class="sig-name descname"><span class="pre">sql_query</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sql_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the SQL query that is equivalent to the relation; values given as <cite>params=</cite> stay markers.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#sql_query">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.std">
<span class="sig-name descname"><span class="pre">std</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.std" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#std">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev">
<span class="sig-name descname"><span class="pre">stddev</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#stddev">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev_pop">
<span class="sig-name descname"><span class="pre">stddev_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the population standard deviation for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#stddev_pop">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev_samp">
<span class="sig-name descname"><span class="pre">stddev_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#stddev_samp">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.string_agg">
<span class="sig-name descname"><span class="pre">string_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">','</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.string_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Concatenates the values present in a given expression with a separator.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#string_agg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sum">
<span class="sig-name descname"><span class="pre">sum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sum of all values present in a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#sum">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.tf">
<span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#tf">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_arrow_reader">
<span class="sig-name descname"><span class="pre">to_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_arrow_reader" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_arrow_reader">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_arrow_table">
<span class="sig-name descname"><span class="pre">to_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_arrow_table">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_csv">
<span class="sig-name descname"><span class="pre">to_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_rep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quoting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_csv">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_df">
<span class="sig-name descname"><span class="pre">to_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_df">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_dicts">
<span class="sig-name descname"><span class="pre">to_dicts</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_dicts" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Every row, as a dict keyed by column name.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_dicts">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_parquet">
<span class="sig-name descname"><span class="pre">to_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">field_ids</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size_bytes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">append</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename_pattern</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_size_bytes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a Parquet file in &#8216;file_name&#8217;.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_parquet">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_table">
<span class="sig-name descname"><span class="pre">to_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object.</p>
<p>The name is table, schema.table or catalog.schema.table, and a part may be double quoted; a name of more than
three parts needs SQL (CREATE TABLE AS) for now.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_table">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_view">
<span class="sig-name descname"><span class="pre">to_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#to_view">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.torch">
<span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">Any</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#torch">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.type">
<span class="sig-name descname"><span class="pre">type</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the type of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#type">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.types">
<span class="sig-name descname"><span class="pre">types</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.types" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the types of the columns of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#types">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.union">
<span class="sig-name descname"><span class="pre">union</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">union_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.union" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set union of this relation object with another relation object in other_rel.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#union">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.union_by_name">
<span class="sig-name descname"><span class="pre">union_by_name</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">other</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">all</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.union_by_name" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Rows from both relations, matching columns by name; keeps duplicates unless <cite>all</cite> is false.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#union_by_name">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.unique">
<span class="sig-name descname"><span class="pre">unique</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">unique_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.unique" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the distinct values in a column.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#unique">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.unnest">
<span class="sig-name descname"><span class="pre">unnest</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.unnest" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Expand list columns to one row per element.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#unnest">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.unpivot">
<span class="sig-name descname"><span class="pre">unpivot</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'name'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'value'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.unpivot" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Turn the named columns into rows; <cite>name</cite> and <cite>value</cite> name the two new columns.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#unpivot">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.update">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">set</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.update" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Update the given relation with the provided expressions.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#update">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.value_counts">
<span class="sig-name descname"><span class="pre">value_counts</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.value_counts" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the number of elements present in a given expression, also projecting the original expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#value_counts">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var">
<span class="sig-name descname"><span class="pre">var</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#var">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var_pop">
<span class="sig-name descname"><span class="pre">var_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the population variance for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#var_pop">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var_samp">
<span class="sig-name descname"><span class="pre">var_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#var_samp">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.variance">
<span class="sig-name descname"><span class="pre">variance</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.variance" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given expression.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#variance">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.with_columns">
<span class="sig-name descname"><span class="pre">with_columns</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.with_columns" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Add columns, replacing any of the same name in place.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#with_columns">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_csv">
<span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_rep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quoting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#write_csv">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_parquet">
<span class="sig-name descname"><span class="pre">write_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">field_ids</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size_bytes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">builtins.list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">append</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename_pattern</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_size_bytes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a Parquet file in &#8216;file_name&#8217;.</p>
<div>Detailed examples can be found at <a href="{% link docs/2.0/clients/python/relational_api.md %}#write_parquet">Relational API page</a>.</div>
<br>
</dd>
</dl>

</dd>
</dl>

</section>
<section id="expressions">
<h2>Expressions<a class="headerlink" href="#expressions" title="Link to this heading">&#182;</a>
</h2>
<dl class="py function">
<dt class="sig sig-object py" id="duckdb.CaseExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CaseExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.CaseExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>CASE WHEN condition THEN value</cite>, extended by <cite>.when(condition, value)</cite> and closed by <cite>.otherwise(value)</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.coalesce">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">coalesce</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.coalesce" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first argument that is not NULL.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.CoalesceOperator">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CoalesceOperator</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.CoalesceOperator" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first argument that is not NULL.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.col">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">col</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">parts</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.col" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A column by name, or by the parts of a qualified name: <cite>col(&#8220;t&#8221;, &#8220;i&#8221;)</cite> is <cite>&#8220;t&#8221;.&#8221;i&#8221;</cite>.</p>
<p>Every part is quoted whole, so any name works and none is split; a struct field is <cite>col(&#8220;st&#8221;)[&#8220;field&#8221;]</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.ColumnExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ColumnExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.ColumnExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A column by name, or by the parts of a qualified name: <cite>ColumnExpression(&#8220;t&#8221;, &#8220;a&#8221;)</cite> is <cite>&#8220;t&#8221;.&#8221;a&#8221;</cite>.</p>
<p>A name is taken whole and never split, so <cite>ColumnExpression(&#8220;a.b&#8221;)</cite> is the column called <cite>a.b</cite>; the one name <cite>*</cite>
is the star, as <cite>StarExpression()</cite> is.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.ConstantExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConstantExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.ConstantExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A value; a <cite>duckdb.Value</cite> is written as a cast to its type, and a numpy array as the list it holds.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.count_all">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">count_all</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.count_all" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many rows there are, as <cite>count(*)</cite>; unlike <cite>col(&#8220;x&#8221;).count()</cite>, NULLs are not skipped.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.DefaultExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DefaultExpression</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.DefaultExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>DEFAULT</cite>, the column&#8217;s default value, where an INSERT or UPDATE takes one.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.dense_rank">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">dense_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.dense_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>dense_rank</cite> window function.</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Expression">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Expression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.Expression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">AggregateMethods</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">FuncNamespaces</span></code></p>
<p>One node of an expression tree; <cite>Expression(&#8220;x&#8221;)</cite> is the column <cite>x</cite> and <cite>Expression(1)</cite> the value 1.</p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.alias">
<span class="sig-name descname"><span class="pre">alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Name the column in the output; an empty name removes the alias, as it did in the earlier API.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.any_value">
<span class="sig-name descname"><span class="pre">any_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.any_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Any one of the values, whichever is cheapest. SQL: <cite>any_value</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.arg_max">
<span class="sig-name descname"><span class="pre">arg_max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.arg_max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The value of the argument where this is largest. SQL: <cite>arg_max</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.arg_min">
<span class="sig-name descname"><span class="pre">arg_min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.arg_min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The value of the argument where this is smallest. SQL: <cite>arg_min</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.array_agg">
<span class="sig-name descname"><span class="pre">array_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.array_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The values gathered into a list. SQL: <cite>array_agg</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.as_order">
<span class="sig-name descname"><span class="pre">as_order</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.Expression.as_order" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The SQL for an ORDER BY item, carrying the direction and the null order where they were asked for.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.as_select">
<span class="sig-name descname"><span class="pre">as_select</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.Expression.as_select" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The SQL for a select list, carrying the alias if there is one.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.asc">
<span class="sig-name descname"><span class="pre">asc</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.asc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Sort ascending. Keeps any null order already set.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.avg">
<span class="sig-name descname"><span class="pre">avg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.avg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The average of the values. The same as <cite>mean</cite>. SQL: <cite>avg</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.between">
<span class="sig-name descname"><span class="pre">between</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">low</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">high</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">lower</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upper</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.between" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inclusive range; <cite>lower</cite> and <cite>upper</cite> are the earlier API&#8217;s names for the same two bounds.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.bit_and">
<span class="sig-name descname"><span class="pre">bit_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.bit_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The bitwise AND of the values. SQL: <cite>bit_and</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.bit_or">
<span class="sig-name descname"><span class="pre">bit_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.bit_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The bitwise OR of the values. SQL: <cite>bit_or</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.bool_and">
<span class="sig-name descname"><span class="pre">bool_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.bool_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether every value is true. SQL: <cite>bool_and</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.bool_or">
<span class="sig-name descname"><span class="pre">bool_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.bool_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether any value is true. SQL: <cite>bool_or</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.cast">
<span class="sig-name descname"><span class="pre">cast</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_text</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">DuckDBPyType</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Statement.type" title="duckdb.Statement.type"><span class="pre">type</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">DuckDBPyType</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Statement.type" title="duckdb.Statement.type"><span class="pre">type</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.cast" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Cast to a SQL type, a <cite>DuckDBPyType</cite>, or text spliced in as SQL and so never taken from untrusted input.</p>
<p><cite>type</cite> is the earlier API&#8217;s name for the same argument.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.collate">
<span class="sig-name descname"><span class="pre">collate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.collate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compare and sort by a collation, such as <cite>nocase</cite>; <cite>nocase.noaccent</cite> combines two.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.concat">
<span class="sig-name descname"><span class="pre">concat</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">others</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.concat" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Join text values.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.count">
<span class="sig-name descname"><span class="pre">count</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.count" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many values are not NULL. For rows, use <cite>count_all()</cite>. SQL: <cite>count</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.desc">
<span class="sig-name descname"><span class="pre">desc</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.desc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Sort descending. Keeps any null order already set.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.dt">
<span class="sig-name descname"><span class="pre">dt</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.DtExpr" title="duckdb._expression_namespaces.DtExpr"><span class="pre">DtExpr</span></a></span></span><a class="headerlink" href="#duckdb.Expression.dt" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>This expression as a date, time or timestamp: <cite>col(&#8220;placed&#8221;).dt().year()</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.entropy">
<span class="sig-name descname"><span class="pre">entropy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.entropy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The entropy of the distribution. SQL: <cite>entropy</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.first">
<span class="sig-name descname"><span class="pre">first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first value seen. Order it with <cite>.over()</cite> or <cite>sort</cite> to make that mean something. SQL: <cite>first</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.fragment">
<span class="sig-name descname"><span class="pre">fragment</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.Expression.fragment" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The SQL for this node, parenthesised so precedence cannot change what it means.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.get_name">
<span class="sig-name descname"><span class="pre">get_name</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.Expression.get_name" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The name a query gives this expression&#8217;s column: its alias, a column&#8217;s own name, or else its SQL text.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.ignore_nulls">
<span class="sig-name descname"><span class="pre">ignore_nulls</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.ignore_nulls" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Skip NULLs, for <cite>first_value</cite>, <cite>last_value</cite>, <cite>lag</cite>, <cite>lead</cite> and <cite>nth_value</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.ilike">
<span class="sig-name descname"><span class="pre">ilike</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pattern</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">escape</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.ilike" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>like</cite>, ignoring case.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.is_not_null">
<span class="sig-name descname"><span class="pre">is_not_null</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.is_not_null" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether this is not NULL.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.is_null">
<span class="sig-name descname"><span class="pre">is_null</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.is_null" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether this is NULL. Not the same as <cite>== None</cite>, which gives NULL.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isin">
<span class="sig-name descname"><span class="pre">isin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Membership of several values, as <cite>isin(1, 2)</cite>, the form of the earlier expression API.</p>
<p>One argument is one member, so a list given as one argument is compared whole; its elements are several
arguments, and asking whether a list-typed column holds a value is <cite>fn(&#8220;list_contains&#8221;, &#8230;)</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isnotin">
<span class="sig-name descname"><span class="pre">isnotin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnotin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The negation of <cite>isin</cite>, taking the same arguments.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isnotnull">
<span class="sig-name descname"><span class="pre">isnotnull</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnotnull" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>is_not_null</cite>, under the name of the earlier expression API.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isnull">
<span class="sig-name descname"><span class="pre">isnull</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnull" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>is_null</cite>, under the name of the earlier expression API.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.json">
<span class="sig-name descname"><span class="pre">json</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb.Expression.json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>This expression as JSON, with the string functions in scope too: <cite>col(&#8220;p&#8221;).json().extract(&#8220;$.id&#8221;)</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.kurtosis">
<span class="sig-name descname"><span class="pre">kurtosis</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.kurtosis" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The kurtosis of the distribution. SQL: <cite>kurtosis</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.last">
<span class="sig-name descname"><span class="pre">last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The last value seen. SQL: <cite>last</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.like">
<span class="sig-name descname"><span class="pre">like</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pattern</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">escape</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.like" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Text match where <cite>%</cite> is any run of characters and <cite>_</cite> is any one; negate with <cite>~</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb.Expression.list" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>This expression as a list: <cite>col(&#8220;tags&#8221;).list().contains(&#8220;vip&#8221;)</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.max">
<span class="sig-name descname"><span class="pre">max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The largest value. SQL: <cite>max</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.mean">
<span class="sig-name descname"><span class="pre">mean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.mean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The average of the values. SQL: <cite>avg</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.median">
<span class="sig-name descname"><span class="pre">median</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.median" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The middle value. SQL: <cite>median</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.min">
<span class="sig-name descname"><span class="pre">min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The smallest value. SQL: <cite>min</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.mode">
<span class="sig-name descname"><span class="pre">mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.mode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The most frequent value. SQL: <cite>mode</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.n_unique">
<span class="sig-name descname"><span class="pre">n_unique</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.n_unique" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many distinct values there are, ignoring NULL.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.nulls_first">
<span class="sig-name descname"><span class="pre">nulls_first</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.nulls_first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Where NULLs sort. Leaves the direction as it was, so the connection&#8217;s default holds until one is given.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.nulls_last">
<span class="sig-name descname"><span class="pre">nulls_last</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.nulls_last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Where NULLs sort. Leaves the direction as it was, so the connection&#8217;s default holds until one is given.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.otherwise">
<span class="sig-name descname"><span class="pre">otherwise</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.otherwise" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The value of a CASE built by <cite>CaseExpression</cite> where no branch matches, NULL until given.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.over">
<span class="sig-name descname"><span class="pre">over</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Exprs</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Exprs</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">range</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">int</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.over" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Turn an aggregate into a window function.</p>
<p><cite>rows</cite> and <cite>range</cite> bound it as (start, end), counted from the current row, with None meaning unbounded.
So <cite>rows=(-2, 0)</cite> is the current row and the two before it.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.product">
<span class="sig-name descname"><span class="pre">product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The product of the values. SQL: <cite>product</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.quantile">
<span class="sig-name descname"><span class="pre">quantile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.quantile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The value at a quantile, one of the values themselves. Pass the quantile, 0 to 1. SQL: <cite>quantile_disc</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.quantile_cont">
<span class="sig-name descname"><span class="pre">quantile_cont</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.quantile_cont" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The value at a quantile, interpolated. Pass the quantile, 0 to 1. SQL: <cite>quantile_cont</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Expression.show" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Print the SQL text.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.skewness">
<span class="sig-name descname"><span class="pre">skewness</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.skewness" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The skewness of the distribution. SQL: <cite>skewness</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.std">
<span class="sig-name descname"><span class="pre">std</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.std" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The sample standard deviation. SQL: <cite>stddev_samp</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.str">
<span class="sig-name descname"><span class="pre">str</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb.Expression.str" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>This expression with the string functions in scope, <cite>col(&#8220;s&#8221;).str().upper()</cite>; nothing is checked or cast.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.string_agg">
<span class="sig-name descname"><span class="pre">string_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.string_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The values joined as text. Pass the separator as an argument. SQL: <cite>string_agg</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.sum">
<span class="sig-name descname"><span class="pre">sum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.sum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The sum of the values. SQL: <cite>sum</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.try_cast">
<span class="sig-name descname"><span class="pre">try_cast</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_text</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">DuckDBPyType</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Statement.type" title="duckdb.Statement.type"><span class="pre">type</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">DuckDBPyType</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Statement.type" title="duckdb.Statement.type"><span class="pre">type</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">&lt;object</span> <span class="pre">object&gt;</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.try_cast" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Cast to a SQL type, giving NULL where the cast would fail; the type is taken as for <cite>cast</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.var">
<span class="sig-name descname"><span class="pre">var</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.var" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The sample variance. SQL: <cite>var_samp</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.when">
<span class="sig-name descname"><span class="pre">when</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.when" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Another branch of a CASE built by <cite>CaseExpression</cite>, tried after the ones before it.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.where">
<span class="sig-name descname"><span class="pre">where</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">predicate</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.where" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Aggregate only rows where the predicate holds; goes before <cite>.over()</cite>, and a scalar call fails at run time.</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.first_value">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">first_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">subject</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></em>, <em class="sig-param"><span class="positional-only-separator o"><abbr title="Positional-only parameter separator (PEP 570)"><span class="pre">/</span></abbr></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.first_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>first_value</cite> window function: <cite>subject</cite> at the first row of the window frame.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fn">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fn</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="p"><span class="pre">...</span></span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="positional-only-separator o"><abbr title="Positional-only parameter separator (PEP 570)"><span class="pre">/</span></abbr></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">named</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.fn" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Any SQL function by name, a tuple for a schema-qualified one, with the arguments treated as anywhere else.</p>
<p>A keyword argument passes by name: <cite>fn(&#8220;round&#8221;, col(&#8220;x&#8221;), precision=1)</cite> is <cite>round(&#8220;x&#8221;, &#8220;precision&#8221; := 1)</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.FunctionExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FunctionExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">function_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="p"><span class="pre">...</span></span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.FunctionExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A call of the function by its name, a bare string argument being a value as everywhere else.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.lag">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">lag</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">subject</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></em>, <em class="sig-param"><span class="positional-only-separator o"><abbr title="Positional-only parameter separator (PEP 570)"><span class="pre">/</span></abbr></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.lag" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>lag</cite> window function: <cite>subject</cite> some rows back, <cite>lag(col(&#8220;x&#8221;))</cite> or <cite>lag(col(&#8220;x&#8221;), 2, 0)</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.LambdaExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">LambdaExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">lhs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="p"><span class="pre">...</span></span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">rhs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.LambdaExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>lambda lhs: rhs</cite>, <cite>lhs</cite> naming one parameter or a tuple of them, for functions such as <cite>list_transform</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.last_value">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">last_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">subject</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></em>, <em class="sig-param"><span class="positional-only-separator o"><abbr title="Positional-only parameter separator (PEP 570)"><span class="pre">/</span></abbr></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.last_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>last_value</cite> window function: <cite>subject</cite> at the last row of the window frame.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.lead">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">lead</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">subject</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></em>, <em class="sig-param"><span class="positional-only-separator o"><abbr title="Positional-only parameter separator (PEP 570)"><span class="pre">/</span></abbr></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.lead" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>lead</cite> window function: <cite>subject</cite> some rows ahead, <cite>lead(col(&#8220;x&#8221;))</cite> or <cite>lead(col(&#8220;x&#8221;), 2, 0)</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.lit">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">lit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.lit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A Python value. Rarely needed, since operators accept values directly.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.ntile">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ntile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.ntile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>ntile</cite> window function.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.rank">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>rank</cite> window function.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.row_number">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">row_number</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.row_number" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>row_number</cite> window function.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.sql_expr">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">sql_expr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">sql</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.sql_expr" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A raw SQL fragment, spliced in unchanged and never escaped, so never build one from untrusted input.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.SQLExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SQLExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">expression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb._expression.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.SQLExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>One SQL expression, checked by the parser here and written as given, never from untrusted input.</p>
<p>An alias in the text names the column, as <cite>SQLExpression(&#8220;sum(x) AS total&#8221;)</cite> does; the rest of the text is what
the SQL holds, in parentheses on lines of its own.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.star">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">star</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ColumnNames</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">()</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">rename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_Renames</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.star" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>*</cite>, optionally dropping or renaming columns; <cite>exclude=&#8221;id&#8221;</cite> drops the one column <cite>id</cite>.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.StarExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StarExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">exclude</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Iterable</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb.StarExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p><cite>*</cite>, leaving out the columns in <cite>exclude</cite>, each a name or a <cite>ColumnExpression</cite> for a qualified one.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.when">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">when</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">CaseBuilder</span></span></span><a class="headerlink" href="#duckdb.when" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Begins a CASE. Continue with <cite>.then(&#8230;)</cite>.</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb._expression_namespaces.</span></span><span class="sig-name descname"><span class="pre">StrExpr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Text functions, applied to this expression as the string.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.SPEC">
<span class="sig-name descname"><span class="pre">SPEC</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">ClassVar</span><span class="p"><span class="pre">[</span></span><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">int</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">{'ascii':</span> <span class="pre">('ascii',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'bin':</span> <span class="pre">('bin',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'bit_length':</span> <span class="pre">('bit_length',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'concat_ws':</span> <span class="pre">('concat_ws',</span> <span class="pre">1,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'ANY']),</span> <span class="pre">'contains':</span> <span class="pre">('contains',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'damerau_levenshtein':</span> <span class="pre">('damerau_levenshtein',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'format':</span> <span class="pre">('format',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'from_base64':</span> <span class="pre">('from_base64',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'hamming':</span> <span class="pre">('hamming',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'ilike_escape':</span> <span class="pre">('ilike_escape',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'instr':</span> <span class="pre">('instr',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'jaccard':</span> <span class="pre">('jaccard',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'jaro_similarity':</span> <span class="pre">('jaro_similarity',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'jaro_winkler_similarity':</span> <span class="pre">('jaro_winkler_similarity',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'left':</span> <span class="pre">('left',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'left_grapheme':</span> <span class="pre">('left_grapheme',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'length':</span> <span class="pre">('length',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'length_grapheme':</span> <span class="pre">('length_grapheme',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'levenshtein':</span> <span class="pre">('levenshtein',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'like_escape':</span> <span class="pre">('like_escape',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'lower':</span> <span class="pre">('lower',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'lpad':</span> <span class="pre">('lpad',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'INTEGER',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'ltrim':</span> <span class="pre">('ltrim',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'md5':</span> <span class="pre">('md5',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'md5_number':</span> <span class="pre">('md5_number',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'nfc_normalize':</span> <span class="pre">('nfc_normalize',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'not_ilike_escape':</span> <span class="pre">('not_ilike_escape',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'not_like_escape':</span> <span class="pre">('not_like_escape',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'overlay':</span> <span class="pre">('overlay',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'parse_dirname':</span> <span class="pre">('parse_dirname',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'parse_dirpath':</span> <span class="pre">('parse_dirpath',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'parse_filename':</span> <span class="pre">('parse_filename',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'parse_formatted_bytes':</span> <span class="pre">('parse_formatted_bytes',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'parse_path':</span> <span class="pre">('parse_path',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'path_join':</span> <span class="pre">('path_join',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'prefix':</span> <span class="pre">('prefix',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'printf':</span> <span class="pre">('printf',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'regexp_escape':</span> <span class="pre">('regexp_escape',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'regexp_extract':</span> <span class="pre">('regexp_extract',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'regexp_extract_all':</span> <span class="pre">('regexp_extract_all',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'regexp_full_match':</span> <span class="pre">('regexp_full_match',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'regexp_matches':</span> <span class="pre">('regexp_matches',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'regexp_replace':</span> <span class="pre">('regexp_replace',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'replace':</span> <span class="pre">('replace',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'reverse':</span> <span class="pre">('reverse',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'right':</span> <span class="pre">('right',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'right_grapheme':</span> <span class="pre">('right_grapheme',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'rpad':</span> <span class="pre">('rpad',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'INTEGER',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'rtrim':</span> <span class="pre">('rtrim',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'sha1':</span> <span class="pre">('sha1',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'sha256':</span> <span class="pre">('sha256',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'string_split':</span> <span class="pre">('string_split',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'string_split_regex':</span> <span class="pre">('string_split_regex',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'strip_accents':</span> <span class="pre">('strip_accents',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'strlen':</span> <span class="pre">('strlen',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'substring':</span> <span class="pre">('substring',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'substring_grapheme':</span> <span class="pre">('substring_grapheme',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'suffix':</span> <span class="pre">('suffix',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'translate':</span> <span class="pre">('translate',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'trim':</span> <span class="pre">('trim',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'unbin':</span> <span class="pre">('unbin',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'unhex':</span> <span class="pre">('unhex',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'unicode':</span> <span class="pre">('unicode',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'upper':</span> <span class="pre">('upper',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'url_decode':</span> <span class="pre">('url_decode',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR']),</span> <span class="pre">'url_encode':</span> <span class="pre">('url_encode',</span> <span class="pre">0,</span> <span class="pre">['VARCHAR'])}</span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.SPEC" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Method name to (function, position of the expression, parameter types).</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.ascii">
<span class="sig-name descname"><span class="pre">ascii</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.ascii" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The Unicode code point of the first character. SQL: <cite>ascii</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.bin">
<span class="sig-name descname"><span class="pre">bin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.bin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts the <cite>string</cite> to binary representation. SQL: <cite>bin</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.bit_length">
<span class="sig-name descname"><span class="pre">bit_length</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.bit_length" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Number of bits in a <cite>string</cite>. SQL: <cite>bit_length</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.concat_ws">
<span class="sig-name descname"><span class="pre">concat_ws</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">separator</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.concat_ws" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Concatenates many strings, separated by <cite>separator</cite>. Arguments: separator. SQL: <cite>concat_ws</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.contains">
<span class="sig-name descname"><span class="pre">contains</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.contains" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns <cite>true</cite> if <cite>search_string</cite> is found within <cite>string</cite>. Arguments: search_string. SQL: <cite>contains</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.damerau_levenshtein">
<span class="sig-name descname"><span class="pre">damerau_levenshtein</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.damerau_levenshtein" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Edit distance, counting a swap of neighbours as one edit. Arguments: s2. SQL: <cite>damerau_levenshtein</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.format">
<span class="sig-name descname"><span class="pre">format</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.format" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Formats a string using the fmt syntax. SQL: <cite>format</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.from_base64">
<span class="sig-name descname"><span class="pre">from_base64</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.from_base64" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts a base64 encoded <cite>string</cite> to a character string (<cite>BLOB</cite>). SQL: <cite>from_base64</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.hamming">
<span class="sig-name descname"><span class="pre">hamming</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.hamming" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many positions differ, for two strings of equal length. Arguments: s2. SQL: <cite>hamming</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.ilike_escape">
<span class="sig-name descname"><span class="pre">ilike_escape</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.ilike_escape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Matches the pattern, ignoring case. Arguments: like_specifier, escape_character. SQL: <cite>ilike_escape</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.instr">
<span class="sig-name descname"><span class="pre">instr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.instr" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Where the search string first occurs, or 0. Arguments: search_string. SQL: <cite>instr</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.jaccard">
<span class="sig-name descname"><span class="pre">jaccard</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.jaccard" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The Jaccard similarity between two strings. Arguments: s2. SQL: <cite>jaccard</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.jaro_similarity">
<span class="sig-name descname"><span class="pre">jaro_similarity</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.jaro_similarity" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The Jaro similarity between two strings. Arguments: s2. SQL: <cite>jaro_similarity</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.jaro_winkler_similarity">
<span class="sig-name descname"><span class="pre">jaro_winkler_similarity</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.jaro_winkler_similarity" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The Jaro-Winkler similarity between two strings. Arguments: s2. SQL: <cite>jaro_winkler_similarity</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.left">
<span class="sig-name descname"><span class="pre">left</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.left" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extracts the left-most count characters. Arguments: count. SQL: <cite>left</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.left_grapheme">
<span class="sig-name descname"><span class="pre">left_grapheme</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.left_grapheme" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extracts the left-most count grapheme clusters. Arguments: count. SQL: <cite>left_grapheme</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.length">
<span class="sig-name descname"><span class="pre">length</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.length" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Number of characters in <cite>string</cite>. SQL: <cite>length</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.length_grapheme">
<span class="sig-name descname"><span class="pre">length_grapheme</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.length_grapheme" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Number of grapheme clusters in <cite>string</cite>. SQL: <cite>length_grapheme</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.levenshtein">
<span class="sig-name descname"><span class="pre">levenshtein</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.levenshtein" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The number of single-character edits between two strings. Arguments: s2. SQL: <cite>levenshtein</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.like_escape">
<span class="sig-name descname"><span class="pre">like_escape</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.like_escape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether it matches the pattern. Arguments: like_specifier, escape_character. SQL: <cite>like_escape</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.lower">
<span class="sig-name descname"><span class="pre">lower</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.lower" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts <cite>string</cite> to lower case. SQL: <cite>lower</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.lpad">
<span class="sig-name descname"><span class="pre">lpad</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.lpad" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Padded on the left with the character, to a total length. Arguments: count, character. SQL: <cite>lpad</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.ltrim">
<span class="sig-name descname"><span class="pre">ltrim</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.ltrim" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Trimmed on the left of any of the characters, spaces by default. SQL: <cite>ltrim</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.md5">
<span class="sig-name descname"><span class="pre">md5</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.md5" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the MD5 hash of the <cite>string</cite> as a <cite>VARCHAR</cite>. SQL: <cite>md5</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.md5_number">
<span class="sig-name descname"><span class="pre">md5_number</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.md5_number" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the MD5 hash of the <cite>string</cite> as a <cite>HUGEINT</cite>. SQL: <cite>md5_number</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.nfc_normalize">
<span class="sig-name descname"><span class="pre">nfc_normalize</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.nfc_normalize" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts <cite>string</cite> to Unicode NFC normalized string. SQL: <cite>nfc_normalize</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.not_ilike_escape">
<span class="sig-name descname"><span class="pre">not_ilike_escape</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.not_ilike_escape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Does not match, ignoring case. Arguments: like_specifier, escape_character. SQL: <cite>not_ilike_escape</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.not_like_escape">
<span class="sig-name descname"><span class="pre">not_like_escape</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.not_like_escape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Does not match the pattern. Arguments: like_specifier, escape_character. SQL: <cite>not_like_escape</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.overlay">
<span class="sig-name descname"><span class="pre">overlay</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.overlay" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The replacement written over the string, at a position. Arguments: replacement, start. SQL: <cite>overlay</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.parse_dirname">
<span class="sig-name descname"><span class="pre">parse_dirname</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.parse_dirname" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the top-level directory name from the given <cite>path</cite>. SQL: <cite>parse_dirname</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.parse_dirpath">
<span class="sig-name descname"><span class="pre">parse_dirpath</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.parse_dirpath" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The path up to the last separator, as Python&#8217;s os.path.dirname gives it. SQL: <cite>parse_dirpath</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.parse_filename">
<span class="sig-name descname"><span class="pre">parse_filename</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.parse_filename" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The last component of the path, optionally without its extension. SQL: <cite>parse_filename</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.parse_formatted_bytes">
<span class="sig-name descname"><span class="pre">parse_formatted_bytes</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.parse_formatted_bytes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A human-readable size such as &#8216;4KB&#8217; as a number of bytes. SQL: <cite>parse_formatted_bytes</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.parse_path">
<span class="sig-name descname"><span class="pre">parse_path</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.parse_path" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The path split into its directories and filename. SQL: <cite>parse_path</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.path_join">
<span class="sig-name descname"><span class="pre">path_join</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.path_join" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The path components joined with the platform&#8217;s separator. SQL: <cite>path_join</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.prefix">
<span class="sig-name descname"><span class="pre">prefix</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.prefix" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns <cite>true</cite> if <cite>string</cite> starts with <cite>search_string</cite>. Arguments: search_string. SQL: <cite>prefix</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.printf">
<span class="sig-name descname"><span class="pre">printf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.printf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Formats a <cite>string</cite> using printf syntax. SQL: <cite>printf</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.regexp_escape">
<span class="sig-name descname"><span class="pre">regexp_escape</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.regexp_escape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The string escaped so it matches itself as a regular expression. SQL: <cite>regexp_escape</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.regexp_extract">
<span class="sig-name descname"><span class="pre">regexp_extract</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.regexp_extract" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first match of the pattern, or an empty string. Arguments: regex. SQL: <cite>regexp_extract</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.regexp_extract_all">
<span class="sig-name descname"><span class="pre">regexp_extract_all</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.regexp_extract_all" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Every match of the pattern, as a list. Arguments: regex. SQL: <cite>regexp_extract_all</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.regexp_full_match">
<span class="sig-name descname"><span class="pre">regexp_full_match</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.regexp_full_match" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns <cite>true</cite> if the entire <cite>string</cite> matches the <cite>regex</cite>. Arguments: regex. SQL: <cite>regexp_full_match</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.regexp_matches">
<span class="sig-name descname"><span class="pre">regexp_matches</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.regexp_matches" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether the pattern matches anywhere in the string. Arguments: regex. SQL: <cite>regexp_matches</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.regexp_replace">
<span class="sig-name descname"><span class="pre">regexp_replace</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.regexp_replace" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first match of the pattern replaced. Arguments: regex, replacement. SQL: <cite>regexp_replace</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.replace">
<span class="sig-name descname"><span class="pre">replace</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.replace" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Every occurrence of the source replaced by the target. Arguments: source, target. SQL: <cite>replace</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.reverse">
<span class="sig-name descname"><span class="pre">reverse</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.reverse" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reverses the <cite>string</cite>. SQL: <cite>reverse</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.right">
<span class="sig-name descname"><span class="pre">right</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.right" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the right-most <cite>count</cite> characters. Arguments: count. SQL: <cite>right</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.right_grapheme">
<span class="sig-name descname"><span class="pre">right_grapheme</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.right_grapheme" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extracts the right-most <cite>count</cite> grapheme clusters. Arguments: count. SQL: <cite>right_grapheme</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.rpad">
<span class="sig-name descname"><span class="pre">rpad</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.rpad" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Padded on the right with the character, to a total length. Arguments: count, character. SQL: <cite>rpad</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.rtrim">
<span class="sig-name descname"><span class="pre">rtrim</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.rtrim" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Trimmed on the right of any of the characters, spaces by default. SQL: <cite>rtrim</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.sha1">
<span class="sig-name descname"><span class="pre">sha1</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.sha1" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns a <cite>VARCHAR</cite> with the SHA-1 hash of the <cite>value</cite>. SQL: <cite>sha1</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.sha256">
<span class="sig-name descname"><span class="pre">sha256</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.sha256" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns a <cite>VARCHAR</cite> with the SHA-256 hash of the <cite>value</cite>. SQL: <cite>sha256</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.string_split">
<span class="sig-name descname"><span class="pre">string_split</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.string_split" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Splits the <cite>string</cite> along the <cite>separator</cite>. Arguments: separator. SQL: <cite>string_split</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.string_split_regex">
<span class="sig-name descname"><span class="pre">string_split_regex</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.string_split_regex" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Splits the <cite>string</cite> along the <cite>regex</cite>. Arguments: regex. SQL: <cite>string_split_regex</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.strip_accents">
<span class="sig-name descname"><span class="pre">strip_accents</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.strip_accents" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Strips accents from <cite>string</cite>. SQL: <cite>strip_accents</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.strlen">
<span class="sig-name descname"><span class="pre">strlen</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.strlen" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Number of bytes in <cite>string</cite>. SQL: <cite>strlen</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.substring">
<span class="sig-name descname"><span class="pre">substring</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.substring" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The rest of the string from a start position. Arguments: start. SQL: <cite>substring</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.substring_grapheme">
<span class="sig-name descname"><span class="pre">substring_grapheme</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.substring_grapheme" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The rest of the string, counting grapheme clusters. Arguments: start. SQL: <cite>substring_grapheme</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.suffix">
<span class="sig-name descname"><span class="pre">suffix</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.suffix" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns <cite>true</cite> if <cite>string</cite> ends with <cite>search_string</cite>. Arguments: search_string. SQL: <cite>suffix</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.translate">
<span class="sig-name descname"><span class="pre">translate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.translate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Each character in <cite>from</cite> replaced by the one in <cite>to</cite>. Arguments: from, to. SQL: <cite>translate</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.trim">
<span class="sig-name descname"><span class="pre">trim</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.trim" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Trimmed on both sides of any of the characters, spaces by default. SQL: <cite>trim</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.unbin">
<span class="sig-name descname"><span class="pre">unbin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.unbin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts a <cite>value</cite> from binary representation to a blob. SQL: <cite>unbin</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.unhex">
<span class="sig-name descname"><span class="pre">unhex</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.unhex" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts a <cite>value</cite> from hexadecimal representation to a blob. SQL: <cite>unhex</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.unicode">
<span class="sig-name descname"><span class="pre">unicode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.unicode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The Unicode code point of the first character, as an INTEGER. SQL: <cite>unicode</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.upper">
<span class="sig-name descname"><span class="pre">upper</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.upper" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts <cite>string</cite> to upper case. SQL: <cite>upper</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.url_decode">
<span class="sig-name descname"><span class="pre">url_decode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.url_decode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Decodes a URL from a representation using Percent-Encoding. SQL: <cite>url_decode</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.StrExpr.url_encode">
<span class="sig-name descname"><span class="pre">url_encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.StrExpr.url_encode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Encodes a URL to a representation using Percent-Encoding. SQL: <cite>url_encode</cite>.</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb._expression_namespaces.</span></span><span class="sig-name descname"><span class="pre">DtExpr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Date and time functions, applied to this expression as the date, time or timestamp.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.SPEC">
<span class="sig-name descname"><span class="pre">SPEC</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">ClassVar</span><span class="p"><span class="pre">[</span></span><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">int</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">{'age':</span> <span class="pre">('age',</span> <span class="pre">0,</span> <span class="pre">['TIMESTAMP']),</span> <span class="pre">'century':</span> <span class="pre">('century',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'day':</span> <span class="pre">('day',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'dayname':</span> <span class="pre">('dayname',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'dayofmonth':</span> <span class="pre">('dayofmonth',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'dayofweek':</span> <span class="pre">('dayofweek',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'dayofyear':</span> <span class="pre">('dayofyear',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'days_in_month':</span> <span class="pre">('days_in_month',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'decade':</span> <span class="pre">('decade',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'diff':</span> <span class="pre">('date_diff',</span> <span class="pre">1,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'DATE',</span> <span class="pre">'DATE']),</span> <span class="pre">'epoch':</span> <span class="pre">('epoch',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'epoch_ns':</span> <span class="pre">('epoch_ns',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'epoch_us':</span> <span class="pre">('epoch_us',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'era':</span> <span class="pre">('era',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'hour':</span> <span class="pre">('hour',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'isodow':</span> <span class="pre">('isodow',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'isoyear':</span> <span class="pre">('isoyear',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'julian':</span> <span class="pre">('julian',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'last_day':</span> <span class="pre">('last_day',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'microsecond':</span> <span class="pre">('microsecond',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'millennium':</span> <span class="pre">('millennium',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'millisecond':</span> <span class="pre">('millisecond',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'minute':</span> <span class="pre">('minute',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'month':</span> <span class="pre">('month',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'monthname':</span> <span class="pre">('monthname',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'nanosecond':</span> <span class="pre">('nanosecond',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'normalized_interval':</span> <span class="pre">('normalized_interval',</span> <span class="pre">0,</span> <span class="pre">['INTERVAL']),</span> <span class="pre">'part':</span> <span class="pre">('date_part',</span> <span class="pre">1,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'DATE']),</span> <span class="pre">'quarter':</span> <span class="pre">('quarter',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'second':</span> <span class="pre">('second',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'strftime':</span> <span class="pre">('strftime',</span> <span class="pre">0,</span> <span class="pre">['DATE',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'sub':</span> <span class="pre">('date_sub',</span> <span class="pre">1,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'DATE',</span> <span class="pre">'DATE']),</span> <span class="pre">'time_bucket':</span> <span class="pre">('time_bucket',</span> <span class="pre">1,</span> <span class="pre">['INTERVAL',</span> <span class="pre">'DATE']),</span> <span class="pre">'timetz_byte_comparable':</span> <span class="pre">('timetz_byte_comparable',</span> <span class="pre">0,</span> <span class="pre">['TIME</span> <span class="pre">WITH</span> <span class="pre">TIME</span> <span class="pre">ZONE']),</span> <span class="pre">'timezone':</span> <span class="pre">('timezone',</span> <span class="pre">0,</span> <span class="pre">['TIMESTAMP']),</span> <span class="pre">'timezone_hour':</span> <span class="pre">('timezone_hour',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'timezone_minute':</span> <span class="pre">('timezone_minute',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'trunc':</span> <span class="pre">('date_trunc',</span> <span class="pre">1,</span> <span class="pre">['VARCHAR',</span> <span class="pre">'DATE']),</span> <span class="pre">'week':</span> <span class="pre">('week',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'weekday':</span> <span class="pre">('weekday',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'weekofyear':</span> <span class="pre">('weekofyear',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'year':</span> <span class="pre">('year',</span> <span class="pre">0,</span> <span class="pre">['DATE']),</span> <span class="pre">'yearweek':</span> <span class="pre">('yearweek',</span> <span class="pre">0,</span> <span class="pre">['DATE'])}</span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.SPEC" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Method name to (function, position of the expression, parameter types).</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.age">
<span class="sig-name descname"><span class="pre">age</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.DtExpr" title="duckdb._expression_namespaces.DtExpr"><span class="pre">DtExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.age" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The time between two timestamps, or between one and now. SQL: <cite>age</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.century">
<span class="sig-name descname"><span class="pre">century</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.century" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the century component from a date or timestamp. SQL: <cite>century</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.day">
<span class="sig-name descname"><span class="pre">day</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.day" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the day component from a date or timestamp. SQL: <cite>day</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.dayname">
<span class="sig-name descname"><span class="pre">dayname</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.dayname" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The (English) name of the weekday. SQL: <cite>dayname</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.dayofmonth">
<span class="sig-name descname"><span class="pre">dayofmonth</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.dayofmonth" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the dayofmonth component from a date or timestamp. SQL: <cite>dayofmonth</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.dayofweek">
<span class="sig-name descname"><span class="pre">dayofweek</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.dayofweek" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the dayofweek component from a date or timestamp. SQL: <cite>dayofweek</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.dayofyear">
<span class="sig-name descname"><span class="pre">dayofyear</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.dayofyear" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the dayofyear component from a date or timestamp. SQL: <cite>dayofyear</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.days_in_month">
<span class="sig-name descname"><span class="pre">days_in_month</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.days_in_month" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many days the date&#8217;s month has. SQL: <cite>days_in_month</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.decade">
<span class="sig-name descname"><span class="pre">decade</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.decade" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the decade component from a date or timestamp. SQL: <cite>decade</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.diff">
<span class="sig-name descname"><span class="pre">diff</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">part</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.diff" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The number of partition boundaries between the timestamps. Arguments: part, enddate. SQL: <cite>date_diff</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.epoch">
<span class="sig-name descname"><span class="pre">epoch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.epoch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the epoch component from a temporal type. SQL: <cite>epoch</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.epoch_ns">
<span class="sig-name descname"><span class="pre">epoch_ns</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.epoch_ns" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the epoch component in nanoseconds from a temporal type. SQL: <cite>epoch_ns</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.epoch_us">
<span class="sig-name descname"><span class="pre">epoch_us</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.epoch_us" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the epoch component in microseconds from a temporal type. SQL: <cite>epoch_us</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.era">
<span class="sig-name descname"><span class="pre">era</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.era" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the era component from a date or timestamp. SQL: <cite>era</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.hour">
<span class="sig-name descname"><span class="pre">hour</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.hour" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the hour component from a date or timestamp. SQL: <cite>hour</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.isodow">
<span class="sig-name descname"><span class="pre">isodow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.isodow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the isodow component from a date or timestamp. SQL: <cite>isodow</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.isoyear">
<span class="sig-name descname"><span class="pre">isoyear</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.isoyear" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the isoyear component from a date or timestamp. SQL: <cite>isoyear</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.julian">
<span class="sig-name descname"><span class="pre">julian</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.julian" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the Julian Day number from a date or timestamp. SQL: <cite>julian</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.last_day">
<span class="sig-name descname"><span class="pre">last_day</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.DtExpr" title="duckdb._expression_namespaces.DtExpr"><span class="pre">DtExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.last_day" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the last day of the month. SQL: <cite>last_day</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.microsecond">
<span class="sig-name descname"><span class="pre">microsecond</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.microsecond" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the microsecond component from a date or timestamp. SQL: <cite>microsecond</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.millennium">
<span class="sig-name descname"><span class="pre">millennium</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.millennium" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the millennium component from a date or timestamp. SQL: <cite>millennium</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.millisecond">
<span class="sig-name descname"><span class="pre">millisecond</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.millisecond" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the millisecond component from a date or timestamp. SQL: <cite>millisecond</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.minute">
<span class="sig-name descname"><span class="pre">minute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.minute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the minute component from a date or timestamp. SQL: <cite>minute</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.month">
<span class="sig-name descname"><span class="pre">month</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.month" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the month component from a date or timestamp. SQL: <cite>month</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.monthname">
<span class="sig-name descname"><span class="pre">monthname</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.monthname" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The (English) name of the month. SQL: <cite>monthname</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.nanosecond">
<span class="sig-name descname"><span class="pre">nanosecond</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.nanosecond" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the nanosecond component from a date or timestamp. SQL: <cite>nanosecond</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.normalized_interval">
<span class="sig-name descname"><span class="pre">normalized_interval</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.DtExpr" title="duckdb._expression_namespaces.DtExpr"><span class="pre">DtExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.normalized_interval" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Normalizes an INTERVAL to an equivalent interval. SQL: <cite>normalized_interval</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.part">
<span class="sig-name descname"><span class="pre">part</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">part</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.part" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get subfield (equivalent to extract). Arguments: part. SQL: <cite>date_part</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.quarter">
<span class="sig-name descname"><span class="pre">quarter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.quarter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the quarter component from a date or timestamp. SQL: <cite>quarter</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.second">
<span class="sig-name descname"><span class="pre">second</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.second" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the second component from a date or timestamp. SQL: <cite>second</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.strftime">
<span class="sig-name descname"><span class="pre">strftime</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.strftime" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Format as text, with a strftime pattern. Arguments: format. SQL: <cite>strftime</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.sub">
<span class="sig-name descname"><span class="pre">sub</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">part</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.sub" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The number of complete partitions between the timestamps. Arguments: part, enddate. SQL: <cite>date_sub</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.time_bucket">
<span class="sig-name descname"><span class="pre">time_bucket</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bucket_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.DtExpr" title="duckdb._expression_namespaces.DtExpr"><span class="pre">DtExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.time_bucket" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Truncate TIMESTAMPTZ by the specified interval bucket_width. Arguments: bucket_width. SQL: <cite>time_bucket</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.timetz_byte_comparable">
<span class="sig-name descname"><span class="pre">timetz_byte_comparable</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.timetz_byte_comparable" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Converts a TIME WITH TIME ZONE to an integer sort key. SQL: <cite>timetz_byte_comparable</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.timezone">
<span class="sig-name descname"><span class="pre">timezone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.timezone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The time zone offset, in seconds. SQL: <cite>timezone</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.timezone_hour">
<span class="sig-name descname"><span class="pre">timezone_hour</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.timezone_hour" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the timezone_hour component from a date or timestamp. SQL: <cite>timezone_hour</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.timezone_minute">
<span class="sig-name descname"><span class="pre">timezone_minute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.timezone_minute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the timezone_minute component from a date or timestamp. SQL: <cite>timezone_minute</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.trunc">
<span class="sig-name descname"><span class="pre">trunc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">part</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.DtExpr" title="duckdb._expression_namespaces.DtExpr"><span class="pre">DtExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.trunc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Truncate to specified precision. Arguments: part. SQL: <cite>date_trunc</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.week">
<span class="sig-name descname"><span class="pre">week</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.week" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the week component from a date or timestamp. SQL: <cite>week</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.weekday">
<span class="sig-name descname"><span class="pre">weekday</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.weekday" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the weekday component from a date or timestamp. SQL: <cite>weekday</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.weekofyear">
<span class="sig-name descname"><span class="pre">weekofyear</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.weekofyear" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the weekofyear component from a date or timestamp. SQL: <cite>weekofyear</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.year">
<span class="sig-name descname"><span class="pre">year</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.year" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the year component from a date or timestamp. SQL: <cite>year</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.DtExpr.yearweek">
<span class="sig-name descname"><span class="pre">yearweek</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.DtExpr.yearweek" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the yearweek component from a date or timestamp. SQL: <cite>yearweek</cite>.</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb._expression_namespaces.</span></span><span class="sig-name descname"><span class="pre">ListExpr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>List functions, applied to this expression as the list. A callable argument is given expressions, not values.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.SPEC">
<span class="sig-name descname"><span class="pre">SPEC</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">ClassVar</span><span class="p"><span class="pre">[</span></span><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">int</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">{'aggregate':</span> <span class="pre">('list_aggregate',</span> <span class="pre">0,</span> <span class="pre">['ANY[]',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'any_value':</span> <span class="pre">('list_any_value',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'append':</span> <span class="pre">('list_append',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'approx_count_distinct':</span> <span class="pre">('list_approx_count_distinct',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'avg':</span> <span class="pre">('list_avg',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'bit_and':</span> <span class="pre">('list_bit_and',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'bit_or':</span> <span class="pre">('list_bit_or',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'bit_xor':</span> <span class="pre">('list_bit_xor',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'bool_and':</span> <span class="pre">('list_bool_and',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'bool_or':</span> <span class="pre">('list_bool_or',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'contains':</span> <span class="pre">('list_contains',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'T']),</span> <span class="pre">'cosine_distance':</span> <span class="pre">('list_cosine_distance',</span> <span class="pre">0,</span> <span class="pre">['DOUBLE[]',</span> <span class="pre">'DOUBLE[]']),</span> <span class="pre">'cosine_similarity':</span> <span class="pre">('list_cosine_similarity',</span> <span class="pre">0,</span> <span class="pre">['DOUBLE[]',</span> <span class="pre">'DOUBLE[]']),</span> <span class="pre">'count':</span> <span class="pre">('list_count',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'distance':</span> <span class="pre">('list_distance',</span> <span class="pre">0,</span> <span class="pre">['DOUBLE[]',</span> <span class="pre">'DOUBLE[]']),</span> <span class="pre">'distinct':</span> <span class="pre">('list_distinct',</span> <span class="pre">0,</span> <span class="pre">['T[]']),</span> <span class="pre">'entropy':</span> <span class="pre">('list_entropy',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'extract':</span> <span class="pre">('list_extract',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'BIGINT']),</span> <span class="pre">'filter':</span> <span class="pre">('list_filter',</span> <span class="pre">0,</span> <span class="pre">['ANY[]',</span> <span class="pre">'LAMBDA']),</span> <span class="pre">'first':</span> <span class="pre">('list_first',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'flatten':</span> <span class="pre">('flatten',</span> <span class="pre">0,</span> <span class="pre">['T[][]']),</span> <span class="pre">'grade_up':</span> <span class="pre">('list_grade_up',</span> <span class="pre">0,</span> <span class="pre">['ANY[]']),</span> <span class="pre">'has_all':</span> <span class="pre">('list_has_all',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'T[]']),</span> <span class="pre">'has_any':</span> <span class="pre">('list_has_any',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'T[]']),</span> <span class="pre">'histogram':</span> <span class="pre">('list_histogram',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'inner_product':</span> <span class="pre">('list_inner_product',</span> <span class="pre">0,</span> <span class="pre">['DOUBLE[]',</span> <span class="pre">'DOUBLE[]']),</span> <span class="pre">'intersect':</span> <span class="pre">('list_intersect',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'T[]']),</span> <span class="pre">'kurtosis':</span> <span class="pre">('list_kurtosis',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'kurtosis_pop':</span> <span class="pre">('list_kurtosis_pop',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'last':</span> <span class="pre">('list_last',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'mad':</span> <span class="pre">('list_mad',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'mask':</span> <span class="pre">('list_where',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'BOOLEAN[]']),</span> <span class="pre">'max':</span> <span class="pre">('list_max',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'median':</span> <span class="pre">('list_median',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'min':</span> <span class="pre">('list_min',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'mode':</span> <span class="pre">('list_mode',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'negative_inner_product':</span> <span class="pre">('list_negative_inner_product',</span> <span class="pre">0,</span> <span class="pre">['DOUBLE[]',</span> <span class="pre">'DOUBLE[]']),</span> <span class="pre">'position':</span> <span class="pre">('list_position',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'T']),</span> <span class="pre">'prepend':</span> <span class="pre">('list_prepend',</span> <span class="pre">1,</span> <span class="pre">[]),</span> <span class="pre">'product':</span> <span class="pre">('list_product',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'reduce':</span> <span class="pre">('list_reduce',</span> <span class="pre">0,</span> <span class="pre">['ANY[]',</span> <span class="pre">'LAMBDA']),</span> <span class="pre">'resize':</span> <span class="pre">('list_resize',</span> <span class="pre">0,</span> <span class="pre">['ANY[]',</span> <span class="pre">'ANY']),</span> <span class="pre">'reverse':</span> <span class="pre">('list_reverse',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'reverse_sort':</span> <span class="pre">('list_reverse_sort',</span> <span class="pre">0,</span> <span class="pre">['ANY[]']),</span> <span class="pre">'select':</span> <span class="pre">('list_select',</span> <span class="pre">0,</span> <span class="pre">['T[]',</span> <span class="pre">'BIGINT[]']),</span> <span class="pre">'sem':</span> <span class="pre">('list_sem',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'skewness':</span> <span class="pre">('list_skewness',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'sort':</span> <span class="pre">('list_sort',</span> <span class="pre">0,</span> <span class="pre">['ANY[]']),</span> <span class="pre">'stddev_pop':</span> <span class="pre">('list_stddev_pop',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'stddev_samp':</span> <span class="pre">('list_stddev_samp',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'string_agg':</span> <span class="pre">('list_string_agg',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'sum':</span> <span class="pre">('list_sum',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'transform':</span> <span class="pre">('list_transform',</span> <span class="pre">0,</span> <span class="pre">['ANY[]',</span> <span class="pre">'LAMBDA']),</span> <span class="pre">'unique':</span> <span class="pre">('list_unique',</span> <span class="pre">0,</span> <span class="pre">['ANY[]']),</span> <span class="pre">'var_pop':</span> <span class="pre">('list_var_pop',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'var_samp':</span> <span class="pre">('list_var_samp',</span> <span class="pre">0,</span> <span class="pre">[])}</span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.SPEC" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Method name to (function, position of the expression, parameter types).</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.aggregate">
<span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.aggregate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The named aggregate applied to the elements. Arguments: function_name. SQL: <cite>list_aggregate</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.any_value">
<span class="sig-name descname"><span class="pre">any_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.any_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Any one element, whichever is cheapest. SQL: <cite>list_any_value</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.append">
<span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.append" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>list_append</cite> function. Arguments: e. SQL: <cite>list_append</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.approx_count_distinct">
<span class="sig-name descname"><span class="pre">approx_count_distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.approx_count_distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>An approximate count of the distinct elements. SQL: <cite>list_approx_count_distinct</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.avg">
<span class="sig-name descname"><span class="pre">avg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.avg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The average of the elements. SQL: <cite>list_avg</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.bit_and">
<span class="sig-name descname"><span class="pre">bit_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.bit_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The bitwise AND of the elements. SQL: <cite>list_bit_and</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.bit_or">
<span class="sig-name descname"><span class="pre">bit_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.bit_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The bitwise OR of the elements. SQL: <cite>list_bit_or</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.bit_xor">
<span class="sig-name descname"><span class="pre">bit_xor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.bit_xor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The bitwise XOR of the elements. SQL: <cite>list_bit_xor</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.bool_and">
<span class="sig-name descname"><span class="pre">bool_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.bool_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether every element is true. SQL: <cite>list_bool_and</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.bool_or">
<span class="sig-name descname"><span class="pre">bool_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.bool_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether any element is true. SQL: <cite>list_bool_or</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.contains">
<span class="sig-name descname"><span class="pre">contains</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.contains" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns true if the list contains the element. Arguments: element. SQL: <cite>list_contains</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.cosine_distance">
<span class="sig-name descname"><span class="pre">cosine_distance</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.cosine_distance" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the cosine distance between two same-sized lists. Arguments: list2. SQL: <cite>list_cosine_distance</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.cosine_similarity">
<span class="sig-name descname"><span class="pre">cosine_similarity</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.cosine_similarity" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The cosine similarity of two lists of numbers. Arguments: list2. SQL: <cite>list_cosine_similarity</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.count">
<span class="sig-name descname"><span class="pre">count</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.count" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many elements are not NULL. SQL: <cite>list_count</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.distance">
<span class="sig-name descname"><span class="pre">distance</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.distance" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The Euclidean distance between two lists of numbers. Arguments: list2. SQL: <cite>list_distance</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.distinct">
<span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Removes all duplicates and <cite>NULL</cite> values from a list. SQL: <cite>list_distinct</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.entropy">
<span class="sig-name descname"><span class="pre">entropy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.entropy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The entropy of the elements. SQL: <cite>list_entropy</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.extract">
<span class="sig-name descname"><span class="pre">extract</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.extract" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the <cite>index`th (1-based) value from the list. Arguments: index. SQL: `list_extract</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.filter">
<span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.filter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The elements the function holds for: <cite>lambda x: x &gt; 0</cite>. SQL: <cite>list_filter</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.first">
<span class="sig-name descname"><span class="pre">first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The first element. SQL: <cite>list_first</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.flatten">
<span class="sig-name descname"><span class="pre">flatten</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.flatten" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Flattens a nested list by one level. SQL: <cite>flatten</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.grade_up">
<span class="sig-name descname"><span class="pre">grade_up</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.grade_up" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The positions the elements would take once sorted, rather than the elements. SQL: <cite>list_grade_up</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.has_all">
<span class="sig-name descname"><span class="pre">has_all</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.has_all" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns true if all elements of list2 are in list1. Arguments: list2. SQL: <cite>list_has_all</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.has_any">
<span class="sig-name descname"><span class="pre">has_any</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.has_any" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns true if the lists have any element in common. Arguments: list2. SQL: <cite>list_has_any</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.histogram">
<span class="sig-name descname"><span class="pre">histogram</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.histogram" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How often each element occurs, as a map. SQL: <cite>list_histogram</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.inner_product">
<span class="sig-name descname"><span class="pre">inner_product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.inner_product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the inner product between two same-sized lists. Arguments: list2. SQL: <cite>list_inner_product</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.intersect">
<span class="sig-name descname"><span class="pre">intersect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.intersect" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The distinct elements present in both lists. Arguments: list2. SQL: <cite>list_intersect</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.kurtosis">
<span class="sig-name descname"><span class="pre">kurtosis</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.kurtosis" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The kurtosis of the elements. SQL: <cite>list_kurtosis</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.kurtosis_pop">
<span class="sig-name descname"><span class="pre">kurtosis_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.kurtosis_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The population kurtosis of the elements. SQL: <cite>list_kurtosis_pop</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.last">
<span class="sig-name descname"><span class="pre">last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The last element. SQL: <cite>list_last</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.mad">
<span class="sig-name descname"><span class="pre">mad</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.mad" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The median absolute deviation of the elements. SQL: <cite>list_mad</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.mask">
<span class="sig-name descname"><span class="pre">mask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.mask" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The elements where the matching boolean is true. Arguments: mask_list. SQL: <cite>list_where</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.max">
<span class="sig-name descname"><span class="pre">max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The largest element. SQL: <cite>list_max</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.median">
<span class="sig-name descname"><span class="pre">median</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.median" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The middle element. SQL: <cite>list_median</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.min">
<span class="sig-name descname"><span class="pre">min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The smallest element. SQL: <cite>list_min</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.mode">
<span class="sig-name descname"><span class="pre">mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.mode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The most frequent element. SQL: <cite>list_mode</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.negative_inner_product">
<span class="sig-name descname"><span class="pre">negative_inner_product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.negative_inner_product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The inner product of two lists, negated. Arguments: list2. SQL: <cite>list_negative_inner_product</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.position">
<span class="sig-name descname"><span class="pre">position</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.position" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The index of the element, or NULL when absent. Arguments: element. SQL: <cite>list_position</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.prepend">
<span class="sig-name descname"><span class="pre">prepend</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">e</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.prepend" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>list_prepend</cite> function. Arguments: e. SQL: <cite>list_prepend</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.product">
<span class="sig-name descname"><span class="pre">product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The product of the elements. SQL: <cite>list_product</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.reduce">
<span class="sig-name descname"><span class="pre">reduce</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.reduce" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The list folded to one value, left to right: <cite>lambda acc, x: acc + x</cite>. SQL: <cite>list_reduce</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.resize">
<span class="sig-name descname"><span class="pre">resize</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.resize" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Resizes the <cite>list</cite> to contain <cite>size</cite> elements. Arguments: size. SQL: <cite>list_resize</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.reverse">
<span class="sig-name descname"><span class="pre">reverse</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.reverse" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The elements in reverse order. SQL: <cite>list_reverse</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.reverse_sort">
<span class="sig-name descname"><span class="pre">reverse_sort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.reverse_sort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Sorts the elements of the list in reverse order. SQL: <cite>list_reverse_sort</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.select">
<span class="sig-name descname"><span class="pre">select</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.select" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The elements at the given indexes. Arguments: index_list. SQL: <cite>list_select</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.sem">
<span class="sig-name descname"><span class="pre">sem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.sem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The standard error of the mean of the elements. SQL: <cite>list_sem</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.skewness">
<span class="sig-name descname"><span class="pre">skewness</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.skewness" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The skewness of the elements. SQL: <cite>list_skewness</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.sort">
<span class="sig-name descname"><span class="pre">sort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.sort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Sorts the elements of the list. SQL: <cite>list_sort</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.stddev_pop">
<span class="sig-name descname"><span class="pre">stddev_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.stddev_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The population standard deviation of the elements. SQL: <cite>list_stddev_pop</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.stddev_samp">
<span class="sig-name descname"><span class="pre">stddev_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.stddev_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The sample standard deviation of the elements. SQL: <cite>list_stddev_samp</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.string_agg">
<span class="sig-name descname"><span class="pre">string_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.string_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The elements joined as text, separated by commas. SQL: <cite>list_string_agg</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.sum">
<span class="sig-name descname"><span class="pre">sum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.sum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The sum of the elements. SQL: <cite>list_sum</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.transform">
<span class="sig-name descname"><span class="pre">transform</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.transform" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Each element through the function: <cite>lambda x: x * 2</cite>. SQL: <cite>list_transform</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.unique">
<span class="sig-name descname"><span class="pre">unique</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.unique" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Counts the unique elements of a <cite>list</cite>. SQL: <cite>list_unique</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.var_pop">
<span class="sig-name descname"><span class="pre">var_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.var_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The population variance of the elements. SQL: <cite>list_var_pop</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.ListExpr.var_samp">
<span class="sig-name descname"><span class="pre">var_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.ListExpr.var_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The sample variance of the elements. SQL: <cite>list_var_samp</cite>.</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb._expression_namespaces.</span></span><span class="sig-name descname"><span class="pre">JsonExpr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>JSON functions, applied to this expression as the document.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.SPEC">
<span class="sig-name descname"><span class="pre">SPEC</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">ClassVar</span><span class="p"><span class="pre">[</span></span><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">tuple</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">int</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span><span class="p"><span class="pre">]</span></span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">{'array_length':</span> <span class="pre">('json_array_length',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'contains':</span> <span class="pre">('json_contains',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'JSON']),</span> <span class="pre">'deep_merge':</span> <span class="pre">('json_deep_merge',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'JSON']),</span> <span class="pre">'exists':</span> <span class="pre">('json_exists',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'extract':</span> <span class="pre">('json_extract',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'extract_path':</span> <span class="pre">('json_extract_path',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'extract_path_text':</span> <span class="pre">('json_extract_path_text',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'extract_string':</span> <span class="pre">('json_extract_string',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'insert':</span> <span class="pre">('json_insert',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'JSON']),</span> <span class="pre">'keys':</span> <span class="pre">('json_keys',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'merge_patch_diff':</span> <span class="pre">('json_merge_patch_diff',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'JSON']),</span> <span class="pre">'normalize':</span> <span class="pre">('json_normalize',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'parse':</span> <span class="pre">('json',</span> <span class="pre">0,</span> <span class="pre">[]),</span> <span class="pre">'pretty':</span> <span class="pre">('json_pretty',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'remove':</span> <span class="pre">('json_remove',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'replace':</span> <span class="pre">('json_replace',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'JSON']),</span> <span class="pre">'set':</span> <span class="pre">('json_set',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR',</span> <span class="pre">'JSON']),</span> <span class="pre">'strip_nulls':</span> <span class="pre">('json_strip_nulls',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'structure':</span> <span class="pre">('json_structure',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'transform':</span> <span class="pre">('json_transform',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'transform_strict':</span> <span class="pre">('json_transform_strict',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR']),</span> <span class="pre">'type':</span> <span class="pre">('json_type',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'valid':</span> <span class="pre">('json_valid',</span> <span class="pre">0,</span> <span class="pre">['JSON']),</span> <span class="pre">'value':</span> <span class="pre">('json_value',</span> <span class="pre">0,</span> <span class="pre">['JSON',</span> <span class="pre">'VARCHAR'])}</span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.SPEC" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Method name to (function, position of the expression, parameter types).</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.array_length">
<span class="sig-name descname"><span class="pre">array_length</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.array_length" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>How many elements the array holds. SQL: <cite>json_array_length</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.contains">
<span class="sig-name descname"><span class="pre">contains</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.contains" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_contains</cite> function. Arguments: needle. SQL: <cite>json_contains</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.deep_merge">
<span class="sig-name descname"><span class="pre">deep_merge</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.deep_merge" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_deep_merge</cite> function. Arguments: json2. SQL: <cite>json_deep_merge</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.exists">
<span class="sig-name descname"><span class="pre">exists</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.exists" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_exists</cite> function. Arguments: path. SQL: <cite>json_exists</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.extract">
<span class="sig-name descname"><span class="pre">extract</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.extract" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_extract</cite> function. Arguments: path. SQL: <cite>json_extract</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.extract_path">
<span class="sig-name descname"><span class="pre">extract_path</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.extract_path" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_extract_path</cite> function. Arguments: path. SQL: <cite>json_extract_path</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.extract_path_text">
<span class="sig-name descname"><span class="pre">extract_path_text</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.extract_path_text" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_extract_path_text</cite> function. Arguments: path. SQL: <cite>json_extract_path_text</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.extract_string">
<span class="sig-name descname"><span class="pre">extract_string</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.extract_string" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_extract_string</cite> function. Arguments: path. SQL: <cite>json_extract_string</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.insert">
<span class="sig-name descname"><span class="pre">insert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.insert" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_insert</cite> function. Arguments: path, value. SQL: <cite>json_insert</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.keys">
<span class="sig-name descname"><span class="pre">keys</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.ListExpr" title="duckdb._expression_namespaces.ListExpr"><span class="pre">ListExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.keys" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The keys of the object, as a list. SQL: <cite>json_keys</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.merge_patch_diff">
<span class="sig-name descname"><span class="pre">merge_patch_diff</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.merge_patch_diff" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_merge_patch_diff</cite> function. Arguments: new. SQL: <cite>json_merge_patch_diff</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.normalize">
<span class="sig-name descname"><span class="pre">normalize</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.normalize" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The document minified, with object keys sorted. SQL: <cite>json_normalize</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.parse">
<span class="sig-name descname"><span class="pre">parse</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.parse" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The text parsed as a JSON document, minified. SQL: <cite>json</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.pretty">
<span class="sig-name descname"><span class="pre">pretty</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.pretty" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The document printed with indentation. SQL: <cite>json_pretty</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.remove">
<span class="sig-name descname"><span class="pre">remove</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.remove" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_remove</cite> function. Arguments: path. SQL: <cite>json_remove</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.replace">
<span class="sig-name descname"><span class="pre">replace</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.replace" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_replace</cite> function. Arguments: path, value. SQL: <cite>json_replace</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.set">
<span class="sig-name descname"><span class="pre">set</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.set" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_set</cite> function. Arguments: path, value. SQL: <cite>json_set</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.strip_nulls">
<span class="sig-name descname"><span class="pre">strip_nulls</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.strip_nulls" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The document without its null-valued object fields. SQL: <cite>json_strip_nulls</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.structure">
<span class="sig-name descname"><span class="pre">structure</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.JsonExpr" title="duckdb._expression_namespaces.JsonExpr"><span class="pre">JsonExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.structure" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The shape of the document, with types in place of values. SQL: <cite>json_structure</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.transform">
<span class="sig-name descname"><span class="pre">transform</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.transform" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_transform</cite> function. Arguments: structure. SQL: <cite>json_transform</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.transform_strict">
<span class="sig-name descname"><span class="pre">transform_strict</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.transform_strict" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_transform_strict</cite> function. Arguments: structure. SQL: <cite>json_transform_strict</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.type">
<span class="sig-name descname"><span class="pre">type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The type of the top value: OBJECT, ARRAY, VARCHAR and so on. SQL: <cite>json_type</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.valid">
<span class="sig-name descname"><span class="pre">valid</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.Expression"><span class="pre">Expression</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.valid" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Whether the text is valid JSON. SQL: <cite>json_valid</cite>.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb._expression_namespaces.JsonExpr.value">
<span class="sig-name descname"><span class="pre">value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ValueOrExpr</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb._expression_namespaces.StrExpr" title="duckdb._expression_namespaces.StrExpr"><span class="pre">StrExpr</span></a></span></span><a class="headerlink" href="#duckdb._expression_namespaces.JsonExpr.value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The <cite>json_value</cite> function. Arguments: path. SQL: <cite>json_value</cite>.</p>
</dd>
</dl>

</dd>
</dl>

</section>
<section id="module-functions">
<h2>Module Functions<a class="headerlink" href="#module-functions" title="Link to this heading">&#182;</a>
</h2>
<dl class="py function">
<dt class="sig sig-object py" id="duckdb.abort">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">abort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.abort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Cancel the rest of the result of execute(); a statement that may write fails an open transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.aggregate">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.aggregate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on the relation.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.alias">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Rename the relation object to new alias.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.append">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">by_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.append" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Append the passed DataFrame to the named table</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.appender">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">appender</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">action</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'insert'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Appender" title="_duckdb.Appender"><span class="pre">_duckdb.Appender</span></a></span></span><a class="headerlink" href="#duckdb.appender" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an appender that buffers rows and inserts, upserts, updates or deletes them in the named table at each flush</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.arrow">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.begin">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">begin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.begin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Start a new transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.build_info">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">build_info</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.build_info" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The versions and the commits this build was made from, for the package and the bundled DuckDB engine.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.checkpoint">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">checkpoint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.checkpoint" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Synchronizes data in the write-ahead log (WAL) to the database data file (no-op for in-memory connections)</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.close">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Close the connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.commit">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">commit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.commit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Commit changes performed within a transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.complete">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">complete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.complete" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the result of execute() to its end without reading its rows</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.connect">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">connect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">database</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">':memory:'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">read_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">config</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">{}</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.connect" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB database instance. Can take a database file name to read/write persistent data and a read_only flag if no changes are desired</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.create_function">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">create_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">collections.abc.Callable</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">return_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">PythonUDFType</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">PythonUDFType.NATIVE</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_handling</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">FunctionNullHandling</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">FunctionNullHandling.DEFAULT</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exception_handling</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.PythonExceptionHandling" title="duckdb.PythonExceptionHandling"><span class="pre">PythonExceptionHandling</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">PythonExceptionHandling.DEFAULT</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">side_effects</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.create_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB function out of the passing in Python function so it can be used in queries</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.cursor">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.cursor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.default_connection">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">default_connection</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.default_connection" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve the connection currently registered as the default to be used by the module</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.description">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">description</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set attributes, mainly column names</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A relation over a DataFrame, or with no DataFrame the DataFrame of the connection&#8217;s pending result.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.disable_profiling">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">disable_profiling</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.disable_profiling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Disable profiling for the current connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.distinct">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve distinct rows from this relation object.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.duplicate">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">duplicate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.duplicate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.enable_profiling">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">enable_profiling</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.enable_profiling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Enable profiling for the current connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.execute">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given SQL query, optionally using prepared statements with parameters set. A query runs until its first rows are ready, so an error there raises here; every other statement runs to its end</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.executemany">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">executemany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.executemany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given prepared statement multiple times using the list of parameter sets in parameters</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.extract_statements">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">extract_statements</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.extract_statements" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Parse the query string and extract the Statement object(s) produced</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetch_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.fetch_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetch_df_chunk">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.fetch_df_chunk" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of the result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchall">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows from a result following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchdf">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchmany">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows from a result following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchnumpy">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as list of NumPy arrays following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchone">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row from a result following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.filesystem_is_registered">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">filesystem_is_registered</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a class="headerlink" href="#duckdb.filesystem_is_registered" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Check if a filesystem with the provided name is currently registered</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.filter">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.filter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the relation object by the filter in filter_expr.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_arrow">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_csv_auto">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_csv_auto" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the DataFrame in df.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_parquet">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">binary_as_string</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Parquet path(s) or file-like object(s) in &#8216;path_or_buffer&#8217;.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_query">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.from_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. A statement that only reads returns a relation that runs the query each time it is read, parameter values bound at every run. Any other statement runs once, now, and gives a relation over what it returned. Statements before the last one run immediately.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_profiling_information">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_profiling_information</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'json'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.get_profiling_information" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get profiling information from a query</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_table_names">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_table_names</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">qualified</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">set</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.get_table_names" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the required table names from a query</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.install_extension">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">install_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">force_install</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">repository</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">repository_url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">version</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.install_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Install an extension by name, with an optional version and/or repository to get the extension from</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.interrupt">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">interrupt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.interrupt" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Interrupt pending operations</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.limit">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.limit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Only retrieve the first n rows from this relation object, starting at offset.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.list_filesystems">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">list_filesystems</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.list_filesystems" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>List registered filesystems, including builtin ones</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.load_extension">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">load_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.load_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Load an installed extension</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.order">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.order" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by order_expr.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.project">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.project" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. A statement that only reads returns a relation that runs the query each time it is read, parameter values bound at every run. Any other statement runs once, now, and gives a relation over what it returned. Statements before the last one run immediately.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query_appender">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query_appender</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">dml</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">source</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Appender" title="_duckdb.Appender"><span class="pre">_duckdb.Appender</span></a></span></span><a class="headerlink" href="#duckdb.query_appender" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an appender that buffers rows of the declared columns and runs the DML over them at each flush</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.query_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query_progress">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query_progress</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span><a class="headerlink" href="#duckdb.query_progress" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Query progress of pending operation</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.read_csv">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">read_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.read_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.read_json">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">read_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.read_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the JSON file in &#8216;name&#8217;.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.read_parquet">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">read_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">binary_as_string</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.read_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Parquet path(s) or file-like object(s) in &#8216;path_or_buffer&#8217;.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.register">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">python_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.register" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register the passed Python Object value for querying with a view</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.register_filesystem">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">register_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filesystem</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.register_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register a fsspec compliant filesystem</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.remove_function">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">remove_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.remove_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Remove a previously created function</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.rollback">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">rollback</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.rollback" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Roll back changes performed within a transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.rowcount">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">rowcount</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span><a class="headerlink" href="#duckdb.rowcount" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set row count</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.set_default_connection">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">set_default_connection</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.set_default_connection" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register the provided connection as the default to be used by the module</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.sql">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">sql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.sql" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. A statement that only reads returns a relation that runs the query each time it is read, parameter values bound at every run. Any other statement runs once, now, and gives a relation over what it returned. Statements before the last one run immediately.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.table">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the named table.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.table_function">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">table_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.table_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the named table function with given parameters.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.tf">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.to_arrow_reader">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">to_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.to_arrow_reader" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>A reader over every row the connection&#8217;s pending result still holds.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.to_arrow_table">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">to_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">131072</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span><a class="headerlink" href="#duckdb.to_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Every row the connection&#8217;s pending result still holds, as an Arrow Table.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.tokenize">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">tokenize</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.tokenize" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Tokenizes a SQL string, returning a list of (position, type) tuples that can be used for e.g., syntax highlighting</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.torch">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.unregister">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">unregister</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.unregister" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister the view name</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.unregister_filesystem">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">unregister_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.unregister_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister a filesystem</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.values">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.values" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the passed values.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.view">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb._relation.DuckDBPyRelation"><span class="pre">DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the named view.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.write_csv">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.write_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;.</p>
</dd>
</dl>

</section>
<section id="types-and-values">
<h2>Types and Values<a class="headerlink" href="#types-and-values" title="Link to this heading">&#182;</a>
</h2>
<dl class="py function">
<dt class="sig sig-object py" id="duckdb.array_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">array_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.array_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BinaryValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinaryValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BinaryValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BitValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BitValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BitValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BlobValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BlobValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BlobValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BooleanValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BooleanValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BooleanValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DateValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DateValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DateValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.decimal_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">decimal_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.decimal_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a decimal type with &#8216;width&#8217; and &#8216;scale&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DecimalValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DecimalValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DecimalValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DoubleValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DoubleValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DoubleValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.dtype">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">dtype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.dtype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.enum_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">enum_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.enum_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an enum type of underlying &#8216;type&#8217;, consisting of the list of &#8216;values&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.FloatValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FloatValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.FloatValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.HugeIntegerValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">HugeIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.HugeIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntegerValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.IntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntervalValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntervalValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.IntervalValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.list_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">list_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.list_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a list type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ListValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ListValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">child_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">DuckDBPyType</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.ListValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.LongValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">LongValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.LongValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.map_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">map_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.map_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a map type object from &#8216;key_type&#8217; and &#8216;value_type&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.MapValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">MapValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">key_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">DuckDBPyType</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.MapValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NullValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NullValue</span></span><a class="headerlink" href="#duckdb.NullValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.row_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">row_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.row_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ShortValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ShortValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.ShortValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.sqltype">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">sqltype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.sqltype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.string_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">string_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.string_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a string type with an optional collation</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.StringValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StringValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.StringValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.struct_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">struct_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.struct_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.StructValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StructValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">children</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">DuckDBPyType</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.StructValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampMillisecondValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampMillisecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampMillisecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampNanosecondValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampNanosecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampNanosecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampSecondValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampSecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampSecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampTimeZoneValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampTimeZoneValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampTimeZoneValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimeTimeZoneValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimeTimeZoneValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimeTimeZoneValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimeValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimeValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimeValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.union_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">union_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">members</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb._sqltypes.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.union_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a union type object from &#8216;members&#8217;</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnionType">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnionType</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">members</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">DuckDBPyType</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnionType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedBinaryValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedBinaryValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedBinaryValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedHugeIntegerValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedHugeIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedHugeIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedIntegerValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedLongValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedLongValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedLongValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedShortValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedShortValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedShortValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UUIDValue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UUIDValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UUIDValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Value">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">DuckDBPyType</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.Value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
</dd>
</dl>

</section>
<section id="enumerations">
<h2>Enumerations<a class="headerlink" href="#enumerations" title="Link to this heading">&#182;</a>
</h2>
<dl class="py class">
<dt class="sig sig-object py" id="duckdb.CSVLineTerminator">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CSVLineTerminator</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.CSVLineTerminator" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ExpectedResultType">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ExpectedResultType</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.ExpectedResultType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ExplainType">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ExplainType</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.ExplainType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PythonExceptionHandling</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.PythonExceptionHandling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.RenderMode">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">RenderMode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.RenderMode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.StatementType">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StatementType</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.StatementType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.token_type">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">token_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">values</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.token_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Enum</span></code></p>
</dd>
</dl>

</section>
<section id="exceptions">
<h2>Exceptions<a class="headerlink" href="#exceptions" title="Link to this heading">&#182;</a>
</h2>
<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BinderException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinderException</span></span><a class="headerlink" href="#duckdb.BinderException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.CatalogException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CatalogException</span></span><a class="headerlink" href="#duckdb.CatalogException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ConnectionException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConnectionException</span></span><a class="headerlink" href="#duckdb.ConnectionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ConstraintException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConstraintException</span></span><a class="headerlink" href="#duckdb.ConstraintException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IntegrityError" title="_duckdb.IntegrityError"><code class="xref py py-class docutils literal notranslate"><span class="pre">IntegrityError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ConversionException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConversionException</span></span><a class="headerlink" href="#duckdb.ConversionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="_duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DatabaseError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DatabaseError</span></span><a class="headerlink" href="#duckdb.DatabaseError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="_duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DataError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DataError</span></span><a class="headerlink" href="#duckdb.DataError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DependencyException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DependencyException</span></span><a class="headerlink" href="#duckdb.DependencyException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Error">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Error</span></span><a class="headerlink" href="#duckdb.Error" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.FatalException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FatalException</span></span><a class="headerlink" href="#duckdb.FatalException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.HTTPException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">HTTPException</span></span><a class="headerlink" href="#duckdb.HTTPException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IOException" title="_duckdb.IOException"><code class="xref py py-class docutils literal notranslate"><span class="pre">IOException</span></code></a></p>
<p>Thrown when an error occurs in the httpfs extension, or whilst downloading an extension.</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntegrityError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegrityError</span></span><a class="headerlink" href="#duckdb.IntegrityError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InternalError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalError</span></span><a class="headerlink" href="#duckdb.InternalError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InternalException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalException</span></span><a class="headerlink" href="#duckdb.InternalException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.InternalError" title="_duckdb.InternalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">InternalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InterruptException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InterruptException</span></span><a class="headerlink" href="#duckdb.InterruptException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InvalidInputException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidInputException</span></span><a class="headerlink" href="#duckdb.InvalidInputException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InvalidTypeException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidTypeException</span></span><a class="headerlink" href="#duckdb.InvalidTypeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IOException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IOException</span></span><a class="headerlink" href="#duckdb.IOException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NotImplementedException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotImplementedException</span></span><a class="headerlink" href="#duckdb.NotImplementedException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.NotSupportedError" title="_duckdb.NotSupportedError"><code class="xref py py-class docutils literal notranslate"><span class="pre">NotSupportedError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NotSupportedError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotSupportedError</span></span><a class="headerlink" href="#duckdb.NotSupportedError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.OperationalError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OperationalError</span></span><a class="headerlink" href="#duckdb.OperationalError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.OutOfMemoryException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfMemoryException</span></span><a class="headerlink" href="#duckdb.OutOfMemoryException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.OutOfRangeException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfRangeException</span></span><a class="headerlink" href="#duckdb.OutOfRangeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="_duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ParserException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ParserException</span></span><a class="headerlink" href="#duckdb.ParserException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.PermissionException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PermissionException</span></span><a class="headerlink" href="#duckdb.PermissionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ProgrammingError">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ProgrammingError</span></span><a class="headerlink" href="#duckdb.ProgrammingError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ResourceInUseException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ResourceInUseException</span></span><a class="headerlink" href="#duckdb.ResourceInUseException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.SequenceException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SequenceException</span></span><a class="headerlink" href="#duckdb.SequenceException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DatabaseError" title="_duckdb.DatabaseError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.SerializationException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SerializationException</span></span><a class="headerlink" href="#duckdb.SerializationException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.SyntaxException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SyntaxException</span></span><a class="headerlink" href="#duckdb.SyntaxException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TransactionException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TransactionException</span></span><a class="headerlink" href="#duckdb.TransactionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TypeMismatchException">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TypeMismatchException</span></span><a class="headerlink" href="#duckdb.TypeMismatchException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="_duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Warning">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Warning</span></span><a class="headerlink" href="#duckdb.Warning" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

</section>


<div class="clearer"></div>
</div>
</div>
</div>
