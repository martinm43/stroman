"""

A script that produces a table of information. Inputs below.
-- start date
-- end date
-- season year (denoted by end)

Output: table (string)

"""
# Standard imports
from datetime import datetime, timedelta

# Third Party Imports
from tabulate import tabulate

# Query imports
from mlb_database.queries import (
    games_query,
    team_abbreviation,
    epochtime,
    new_elo_ratings_list,
    new_srs_ratings_list,
    form_query,
)

from mlb_database.mlb_models import Games

# Analytics imports
from analytics.SRS import SRS
from analytics.pythag import league_pythagorean_wins
from random import randint

# Wins script import
from analytics.wins_script import get_wins

# Query Testing
season_year = 2023
start_datetime = datetime(season_year,3,15)
end_datetime = datetime.today()

games_list = games_query(start_datetime, end_datetime)

print(len(games_list))

# Custom SRS calculation options
max_MOV = 100  # no real max MOV
home_team_adv = 2.124
win_floor = 0

teams_constant = 30

wins_dict_list = [
    get_wins(i, season_year, start_datetime, end_datetime) for i in range(1, teams_constant+1)
]
wins_list = [[x["away_record"], x["home_record"], x["record"]] for x in wins_dict_list]

# Pythagorean Wins
lpw_results = league_pythagorean_wins(
    Games,
    mincalcdatetime=epochtime(start_datetime),
    maxcalcdatetime=epochtime(end_datetime),
)

""" srs_list = SRS(
    games_list, max_MOV=max_MOV, home_team_adv=home_team_adv, win_floor=win_floor
) """

elo_list = new_elo_ratings_list(epochtime(end_datetime))

srs_list = new_srs_ratings_list(epochtime(end_datetime))

form_list = [form_query(i) for i in range(1, teams_constant+1)]

lpw_results.sort(key=lambda x: x[0])

results = list(zip(lpw_results, srs_list, wins_list, elo_list, form_list))

results = [
    [x[0][0], x[0][1], x[1], x[2][0], x[2][1], x[2][2], x[3], x[4]] for x in results
]

results_print_list = [
    [
        team_abbreviation(x[0]),
        round(x[1], 0),
        round(x[2] * 100.0 / 100.0, 3),
        x[6],
        x[3],
        x[4],
        x[5],
        x[7],
        ]
    for x in results
]

#Team name change
for x in results_print_list:
    if x[0] == "WSN" and season_year <= 2004:
        x[0] = "MON"

#Remove zero entries
results_print_list = [x for x in results_print_list if x[1] > 0]

results_print_list.sort(key=lambda x: x[0])



results_table = tabulate(
    results_print_list,
    headers=[
        "Team",
        "Pythag. Wins",
        "Est. SRS",
        "Elo Rating",
        "Away Record",
        "Home Record",
        "Overall Record",
        "Form",
    ],
    tablefmt="rst",
    numalign="left",
)

print(
    "Pythagorean Win Expectations, Est. SRS, Elo, and Records \n"
    + "Based on Games Played Between: "
    + start_datetime.strftime("%b %d %Y")
    + " and "
    + end_datetime.strftime("%b %d %Y")
)
print(results_table)
