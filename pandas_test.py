# coding: utf-8
import pandas as pd
import sqlite3
conn=sqlite3
conn=sqlite3.connect("mlb_data.sqlite")
df=pd.read_sql_query("select * from games where not (away_runs=0 and home_runs=0) and scheduled_date < datetime('now')")
df=pd.read_sql_query("select * from games where not (away_runs=0 and home_runs=0) and scheduled_date < datetime('now');",conn)
df
df
