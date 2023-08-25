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

year_max = 2023
year_min = 1977

""" try:
    season_year = int(input(f"Please select a year between {year_min} and {year_max}, or enter 0 for random year: "))
except ValueError:
    print("Invalid value entered, quitting!!")
    sys.exit(1)
    0
if season_year == 0:
    season_year = random.randint(year_min,year_max)
if season_year > year_max or season_year < year_min:
    print("Year outside range, exiting!")
    sys.exit(1)

#Select a division
if season_year >= 1994:
    mode_dict={1:"AL Central",
    2:"AL East",
    3:"AL West",
    4:"NL Central",
    5:"NL East",
    6:"NL West"}
    print("Divisions in "+str(season_year)+" are as follows: ")
    print(" 1: AL Central \n 2: AL East \n 3: AL West \n 4: NL Central \n 5: NL East \n 6: NL West")
    dn = int(input("Please select a division: "))
    #dn = random.randint(1,6)
else:
    mode_dict={1:"AL East",
    2:"AL West",
    3:"NL East",
    4:"NL West"}
    print("Divisions in "+str(season_year)+" are as follows: ")
    print(" 1: AL East \n 2: AL West \n 3: NL East \n 4: NL West")
    dn = int(input("Please select a division: "))
    #dn = random.randint(1,4)

try:
    division_name = mode_dict[int(dn)]
    print(division_name)
except KeyError:
    print("Invalid division key provided, quitting")
    sys.exit(1) """

season_year = 2023
division_name = "NL Central"
ratings_mode = "Elo"

a = datetime(season_year, 3, 20)
b = datetime(season_year, 4, 10)
end = min(datetime(season_year, 11, 1), datetime.today())

if season_year == 2020:    
    a = datetime(season_year, 7, 23)
    b = datetime(season_year, 8, 5)
    end = datetime(season_year,10,29)

if b >= end:
    print("Error in script, check first calc and end date")
    sys.exit(1)


# Python Moving Average, taken by:
# https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# note that there's a faster version using pandas but NO PANDAS.
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N


team_labels = [team_abbreviation(i) for i in range(1, 31)]



#Choosing appropriate divisions
if season_year >= 2013:
    print("ONE")
    query = Teams.select().where(Teams.division == division_name)
    division_team_id_list = [i.team_id for i in query]
if season_year >= 1998 and season_year <= 2012:
    print("TWO")
    query = Teams.select().where(Teams.legacy_divisions_1 == division_name)
    division_team_id_list = [i.team_id for i in query]
if season_year >= 1994 and season_year <= 1997:
    print("THREE")
    query = Teams.select().where(Teams.legacy_divisions_2 == division_name)
    division_team_id_list = [i.team_id for i in query]
elif season_year <= 1993:
    print("FOUR")
    query = Teams.select().where(Teams.legacy_divisions_3 == division_name)
    division_team_id_list = [i.team_id for i in query]



# Odds calculations
odds_list = []
x_odds = playoff_odds_calc(a, b, season_year)
x_odds = [x[4] for x in x_odds]

odds_list.append(x_odds)

dates_list = []
dates_list.append(b)



while b < end:
    
    x_odds = playoff_odds_calc(a, b, season_year, ratings_mode=ratings_mode)

    #print(b)
    #pprint(x_odds)

    x_odds = [x[4] for x in x_odds]

    odds_list.append(x_odds)
    dates_list.append(b)
    print("Finished processing "+b.strftime("%m %d %Y"))
    b = b + timedelta(days=4) #1



odds_array = np.asarray(odds_list)


plt.figure(figsize=(6, 6))
plt.ylim(-5, 105)  # so 100 shows up on the graph, and 0 (thanks V.)

# Get team data
for team_id_db in division_team_id_list:
    team_id = team_id_db - 1
    team_data = odds_array[:, team_id]
    N = len(team_data)
    average_count = 10
    average_team_data = running_mean(team_data, average_count)
    average_dates_list = dates_list[average_count - 1 :]
    # plt.plot(dates_list,team_data)
    label_str = label=team_abbreviation(team_id + 1)
    if label_str == "WSN" and season_year <= 2004:
        label_str = "MON" #Expos correction.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
    plt.plot(
        average_dates_list,
        average_team_data,
        label=label_str,
        alpha=0.6,
    )

plt.xlabel("Date")
plt.ylabel("Team Playoff Odds")
plt.title(
    division_name
    + " Playoff Odds, "+ratings_mode+", "
+ str(season_year)
+ "\n (includes wild card(s) if applicable. Invalid for 1994, 1981)"
)
plt.legend()
plt.xticks(rotation=15)
plt.savefig(division_name + "_" + str(season_year) + "-"+ratings_mode + ".png")
plt.show(block=False)
plt.pause(10)
plt.close()

