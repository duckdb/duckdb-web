import pandas as pd
import numpy as np
import duckdb
import time

con = duckdb.connect()

def generate_df(size):
  race_categories = ['Hobbit', 'Elf', 'Man','Mayar']
  race = np.random.choice(race_categories, size)
  subrace = np.random.choice(race_categories, size)
  return pd.DataFrame({'race': pd.Categorical(race),
                       'subrace': pd.Categorical(subrace),
                       'race_string': race,
                       'subrace_string': subrace,})

size = pow(10,7) #10,000,000 rows
df = generate_df(size)

def duck_group(df):
  start_time = time.monotonic()
  res = con.execute("select race, count(*) from df group by race").df()
  print ("Duck (Cat) : " + str(time.monotonic() - start_time))
  return res

def duck_group_string(df):
  start_time = time.monotonic()
  res = con.execute("select race_string, count(*) from df group by race_string").df()
  print ("Duck (Str) : " + str(time.monotonic() - start_time))
  return res

def pandas_group(df):
  start_time = time.monotonic()
  res = df.groupby(['race']).agg({'race': 'count'})
  print ("Pandas (Cat) : " + str(time.monotonic() - start_time))
  return res

def pandas_group_string(df):
  start_time = time.monotonic()
  res = df.groupby(['race_string']).agg({'race_string': 'count'})
  print ("Pandas (String) : " + str(time.monotonic() - start_time))
  return res

def duck_filter(df):
  start_time = time.monotonic()
  res = con.execute("select count(*) from df where race = 'Hobbit'").df()
  print ("Duck (Cat) : " + str(time.monotonic() - start_time))
  return res

def duck_filter_string(df):
  start_time = time.monotonic()
  res = con.execute("select count(*) from df where race_string = 'Hobbit'").df()
  print ("Duck (Str) : " + str(time.monotonic() - start_time))
  return res

def pandas_filter(df):
  start_time = time.monotonic()
  filtered_df = df[df.race == "Hobbit"]
  res = filtered_df.agg({'race': 'count'})
  print ("Pandas (Cat) : " + str(time.monotonic() - start_time))
  return res

def pandas_filter_string(df):
  start_time = time.monotonic()
  filtered_df = df[df.race_string == "Hobbit"]
  res = filtered_df.agg({'race_string': 'count'})
  print ("Pandas (String) : " + str(time.monotonic() - start_time))
  return res


def duck_comparison(df):
  start_time = time.monotonic()
  res = con.execute("select count(*) from df where race = subrace").df()
  print ("Duck (Cat) : " + str(time.monotonic() - start_time))
  return res

def duck_comparison_string(df):
  start_time = time.monotonic()
  res = con.execute("select count(*) from df where race_string = subrace_string").df()
  print ("Duck (Str) : " + str(time.monotonic() - start_time))
  return res

def pandas_comparison(df):
  start_time = time.monotonic()
  filtered_df = df[df.race == df.subrace]
  res = filtered_df.agg({'race': 'count'})
  print ("Pandas (Cat) : " + str(time.monotonic() - start_time))
  return res

def pandas_comparison_string(df):
  start_time = time.monotonic()
  filtered_df = df[df.race_string == df.subrace_string]
  res = filtered_df.agg({'race_string': 'count'})
  print ("Pandas (Str) : " + str(time.monotonic() - start_time))
  return res


print ("--- Group ---")
duck_group(df)
duck_group_string(df)
pandas_group(df)
pandas_group_string(df)

print ("--- Filter ---")
duck_filter(df)
duck_filter_string(df)
pandas_filter(df)
pandas_filter_string(df)

print ("--- Enum - Enum Comparison ---")
duck_comparison(df)
duck_comparison_string(df)
pandas_comparison(df)
pandas_comparison_string(df)

def storage():
  race_categories = ['Hobbit', 'Elf', 'Man','Mayar']
  race = np.random.choice(race_categories, size)
  categorical_race = pd.DataFrame({'race': pd.Categorical(race),})
  string_race = pd.DataFrame({'race': race,})
  categorical_race.to_pickle("./pandas_cat.pkl")
  string_race.to_pickle("./pandas_str.pkl")
  con = duckdb.connect('duck_cat.db')
  con.execute("CREATE TABLE T as select * from categorical_race")
  con = duckdb.connect('duck_str.db')
  con.execute("CREATE TABLE T as select * from string_race")

storage()

