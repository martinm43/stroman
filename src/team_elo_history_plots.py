"""
Short sample script that plots the moving elo for a given team over their 
available history in the Elo database.

Inputs: None
    
Outputs: Bitmap images of the Elo rating history of all 30 teams

"""

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import time

from mlb_database.queries import team_abbreviation

for team_id in range(30, 0, -1):
    conn = sqlite3.connect("mlb_data.sqlite")
    query = "SELECT epochtime,elo_rating FROM ratings where team_id = " + str(
        team_id)+ " order by epochtime desc"
    

    df = pd.read_sql_query(query, conn)

    df["epochtime"] = pd.to_datetime(df["epochtime"], unit="s")

    # get the appropriate colours
    cursor = conn.cursor()
    cursor.execute(
        "SELECT primary_color from teams where team_id=" + str(team_id)
    )
    s = cursor.fetchall()

    plt.plot(
        df["epochtime"],
        df["elo_rating"].rolling(162).mean(),
        label="41 game moving avg.",
        color=s[0][0],
    )
    plt.xticks(rotation=45)
    plt.legend()
    plt.title("Elo rating history of " + team_abbreviation(team_id))
    plt.savefig("Elo rating history of " + team_abbreviation(team_id)+".png")
    plt.show(block=False)
    plt.pause(1)
    plt.close()
