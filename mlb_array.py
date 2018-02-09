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
#some type of time import

#only use if loading into ipython
#get_ipython().magic(u'load mlb_array.py')

mlb_schedule_2018=pd.read_excel('MLB_schedule_2018_1_.xls',header=None)
mlb_array=mlb_schedule_2018.as_matrix()

mlb_team_list=mlb_array[0,2:].tolist()
mlb_team_list.sort()

id_dict_list=[{'id':i+1,'Abbreviation':abbrev} for i,abbrev in enumerate(mlb_team_list)]

game_dict_list=[]
for i in range(1,mlb_array.shape[0]):    
    #trial for row 1 with real data
    for j in range(2,mlb_array.shape[1]):
        #date,column header team, opponent
        if str(mlb_array[i,j])!='nan':
            #date,home team,away team
            if mlb_array[i,j][0]=='@':
                game_dict_list.append({'date':mlb_array[i,1],'home_team':mlb_array[i,j].replace('@',''),'away_team':mlb_array[0,j]})
            else:
                game_dict_list.append({'date':mlb_array[i,1],'home_team':mlb_array[0,j],'away_team':mlb_array[i,j]})

pprint(game_dict_list)
