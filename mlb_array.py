# coding: utf-8
"""
mlb_array

The objectives of this script are to:

1. Generate a list of teams, with league and conference, in order to create a table:
   Intermediate step is of course a list of dicts

id(alphabetical),teamabbrev,league,division

2. Parse the season schedule into 'standard format',i.e.

date,awayteam,awayscore,hometeam,homescore,season_year



"""
import pandas as pd
from pprint import pprint

#only use if loading into ipython
#get_ipython().magic(u'load mlb_array.py')

mlb_schedule_2018=pd.read_excel('MLB_schedule_2018_1_.xls')
mlb_array=mlb_schedule_2018.as_matrix()

#AL list using Boston
mlb_games_list=mlb_array[:,4].tolist()
mlb_games_list_bos=[x for x in mlb_games_list if str(x) != 'nan']
[x.replace('@','') for x in mlb_games_list_bos]
clean_bos_list=[x.replace('@','') for x in mlb_games_list_bos]

#Get a NL list using Arizona
mlb_games_list=mlb_array[:,17].tolist()
mlb_games_list_ari=[x for x in mlb_games_list if str(x) != 'nan']
clean_ari_list=[x.replace('@','') for x in mlb_games_list_ari]
list(set(clean_ari_list))

#Combine the lists
nl_al_teams=list(set((clean_bos_list+clean_ari_list)))
nl_al_teams.append(u'Bos')
nl_al_teams.append(u'Ari')
nl_al_teams.sort()

pprint(nl_al_teams)
