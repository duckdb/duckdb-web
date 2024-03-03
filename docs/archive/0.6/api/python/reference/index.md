---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
selected: Documentation/Python/Client API
title: Python Client API
---
<div class="documentwrapper">
<div class="bodywrapper">
<div class="body" role="main">

<span class="target" id="module-duckdb"></span><p>DuckDB is an embeddable SQL OLAP Database Management System</p>
<dl class="py data">
<dt class="sig sig-object py" id="duckdb.threadsafety">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">threadsafety</span></span><em class="property"><span class="w"> </span><span class="pre">bool</span></em><a class="headerlink" href="#duckdb.threadsafety" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Indicates that this package is threadsafe</p>
</dd>
</dl>

<dl class="py data">
<dt class="sig sig-object py" id="duckdb.apilevel">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">apilevel</span></span><em class="property"><span class="w"> </span><span class="pre">int</span></em><a class="headerlink" href="#duckdb.apilevel" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Indicates which Python DBAPI version this package implements</p>
</dd>
</dl>

<dl class="py data">
<dt class="sig sig-object py" id="duckdb.paramstyle">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">paramstyle</span></span><em class="property"><span class="w"> </span><span class="pre">str</span></em><a class="headerlink" href="#duckdb.paramstyle" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Indicates which parameter style duckdb supports</p>
</dd>
</dl>

