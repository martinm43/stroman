# coding: utf-8
import pandas as pd
from pprint import pprint

from models import Games, Teams
from supports import team_identifier

df = pd.read_excel("MLB_schedule_2020.xls")

#Two iterations are used for clarity.
#First loop looks through all the dates and then through
#all the teams. This creates a list of teams in the format
#Date, Team, Team.
game_list = []
for i,j in enumerate(df['Date']):
   for t in df.keys():
       if t != "Date" and type(df[t][i]) is str:
           game_list.append([j,t,df[t][i]])

game_dict_list=[]

for g in game_list:
    game_dict={}
    game_dict.update({'Date': g[0]})
    if g[2].find('@') == 0:
        game_dict.update({'home_team_name': g[2][1:4]})
        game_dict.update({'away_team_name': g[1]})
    else:
        game_dict.update({'home_team_name': g[1]})
        game_dict.update({'away_team_name': g[2]})

    game_dict.update({'season_year':2020})

    game_dict['scheduled_date']=game_dict['Date'].to_pydatetime()
    del game_dict['Date']

    game_dict.update({'home_team':team_identifier(game_dict['home_team_name'])})
    game_dict.update({'away_team':team_identifier(game_dict['away_team_name'])})

    game_dict_list.append(game_dict)

# Need to delete double entries because games are counted twice.
game_dict_list = [dict(t) for t in {tuple(d.items()) for d in game_dict_list}]

Games.replace_many(game_dict_list).execute()
