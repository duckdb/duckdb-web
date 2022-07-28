Python Client API

.. automodule:: duckdb
    :members:
    :undoc-members:
    :show-inheritance:

    .. data:: threadsafety
        :annotation: bool

        Indicates that this package is threadsafe

    .. data:: apilevel
        :annotation: int

        Indicates which Python DBAPI version this package implements

    .. data:: paramstyle
        :annotation: str

        Indicates which parameter style duckdb supports

    .. data:: default_connection
        :annotation: duckdb.DuckDBPyConnection

        The connection that is used by default if you don't explicitly pass one to the root methods in this module
