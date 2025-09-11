// Get a list of train stations by traffic
Connection conn =
    DriverManager.getConnection("jdbc:duckdb:");
Statement st = conn.createStatement();
ResultSet rs = st.executeQuery(
    """
    SELECT station_name,
           count(*) AS num_services
    FROM train_services
    GROUP BY ALL
    ORDER BY num_services DESC;
    """);

System.out.println(rs.next());
