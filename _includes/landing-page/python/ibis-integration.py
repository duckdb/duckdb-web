# Querying data with ibis using DuckDB
import ibis
from ibis import _

t = ibis.memtable({
    'station': ['Delft', 'Delft', 'Gouda', 'Gouda'],
    'day': ['Mon', 'Tue', 'Mon', 'Tue'],
    'num_services' : [22, 20, 27, 25]})

# execute a query on duckdb and return a dataframe
data = t.group_by("station").agg(_.num_services.sum()).to_pandas()
