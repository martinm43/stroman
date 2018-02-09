# coding: utf-8
"""
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

#only use if loading into ipython
#get_ipython().magic(u'load mlb_array.py')

mlb_schedule_2018=pd.read_excel('MLB_schedule_2018_1_.xls',header=None)
mlb_array=mlb_schedule_2018.as_matrix()

mlb_team_list=mlb_array[0,2:].tolist()
mlb_team_list.sort()
pprint(mlb_team_list)
