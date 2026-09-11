#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 13:56:43 2026

@author: mmiller
This script selects the most recent SRS rating and appends it to the 
win loss records + run differential. 
"""

import sqlite3
from pprint import pprint
from tabulate import tabulate
from mlb_database.queries import abbrev_to_id

sql_script_path = 'wlquery.sql'
database_path = 'mlb_data.sqlite'

try:

    with open(sql_script_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        
    rows = cursor.execute(sql_script)
    raw_team_data  = [ row for row in rows]
    
    team_data = [[abbrev_to_id(row[0]),row[0],row[1],row[2],row[3],row[4]] for row in raw_team_data]
    
    team_data = sorted(team_data,key=lambda x:x[0])
    for z in team_data:
        z.pop(0)
    
    srs_script = "select srs_rating from srs where epochtime = (select max(epochtime) from srs) order by team_id asc"
    srs_rows = cursor.execute(srs_script)
    srs_team_data  = [row for row in rows]
    srs_team_data  = [list(row) for row in srs_team_data]

    new_data = [row2 + row1 for row2, row1 in zip(team_data,srs_team_data)]
    sorted_data = sorted(new_data,key=lambda x:x[5],reverse=True)
        
    results_table = tabulate(sorted_data,headers=["Team","Overall Record", "Home Record", "Away Record", "Run Diff.","SRS"])
    
    conn.commit()
    print(results_table)

except sqlite3.Error as e:
    print(class_name := f"SQLite error occurred: {e}")
except FileNotFoundError:
    print(f"Error: The file '{sql_script_path}' was not found.")
