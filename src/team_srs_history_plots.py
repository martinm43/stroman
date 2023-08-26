"""
Short sample script that plots the moving SRS for a given team over their 
available history in the SRS database.

Inputs: None
    
Outputs: Bitmap images of the SRS rating history of all 30 teams

"""

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

from mlb_database.queries import team_abbreviation
rolling_average = 41

for team_id in range(30, 0, -1):
    conn = sqlite3.connect("mlb_data.sqlite")
    query = "SELECT epochtime,srs_rating FROM SRS where team_id = " + str(
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
        df["srs_rating"].rolling(rolling_average).mean(),
        label="41 game moving avg.",
        color=s[0][0],
    )
    plt.xticks(rotation=45)
    plt.legend()
    plt.title("SRS rating history of " + team_abbreviation(team_id))
    plt.savefig("SRS rating history of " + team_abbreviation(team_id)+".png")
    plt.show(block=False)
    plt.pause(1)
    plt.close()
