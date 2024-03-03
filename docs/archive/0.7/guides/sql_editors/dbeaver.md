---
layout: docu
title: DBeaver SQL IDE
selected: DBeaver SQL IDE
---

# How to set up DBeaver SQL IDE for DuckDB

[DBeaver](https://dbeaver.io/) is a powerful and popular desktop sql editor and integrated development environment (IDE). It has both an open source and enterprise version. It is useful for visually inspecting the available tables in DuckDB and for quickly building complex queries. DuckDB's [JDBC connector](https://search.maven.org/artifact/org.duckdb/duckdb_jdbc) allows DBeaver to query DuckDB files, and by extension, any other files that DuckDB can access ([like parquet files](../../guides/import/query_parquet)).  

1. Install DBeaver using the download links and instructions found at their [download page](https://dbeaver.io/download/).  

2. Open DBeaver and create a new connection. Either click on the "New Database Connector" button or go to Database > New Database Connection in the menu bar.  
<img src="/images/guides/DBeaver_new_database_connection.png" alt="DBeaver New Database Connection" title="DBeaver New Database Connection"/>
<img src="/images/guides/DBeaver_new_database_connection_menu.png" alt="DBeaver New Database Connection Menu" title="DBeaver New Database Connection Menu"/>

3. Search for DuckDB, select it, and click Next.  
<img src="/images/guides/DBeaver_select_database_driver.png" alt="DBeaver Select Database Driver" title="DBeaver Select Database Driver"/>

4. Enter the path or browse to the DuckDB database file you wish to query. To use an in-memory DuckDB (useful primarily if just interested in querying parquet files, or for testing) enter ":memory:" as the path.  
<img src="/images/guides/DBeaver_connection_settings_path.png" alt="DBeaver Set Path" title="DBeaver Set Path"/>

5. Click "Test Connection". This will then prompt you to install the DuckDB JDBC driver. If you are not prompted, see alternative driver installation instructions below.  
<img src="/images/guides/DBeaver_connection_settings_test_connection.png" alt="DBeaver Test Connection" title="DBeaver Test Connection"/>

6. Click "Download" to download DuckDB's JDBC driver from Maven. Once download is complete, click "OK", then click "Finish". 
* Note: If you are in a corporate environment or behind a firewall, before clicking download, click the "Download Configuration" link to configure your proxy settings.  
<img src="/images/guides/DBeaver_download_driver_files.png" alt="DBeaver Download Driver Files" title="DBeaver Download Driver Files"/>

7. You should now see a database connection to your DuckDB database in the left hand "Database Navigator" pane. Expand it to see the tables and views in your database. Right click on that connection and create a new SQL script.  
<img src="/images/guides/DBeaver_new_sql_script.png" alt="DBeaver New SQL Script" title="DBeaver New SQL Script"/>

8. Write some SQL and click the "Execute" button.  
<img src="/images/guides/DBeaver_execute_query.png" alt="DBeaver Execute Query" title="DBeaver Execute Query"/>

9. Now you're ready to fly with DuckDB and DBeaver!  
<img src="/images/guides/DBeaver_query_results.png" alt="DBeaver Query Results" title="DBeaver Query Results"/>


## Alternative Driver Installation
1. If not prompted to install the DuckDB driver when testing your connection, return to the "Connect to a database" dialog and click "Edit Driver Settings".  
<img src="/images/guides/DBeaver_edit_driver_settings.png" alt="DBeaver Edit Driver Settings" title="DBeaver Edit Driver Settings"/>

1. (Alternate) You may also access the driver settings menu by returning to the main DBeaver window and clicking Database > Driver Manager in the menu bar. Then select DuckDB, then click Edit.  
<img src="/images/guides/DBeaver_driver_manager.png" alt="DBeaver Driver Manager" title="DBeaver Driver Manager"/>
<img src="/images/guides/DBeaver_driver_manager_edit.png" alt="DBeaver Driver Manager Edit" title="DBeaver Driver Manager Edit"/>

2. Go to the "Libraries" tab, then click on the DuckDB driver and click "Download/Update". If you do not see the DuckDB driver, first click on "Reset to Defaults".  
<img src="/images/guides/DBeaver_edit_driver_duckdb.png" alt="DBeaver Edit Driver" title="DBeaver Edit Driver"/>

3. Click "Download" to download DuckDB's JDBC driver from Maven. Once download is complete, click "OK", then return to the main DBeaver window and continue with step 7 above. 
* Note: If you are in a corporate environment or behind a firewall, before clicking download, click the "Download Configuration" link to configure your proxy settings.  
<img src="/images/guides/DBeaver_download_driver_files_from_driver_settings.png" alt="DBeaver Download Driver Files 2" title="DBeaver Download Driver Files 2" />