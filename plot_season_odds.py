# coding: utf-8
"""
A script that plots the playoff odds for a given division and given "season_year".

Inputs:
    season_year - can be randomized (random.randint) or user-selected
    division_name - can be randomized (random.choice) or user-selected
    
    Constants: max_year and min_year
    
Output:
    A bitmap image plot of the playoff odds 
    for a given division and given "season_year"

"""
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pprint import pprint 

import random

from prediction_table import playoff_odds_calc

from mlb_database.queries import team_abbreviation
from mlb_database.mlb_models import Teams

season_year = 2007 #random.randint(2012,2019)
division_name = "NL East" #["AL East", "AL Central", "AL West", "NL East", "NL Central", "NL West"]


a = datetime(season_year, 3, 20)
b = datetime(season_year, 10, 15)
end = min(datetime(season_year, 10, 15), datetime.today() - timedelta(days=1))


# Python Moving Average, taken by:
# https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# note that there's a faster version using pandas but NO PANDAS.
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N


team_labels = [team_abbreviation(i) for i in range(1, 30)]

query = Teams.select().where(Teams.division == division_name)
division_team_id_list = [i.team_id for i in query]


# Odds calculations
odds_list = []
x_odds = playoff_odds_calc(a, b, season_year)
x_odds = [x[4] for x in x_odds]

odds_list.append(x_odds)

dates_list = []
dates_list.append(b)

ratings_mode = "Elo"


while b < end:
    
    x_odds = playoff_odds_calc(a, b, season_year, ratings_mode=ratings_mode)

    #print(b)
    #pprint(x_odds)

    x_odds = [x[4] for x in x_odds]

    odds_list.append(x_odds)
    dates_list.append(b)
    print("Finished processing "+b.strftime("%m %d %Y"))
    b = b + timedelta(days=1) #1



odds_array = np.asarray(odds_list)


plt.figure(figsize=(6, 6))
plt.ylim(-5, 105)  # so 100 shows up on the graph, and 0 (thanks V.)

# Get team data
for team_id_db in division_team_id_list:
    team_id = team_id_db - 1
    team_data = odds_array[:, team_id]
    N = len(team_data)
    average_count = 5
    average_team_data = running_mean(team_data, average_count)
    average_dates_list = dates_list[average_count - 1 :]
    # plt.plot(dates_list,team_data)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    plt.plot(
        average_dates_list,
        average_team_data,
        label=team_abbreviation(team_id + 1),
        alpha=0.6,
    )

plt.xlabel("Date")
plt.ylabel("Team Playoff Odds")
plt.title(
    division_name
    + " Division Playoff Odds "
+ str(season_year - 1)
+ "-"
+ str(season_year)
+ "\n (teams in division may not be accurate before 2004)"
)
plt.legend()
plt.xticks(rotation=15)
plt.savefig(division_name + "_" + str(season_year) + ".png")
plt.show()

