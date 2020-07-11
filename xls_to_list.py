# coding: utf-8
import pandas as pd
from pprint import pprint

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
    print(g[2].find('@'))
    if g[2].find('@') == 0:
        game_dict.update({'Home_Team': g[2][1:4]})
        game_dict.update({'Away_Team': g[1]})
    else:
        game_dict.update({'Home_Team': g[1]})
        game_dict.update({'Away_Team': g[2]})
    game_dict_list.append(game_dict)

pprint(game_dict_list)
