#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 13:56:43 2026

@author: mmiller
"""

import sqlite3
from pprint import pprint
from tabulate import tabulate

sql_script_path = 'wlquery.sql'
database_path = 'mlb_data.sqlite'

try:

    with open(sql_script_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        
        rows = cursor.execute(sql_script)
    

    team_data  = [ row for row in rows]
        
    results_table = tabulate(team_data,headers=["Team","Overall Record", "Home Record", "Away Record", "Run Diff."])
    conn.commit()
    print(results_table)

except sqlite3.Error as e:
    print(class_name := f"SQLite error occurred: {e}")
except FileNotFoundError:
    print(f"Error: The file '{sql_script_path}' was not found.")
