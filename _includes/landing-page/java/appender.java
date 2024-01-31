// Using the appender for bulk inserts
DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
Statement stmt = conn.createStatement();
stmt.execute("CREATE TABLE perosn (first_name VARCHAR, last_name VARCHAR, age INT)");

try (var appender = conn.createAppender(DuckDBConnection.DEFAULT_SCHEMA, "tbl")) {
    appender.beginRow();
    appender.append("John");
    appender.append("Smith");
    appender.append(42);
    appender.endRow();
}
