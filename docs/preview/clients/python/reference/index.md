---
layout: docu
title: Python Client API
---

<div class="documentwrapper">
<div class="bodywrapper">
<div class="body" role="main">

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BinaryValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinaryValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BinaryValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BinderException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BinderException</span></span><a class="headerlink" href="#duckdb.BinderException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BitValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BitValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BitValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BlobValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BlobValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BlobValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.BooleanValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">BooleanValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.BooleanValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.CSVLineTerminator">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CSVLineTerminator</span></span><a class="headerlink" href="#duckdb.CSVLineTerminator" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>LINE_FEED</p>
<p>CARRIAGE_RETURN_LINE_FEED</p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.CSVLineTerminator.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.CSVLineTerminator.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.CatalogException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">CatalogException</span></span><a class="headerlink" href="#duckdb.CatalogException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ConnectionException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConnectionException</span></span><a class="headerlink" href="#duckdb.ConnectionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ConstraintException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConstraintException</span></span><a class="headerlink" href="#duckdb.ConstraintException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IntegrityError" title="_duckdb.IntegrityError"><code class="xref py py-class docutils literal notranslate"><span class="pre">IntegrityError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ConversionException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ConversionException</span></span><a class="headerlink" href="#duckdb.ConversionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="_duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DBAPITypeObject">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DBAPITypeObject</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">DuckDBPyType</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DBAPITypeObject" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DataError">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DataError</span></span><a class="headerlink" href="#duckdb.DataError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DateValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DateValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DateValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DecimalValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DecimalValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DecimalValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DoubleValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DoubleValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DoubleValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyConnection</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.append">
<span class="sig-name descname"><span class="pre">append</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">by_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.append" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Append the passed DataFrame to the named table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.array_type">
<span class="sig-name descname"><span class="pre">array_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.array_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an array type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch an Arrow RecordBatchReader following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.begin">
<span class="sig-name descname"><span class="pre">begin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.begin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Start a new transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.checkpoint">
<span class="sig-name descname"><span class="pre">checkpoint</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.checkpoint" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Synchronizes data in the write-ahead log (WAL) to the database data file (no-op for in-memory connections)</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Close the connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.commit">
<span class="sig-name descname"><span class="pre">commit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.commit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Commit changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.create_function">
<span class="sig-name descname"><span class="pre">create_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self:</span> <span class="pre">_duckdb.DuckDBPyConnection</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">name:</span> <span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function:</span> <span class="pre">collections.abc.Callable</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters:</span> <span class="pre">object</span> <span class="pre">=</span> <span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">return_type:</span> <span class="pre">_duckdb.typing.DuckDBPyType</span> <span class="pre">=</span> <span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">*</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type:</span> <span class="pre">_duckdb.functional.PythonUDFType</span> <span class="pre">=</span> <span class="pre">&lt;PythonUDFType.NATIVE:</span> <span class="pre">0&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_handling:</span> <span class="pre">_duckdb.functional.FunctionNullHandling</span> <span class="pre">=</span> <span class="pre">&lt;FunctionNullHandling.DEFAULT:</span> <span class="pre">0&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">exception_handling:</span> <span class="pre">_duckdb.PythonExceptionHandling</span> <span class="pre">=</span> <span class="pre">&lt;PythonExceptionHandling.DEFAULT:</span> <span class="pre">0&gt;</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">side_effects:</span> <span class="pre">bool</span> <span class="pre">=</span> <span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.create_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a DuckDB function out of the passing in Python function so it can be used in queries</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.cursor">
<span class="sig-name descname"><span class="pre">cursor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.cursor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.decimal_type">
<span class="sig-name descname"><span class="pre">decimal_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">scale</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.decimal_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a decimal type with &#8216;width&#8217; and &#8216;scale&#8217;</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.description">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set attributes, mainly column names</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.dtype">
<span class="sig-name descname"><span class="pre">dtype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.dtype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.duplicate">
<span class="sig-name descname"><span class="pre">duplicate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.duplicate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a duplicate of the current connection</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.enum_type">
<span class="sig-name descname"><span class="pre">enum_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.enum_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create an enum type of underlying &#8216;type&#8217;, consisting of the list of &#8216;values&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given SQL query, optionally using prepared statements with parameters set</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.executemany">
<span class="sig-name descname"><span class="pre">executemany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.executemany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute the given prepared statement multiple times using the list of parameter sets in parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.extract_statements">
<span class="sig-name descname"><span class="pre">extract_statements</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.extract_statements" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Parse the query string and extract the Statement object(s) produced</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Arrow table following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df">
<span class="sig-name descname"><span class="pre">fetch_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_df_chunk">
<span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_df_chunk" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a chunk of the result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetch_record_batch">
<span class="sig-name descname"><span class="pre">fetch_record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetch_record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch an Arrow RecordBatchReader following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch all rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch the next set of rows from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as list of NumPy arrays following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a single row from a result following execute</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.filesystem_is_registered">
<span class="sig-name descname"><span class="pre">filesystem_is_registered</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.filesystem_is_registered" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Check if a filesystem with the provided name is currently registered</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_arrow">
<span class="sig-name descname"><span class="pre">from_arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arrow_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from an Arrow object</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_csv_auto">
<span class="sig-name descname"><span class="pre">from_csv_auto</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_csv_auto" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_df">
<span class="sig-name descname"><span class="pre">from_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">df</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the DataFrame in df</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_parquet">
<span class="sig-name descname"><span class="pre">from_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Overloaded function.</p>
<ol class="arabic simple">
<li><p>from_parquet(self: _duckdb.DuckDBPyConnection, file_glob: str, binary_as_string: bool = False, <a href="#id1"><span class="problematic" id="id2">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; _duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_glob</p>
<ol class="arabic simple" start="2">
<li><p>from_parquet(self: _duckdb.DuckDBPyConnection, file_globs: collections.abc.Sequence[str], binary_as_string: bool = False, <a href="#id3"><span class="problematic" id="id4">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; _duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_globs</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.from_query">
<span class="sig-name descname"><span class="pre">from_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.from_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.get_table_names">
<span class="sig-name descname"><span class="pre">get_table_names</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">qualified</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">set</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.get_table_names" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Extract the required table names from a query</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.install_extension">
<span class="sig-name descname"><span class="pre">install_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">force_install</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">repository</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">repository_url</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">version</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.install_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Install an extension by name, with an optional version and/or repository to get the extension from</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.interrupt">
<span class="sig-name descname"><span class="pre">interrupt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.interrupt" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Interrupt pending operations</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.list_filesystems">
<span class="sig-name descname"><span class="pre">list_filesystems</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.list_filesystems" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>List registered filesystems, including builtin ones</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.list_type">
<span class="sig-name descname"><span class="pre">list_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.list_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a list type object of &#8216;type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.load_extension">
<span class="sig-name descname"><span class="pre">load_extension</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">extension</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.load_extension" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Load an installed extension</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.map_type">
<span class="sig-name descname"><span class="pre">map_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.map_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a map type object from &#8216;key_type&#8217; and &#8216;value_type&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.pl">
<span class="sig-name descname"><span class="pre">pl</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">lazy</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb::PolarsDataFrame</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.pl" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as Polars DataFrame following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.query_progress">
<span class="sig-name descname"><span class="pre">query_progress</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.query_progress" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Query progress of pending operation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_csv">
<span class="sig-name descname"><span class="pre">read_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the CSV file in &#8216;name&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.read_json">
<span class="sig-name descname"><span class="pre">read_json</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">path_or_buffer</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sample_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">maximum_depth</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">records</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">maximum_object_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_errors</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">convert_strings_to_integers</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">field_appearance_threshold</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">map_inference_threshold</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">maximum_sample_files</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filename</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">hive_partitioning</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">union_by_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">hive_types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">hive_types_autocast</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.read_json" title="Link to this definition">&#182;</a>
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
<li><p>read_parquet(self: _duckdb.DuckDBPyConnection, file_glob: str, binary_as_string: bool = False, <a href="#id5"><span class="problematic" id="id6">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; _duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_glob</p>
<ol class="arabic simple" start="2">
<li><p>read_parquet(self: _duckdb.DuckDBPyConnection, file_globs: collections.abc.Sequence[str], binary_as_string: bool = False, <a href="#id7"><span class="problematic" id="id8">*</span></a>, file_row_number: bool = False, filename: bool = False, hive_partitioning: bool = False, union_by_name: bool = False, compression: object = None) -&gt; _duckdb.DuckDBPyRelation</p></li>
</ol>
<p>Create a relation object from the Parquet files in file_globs</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register">
<span class="sig-name descname"><span class="pre">register</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">python_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register the passed Python Object value for querying with a view</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.register_filesystem">
<span class="sig-name descname"><span class="pre">register_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filesystem</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">fsspec.AbstractFileSystem</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.register_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Register a fsspec compliant filesystem</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.remove_function">
<span class="sig-name descname"><span class="pre">remove_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.remove_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Remove a previously created function</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rollback">
<span class="sig-name descname"><span class="pre">rollback</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rollback" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Roll back changes performed within a transaction</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.row_type">
<span class="sig-name descname"><span class="pre">row_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.row_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.rowcount">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">rowcount</span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.rowcount" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get result set row count</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.sql">
<span class="sig-name descname"><span class="pre">sql</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">params</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.sql" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run a SQL query. If it is a SELECT statement, create a relation object from the given SQL query, otherwise run the query as-is.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.sqltype">
<span class="sig-name descname"><span class="pre">sqltype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.sqltype" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.string_type">
<span class="sig-name descname"><span class="pre">string_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.string_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a string type with an optional collation</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.struct_type">
<span class="sig-name descname"><span class="pre">struct_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">fields</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.struct_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a struct type object from &#8216;fields&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table">
<span class="sig-name descname"><span class="pre">table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the named table</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.table_function">
<span class="sig-name descname"><span class="pre">table_function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">parameters</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.table_function" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the named table function with given parameters</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.tf">
<span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.torch">
<span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors following execute()</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.type">
<span class="sig-name descname"><span class="pre">type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type_str</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a type object by parsing the &#8216;type_str&#8217; string</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.union_type">
<span class="sig-name descname"><span class="pre">union_type</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">members</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.union_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a union type object from &#8216;members&#8217;</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister">
<span class="sig-name descname"><span class="pre">unregister</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister the view name</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.unregister_filesystem">
<span class="sig-name descname"><span class="pre">unregister_filesystem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.unregister_filesystem" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Unregister a filesystem</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.values">
<span class="sig-name descname"><span class="pre">values</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.values" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object from the passed values</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyConnection.view">
<span class="sig-name descname"><span class="pre">view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyConnection" title="_duckdb.DuckDBPyConnection"><span class="pre">_duckdb.DuckDBPyConnection</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyConnection.view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a relation object for the named view</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">DuckDBPyRelation</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}">Relational API page</a>.</div>
<br><dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.aggregate">
<span class="sig-name descname"><span class="pre">aggregate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">aggr_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.aggregate" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the aggregate aggr_expr by the optional groups group_expr on the relation</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#aggregate">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.alias">
<span class="sig-name descname"><span class="pre">alias</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the name of the current alias</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#alias">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.any_value">
<span class="sig-name descname"><span class="pre">any_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.any_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the first non-null value from a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#any_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.apply">
<span class="sig-name descname"><span class="pre">apply</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">function_parameter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.apply" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Compute the function of a single column or a list of columns by the optional groups on the relation</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#apply">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arg_max">
<span class="sig-name descname"><span class="pre">arg_max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arg_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arg_max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Finds the row with the maximum value for a value column and returns the value of that row for an argument column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#arg_max">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arg_min">
<span class="sig-name descname"><span class="pre">arg_min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arg_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">value_column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arg_min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Finds the row with the minimum value for a value column and returns the value of that row for an argument column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#arg_min">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.arrow">
<span class="sig-name descname"><span class="pre">arrow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.arrow" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#arrow">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.avg">
<span class="sig-name descname"><span class="pre">avg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.avg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average on a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#avg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_and">
<span class="sig-name descname"><span class="pre">bit_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise AND of all bits present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#bit_and">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_or">
<span class="sig-name descname"><span class="pre">bit_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise OR of all bits present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#bit_or">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bit_xor">
<span class="sig-name descname"><span class="pre">bit_xor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bit_xor" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the bitwise XOR of all bits present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#bit_xor">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bitstring_agg">
<span class="sig-name descname"><span class="pre">bitstring_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">min</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bitstring_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes a bitstring with bits set for each distinct value in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#bitstring_agg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bool_and">
<span class="sig-name descname"><span class="pre">bool_and</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bool_and" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the logical AND of all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#bool_and">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.bool_or">
<span class="sig-name descname"><span class="pre">bool_or</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.bool_or" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the logical OR of all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#bool_or">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.close">
<span class="sig-name descname"><span class="pre">close</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.close" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Closes the result</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#close">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.columns">
<span class="sig-name descname"><span class="pre">columns</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.columns" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the names of the columns of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#columns">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.count">
<span class="sig-name descname"><span class="pre">count</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.count" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the number of elements present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#count">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create">
<span class="sig-name descname"><span class="pre">create</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#create">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.create_view">
<span class="sig-name descname"><span class="pre">create_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.create_view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#create_view">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cross">
<span class="sig-name descname"><span class="pre">cross</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cross" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create cross/cartesian product of two relational objects</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#cross">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.cume_dist">
<span class="sig-name descname"><span class="pre">cume_dist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.cume_dist" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the cumulative distribution within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#cume_dist">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dense_rank">
<span class="sig-name descname"><span class="pre">dense_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dense_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the dense rank within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#dense_rank">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.describe">
<span class="sig-name descname"><span class="pre">describe</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.describe" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Gives basic statistics (e.g., min, max) and if NULL exists for each column of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#describe">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.description">
<span class="sig-name descname"><span class="pre">description</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.description" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return the description of the result</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#description">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.df">
<span class="sig-name descname"><span class="pre">df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#df">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.distinct">
<span class="sig-name descname"><span class="pre">distinct</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.distinct" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Retrieve distinct rows from this relation object</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#distinct">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.dtypes">
<span class="sig-name descname"><span class="pre">dtypes</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.dtypes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the types of the columns of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#dtypes">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.except_">
<span class="sig-name descname"><span class="pre">except_</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.except_" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set except of this relation object with another relation object in other_rel</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#except_">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.execute">
<span class="sig-name descname"><span class="pre">execute</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.execute" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Transform the relation into a result set</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#execute">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.explain">
<span class="sig-name descname"><span class="pre">explain</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.ExplainType" title="_duckdb.ExplainType"><span class="pre">_duckdb.ExplainType</span></a></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'standard'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.explain" title="Link to this definition">&#182;</a>
</dt>
<dd>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#explain">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.favg">
<span class="sig-name descname"><span class="pre">favg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.favg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average of all values present in a given column using a more accurate floating point summation (Kahan Sum)</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#favg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_arrow_reader">
<span class="sig-name descname"><span class="pre">fetch_arrow_reader</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_arrow_reader" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetch_arrow_reader">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_arrow_table">
<span class="sig-name descname"><span class="pre">fetch_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetch_arrow_table">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_df_chunk">
<span class="sig-name descname"><span class="pre">fetch_df_chunk</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">vectors_per_chunk</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_df_chunk" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch a chunk of the rows</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetch_df_chunk">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetch_record_batch">
<span class="sig-name descname"><span class="pre">fetch_record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">rows_per_batch</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.RecordBatchReader.html#pyarrow.RecordBatchReader" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.RecordBatchReader</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetch_record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and return an Arrow Record Batch Reader that yields all rows</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetch_record_batch">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchall">
<span class="sig-name descname"><span class="pre">fetchall</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchall" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a list of tuples</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetchall">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchdf">
<span class="sig-name descname"><span class="pre">fetchdf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchdf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetchdf">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchmany">
<span class="sig-name descname"><span class="pre">fetchmany</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">list</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchmany" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch the next set of rows as a list of tuples</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetchmany">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchnumpy">
<span class="sig-name descname"><span class="pre">fetchnumpy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchnumpy" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Python dict mapping each column to one numpy arrays</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetchnumpy">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fetchone">
<span class="sig-name descname"><span class="pre">fetchone</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">tuple</span><span class="p"><span class="pre">]</span></span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fetchone" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch a single row as a tuple</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fetchone">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.filter">
<span class="sig-name descname"><span class="pre">filter</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.filter" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Filter the relation object by the filter in filter_expr</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#filter">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.first">
<span class="sig-name descname"><span class="pre">first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the first value of a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#first">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.first_value">
<span class="sig-name descname"><span class="pre">first_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.first_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the first value within the group or partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#first_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.fsum">
<span class="sig-name descname"><span class="pre">fsum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.fsum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sum of all values present in a given column using a more accurate floating point summation (Kahan Sum)</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#fsum">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.geomean">
<span class="sig-name descname"><span class="pre">geomean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.geomean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the geometric mean over all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#geomean">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.histogram">
<span class="sig-name descname"><span class="pre">histogram</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.histogram" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the histogram over all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#histogram">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert">
<span class="sig-name descname"><span class="pre">insert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the given values into the relation</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#insert">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.insert_into">
<span class="sig-name descname"><span class="pre">insert_into</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.insert_into" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Inserts the relation object into an existing table named table_name</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#insert_into">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.intersect">
<span class="sig-name descname"><span class="pre">intersect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.intersect" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set intersection of this relation object with another relation object in other_rel</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#intersect">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.join">
<span class="sig-name descname"><span class="pre">join</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">other_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">how</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'inner'</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.join" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Join the relation object with another relation object in other_rel using the join condition expression in join_condition. Types supported are &#8216;inner&#8217;, &#8216;left&#8217;, &#8216;right&#8217;, &#8216;outer&#8217;, &#8216;semi&#8217; and &#8216;anti&#8217;</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#join">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.lag">
<span class="sig-name descname"><span class="pre">lag</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'NULL'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.lag" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the lag within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#lag">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.last">
<span class="sig-name descname"><span class="pre">last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the last value of a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#last">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.last_value">
<span class="sig-name descname"><span class="pre">last_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.last_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the last value within the group or partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#last_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.lead">
<span class="sig-name descname"><span class="pre">lead</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">'NULL'</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.lead" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the lead within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#lead">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.limit">
<span class="sig-name descname"><span class="pre">limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">n</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.limit" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Only retrieve the first n rows from this relation object, starting at offset</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#limit">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.list">
<span class="sig-name descname"><span class="pre">list</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.list" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns a list containing all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#list">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.map">
<span class="sig-name descname"><span class="pre">map</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">map_function</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">collections.abc.Callable</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">schema</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">object</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.map" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Calls the passed function on the relation</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#map">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.max">
<span class="sig-name descname"><span class="pre">max</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.max" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the maximum value present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#max">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mean">
<span class="sig-name descname"><span class="pre">mean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mean" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the average on a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#mean">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.median">
<span class="sig-name descname"><span class="pre">median</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.median" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the median over all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#median">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.min">
<span class="sig-name descname"><span class="pre">min</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.min" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the minimum value present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#min">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.mode">
<span class="sig-name descname"><span class="pre">mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.mode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the mode over all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#mode">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.n_tile">
<span class="sig-name descname"><span class="pre">n_tile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">num_buckets</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.n_tile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Divides the partition as equally as possible into num_buckets</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#n_tile">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.nth_value">
<span class="sig-name descname"><span class="pre">nth_value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">offset</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore_nulls</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.nth_value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the nth value within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#nth_value">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.order">
<span class="sig-name descname"><span class="pre">order</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">order_expr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.order" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by order_expr</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#order">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.percent_rank">
<span class="sig-name descname"><span class="pre">percent_rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.percent_rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the relative rank within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#percent_rank">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.pl">
<span class="sig-name descname"><span class="pre">pl</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">lazy</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">duckdb::PolarsDataFrame</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.pl" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a Polars DataFrame</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#pl">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.product">
<span class="sig-name descname"><span class="pre">product</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.product" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the product of all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#product">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.project">
<span class="sig-name descname"><span class="pre">project</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.project" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#project">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile">
<span class="sig-name descname"><span class="pre">quantile</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the exact quantile value for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#quantile">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile_cont">
<span class="sig-name descname"><span class="pre">quantile_cont</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile_cont" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the interpolated quantile value for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#quantile_cont">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.quantile_disc">
<span class="sig-name descname"><span class="pre">quantile_disc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">q</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0.5</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.quantile_disc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the exact quantile value for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#quantile_disc">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.query">
<span class="sig-name descname"><span class="pre">query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">virtual_table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sql_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Run the given SQL query in sql_query on the view named virtual_table_name that refers to the relation object</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#query">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rank">
<span class="sig-name descname"><span class="pre">rank</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rank" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the rank within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#rank">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.rank_dense">
<span class="sig-name descname"><span class="pre">rank_dense</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.rank_dense" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the dense rank within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#rank_dense">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.record_batch">
<span class="sig-name descname"><span class="pre">record_batch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">object</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.record_batch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#record_batch">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.row_number">
<span class="sig-name descname"><span class="pre">row_number</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.row_number" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the row number within the partition</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#row_number">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select">
<span class="sig-name descname"><span class="pre">select</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Project the relation object by the projection in project_expr</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#select">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select_dtypes">
<span class="sig-name descname"><span class="pre">select_dtypes</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select_dtypes" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Select columns from the relation, by filtering based on type(s)</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#select_dtypes">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.select_types">
<span class="sig-name descname"><span class="pre">select_types</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">types</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.select_types" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Select columns from the relation, by filtering based on type(s)</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#select_types">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.set_alias">
<span class="sig-name descname"><span class="pre">set_alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">alias</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.set_alias" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Rename the relation object to new alias</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#set_alias">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.shape">
<span class="sig-name descname"><span class="pre">shape</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.shape" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Tuple of # of rows, # of columns in relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#shape">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">SupportsInt</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_rows</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">SupportsInt</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">max_col_width</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">SupportsInt</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">null_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Optional</span><span class="p"><span class="pre">[</span></span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">render_mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.show" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Display a summary of the data</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#show">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sort">
<span class="sig-name descname"><span class="pre">sort</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sort" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Reorder the relation object by the provided expressions</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#sort">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sql_query">
<span class="sig-name descname"><span class="pre">sql_query</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sql_query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the SQL query that is equivalent to the relation</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#sql_query">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.std">
<span class="sig-name descname"><span class="pre">std</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.std" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#std">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev">
<span class="sig-name descname"><span class="pre">stddev</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#stddev">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev_pop">
<span class="sig-name descname"><span class="pre">stddev_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the population standard deviation for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#stddev_pop">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.stddev_samp">
<span class="sig-name descname"><span class="pre">stddev_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.stddev_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample standard deviation for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#stddev_samp">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.string_agg">
<span class="sig-name descname"><span class="pre">string_agg</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">','</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.string_agg" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Concatenates the values present in a given column with a separator</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#string_agg">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.sum">
<span class="sig-name descname"><span class="pre">sum</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.sum" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sum of all values present in a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#sum">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.tf">
<span class="sig-name descname"><span class="pre">tf</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.tf" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of TensorFlow Tensors</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#tf">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_arrow_table">
<span class="sig-name descname"><span class="pre">to_arrow_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">batch_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SupportsInt</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">1000000</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://arrow.apache.org/docs/9.0/python/generated/pyarrow.Table.html#pyarrow.Table" title="(in Apache Arrow v9.0.0)"><span class="pre">pyarrow.lib.Table</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_arrow_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as an Arrow Table</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#to_arrow_table">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_csv">
<span class="sig-name descname"><span class="pre">to_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_rep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quoting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#to_csv">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_df">
<span class="sig-name descname"><span class="pre">to_df</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_as_object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference external" href="https://pandas.pydata.org/pandas-docs/version/1.5.1/reference/api/pandas.DataFrame.html#pandas.DataFrame" title="(in pandas v1.5.1)"><span class="pre">pandas.DataFrame</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_df" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Execute and fetch all rows as a pandas DataFrame</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#to_df">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_parquet">
<span class="sig-name descname"><span class="pre">to_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">field_ids</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size_bytes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">append</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a Parquet file in &#8216;file_name&#8217;</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#to_parquet">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_table">
<span class="sig-name descname"><span class="pre">to_table</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">table_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_table" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a new table named table_name with the contents of the relation object</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#to_table">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.to_view">
<span class="sig-name descname"><span class="pre">to_view</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">view_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">replace</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.to_view" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Creates a view named view_name that refers to the relation object</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#to_view">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.torch">
<span class="sig-name descname"><span class="pre">torch</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.torch" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Fetch a result as dict of PyTorch Tensors</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#torch">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.type">
<span class="sig-name descname"><span class="pre">type</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the type of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#type">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.types">
<span class="sig-name descname"><span class="pre">types</span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.types" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return a list containing the types of the columns of the relation.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#types">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.union">
<span class="sig-name descname"><span class="pre">union</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">union_rel</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.union" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create the set union of this relation object with another relation object in other_rel</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#union">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.unique">
<span class="sig-name descname"><span class="pre">unique</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">unique_aggr</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.unique" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Returns the distinct values in a column.</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#unique">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.update">
<span class="sig-name descname"><span class="pre">update</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">set</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.update" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Update the given relation with the provided expressions</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#update">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.value_counts">
<span class="sig-name descname"><span class="pre">value_counts</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.value_counts" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the number of elements present in a given column, also projecting the original column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#value_counts">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var">
<span class="sig-name descname"><span class="pre">var</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#var">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var_pop">
<span class="sig-name descname"><span class="pre">var_pop</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var_pop" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the population variance for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#var_pop">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.var_samp">
<span class="sig-name descname"><span class="pre">var_samp</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.var_samp" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#var_samp">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.variance">
<span class="sig-name descname"><span class="pre">variance</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">column</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">window_spec</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">projected_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.variance" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Computes the sample variance for a given column</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#variance">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_csv">
<span class="sig-name descname"><span class="pre">write_csv</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">na_rep</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">header</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quotechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">escapechar</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">date_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">timestamp_format</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">quoting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">encoding</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_csv" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a CSV file in &#8216;file_name&#8217;</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#write_csv">Relational API page</a>.</div>
<br>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.DuckDBPyRelation.write_parquet">
<span class="sig-name descname"><span class="pre">write_parquet</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.DuckDBPyRelation" title="_duckdb.DuckDBPyRelation"><span class="pre">_duckdb.DuckDBPyRelation</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">file_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="keyword-only-separator o"><abbr title="Keyword-only parameters separator (PEP 3102)"><span class="pre">*</span></abbr></span></em>, <em class="sig-param"><span class="n"><span class="pre">compression</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">field_ids</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size_bytes</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">row_group_size</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">overwrite</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">per_thread_output</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">use_tmp_file</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">partition_by</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">write_partition_columns</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">append</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.DuckDBPyRelation.write_parquet" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Write the relation object to a Parquet file in &#8216;file_name&#8217;</p>
<div>Detailed examples can be found at <a href="{% link docs/preview/clients/python/relational_api.md %}#write_parquet">Relational API page</a>.</div>
<br>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Error">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Error</span></span><a class="headerlink" href="#duckdb.Error" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ExpectedResultType">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ExpectedResultType</span></span><a class="headerlink" href="#duckdb.ExpectedResultType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>QUERY_RESULT</p>
<p>CHANGED_ROWS</p>
<p>NOTHING</p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.ExpectedResultType.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.ExpectedResultType.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ExplainType">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ExplainType</span></span><a class="headerlink" href="#duckdb.ExplainType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>STANDARD</p>
<p>ANALYZE</p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.ExplainType.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.ExplainType.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Expression">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Expression</span></span><a class="headerlink" href="#duckdb.Expression" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.alias">
<span class="sig-name descname"><span class="pre">alias</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">arg0</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.alias" title="Link to this definition">&#182;</a>
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
<span class="sig-name descname"><span class="pre">asc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.asc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the order by modifier to ASCENDING.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.between">
<span class="sig-name descname"><span class="pre">between</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">lower</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">upper</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.between" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.cast">
<span class="sig-name descname"><span class="pre">cast</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">_duckdb.typing.DuckDBPyType</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.cast" title="Link to this definition">&#182;</a>
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
<dt class="sig sig-object py" id="duckdb.Expression.collate">
<span class="sig-name descname"><span class="pre">collate</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">collation</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.collate" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.desc">
<span class="sig-name descname"><span class="pre">desc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.desc" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the order by modifier to DESCENDING.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.get_name">
<span class="sig-name descname"><span class="pre">get_name</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#duckdb.Expression.get_name" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return the stringified version of the expression.</p>
<dl class="simple">
<dt>Returns:</dt>
<dd>
<p>str: The string representation.</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isin">
<span class="sig-name descname"><span class="pre">isin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isin" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Return an IN expression comparing self to the input arguments.</p>
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
<span class="sig-name descname"><span class="pre">isnotin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="o"><span class="pre">*</span></span><span class="n"><span class="pre">args</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnotin" title="Link to this definition">&#182;</a>
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
<dt class="sig sig-object py" id="duckdb.Expression.isnotnull">
<span class="sig-name descname"><span class="pre">isnotnull</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnotnull" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a binary IS NOT NULL expression from self</p>
<dl class="simple">
<dt>Returns:</dt>
<dd>
<p>DuckDBPyExpression: self IS NOT NULL</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.isnull">
<span class="sig-name descname"><span class="pre">isnull</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.isnull" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Create a binary IS NULL expression from self</p>
<dl class="simple">
<dt>Returns:</dt>
<dd>
<p>DuckDBPyExpression: self IS NULL</p>
</dd>
</dl>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.nulls_first">
<span class="sig-name descname"><span class="pre">nulls_first</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.nulls_first" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the NULL order by modifier to NULLS FIRST.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.nulls_last">
<span class="sig-name descname"><span class="pre">nulls_last</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.nulls_last" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Set the NULL order by modifier to NULLS LAST.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.otherwise">
<span class="sig-name descname"><span class="pre">otherwise</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.otherwise" title="Link to this definition">&#182;</a>
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
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#duckdb.Expression.show" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Print the stringified version of the expression.</p>
</dd>
</dl>

<dl class="py method">
<dt class="sig sig-object py" id="duckdb.Expression.when">
<span class="sig-name descname"><span class="pre">when</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">self</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">condition</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em>, <em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#8594;</span> <span class="sig-return-typehint"><a class="reference internal" href="#duckdb.Expression" title="_duckdb.Expression"><span class="pre">_duckdb.Expression</span></a></span></span><a class="headerlink" href="#duckdb.Expression.when" title="Link to this definition">&#182;</a>
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

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.FatalException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FatalException</span></span><a class="headerlink" href="#duckdb.FatalException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.FloatValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">FloatValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.FloatValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.HTTPException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">HTTPException</span></span><a class="headerlink" href="#duckdb.HTTPException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.IOException" title="_duckdb.IOException"><code class="xref py py-class docutils literal notranslate"><span class="pre">IOException</span></code></a></p>
<p>Thrown when an error occurs in the httpfs extension, or whilst downloading an extension.</p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.HugeIntegerValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">HugeIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.HugeIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IOException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IOException</span></span><a class="headerlink" href="#duckdb.IOException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntegerValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.IntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntegrityError">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntegrityError</span></span><a class="headerlink" href="#duckdb.IntegrityError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InternalError">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalError</span></span><a class="headerlink" href="#duckdb.InternalError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InternalException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InternalException</span></span><a class="headerlink" href="#duckdb.InternalException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.InternalError" title="_duckdb.InternalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">InternalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InterruptException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InterruptException</span></span><a class="headerlink" href="#duckdb.InterruptException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.IntervalValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">IntervalValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.IntervalValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InvalidInputException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidInputException</span></span><a class="headerlink" href="#duckdb.InvalidInputException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.InvalidTypeException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">InvalidTypeException</span></span><a class="headerlink" href="#duckdb.InvalidTypeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.LongValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">LongValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.LongValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NotImplementedException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotImplementedException</span></span><a class="headerlink" href="#duckdb.NotImplementedException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.NotSupportedError" title="_duckdb.NotSupportedError"><code class="xref py py-class docutils literal notranslate"><span class="pre">NotSupportedError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NotSupportedError">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NotSupportedError</span></span><a class="headerlink" href="#duckdb.NotSupportedError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.NullValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">NullValue</span></span><a class="headerlink" href="#duckdb.NullValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.OperationalError">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OperationalError</span></span><a class="headerlink" href="#duckdb.OperationalError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.OutOfMemoryException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfMemoryException</span></span><a class="headerlink" href="#duckdb.OutOfMemoryException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.OutOfRangeException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">OutOfRangeException</span></span><a class="headerlink" href="#duckdb.OutOfRangeException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="_duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ParserException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ParserException</span></span><a class="headerlink" href="#duckdb.ParserException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.PermissionException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PermissionException</span></span><a class="headerlink" href="#duckdb.PermissionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ProgrammingError">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ProgrammingError</span></span><a class="headerlink" href="#duckdb.ProgrammingError" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">PythonExceptionHandling</span></span><a class="headerlink" href="#duckdb.PythonExceptionHandling" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>DEFAULT</p>
<p>RETURN_NULL</p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.PythonExceptionHandling.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.PythonExceptionHandling.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.RenderMode">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">RenderMode</span></span><a class="headerlink" href="#duckdb.RenderMode" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>ROWS</p>
<p>COLUMNS</p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.RenderMode.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.RenderMode.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.SequenceException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SequenceException</span></span><a class="headerlink" href="#duckdb.SequenceException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DatabaseError</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.SerializationException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SerializationException</span></span><a class="headerlink" href="#duckdb.SerializationException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.ShortValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">ShortValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.ShortValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Statement">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Statement</span></span><a class="headerlink" href="#duckdb.Statement" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.expected_result_type">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">expected_result_type</span></span><a class="headerlink" href="#duckdb.Statement.expected_result_type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the expected type of result produced by this statement, actual type may vary depending on the statement.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.named_parameters">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">named_parameters</span></span><a class="headerlink" href="#duckdb.Statement.named_parameters" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the map of named parameters this statement has.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.query">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">query</span></span><a class="headerlink" href="#duckdb.Statement.query" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the query equivalent to this statement.</p>
</dd>
</dl>

<dl class="py property">
<dt class="sig sig-object py" id="duckdb.Statement.type">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">type</span></span><a class="headerlink" href="#duckdb.Statement.type" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Get the type of the statement.</p>
</dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.StatementType">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StatementType</span></span><a class="headerlink" href="#duckdb.StatementType" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">pybind11_object</span></code></p>
<p>Members:</p>
<p>INVALID</p>
<p>SELECT</p>
<p>INSERT</p>
<p>UPDATE</p>
<p>CREATE</p>
<p>DELETE</p>
<p>PREPARE</p>
<p>EXECUTE</p>
<p>ALTER</p>
<p>TRANSACTION</p>
<p>COPY</p>
<p>ANALYZE</p>
<p>VARIABLE_SET</p>
<p>CREATE_FUNC</p>
<p>EXPLAIN</p>
<p>DROP</p>
<p>EXPORT</p>
<p>PRAGMA</p>
<p>VACUUM</p>
<p>CALL</p>
<p>SET</p>
<p>LOAD</p>
<p>RELATION</p>
<p>EXTENSION</p>
<p>LOGICAL_PLAN</p>
<p>ATTACH</p>
<p>DETACH</p>
<p>MULTI</p>
<p>COPY_DATABASE</p>
<p>MERGE_INTO</p>
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.StatementType.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.StatementType.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.StringValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">StringValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.StringValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.SyntaxException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">SyntaxException</span></span><a class="headerlink" href="#duckdb.SyntaxException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.ProgrammingError" title="_duckdb.ProgrammingError"><code class="xref py py-class docutils literal notranslate"><span class="pre">ProgrammingError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimeTimeZoneValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimeTimeZoneValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimeTimeZoneValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimeValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimeValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimeValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampMilisecondValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampMilisecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampMilisecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampNanosecondValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampNanosecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampNanosecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampSecondValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampSecondValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampSecondValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampTimeZoneValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampTimeZoneValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampTimeZoneValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TimestampValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TimestampValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.TimestampValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TransactionException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TransactionException</span></span><a class="headerlink" href="#duckdb.TransactionException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.OperationalError" title="_duckdb.OperationalError"><code class="xref py py-class docutils literal notranslate"><span class="pre">OperationalError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.TypeMismatchException">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">TypeMismatchException</span></span><a class="headerlink" href="#duckdb.TypeMismatchException" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.DataError" title="_duckdb.DataError"><code class="xref py py-class docutils literal notranslate"><span class="pre">DataError</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UUIDValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UUIDValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UUIDValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedBinaryValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedBinaryValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedBinaryValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedIntegerValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedIntegerValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedIntegerValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedLongValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedLongValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedLongValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.UnsignedShortValue">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">UnsignedShortValue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.UnsignedShortValue" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <a class="reference internal" href="#duckdb.Value" title="duckdb.value.constant.Value"><code class="xref py py-class docutils literal notranslate"><span class="pre">Value</span></code></a></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Value">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Value</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">object</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">type</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">DuckDBPyType</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#duckdb.Value" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.Warning">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">Warning</span></span><a class="headerlink" href="#duckdb.Warning" title="Link to this definition">&#182;</a>
</dt>
<dd>
<p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Exception</span></code></p>
</dd>
</dl>

<dl class="py class">
<dt class="sig sig-object py" id="duckdb.token_type">
<em class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></em><span class="sig-prename descclassname"><span class="pre">duckdb.</span></span><span class="sig-name descname"><span class="pre">token_type</span></span><a class="headerlink" href="#duckdb.token_type" title="Link to this definition">&#182;</a>
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
<dl class="py property">
<dt class="sig sig-object py" id="duckdb.token_type.name">
<em class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></em><span class="sig-name descname"><span class="pre">name</span></span><a class="headerlink" href="#duckdb.token_type.name" title="Link to this definition">&#182;</a>
</dt>
<dd></dd>
</dl>

</dd>
</dl>



<div class="clearer"></div>
</div>
</div>
</div>
