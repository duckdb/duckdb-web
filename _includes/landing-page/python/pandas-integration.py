# Reading and writing Pandas dataframes
import pandas as pd
import duckdb

df_in = pd.DataFrame({
    'station': ['Delft', 'Delft', 'Gouda', 'Gouda'],
    'day': ['Mon', 'Tue', 'Mon', 'Tue'],
    'num_services' : [22, 20, 27, 25]})

# Run query on a dataframe and return a dataframe
df_out = duckdb.sql("""
    SELECT station, sum(num_services)
    FROM df_in
    GROUP BY station
    """).to_df()
