.. currentmodule:: duckdb

Connection
==========

.. autoclass:: Appender
   :members:
   :show-inheritance:
.. autoclass:: DuckDBPyConnection
   :members:
   :show-inheritance:
.. autoclass:: Statement
   :members:
   :show-inheritance:

.. currentmodule:: duckdb

Relation
========

.. include:: relation.rst

.. currentmodule:: duckdb

Expressions
===========

.. autofunction:: CaseExpression
.. autofunction:: coalesce
.. autofunction:: CoalesceOperator
.. autofunction:: col
.. autofunction:: ColumnExpression
.. autofunction:: ConstantExpression
.. autofunction:: count_all
.. autofunction:: DefaultExpression
.. autofunction:: dense_rank
.. autoclass:: Expression
   :members:
   :show-inheritance:
   :inherited-members:
.. autofunction:: first_value
.. autofunction:: fn
.. autofunction:: FunctionExpression
.. autofunction:: lag
.. autofunction:: LambdaExpression
.. autofunction:: last_value
.. autofunction:: lead
.. autofunction:: lit
.. autofunction:: ntile
.. autofunction:: rank
.. autofunction:: row_number
.. autofunction:: sql_expr
.. autofunction:: SQLExpression
.. autofunction:: star
.. autofunction:: StarExpression
.. autofunction:: when

.. currentmodule:: duckdb._expression_namespaces

.. autoclass:: StrExpr
   :members:
.. autoclass:: DtExpr
   :members:
.. autoclass:: ListExpr
   :members:
.. autoclass:: JsonExpr
   :members:

.. currentmodule:: duckdb

Module Functions
================

.. autofunction:: abort
.. autofunction:: aggregate
.. autofunction:: alias
.. autofunction:: append
.. autofunction:: appender
.. autofunction:: arrow
.. autofunction:: begin
.. autofunction:: build_info
.. autofunction:: checkpoint
.. autofunction:: close
.. autofunction:: commit
.. autofunction:: complete
.. autofunction:: connect
.. autofunction:: create_function
.. autofunction:: cursor
.. autofunction:: default_connection
.. autofunction:: description
.. autofunction:: df
.. autofunction:: disable_profiling
.. autofunction:: distinct
.. autofunction:: duplicate
.. autofunction:: enable_profiling
.. autofunction:: execute
.. autofunction:: executemany
.. autofunction:: extract_statements
.. autofunction:: fetch_df
.. autofunction:: fetch_df_chunk
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
.. autofunction:: load_extension
.. autofunction:: order
.. autofunction:: project
.. autofunction:: query
.. autofunction:: query_appender
.. autofunction:: query_df
.. autofunction:: query_progress
.. autofunction:: read_csv
.. autofunction:: read_json
.. autofunction:: read_parquet
.. autofunction:: register
.. autofunction:: register_filesystem
.. autofunction:: remove_function
.. autofunction:: rollback
.. autofunction:: rowcount
.. autofunction:: set_default_connection
.. autofunction:: sql
.. autofunction:: table
.. autofunction:: table_function
.. autofunction:: tf
.. autofunction:: to_arrow_reader
.. autofunction:: to_arrow_table
.. autofunction:: tokenize
.. autofunction:: torch
.. autofunction:: unregister
.. autofunction:: unregister_filesystem
.. autofunction:: values
.. autofunction:: view
.. autofunction:: write_csv

.. currentmodule:: duckdb

Types and Values
================

.. autofunction:: array_type
.. autoclass:: BinaryValue
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
.. autoclass:: DateValue
   :members:
   :show-inheritance:
.. autofunction:: decimal_type
.. autoclass:: DecimalValue
   :members:
   :show-inheritance:
.. autoclass:: DoubleValue
   :members:
   :show-inheritance:
.. autofunction:: dtype
.. autofunction:: enum_type
.. autoclass:: FloatValue
   :members:
   :show-inheritance:
.. autoclass:: HugeIntegerValue
   :members:
   :show-inheritance:
.. autoclass:: IntegerValue
   :members:
   :show-inheritance:
.. autoclass:: IntervalValue
   :members:
   :show-inheritance:
.. autofunction:: list_type
.. autoclass:: ListValue
   :members:
   :show-inheritance:
.. autoclass:: LongValue
   :members:
   :show-inheritance:
.. autofunction:: map_type
.. autoclass:: MapValue
   :members:
   :show-inheritance:
.. autoclass:: NullValue
   :members:
   :show-inheritance:
.. autofunction:: row_type
.. autoclass:: ShortValue
   :members:
   :show-inheritance:
.. autofunction:: sqltype
.. autofunction:: string_type
.. autoclass:: StringValue
   :members:
   :show-inheritance:
.. autofunction:: struct_type
.. autoclass:: StructValue
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
.. autoclass:: TimeTimeZoneValue
   :members:
   :show-inheritance:
.. autoclass:: TimeValue
   :members:
   :show-inheritance:
.. autofunction:: type
.. autofunction:: union_type
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
.. autoclass:: UUIDValue
   :members:
   :show-inheritance:
.. autoclass:: Value
   :members:
   :show-inheritance:

.. currentmodule:: duckdb

Enumerations
============

.. autoclass:: CSVLineTerminator
   :members:
   :show-inheritance:
.. autoclass:: ExpectedResultType
   :members:
   :show-inheritance:
.. autoclass:: ExplainType
   :members:
   :show-inheritance:
.. autoclass:: PythonExceptionHandling
   :members:
   :show-inheritance:
.. autoclass:: RenderMode
   :members:
   :show-inheritance:
.. autoclass:: StatementType
   :members:
   :show-inheritance:
.. autoclass:: token_type
   :members:
   :show-inheritance:

.. currentmodule:: duckdb

Exceptions
==========

.. autoclass:: BinderException
   :members:
   :show-inheritance:
.. autoclass:: CatalogException
   :members:
   :show-inheritance:
.. autoclass:: ConnectionException
   :members:
   :show-inheritance:
.. autoclass:: ConstraintException
   :members:
   :show-inheritance:
.. autoclass:: ConversionException
   :members:
   :show-inheritance:
.. autoclass:: DatabaseError
   :members:
   :show-inheritance:
.. autoclass:: DataError
   :members:
   :show-inheritance:
.. autoclass:: DependencyException
   :members:
   :show-inheritance:
.. autoclass:: Error
   :members:
   :show-inheritance:
.. autoclass:: FatalException
   :members:
   :show-inheritance:
.. autoclass:: HTTPException
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
.. autoclass:: InvalidInputException
   :members:
   :show-inheritance:
.. autoclass:: InvalidTypeException
   :members:
   :show-inheritance:
.. autoclass:: IOException
   :members:
   :show-inheritance:
.. autoclass:: NotImplementedException
   :members:
   :show-inheritance:
.. autoclass:: NotSupportedError
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
.. autoclass:: ResourceInUseException
   :members:
   :show-inheritance:
.. autoclass:: SequenceException
   :members:
   :show-inheritance:
.. autoclass:: SerializationException
   :members:
   :show-inheritance:
.. autoclass:: SyntaxException
   :members:
   :show-inheritance:
.. autoclass:: TransactionException
   :members:
   :show-inheritance:
.. autoclass:: TypeMismatchException
   :members:
   :show-inheritance:
.. autoclass:: Warning
   :members:
   :show-inheritance:

