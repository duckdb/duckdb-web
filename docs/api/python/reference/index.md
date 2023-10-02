---
# this file is GENERATED, regenerate it with scripts/generate_python_docs.py
layout: docu
title: Python Client API
---
<div class="documentwrapper">
<div class="bodywrapper">
<div class="body" role="main">

<dl class="py data" id="module-duckdb">
<dt class="sig sig-object py" id="duckdb.threadsafety">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">threadsafety</span></span><em class="property"><span class="w"> </span><span class="pre">bool</span></em><a class="headerlink" href="#duckdb.threadsafety" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Indicates that this package is threadsafe</p>
</dd>
</dl>

<dl class="py data">
<dt class="sig sig-object py" id="duckdb.apilevel">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">apilevel</span></span><em class="property"><span class="w"> </span><span class="pre">int</span></em><a class="headerlink" href="#duckdb.apilevel" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Indicates which Python DBAPI version this package implements</p>
</dd>
</dl>

<dl class="py data">
<dt class="sig sig-object py" id="duckdb.paramstyle">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">paramstyle</span></span><em class="property"><span class="w"> </span><span class="pre">str</span></em><a class="headerlink" href="#duckdb.paramstyle" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Indicates which parameter style duckdb supports</p>
</dd>
</dl>

<dl class="py data">
<dt class="sig sig-object py" id="duckdb.default_connection">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">default_connection</span></span><em class="property"><span class="w"> </span><span class="pre">duckdb.DuckDBPyConnection</span></em><a class="headerlink" href="#duckdb.default_connection" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>The connection that is used by default if you don&#8217;t explicitly pass one to the root methods in this module</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BinaryValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinaryValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BinaryValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.BinderException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinderException</span></span><a class="headerlink" href="#duckdb.BinderException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BitValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BitValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BitValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BlobValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BlobValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BlobValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BooleanValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BooleanValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BooleanValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.CaseExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CaseExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.CaseExpression" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.CastException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CastException</span></span><a class="headerlink" href="#duckdb.CastException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.CatalogException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CatalogException</span></span><a class="headerlink" href="#duckdb.CatalogException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.ColumnExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ColumnExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.ColumnExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a column reference from the provided column name</p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ConnectionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConnectionException</span></span><a class="headerlink" href="#duckdb.ConnectionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.ConstantExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConstantExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.ConstantExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a constant expression from the provided value</p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ConstraintException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConstraintException</span></span><a class="headerlink" href="#duckdb.ConstraintException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IntegrityError" title="duckdb.duckdb.IntegrityError"><code class="xref py py-class docutils literal notranslate"><span class="pre">IntegrityError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ConversionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConversionException</span></span><a class="headerlink" href="#duckdb.ConversionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.DataError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DataError</span></span><a class="headerlink" href="#duckdb.DataError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DateValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DateValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DateValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DecimalValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DecimalValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DecimalValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DoubleValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DoubleValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DoubleValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyConnection</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.append">
<span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">by_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.append" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Append the passed DataFrame to the named table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.array_type">
<span class="sig-name descname"><span class="pre">array_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.array_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Arrow table following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.begin">
<span class="sig-name descname"><span class="pre">begin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.begin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Start a new transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Close the connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.commit">
<span class="sig-name descname"><span class="pre">commit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.commit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Commit changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.create_function">
<span class="sig-name descname"><span class="pre">create_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self:</span> <span class="pre">duckdb.duckdb.DuckDBPyConnection</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name:</span> <span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function:</span> <span class="pre">function</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">return_type:</span> <span class="pre">object</span> <span class="pre">=</span> <span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters:</span> <span class="pre">duckdb.duckdb.typing.DuckDBPyType</span> <span class="pre">=</span> <span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type:</span> <span class="pre">duckdb.duckdb.functional.PythonUDFType</span> <span class="pre">=</span> <span class="pre">&lt;PythonUDFType.NATIVE:</span> <span class="pre">0&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_handling:</span> <span class="pre">duckdb.duckdb.functional.FunctionNullHandling</span> <span class="pre">=</span> <span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exception_handling:</span> <span class="pre">duckdb.duckdb.PythonExceptionHandling</span> <span class="pre">=</span> <span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">side_effects:</span> <span class="pre">bool</span> <span class="pre">=</span> <span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.create_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB function out of the passing in python function so it can be used in queries</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.cursor">
<span class="sig-name descname"><span class="pre">cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.cursor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.decimal_type">
<span class="sig-name descname"><span class="pre">decimal_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.decimal_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a decimal type with &#8216;width&#8217; and &#8216;scale&#8217;</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.description">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set attributes, mainly column names</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.dtype">
<span class="sig-name descname"><span class="pre">dtype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.dtype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.duplicate">
<span class="sig-name descname"><span class="pre">duplicate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.duplicate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.enum_type">
<span class="sig-name descname"><span class="pre">enum_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.enum_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an enum type of underlying &#8216;type&#8217;, consisting of the list of &#8216;values&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">multiple_parameter_sets</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given SQL query, optionally using prepared statements with parameters set</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.executemany">
<span class="sig-name descname"><span class="pre">executemany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.executemany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given prepared statement multiple times using the list of parameter sets in parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Arrow table following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df">
<span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df_chunk">
<span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df_chunk" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of the result as Data.Frame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_record_batch">
<span class="sig-name descname"><span class="pre">fetch_record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch an Arrow RecordBatchReader following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as list of NumPy arrays following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.filesystem_is_registered">
<span class="sig-name descname"><span class="pre">filesystem_is_registered</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.filesystem_is_registered" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Check if a filesystem with the provided name is currently registered</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_arrow">
<span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_csv_auto">
<span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">delimiter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dtype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">skiprows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parallel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">all_varchar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">normalize_names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_padding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_csv_auto" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_df">
<span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the Data.Frame in df</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_parquet">
<span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>from_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_glob: str, binary_as_string: bool = False, <a href="#id1"><span class="problematic" id="id2">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_glob</p>
<ol class="arabic simple" start="2">
<li><p>from_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_globs: List[str], binary_as_string: bool = False, <a href="#id3"><span class="problematic" id="id4">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_globs</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_query">
<span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_substrait">
<span class="sig-name descname"><span class="pre">from_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">proto</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bytes</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_substrait" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a query object from protobuf plan</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_substrait_json">
<span class="sig-name descname"><span class="pre">from_substrait_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">json</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_substrait_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a query object from a JSON protobuf plan</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_substrait">
<span class="sig-name descname"><span class="pre">get_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">enable_optimizer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_substrait" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query to protobuf</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_substrait_json">
<span class="sig-name descname"><span class="pre">get_substrait_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">enable_optimizer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_substrait_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query to protobuf on the JSON format</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_table_names">
<span class="sig-name descname"><span class="pre">get_table_names</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Set</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_table_names" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the required table names from a query</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.install_extension">
<span class="sig-name descname"><span class="pre">install_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">force_install</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.install_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Install an extension by name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.interrupt">
<span class="sig-name descname"><span class="pre">interrupt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.interrupt" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Interrupt pending operations</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.list_filesystems">
<span class="sig-name descname"><span class="pre">list_filesystems</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.list_filesystems" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>List registered filesystems, including builtin ones</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.list_type">
<span class="sig-name descname"><span class="pre">list_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.list_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.load_extension">
<span class="sig-name descname"><span class="pre">load_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.load_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Load an installed extension</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.map_type">
<span class="sig-name descname"><span class="pre">map_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.map_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a map type object from &#8216;key_type&#8217; and &#8216;value_type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.pl">
<span class="sig-name descname"><span class="pre">pl</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb::PolarsDataFrame</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.pl" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Polars DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_csv">
<span class="sig-name descname"><span class="pre">read_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">delimiter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dtype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">skiprows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parallel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">all_varchar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">normalize_names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_padding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_json">
<span class="sig-name descname"><span class="pre">read_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">maximum_depth</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">records</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the JSON file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_parquet">
<span class="sig-name descname"><span class="pre">read_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>read_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_glob: str, binary_as_string: bool = False, <a href="#id5"><span class="problematic" id="id6">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_glob</p>
<ol class="arabic simple" start="2">
<li><p>read_parquet(self: duckdb.duckdb.DuckDBPyConnection, file_globs: List[str], binary_as_string: bool = False, <a href="#id7"><span class="problematic" id="id8">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_globs</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register">
<span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">python_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register the passed Python Object value for querying with a view</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register_filesystem">
<span class="sig-name descname"><span class="pre">register_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filesystem</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">fsspec.AbstractFileSystem</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register a fsspec compliant filesystem</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.remove_function">
<span class="sig-name descname"><span class="pre">remove_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.remove_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Remove a previously created function</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rollback">
<span class="sig-name descname"><span class="pre">rollback</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rollback" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Roll back changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.row_type">
<span class="sig-name descname"><span class="pre">row_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.row_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rowcount">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">rowcount</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rowcount" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set row count</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.sql">
<span class="sig-name descname"><span class="pre">sql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.sql" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.sqltype">
<span class="sig-name descname"><span class="pre">sqltype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.sqltype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.string_type">
<span class="sig-name descname"><span class="pre">string_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.string_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a string type with an optional collation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.struct_type">
<span class="sig-name descname"><span class="pre">struct_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.struct_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table">
<span class="sig-name descname"><span class="pre">table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the name&#8217;d table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table_function">
<span class="sig-name descname"><span class="pre">table_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the name&#8217;d table function with given parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.tf">
<span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.torch">
<span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.type">
<span class="sig-name descname"><span class="pre">type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.union_type">
<span class="sig-name descname"><span class="pre">union_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">members</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.union_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a union type object from &#8216;members&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister">
<span class="sig-name descname"><span class="pre">unregister</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister the view name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister_filesystem">
<span class="sig-name descname"><span class="pre">unregister_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister a filesystem</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.values">
<span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.values" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the passed values</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.view">
<span class="sig-name descname"><span class="pre">view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the name&#8217;d view</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyRelation</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.aggregate">
<span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.aggregate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on the relation</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.alias">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">alias</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the name of the current alias</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.any_value">
<span class="sig-name descname"><span class="pre">any_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.any_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the first non-null value from a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.apply">
<span class="sig-name descname"><span class="pre">apply</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_parameter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.apply" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the function of a single column or a list of columns by the optional groups on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arg_max">
<span class="sig-name descname"><span class="pre">arg_max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arg_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arg_max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Finds the row with the maximum value for a value column and returns the value of that row for an argument column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arg_min">
<span class="sig-name descname"><span class="pre">arg_min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arg_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arg_min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Finds the row with the minimum value for a value column and returns the value of that row for an argument column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.avg">
<span class="sig-name descname"><span class="pre">avg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.avg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average on a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_and">
<span class="sig-name descname"><span class="pre">bit_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise AND of all bits present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_or">
<span class="sig-name descname"><span class="pre">bit_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise OR of all bits present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_xor">
<span class="sig-name descname"><span class="pre">bit_xor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_xor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise XOR of all bits present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bitstring_agg">
<span class="sig-name descname"><span class="pre">bitstring_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">min</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bitstring_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes a bitstring with bits set for each distinct value in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bool_and">
<span class="sig-name descname"><span class="pre">bool_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bool_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the logical AND of all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bool_or">
<span class="sig-name descname"><span class="pre">bool_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bool_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the logical OR of all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Closes the result</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.columns">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">columns</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.columns" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the names of the columns of the relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.count">
<span class="sig-name descname"><span class="pre">count</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.count" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the number of elements present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create_view">
<span class="sig-name descname"><span class="pre">create_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create_view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cume_dist">
<span class="sig-name descname"><span class="pre">cume_dist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cume_dist" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the cumulative distribution within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dense_rank">
<span class="sig-name descname"><span class="pre">dense_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dense_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the dense rank within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.describe">
<span class="sig-name descname"><span class="pre">describe</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.describe" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Gives basic statistics (e.g., min,max) and if null exists for each column of the relation.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.description">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return the description of the result</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.distinct">
<span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve distinct rows from this relation object</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dtypes">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">dtypes</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dtypes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the types of the columns of the relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.except_">
<span class="sig-name descname"><span class="pre">except_</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.except_" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set except of this relation object with another relation object in other_rel</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Transform the relation into a result set</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.explain">
<span class="sig-name descname"><span class="pre">explain</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.ExplainType" title="duckdb.duckdb.ExplainType"><span class="pre">duckdb.duckdb.ExplainType</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'standard'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.explain" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.favg">
<span class="sig-name descname"><span class="pre">favg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.favg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average of all values present in a given column using a more accurate floating point summation (Kahan Sum)</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_arrow_reader">
<span class="sig-name descname"><span class="pre">fetch_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_arrow_reader" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a list of tuples</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch the next set of rows as a list of tuples</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Python dict mapping each column to one numpy arrays</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch a single row as a tuple</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.filter">
<span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.filter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the relation object by the filter in filter_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.first">
<span class="sig-name descname"><span class="pre">first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the first value of a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.first_value">
<span class="sig-name descname"><span class="pre">first_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.first_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the first value within the group or partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fsum">
<span class="sig-name descname"><span class="pre">fsum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fsum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sum of all values present in a given column using a more accurate floating point summation (Kahan Sum)</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.geomean">
<span class="sig-name descname"><span class="pre">geomean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.geomean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the geometric mean over all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.histogram">
<span class="sig-name descname"><span class="pre">histogram</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.histogram" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the histogram over all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert">
<span class="sig-name descname"><span class="pre">insert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the given values into the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert_into">
<span class="sig-name descname"><span class="pre">insert_into</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert_into" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the relation object into an existing table named table_name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.intersect">
<span class="sig-name descname"><span class="pre">intersect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.intersect" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set intersection of this relation object with another relation object in other_rel</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.join">
<span class="sig-name descname"><span class="pre">join</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">how</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'inner'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.join" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Join the relation object with another relation object in other_rel using the join condition expression in join_condition. Types supported are &#8216;inner&#8217; and &#8216;left&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.lag">
<span class="sig-name descname"><span class="pre">lag</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'NULL'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.lag" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the lag within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.last">
<span class="sig-name descname"><span class="pre">last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the last value of a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.last_value">
<span class="sig-name descname"><span class="pre">last_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.last_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the last value within the group or partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.lead">
<span class="sig-name descname"><span class="pre">lead</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'NULL'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.lead" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the lead within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.limit">
<span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.limit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Only retrieve the first n rows from this relation object, starting at offset</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.list" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns a list containing all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.map">
<span class="sig-name descname"><span class="pre">map</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">map_function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">function</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.map" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Calls the passed function on the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.max">
<span class="sig-name descname"><span class="pre">max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the maximum value present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mean">
<span class="sig-name descname"><span class="pre">mean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average on a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.median">
<span class="sig-name descname"><span class="pre">median</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.median" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the median over all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.min">
<span class="sig-name descname"><span class="pre">min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the minimum value present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mode">
<span class="sig-name descname"><span class="pre">mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the mode over all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.n_tile">
<span class="sig-name descname"><span class="pre">n_tile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">num_buckets</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.n_tile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Divides the partition as equally as possible into num_buckets</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.nth_value">
<span class="sig-name descname"><span class="pre">nth_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.nth_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the nth value within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.order">
<span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.order" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by order_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.percent_rank">
<span class="sig-name descname"><span class="pre">percent_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.percent_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the relative rank within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.pl">
<span class="sig-name descname"><span class="pre">pl</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb::PolarsDataFrame</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.pl" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Polars DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.product">
<span class="sig-name descname"><span class="pre">product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the product of all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.project">
<span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.project" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile">
<span class="sig-name descname"><span class="pre">quantile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the exact quantile value for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile_cont">
<span class="sig-name descname"><span class="pre">quantile_cont</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile_cont" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the interpolated quantile value for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile_disc">
<span class="sig-name descname"><span class="pre">quantile_disc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile_disc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the exact quantile value for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rank">
<span class="sig-name descname"><span class="pre">rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the rank within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rank_dense">
<span class="sig-name descname"><span class="pre">rank_dense</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rank_dense" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the dense rank within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.record_batch">
<span class="sig-name descname"><span class="pre">record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.row_number">
<span class="sig-name descname"><span class="pre">row_number</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.row_number" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the row number within the partition</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select">
<span class="sig-name descname"><span class="pre">select</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select_dtypes">
<span class="sig-name descname"><span class="pre">select_dtypes</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select_dtypes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Select columns from the relation, by filtering based on type(s)</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select_types">
<span class="sig-name descname"><span class="pre">select_types</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select_types" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Select columns from the relation, by filtering based on type(s)</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.set_alias">
<span class="sig-name descname"><span class="pre">set_alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.set_alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Rename the relation object to new alias</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.shape">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">shape</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.shape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Tuple of # of rows, # of columns in relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">int</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_rows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">int</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_col_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">int</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">render_mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.show" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Display a summary of the data</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sort">
<span class="sig-name descname"><span class="pre">sort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by the provided expressions</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sql_query">
<span class="sig-name descname"><span class="pre">sql_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sql_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the SQL query that is equivalent to the relation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.std">
<span class="sig-name descname"><span class="pre">std</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.std" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev">
<span class="sig-name descname"><span class="pre">stddev</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev_pop">
<span class="sig-name descname"><span class="pre">stddev_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the population standard deviation for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev_samp">
<span class="sig-name descname"><span class="pre">stddev_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.string_agg">
<span class="sig-name descname"><span class="pre">string_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">','</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.string_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Concatenates the values present in a given column with a separator</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sum">
<span class="sig-name descname"><span class="pre">sum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sum of all values present in a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.tf">
<span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_arrow_table">
<span class="sig-name descname"><span class="pre">to_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_csv">
<span class="sig-name descname"><span class="pre">to_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_rep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quoting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_df">
<span class="sig-name descname"><span class="pre">to_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_parquet">
<span class="sig-name descname"><span class="pre">to_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a Parquet file in &#8216;file_name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_table">
<span class="sig-name descname"><span class="pre">to_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_view">
<span class="sig-name descname"><span class="pre">to_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.torch">
<span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.type">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">type</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the type of the relation.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.types">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">types</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.types" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the types of the columns of the relation.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.union">
<span class="sig-name descname"><span class="pre">union</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">union_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.union" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set union of this relation object with another relation object in other_rel</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.unique">
<span class="sig-name descname"><span class="pre">unique</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">unique_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.unique" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Number of distinct values in a column.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var">
<span class="sig-name descname"><span class="pre">var</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var_pop">
<span class="sig-name descname"><span class="pre">var_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the population variance for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var_samp">
<span class="sig-name descname"><span class="pre">var_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.variance">
<span class="sig-name descname"><span class="pre">variance</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.variance" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given column</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_csv">
<span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_rep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quoting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_parquet">
<span class="sig-name descname"><span class="pre">write_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a Parquet file in &#8216;file_name&#8217;</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.Error">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Error</span></span><a class="headerlink" href="#duckdb.Error" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ExplainType">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ExplainType</span></span><a class="headerlink" href="#duckdb.ExplainType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>STANDARD</p>
<p>ANALYZE</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.ExplainType.ANALYZE">
<span class="sig-name descname"><span class="pre">ANALYZE</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;ExplainType.ANALYZE:</span> <span class="pre">1&gt;</span></em><a class="headerlink" href="#duckdb.ExplainType.ANALYZE" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.ExplainType.STANDARD">
<span class="sig-name descname"><span class="pre">STANDARD</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;ExplainType.STANDARD:</span> <span class="pre">0&gt;</span></em><a class="headerlink" href="#duckdb.ExplainType.STANDARD" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.ExplainType.name">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.ExplainType.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.ExplainType.value">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">value</span></span><a class="headerlink" href="#duckdb.ExplainType.value" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Expression">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Expression</span></span><a class="headerlink" href="#duckdb.Expression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.alias">
<span class="sig-name descname"><span class="pre">alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arg0</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a copy of this expression with the given alias.</p>
<dl class="simple">
<dt>Parameters:</dt>
<dd>
<p>name: The alias to use for the expression, this will affect how it can be referenced.</p>
</dd>
<dt>Returns:</dt>
<dd>
<p>Expression: self with an alias.</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.asc">
<span class="sig-name descname"><span class="pre">asc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.asc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the order by modifier to ASCENDING.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.cast">
<span class="sig-name descname"><span class="pre">cast</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.cast" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a CastExpression to type from self</p>
<dl class="simple">
<dt>Parameters:</dt>
<dd>
<p>type: The type to cast to</p>
</dd>
<dt>Returns:</dt>
<dd>
<p>CastExpression: self::type</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.desc">
<span class="sig-name descname"><span class="pre">desc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.desc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the order by modifier to DESCENDING.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isin">
<span class="sig-name descname"><span class="pre">isin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a IN expression comparing self to the input arguments.</p>
<dl class="simple">
<dt>Returns:</dt>
<dd>
<p>DuckDBPyExpression: The compare IN expression</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isnotin">
<span class="sig-name descname"><span class="pre">isnotin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnotin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a NOT IN expression comparing self to the input arguments.</p>
<dl class="simple">
<dt>Returns:</dt>
<dd>
<p>DuckDBPyExpression: The compare NOT IN expression</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.nulls_first">
<span class="sig-name descname"><span class="pre">nulls_first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.nulls_first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the NULL order by modifier to NULLS FIRST.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.nulls_last">
<span class="sig-name descname"><span class="pre">nulls_last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.nulls_last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the NULL order by modifier to NULLS LAST.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.otherwise">
<span class="sig-name descname"><span class="pre">otherwise</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.otherwise" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Add an ELSE &lt;value&gt; clause to the CaseExpression.</p>
<dl class="simple">
<dt>Parameters:</dt>
<dd>
<p>value: The value to use if none of the WHEN conditions are met.</p>
</dd>
<dt>Returns:</dt>
<dd>
<p>CaseExpression: self with an ELSE clause.</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Expression.show" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Print the stringified version of the expression.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.when">
<span class="sig-name descname"><span class="pre">when</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.when" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Add an additional WHEN &lt;condition&gt; THEN &lt;value&gt; clause to the CaseExpression.</p>
<dl class="simple">
<dt>Parameters:</dt>
<dd>
<p>condition: The condition that must be met.
value: The value to use if the condition is met.</p>
</dd>
<dt>Returns:</dt>
<dd>
<p>CaseExpression: self with an additional WHEN clause.</p>
</dd>
</dl>
</dd>
</dl>

</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.FatalException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FatalException</span></span><a class="headerlink" href="#duckdb.FatalException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.FloatValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FloatValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.FloatValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.FunctionExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FunctionExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">function_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="duckdb.duckdb.Expression"><span class="pre">duckdb.duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.FunctionExpression" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.HTTPException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">HTTPException</span></span><a class="headerlink" href="#duckdb.HTTPException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IOException" title="duckdb.duckdb.IOException"><code class="xref py py-class docutils literal notranslate"><span class="pre">IOException</span></code></a></p>
<p>Thrown when an error occurs in the httpfs extension, or whilst downloading an extension.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.HTTPException.body">
<span class="sig-name descname"><span class="pre">body</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">str</span></em><a class="headerlink" href="#duckdb.HTTPException.body" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.HTTPException.headers">
<span class="sig-name descname"><span class="pre">headers</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">Dict</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></em><a class="headerlink" href="#duckdb.HTTPException.headers" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.HTTPException.reason">
<span class="sig-name descname"><span class="pre">reason</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">str</span></em><a class="headerlink" href="#duckdb.HTTPException.reason" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.HTTPException.status_code">
<span class="sig-name descname"><span class="pre">status_code</span></span><em class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">int</span></em><a class="headerlink" href="#duckdb.HTTPException.status_code" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.HugeIntegerValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">HugeIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.HugeIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.IOException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IOException</span></span><a class="headerlink" href="#duckdb.IOException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntegerValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.IntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.IntegrityError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegrityError</span></span><a class="headerlink" href="#duckdb.IntegrityError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InternalError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalError</span></span><a class="headerlink" href="#duckdb.InternalError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InternalException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalException</span></span><a class="headerlink" href="#duckdb.InternalException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.InternalError" title="duckdb.duckdb.InternalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">InternalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InterruptException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InterruptException</span></span><a class="headerlink" href="#duckdb.InterruptException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntervalValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntervalValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.IntervalValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InvalidInputException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidInputException</span></span><a class="headerlink" href="#duckdb.InvalidInputException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.InvalidTypeException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidTypeException</span></span><a class="headerlink" href="#duckdb.InvalidTypeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.LongValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">LongValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.LongValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.NotImplementedException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotImplementedException</span></span><a class="headerlink" href="#duckdb.NotImplementedException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.NotSupportedError" title="duckdb.duckdb.NotSupportedError"><code class="xref py py-class docutils literal notranslate"><span class="pre">NotSupportedError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.NotSupportedError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotSupportedError</span></span><a class="headerlink" href="#duckdb.NotSupportedError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NullValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NullValue</span></span><a class="headerlink" href="#duckdb.NullValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.OperationalError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OperationalError</span></span><a class="headerlink" href="#duckdb.OperationalError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.OutOfMemoryException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfMemoryException</span></span><a class="headerlink" href="#duckdb.OutOfMemoryException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.OutOfRangeException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfRangeException</span></span><a class="headerlink" href="#duckdb.OutOfRangeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ParserException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ParserException</span></span><a class="headerlink" href="#duckdb.ParserException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.PermissionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PermissionException</span></span><a class="headerlink" href="#duckdb.PermissionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ProgrammingError">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ProgrammingError</span></span><a class="headerlink" href="#duckdb.ProgrammingError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PythonExceptionHandling</span></span><a class="headerlink" href="#duckdb.PythonExceptionHandling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>DEFAULT</p>
<p>RETURN_NULL</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling.DEFAULT">
<span class="sig-name descname"><span class="pre">DEFAULT</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;PythonExceptionHandling.DEFAULT:</span> <span class="pre">0&gt;</span></em><a class="headerlink" href="#duckdb.PythonExceptionHandling.DEFAULT" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling.RETURN_NULL">
<span class="sig-name descname"><span class="pre">RETURN_NULL</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;PythonExceptionHandling.RETURN_NULL:</span> <span class="pre">1&gt;</span></em><a class="headerlink" href="#duckdb.PythonExceptionHandling.RETURN_NULL" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling.name">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.PythonExceptionHandling.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling.value">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">value</span></span><a class="headerlink" href="#duckdb.PythonExceptionHandling.value" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.SequenceException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SequenceException</span></span><a class="headerlink" href="#duckdb.SequenceException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.SerializationException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SerializationException</span></span><a class="headerlink" href="#duckdb.SerializationException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ShortValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ShortValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.ShortValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.StandardException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StandardException</span></span><a class="headerlink" href="#duckdb.StandardException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Error" title="duckdb.duckdb.Error"><code class="xref py py-class docutils literal notranslate"><span class="pre">Error</span></code></a></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.StarExpression">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StarExpression</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.StarExpression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>StarExpression(<a href="#id9"><span class="problematic" id="id10">*</span></a>, exclude: list = []) -&gt; duckdb.duckdb.Expression</p></li>
<li><p>StarExpression() -&gt; duckdb.duckdb.Expression</p></li>
</ol>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.StringValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StringValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.StringValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.SyntaxException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SyntaxException</span></span><a class="headerlink" href="#duckdb.SyntaxException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="duckdb.duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimeTimeZoneValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimeTimeZoneValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimeTimeZoneValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimeValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimeValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimeValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampMilisecondValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampMilisecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampMilisecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampNanosecondValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampNanosecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampNanosecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampSecondValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampSecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampSecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampTimeZoneValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampTimeZoneValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampTimeZoneValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.TransactionException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TransactionException</span></span><a class="headerlink" href="#duckdb.TransactionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="duckdb.duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.TypeMismatchException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TypeMismatchException</span></span><a class="headerlink" href="#duckdb.TypeMismatchException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UUIDValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UUIDValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UUIDValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedBinaryValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedBinaryValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedBinaryValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedIntegerValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedLongValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedLongValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedLongValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedShortValue">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedShortValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedShortValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Value">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">DuckDBPyType</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.Value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.ValueOutOfRangeException">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ValueOutOfRangeException</span></span><a class="headerlink" href="#duckdb.ValueOutOfRangeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="duckdb.duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py exception">
<dt class="sig sig-object py" id="duckdb.Warning">
<em class="property"><span class="pre">exception</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Warning</span></span><a class="headerlink" href="#duckdb.Warning" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.aggregate">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.aggregate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on DataFrame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.alias">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation from DataFrame df with the passed alias</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.append">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">by_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.append" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Append the passed DataFrame to the named table</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.array_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">array_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.array_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.arrow">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>arrow(rows_per_batch: int = 1000000, connection: duckdb.DuckDBPyConnection = None) -&gt; pyarrow.lib.Table</p></li>
</ol>
<p>Fetch a result as Arrow table following execute()</p>
<ol class="arabic simple" start="2">
<li><p>arrow(arrow_object: object, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.begin">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">begin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.begin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Start a new transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.close">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Close the connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.commit">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">commit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.commit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Commit changes performed within a transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.connect">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">connect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">database</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">':memory:'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">read_only</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">config</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.connect" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB database instance. Can take a database file name to read/write persistent data and a read_only flag if no changes are desired</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.create_function">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">create_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name:</span> <span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function:</span> <span class="pre">function</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">return_type:</span> <span class="pre">object</span> <span class="pre">=</span> <span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters:</span> <span class="pre">duckdb.duckdb.typing.DuckDBPyType</span> <span class="pre">=</span> <span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type:</span> <span class="pre">duckdb.duckdb.functional.PythonUDFType</span> <span class="pre">=</span> <span class="pre">&lt;PythonUDFType.NATIVE:</span> <span class="pre">0&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_handling:</span> <span class="pre">duckdb.duckdb.functional.FunctionNullHandling</span> <span class="pre">=</span> <span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exception_handling:</span> <span class="pre">duckdb.duckdb.PythonExceptionHandling</span> <span class="pre">=</span> <span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">side_effects:</span> <span class="pre">bool</span> <span class="pre">=</span> <span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection:</span> <span class="pre">duckdb.DuckDBPyConnection</span> <span class="pre">=</span> <span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.create_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB function out of the passing in python function so it can be used in queries</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.cursor">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.cursor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.decimal_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">decimal_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.decimal_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a decimal type with &#8216;width&#8217; and &#8216;scale&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.description">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">description</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">list</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set attributes, mainly column names</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>df(<a href="#id11"><span class="problematic" id="id12">*</span></a>, date_as_object: bool = False, connection: duckdb.DuckDBPyConnection = None) -&gt; pandas.DataFrame</p></li>
</ol>
<p>Fetch a result as DataFrame following execute()</p>
<ol class="arabic simple" start="2">
<li><p>df(df: pandas.DataFrame, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the DataFrame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.distinct">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the distinct rows from DataFrame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.dtype">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">dtype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.dtype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object from &#8216;type_str&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.duplicate">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">duplicate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.duplicate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.enum_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">enum_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.enum_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an enum type of underlying &#8216;type&#8217;, consisting of the list of &#8216;values&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.execute">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">multiple_parameter_sets</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given SQL query, optionally using prepared statements with parameters set</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.executemany">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">executemany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.executemany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given prepared statement multiple times using the list of parameter sets in parameters</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetch_arrow_table">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.fetch_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Arrow table following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetch_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.fetch_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetch_df_chunk">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.fetch_df_chunk" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of the result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetch_record_batch">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetch_record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.fetch_record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch an Arrow RecordBatchReader following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchall">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows from a result following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchdf">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchmany">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows from a result following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchnumpy">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as list of NumPy arrays following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.fetchone">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row from a result following execute</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.filesystem_is_registered">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">filesystem_is_registered</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a class="headerlink" href="#duckdb.filesystem_is_registered" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Check if a filesystem with the provided name is currently registered</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.filter">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.filter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the DataFrame df by the filter in filter_expr</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_arrow">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_csv_auto">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">delimiter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dtype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">skiprows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parallel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">all_varchar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">normalize_names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_padding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_csv_auto" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the DataFrame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_parquet">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.from_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>from_parquet(file_glob: str, binary_as_string: bool = False, <a href="#id13"><span class="problematic" id="id14">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_glob</p>
<ol class="arabic simple" start="2">
<li><p>from_parquet(file_globs: List[str], binary_as_string: bool = False, <a href="#id15"><span class="problematic" id="id16">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_globs</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_query">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_substrait">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.from_substrait" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>from_substrait(proto: bytes, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Creates a query object from the substrait plan</p>
<ol class="arabic simple" start="2">
<li><p>from_substrait(proto: bytes, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a query object from protobuf plan</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.from_substrait_json">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">from_substrait_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">json</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.from_substrait_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Serialize a query object to protobuf</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_substrait">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_substrait</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.get_substrait" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>get_substrait(query: str, connection: duckdb.DuckDBPyConnection = None, <a href="#id17"><span class="problematic" id="id18">*</span></a>, enable_optimizer: bool = True) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Serialize a query object to protobuf</p>
<ol class="arabic simple" start="2">
<li><p>get_substrait(query: str, connection: duckdb.DuckDBPyConnection = None, <a href="#id19"><span class="problematic" id="id20">*</span></a>, enable_optimizer: bool = True) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Serialize a query to protobuf</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_substrait_json">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_substrait_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.get_substrait_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>get_substrait_json(query: str, connection: duckdb.DuckDBPyConnection = None, <a href="#id21"><span class="problematic" id="id22">*</span></a>, enable_optimizer: bool = True) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Serialize a query object to protobuf</p>
<ol class="arabic simple" start="2">
<li><p>get_substrait_json(query: str, connection: duckdb.DuckDBPyConnection = None, <a href="#id23"><span class="problematic" id="id24">*</span></a>, enable_optimizer: bool = True) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Serialize a query to protobuf on the JSON format</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.get_table_names">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">get_table_names</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Set</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.get_table_names" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the required table names from a query</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.install_extension">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">install_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">force_install</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.install_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Install an extension by name</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.interrupt">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">interrupt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.interrupt" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Interrupt pending operations</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.limit">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.limit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve the first n rows from the DataFrame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.list_filesystems">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">list_filesystems</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.list_filesystems" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>List registered filesystems, including builtin ones</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.list_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">list_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.list_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.load_extension">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">load_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.load_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Load an installed extension</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.map_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">map_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.map_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a map type object from &#8216;key_type&#8217; and &#8216;value_type&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.order">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.order" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the DataFrame df by order_expr</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.pl">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">pl</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb::PolarsDataFrame</span></span></span><a class="headerlink" href="#duckdb.pl" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Polars DataFrame following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.project">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">project_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.project" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the DataFrame df by the projection in project_expr</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.query_df">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">query_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.query_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that contains the content of DataFrame df</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.read_csv">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">read_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">delimiter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">dtype</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">skiprows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parallel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">all_varchar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">normalize_names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_padding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">names</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.read_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.read_json">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">read_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">maximum_depth</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">records</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.read_json" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the JSON file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.read_parquet">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">read_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.read_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>read_parquet(file_glob: str, binary_as_string: bool = False, <a href="#id25"><span class="problematic" id="id26">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_glob</p>
<ol class="arabic simple" start="2">
<li><p>read_parquet(file_globs: List[str], binary_as_string: bool = False, <a href="#id27"><span class="problematic" id="id28">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_globs</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.register">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">python_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.register" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register the passed Python Object value for querying with a view</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.register_filesystem">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">register_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">filesystem</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">fsspec.AbstractFileSystem</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.register_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register a fsspec compliant filesystem</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.remove_function">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">remove_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.remove_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Remove a previously created function</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.rollback">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">rollback</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.rollback" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Roll back changes performed within a transaction</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.row_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">row_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.row_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.rowcount">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">rowcount</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span><a class="headerlink" href="#duckdb.rowcount" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set row count</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.sql">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">sql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.sql" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.sqltype">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">sqltype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.sqltype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object from &#8216;type_str&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.string_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">string_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.string_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a string type with an optional collation</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.struct_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">struct_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.struct_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.table">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the name&#8217;d table</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.table_function">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">table_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.table_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the name&#8217;d table function with given parameters</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.tf">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors following execute()</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.token_type">
<em class="property"><span class="pre">class</span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">token_type</span></span><a class="headerlink" href="#duckdb.token_type" title="Link to this definition">&#182;</a>
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
<span class="sig-name descname"><span class="pre">comment</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.comment:</span> <span class="pre">5&gt;</span></em><a class="headerlink" href="#duckdb.token_type.comment" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.identifier">
<span class="sig-name descname"><span class="pre">identifier</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.identifier:</span> <span class="pre">0&gt;</span></em><a class="headerlink" href="#duckdb.token_type.identifier" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.keyword">
<span class="sig-name descname"><span class="pre">keyword</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.keyword:</span> <span class="pre">4&gt;</span></em><a class="headerlink" href="#duckdb.token_type.keyword" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.token_type.name">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.token_type.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.numeric_const">
<span class="sig-name descname"><span class="pre">numeric_const</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.numeric_const:</span> <span class="pre">1&gt;</span></em><a class="headerlink" href="#duckdb.token_type.numeric_const" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.operator">
<span class="sig-name descname"><span class="pre">operator</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.operator:</span> <span class="pre">3&gt;</span></em><a class="headerlink" href="#duckdb.token_type.operator" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.token_type.string_const">
<span class="sig-name descname"><span class="pre">string_const</span></span><em class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;token_type.string_const:</span> <span class="pre">2&gt;</span></em><a class="headerlink" href="#duckdb.token_type.string_const" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.token_type.value">
<em class="property"><span class="pre">property</span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">value</span></span><a class="headerlink" href="#duckdb.token_type.value" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.tokenize">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">tokenize</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.tokenize" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Tokenizes a SQL string, returning a list of (position, type) tuples that can be used for e.g. syntax highlighting</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.torch">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors following execute()</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object from &#8216;type_str&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.union_type">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">union_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">members</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb.duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.union_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a union type object from &#8216;members&#8217;</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.unregister">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">unregister</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.unregister" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister the view name</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.unregister_filesystem">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">unregister_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.unregister_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister a filesystem</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.values">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.values" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>values(values: object, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the passed values</p>
<ol class="arabic simple" start="2">
<li><p>values(values: object, connection: duckdb.DuckDBPyConnection = None) -&gt; duckdb.duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the passed values</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.view">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="duckdb.duckdb.DuckDBPyRelation"><span class="pre">duckdb.duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the name&#8217;d view</p>
</dd>
</dl>

<dl class="py function">
<dt class="sig sig-object py" id="duckdb.write_csv">
<span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">connection</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="duckdb.duckdb.DuckDBPyConnection"><span class="pre">duckdb.DuckDBPyConnection</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.write_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the DataFrame df to a CSV file in file_name</p>
</dd>
</dl>



<div class="clearer"></div>
</div>
</div>
</div>