<dl class="py data">
<dt class="sig sig-object py" id="duckdb.default_connection">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">default_connection</span></span><em class="property"><span class="w"> </span><span class="pre">duckdb.DuckDBPyConnection</span></em><a class="headerlink" href="#duckdb.default_connection" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>The connection that is used by default if you don&#8217;t explicitly pass one to the root methods in this module</p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.BinderException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinderException</span></span><a class="headerlink" href="#duckdb.BinderException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.CastException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CastException</span></span><a class="headerlink" href="#duckdb.CastException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.CatalogException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CatalogException</span></span><a class="headerlink" href="#duckdb.CatalogException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ConnectionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConnectionException</span></span><a class="headerlink" href="#duckdb.ConnectionException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ConstraintException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConstraintException</span></span><a class="headerlink" href="#duckdb.ConstraintException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IntegrityError" title="duckdb.IntegrityError"><code class="xref py py-class docutils literal notranslate"><span class="pre">IntegrityError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ConversionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConversionException</span></span><a class="headerlink" href="#duckdb.ConversionException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.DataError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DataError</span></span><a class="headerlink" href="#duckdb.DataError" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyConnection</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.append">
<span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.append" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Append the passed Data.Frame to the named table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">chunk_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.arrow" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Arrow table following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.begin">
<span class="sig-name descname"><span class="pre">begin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.begin" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Start a new transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.close" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Close the connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.commit">
<span class="sig-name descname"><span class="pre">commit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.commit" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Commit changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.cursor">
<span class="sig-name descname"><span class="pre">cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.cursor" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.description">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.description" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set attributes, mainly column names</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Data.Frame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.duplicate">
<span class="sig-name descname"><span class="pre">duplicate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.duplicate" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">multiple_parameter_sets</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.execute" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given SQL query, optionally using prepared statements with parameters set</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.executemany">
<span class="sig-name descname"><span class="pre">executemany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.executemany" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given prepared statement multiple times using the list of parameter sets in parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">chunk_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_arrow_table" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Arrow table following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df">
<span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Data.Frame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df_chunk">
<span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df_chunk" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of the result as Data.Frame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_record_batch">
<span class="sig-name descname"><span class="pre">fetch_record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">chunk_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_record_batch" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch an Arrow RecordBatchReader following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchall" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchdf" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Data.Frame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchmany" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchnumpy" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as list of NumPy arrays following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchone" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_arrow">
<span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_arrow" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_csv_auto">
<span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_csv_auto" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in file_name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_df">
<span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Data.Frame in df</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_parquet">
<span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">binary_as_string</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_parquet" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Parquet file in file_name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_query">
<span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'query_relation'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_query" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the given SQL query</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_substrait">
<span class="sig-name descname"><span class="pre">from_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">proto</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bytes</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_substrait" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a query object from protobuf plan</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_substrait">
<span class="sig-name descname"><span class="pre">get_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_substrait" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query to protobuf</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_substrait_json">
<span class="sig-name descname"><span class="pre">get_substrait_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_substrait_json" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query to protobuf on the JSON format</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_table_names">
<span class="sig-name descname"><span class="pre">get_table_names</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Set</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_table_names" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the required table names from a query</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.install_extension">
<span class="sig-name descname"><span class="pre">install_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">force_install</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.install_extension" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Install an extension by name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.load_extension">
<span class="sig-name descname"><span class="pre">load_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.load_extension" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Load an installed extension</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'query_relation'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register">
<span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">python_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Register the passed Python Object value for querying with a view</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rollback">
<span class="sig-name descname"><span class="pre">rollback</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rollback" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Roll back changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table">
<span class="sig-name descname"><span class="pre">table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the name&#8217;d table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table_function">
<span class="sig-name descname"><span class="pre">table_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table_function" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the name&#8217;d table function with given parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister">
<span class="sig-name descname"><span class="pre">unregister</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister the view name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.values">
<span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.values" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the passed values</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.view">
<span class="sig-name descname"><span class="pre">view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.view" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the name&#8217;d view</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyRelation</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.abs">
<span class="sig-name descname"><span class="pre">abs</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.abs" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the absolute value for the specified columns.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.aggregate">
<span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.aggregate" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on the relation</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.alias">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">alias</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.alias" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Get the name of the current alias</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.apply">
<span class="sig-name descname"><span class="pre">apply</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_parameter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.apply" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the function of a single column or a list of columns  by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arrow" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.columns">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">columns</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.columns" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Get the names of the columns of this relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.count">
<span class="sig-name descname"><span class="pre">count</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">count_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.count" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate count of a single column or a list of columns  by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create_view">
<span class="sig-name descname"><span class="pre">create_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create_view" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cummax">
<span class="sig-name descname"><span class="pre">cummax</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cummax" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the cumulative maximum of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cummin">
<span class="sig-name descname"><span class="pre">cummin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cummin" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the cumulative minimum of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cumprod">
<span class="sig-name descname"><span class="pre">cumprod</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cumprod" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the cumulative product of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cumsum">
<span class="sig-name descname"><span class="pre">cumsum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cumsum" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the cumulative sum of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.describe">
<span class="sig-name descname"><span class="pre">describe</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.describe" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Gives basic statistics (e.g., min,max) and if null exists for each column of the relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.distinct">
<span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.distinct" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve distinct rows from this relation object</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dtypes">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">dtypes</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dtypes" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Get the columns types of the result.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.except_">
<span class="sig-name descname"><span class="pre">except_</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.except_" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set except of this relation object with another relation object in other_rel</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb::DuckDBPyResult</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.execute" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Transform the relation into a result set</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.explain">
<span class="sig-name descname"><span class="pre">explain</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.explain" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchall" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a list of tuples</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchmany" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch the next set of rows as a list of tuples</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchnumpy" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Python dict mapping each column to one numpy arrays</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchone" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch a single row as a tuple</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.filter">
<span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.filter" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the relation object by the filter in filter_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert">
<span class="sig-name descname"><span class="pre">insert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the given values into the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert_into">
<span class="sig-name descname"><span class="pre">insert_into</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert_into" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the relation object into an existing table named table_name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.intersect">
<span class="sig-name descname"><span class="pre">intersect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.intersect" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set intersection of this relation object with another relation object in other_rel</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.join">
<span class="sig-name descname"><span class="pre">join</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">how</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'inner'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.join" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Join the relation object with another relation object in other_rel using the join condition expression in join_condition. Types supported are &#8216;inner&#8217; and &#8216;left&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.kurt">
<span class="sig-name descname"><span class="pre">kurt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.kurt" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the excess kurtosis of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.limit">
<span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.limit" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Only retrieve the first n rows from this relation object, starting at offset</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mad">
<span class="sig-name descname"><span class="pre">mad</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mad" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the median absolute deviation for the  aggregate columns. NULL values are ignored. Temporal types return a positive INTERVAL.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.map">
<span class="sig-name descname"><span class="pre">map</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">map_function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">function</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.map" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Calls the passed function on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.max">
<span class="sig-name descname"><span class="pre">max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.max" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate max of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mean">
<span class="sig-name descname"><span class="pre">mean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">mean_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mean" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate mean of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.median">
<span class="sig-name descname"><span class="pre">median</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">median_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.median" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate median of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.min">
<span class="sig-name descname"><span class="pre">min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">min_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.min" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate min of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mode">
<span class="sig-name descname"><span class="pre">mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mode" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the most frequent value for the aggregate columns. NULL values are ignored.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.order">
<span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.order" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by order_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.prod">
<span class="sig-name descname"><span class="pre">prod</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.prod" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Calculates the product of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.project">
<span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">project_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.project" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile">
<span class="sig-name descname"><span class="pre">quantile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quantile_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the quantile of a single column or a list of columns  by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.query" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.record_batch">
<span class="sig-name descname"><span class="pre">record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.record_batch" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sem">
<span class="sig-name descname"><span class="pre">sem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sem" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the standard error of the mean of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.set_alias">
<span class="sig-name descname"><span class="pre">set_alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.set_alias" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Rename the relation object to new alias</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.shape">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">shape</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.shape" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Tuple of # of rows, # of columns in relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.skew">
<span class="sig-name descname"><span class="pre">skew</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggregation_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.skew" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the skewness of the aggregate column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.std">
<span class="sig-name descname"><span class="pre">std</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">std_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.std" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the standard deviation of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sum">
<span class="sig-name descname"><span class="pre">sum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">sum_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sum" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate sum of a single column or a list of columns  by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_arrow_table">
<span class="sig-name descname"><span class="pre">to_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_arrow_table" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_df">
<span class="sig-name descname"><span class="pre">to_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.type">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">type</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.type" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Get the type of the relation.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.types">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">types</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.types" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Get the columns types of the result.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.union">
<span class="sig-name descname"><span class="pre">union</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">union_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.union" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set union of this relation object with another relation object in other_rel</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.unique">
<span class="sig-name descname"><span class="pre">unique</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">unique_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.unique" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Number of distinct values in a column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.value_counts">
<span class="sig-name descname"><span class="pre">value_counts</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_counts_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.value_counts" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Count number of rows with each unique value of variable</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var">
<span class="sig-name descname"><span class="pre">var</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">var_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the variance of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_csv">
<span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_csv" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in file_name</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyResult</span></span><a class="headerlink" href="#duckdb.DuckDBPyResult" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">chunk_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.arrow" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.close" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.description">
<span class="sig-name descname"><span class="pre">description</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.description" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetch_arrow_reader">
<span class="sig-name descname"><span class="pre">fetch_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">approx_batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetch_arrow_reader" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as an Arrow Record Batch Reader</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">chunk_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetch_arrow_table" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetch_df">
<span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetch_df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetch_df_chunk">
<span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">num_of_vectors</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetch_df_chunk" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetchall" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as a list of tuples</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetchdf" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetchmany" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows as a list of tuples</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetchnumpy" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows as a Python dict mapping each column to one numpy arrays</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyResult.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyResult.fetchone" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row as a tuple</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.Error">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Error</span></span><a class="headerlink" href="#duckdb.Error" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.FatalException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FatalException</span></span><a class="headerlink" href="#duckdb.FatalException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.IOException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IOException</span></span><a class="headerlink" href="#duckdb.IOException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.IntegrityError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegrityError</span></span><a class="headerlink" href="#duckdb.IntegrityError" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InternalError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalError</span></span><a class="headerlink" href="#duckdb.InternalError" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InternalException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalException</span></span><a class="headerlink" href="#duckdb.InternalException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.InternalError" title="duckdb.InternalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">InternalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InterruptException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InterruptException</span></span><a class="headerlink" href="#duckdb.InterruptException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InvalidInputException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidInputException</span></span><a class="headerlink" href="#duckdb.InvalidInputException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InvalidTypeException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidTypeException</span></span><a class="headerlink" href="#duckdb.InvalidTypeException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.NotImplementedException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotImplementedException</span></span><a class="headerlink" href="#duckdb.NotImplementedException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.NotSupportedError" title="duckdb.NotSupportedError"><code class="xref py py-class docutils literal notranslate"><span class="pre">NotSupportedError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.NotSupportedError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotSupportedError</span></span><a class="headerlink" href="#duckdb.NotSupportedError" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.OperationalError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OperationalError</span></span><a class="headerlink" href="#duckdb.OperationalError" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.OutOfMemoryException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfMemoryException</span></span><a class="headerlink" href="#duckdb.OutOfMemoryException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.OutOfRangeException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfRangeException</span></span><a class="headerlink" href="#duckdb.OutOfRangeException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ParserException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ParserException</span></span><a class="headerlink" href="#duckdb.ParserException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.PermissionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PermissionException</span></span><a class="headerlink" href="#duckdb.PermissionException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ProgrammingError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ProgrammingError</span></span><a class="headerlink" href="#duckdb.ProgrammingError" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.SequenceException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SequenceException</span></span><a class="headerlink" href="#duckdb.SequenceException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.SerializationException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SerializationException</span></span><a class="headerlink" href="#duckdb.SerializationException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.StandardException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StandardException</span></span><a class="headerlink" href="#duckdb.StandardException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.SyntaxException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SyntaxException</span></span><a class="headerlink" href="#duckdb.SyntaxException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.TransactionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TransactionException</span></span><a class="headerlink" href="#duckdb.TransactionException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.TypeMismatchException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TypeMismatchException</span></span><a class="headerlink" href="#duckdb.TypeMismatchException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ValueOutOfRangeException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ValueOutOfRangeException</span></span><a class="headerlink" href="#duckdb.ValueOutOfRangeException" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.Warning">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Warning</span></span><a class="headerlink" href="#duckdb.Warning" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.aggregate">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.aggregate" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on Data.frame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.alias">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.alias" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation from Data.Frame df with the passed alias</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.arrow">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.arrow" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.connect">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">connect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">database</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">':memory:'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">read_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">config</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.connect" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB database instance. Can take a database file name to read/write persistent data and a read_only flag if no changes are desired</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Data.Frame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.distinct">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.distinct" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the distinct rows from Data.Frame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.filter">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.filter" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the Data.Frame df by the filter in filter_expr</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_arrow">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_arrow" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_csv_auto">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_csv_auto" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a relation object from the CSV file in file_name</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Data.Frame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_parquet">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.from_parquet" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>from_parquet(file_name: str, binary_as_string: bool, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Creates a relation object from the Parquet file in file_name</p>
<ol class="arabic simple" start="2">
<li><p>from_parquet(file_name: str, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Creates a relation object from the Parquet file in file_name</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_query">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'query_relation'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_query" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the given SQL query</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_substrait">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">proto</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bytes</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_substrait" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a query object from the substrait plan</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_substrait">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.get_substrait" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query object to protobuf</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_substrait_json">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_substrait_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.get_substrait_json" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query object to protobuf</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.limit">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.limit" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve the first n rows from the Data.Frame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.order">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.order" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the Data.Frame df by order_expr</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.project">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">project_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.project" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Project the Data.Frame df by the projection in project_expr</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'query_relation'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.query" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyResult" title="duckdb.DuckDBPyResult"><span class="pre">duckdb.DuckDBPyResult</span></a></span></span><a class="headerlink" href="#duckdb.query_df" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that contains the content of Data.Frame df</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.token_type">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">token_type</span></span><a class="headerlink" href="#duckdb.token_type" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>identifier</p>
<p>numeric_const</p>
<p>string_const</p>
<p>operator</p>
<p>keyword</p>
<p>comment</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.comment">
<span class="sig-name descname"><span class="pre">comment</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.comment:</span> <span class="pre">5&gt;</span></em><a class="headerlink" href="#duckdb.token_type.comment" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.identifier">
<span class="sig-name descname"><span class="pre">identifier</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.identifier:</span> <span class="pre">0&gt;</span></em><a class="headerlink" href="#duckdb.token_type.identifier" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.keyword">
<span class="sig-name descname"><span class="pre">keyword</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.keyword:</span> <span class="pre">4&gt;</span></em><a class="headerlink" href="#duckdb.token_type.keyword" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.token_type.name">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.token_type.name" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.numeric_const">
<span class="sig-name descname"><span class="pre">numeric_const</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.numeric_const:</span> <span class="pre">1&gt;</span></em><a class="headerlink" href="#duckdb.token_type.numeric_const" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.operator">
<span class="sig-name descname"><span class="pre">operator</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.operator:</span> <span class="pre">3&gt;</span></em><a class="headerlink" href="#duckdb.token_type.operator" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.string_const">
<span class="sig-name descname"><span class="pre">string_const</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.string_const:</span> <span class="pre">2&gt;</span></em><a class="headerlink" href="#duckdb.token_type.string_const" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.token_type.value">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">value</span></span><a class="headerlink" href="#duckdb.token_type.value" title="Permalink to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.tokenize">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">tokenize</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.tokenize" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Tokenizes a SQL string, returning a list of (position, type) tuples that can be used for e.g. syntax highlighting</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.values">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.DuckDBPyRelation"><span class="pre">duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.values" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the passed values</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.write_csv">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.write_csv" title="Permalink to this definition">&#182;</a>
</dt>
<dd>
<p>Write the Data.Frame df to a CSV file in file_name</p>
</dd>
</dl>



<div class="clearer"></div>
</div>
</div>
</div>
