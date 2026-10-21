.. currentmodule:: duckdb

.. autoclass:: BinaryValue
   :members:
   :show-inheritance:
.. autoclass:: BinderException
   :members:
   :show-inheritance:
.. autoclass:: BitValue
   :members:
   :show-inheritance:
.. autoclass:: BlobValue
   :members:
   :show-inheritance:
.. autoclass:: BooleanValue
   :members:
   :show-inheritance:
.. autoclass:: CSVLineTerminator
   :members:
   :show-inheritance:
.. autofunction:: CaseExpression
.. autoclass:: CatalogException
   :members:
   :show-inheritance:
.. autofunction:: CoalesceOperator
.. autofunction:: ColumnExpression
.. autoclass:: ConnectionException
   :members:
   :show-inheritance:
.. autofunction:: ConstantExpression
.. autoclass:: ConstraintException
   :members:
   :show-inheritance:
.. autoclass:: ConversionException
   :members:
   :show-inheritance:
.. autoclass:: DBAPITypeObject
   :members:
   :show-inheritance:
.. autoclass:: DataError
   :members:
   :show-inheritance:
.. autoclass:: DatabaseError
   :members:
   :show-inheritance:
.. autoclass:: DateValue
   :members:
   :show-inheritance:
.. autoclass:: DecimalValue
   :members:
   :show-inheritance:
.. autofunction:: DefaultExpression
.. autoclass:: DependencyException
   :members:
   :show-inheritance:
.. autoclass:: DoubleValue
   :members:
   :show-inheritance:
.. autoclass:: DuckDBPyConnection
   :members:
   :show-inheritance:
.. include:: relation.rst
.. autoclass:: Error
   :members:
   :show-inheritance:
.. autoclass:: ExpectedResultType
   :members:
   :show-inheritance:
.. autoclass:: ExplainType
   :members:
   :show-inheritance:
.. autoclass:: Expression
   :members:
   :show-inheritance:
.. autoclass:: FatalException
   :members:
   :show-inheritance:
.. autoclass:: FloatValue
   :members:
   :show-inheritance:
.. autofunction:: FunctionExpression
.. autoclass:: HTTPException
   :members:
   :show-inheritance:
.. autoclass:: HugeIntegerValue
   :members:
   :show-inheritance:
.. autoclass:: IOException
   :members:
   :show-inheritance:
.. autoclass:: IntegerValue
   :members:
   :show-inheritance:
.. autoclass:: IntegrityError
   :members:
   :show-inheritance:
.. autoclass:: InternalError
   :members:
   :show-inheritance:
.. autoclass:: InternalException
   :members:
   :show-inheritance:
.. autoclass:: InterruptException
   :members:
   :show-inheritance:
.. autoclass:: IntervalValue
   :members:
   :show-inheritance:
.. autoclass:: InvalidInputException
   :members:
   :show-inheritance:
.. autoclass:: InvalidTypeException
   :members:
   :show-inheritance:
.. autofunction:: LambdaExpression
.. autoclass:: ListValue
   :members:
   :show-inheritance:
.. autoclass:: LongValue
   :members:
   :show-inheritance:
.. autoclass:: MapValue
   :members:
   :show-inheritance:
.. autoclass:: NotImplementedException
   :members:
   :show-inheritance:
.. autoclass:: NotSupportedError
   :members:
   :show-inheritance:
.. autoclass:: NullValue
   :members:
   :show-inheritance:
.. autoclass:: OperationalError
   :members:
   :show-inheritance:
.. autoclass:: OutOfMemoryException
   :members:
   :show-inheritance:
.. autoclass:: OutOfRangeException
   :members:
   :show-inheritance:
.. autoclass:: ParserException
   :members:
   :show-inheritance:
.. autoclass:: PermissionException
   :members:
   :show-inheritance:
.. autoclass:: ProgrammingError
   :members:
   :show-inheritance:
.. autoclass:: PythonExceptionHandling
   :members:
   :show-inheritance:
.. autoclass:: RenderMode
   :members:
   :show-inheritance:
.. autofunction:: SQLExpression
.. autoclass:: SequenceException
   :members:
   :show-inheritance:
.. autoclass:: SerializationException
   :members:
   :show-inheritance:
.. autoclass:: ShortValue
   :members:
   :show-inheritance:
.. autofunction:: StarExpression
.. autoclass:: Statement
   :members:
   :show-inheritance:
.. autoclass:: StatementType
   :members:
   :show-inheritance:
