// Get a list of train stations by traffic
Connection conn =
    DriverManager.getConnection("jdbc:duckdb:");
Statement st = conn.createStatement();
ResultSet rs = st.executeQuery(
    "SELECT station_name,\n" +
    "       count(*) AS num_services\n" +
    "FROM train_services\n" +
    "GROUP BY ALL\n" +
    "ORDER BY num_services DESC;");

System.out.println(rs.next());
