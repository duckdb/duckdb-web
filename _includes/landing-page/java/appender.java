// Perform bulk inserts using the Appender API
DuckDBConnection conn = (DuckDBConnection)
    DriverManager.getConnection("jdbc:duckdb:");
Statement st = conn.createStatement();
st.execute("CREATE TABLE person " +
    "(name VARCHAR, age INT)");

var appender = conn.createAppender(
    DuckDBConnection.DEFAULT_SCHEMA, "person");

appender.beginRow();
appender.append("MC Ducky");
appender.append(49);
appender.endRow();
appender.close();