.. autoclass:: StringValue
   :members:
   :show-inheritance:
.. autoclass:: StructValue
   :members:
   :show-inheritance:
.. autoclass:: SyntaxException
   :members:
   :show-inheritance:
.. autoclass:: TimeTimeZoneValue
   :members:
   :show-inheritance:
.. autoclass:: TimeValue
   :members:
   :show-inheritance:
.. autoclass:: TimestampMillisecondValue
   :members:
   :show-inheritance:
.. autoclass:: TimestampNanosecondValue
   :members:
   :show-inheritance:
.. autoclass:: TimestampSecondValue
   :members:
   :show-inheritance:
.. autoclass:: TimestampTimeZoneValue
   :members:
   :show-inheritance:
.. autoclass:: TimestampValue
   :members:
   :show-inheritance:
.. autoclass:: TransactionException
   :members:
   :show-inheritance:
.. autoclass:: TypeMismatchException
   :members:
   :show-inheritance:
.. autoclass:: UUIDValue
   :members:
   :show-inheritance:
.. autoclass:: UnionType
   :members:
   :show-inheritance:
.. autoclass:: UnsignedBinaryValue
   :members:
   :show-inheritance:
.. autoclass:: UnsignedHugeIntegerValue
   :members:
   :show-inheritance:
.. autoclass:: UnsignedIntegerValue
   :members:
   :show-inheritance:
.. autoclass:: UnsignedLongValue
   :members:
   :show-inheritance:
.. autoclass:: UnsignedShortValue
   :members:
   :show-inheritance:
.. autoclass:: Value
   :members:
   :show-inheritance:
.. autoclass:: Warning
   :members:
   :show-inheritance:
.. autofunction:: __annotate__
.. autofunction:: aggregate
.. autofunction:: alias
.. autofunction:: append
.. autofunction:: array_type
.. autofunction:: arrow
.. autofunction:: begin
.. autofunction:: checkpoint
.. autofunction:: close
.. autofunction:: commit
.. autofunction:: connect
.. autofunction:: create_function
.. autofunction:: cursor
.. autofunction:: decimal_type
.. autofunction:: default_connection
.. autofunction:: description
.. autofunction:: df
.. autofunction:: disable_profiling
.. autofunction:: distinct
.. autofunction:: dtype
.. autofunction:: duplicate
.. autofunction:: enable_profiling
.. autofunction:: enum_type
.. autofunction:: execute
.. autofunction:: executemany
.. autofunction:: extract_statements
.. autofunction:: fetch_arrow_table
.. autofunction:: fetch_df
.. autofunction:: fetch_df_chunk
.. autofunction:: fetch_record_batch
.. autofunction:: fetchall
.. autofunction:: fetchdf
.. autofunction:: fetchmany
.. autofunction:: fetchnumpy
.. autofunction:: fetchone
.. autofunction:: filesystem_is_registered
.. autofunction:: filter
.. autofunction:: from_arrow
.. autofunction:: from_csv_auto
.. autofunction:: from_df
.. autofunction:: from_parquet
.. autofunction:: from_query
.. autofunction:: get_profiling_information
.. autofunction:: get_table_names
.. autofunction:: install_extension
.. autofunction:: interrupt
.. autofunction:: limit
.. autofunction:: list_filesystems
.. autofunction:: list_type
.. autofunction:: load_extension
.. autofunction:: map_type
.. autofunction:: order
.. autofunction:: pl
.. autofunction:: project
.. autofunction:: query
.. autofunction:: query_df
.. autofunction:: query_progress
.. autofunction:: read_csv
.. autofunction:: read_json
.. autofunction:: read_parquet
.. autofunction:: register
.. autofunction:: register_filesystem
.. autofunction:: remove_function
.. autofunction:: rollback
.. autofunction:: row_type
.. autofunction:: rowcount
.. autofunction:: set_default_connection
.. autofunction:: sql
.. autofunction:: sqltype
.. autofunction:: string_type
.. autofunction:: struct_type
.. autofunction:: table
.. autofunction:: table_function
.. autofunction:: tf
.. autofunction:: to_arrow_reader
.. autofunction:: to_arrow_table
.. autoclass:: token_type
   :members:
   :show-inheritance:
.. autofunction:: tokenize
.. autofunction:: torch
.. autofunction:: type
.. autofunction:: union_type
.. autofunction:: unregister
.. autofunction:: unregister_filesystem
.. autofunction:: values
.. autofunction:: version
.. autofunction:: view
.. autofunction:: write_csv
