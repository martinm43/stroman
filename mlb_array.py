# coding: utf-8
"""
INITIAL SETUP SCRIPT

ONLY USED TO CREATE THE INITIAL SEASON SCHEDULE
DO NOT USE ONCE INITIAL SETUP IS COMPLETE!

mlb_array

The objectives of this script are to:

1. Parse the season schedule into 'standard format',i.e.

date,awayteam,awayscore,hometeam,homescore,season_year

2. Generate a list of teams, with league and conference, in order to create a table:
   Intermediate step is of course a list of dicts

id(alphabetical),teamabbrev,league,division

"""

import pandas as pd
from pprint import pprint
from mlb_data_models import Team, Game, database
from long_dict_inserter import big_inserter
from supports import abbrev_to_id

max_variable_size = 500

mlb_schedule_2018 = pd.read_excel('MLB_schedule_2018_1_.xls', header=None)
mlb_array = mlb_schedule_2018.as_matrix()

mlb_team_list = sorted(mlb_array[0, 2:].tolist())

id_dict_list = [{'id': i + 1, 'abbreviation': abbrev}
                for i, abbrev in enumerate(mlb_team_list)]

# Need to insert teams before you insert games.
big_inserter(database, max_variable_size, Team, id_dict_list)

game_dict_list = []
for i in range(1, mlb_array.shape[0]):
    # trial for row 1 with real data
    for j in range(2, mlb_array.shape[1]):
        # date,column header team, opponent
        if str(mlb_array[i, j]) != 'nan':
            # date,home team,away team
            if mlb_array[i, j][0] == '@':
                game_dict_list.append({'scheduled_date': mlb_array[i, 1],
                                       'home_team_name': mlb_array[i, j].replace('@', ''),
                                       'away_team_name': mlb_array[0, j],
                                       'home_team': abbrev_to_id(mlb_array[i, j].replace('@', '')),
                                       'away_team': abbrev_to_id(mlb_array[0, j])})
            else:
                game_dict_list.append({'scheduled_date': mlb_array[i, 1],
                                       'home_team_name': mlb_array[0, j],
                                       'away_team_name': mlb_array[i, j],
                                       'home_team': abbrev_to_id(mlb_array[0, j]),
                                       'away_team': abbrev_to_id(mlb_array[i, j])})

# One last thing. Because of the way that the MLB array is set up, note that each game shows up twice (ChS @KC, then KC ChS). So:
# Convert dicts to lists of tuples

print('Pre correction')
print(len(game_dict_list))
game_dict_list_corr = [dict(t) for t in set(
    [tuple(d.items()) for d in game_dict_list])]
print('Post correction')
print(len(game_dict_list_corr))

# Insert games
print(game_dict_list[0])
big_inserter(database, max_variable_size, Game, game_dict_list_corr)
