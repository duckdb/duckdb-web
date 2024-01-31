// Get a list of train stations by traffic
Connection conn = DriverManager.getConnection("jdbc:duckdb:");
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(
    "SELECT station, count(*) AS num_services\n" + 
    "FROM train_services\n" + 
    "GROUP BY ALL\n" + 
    "ORDER BY num_services DESC;");
    
while (rs.next()) {
    System.out.println(rs.getString(1));
    System.out.println(rs.getInt(2));
}
