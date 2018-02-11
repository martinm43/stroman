# coding: utf-8
get_ipython().magic(u'load standings_projection.py')
# %load standings_projection.py
"""
This script will implement the same strategy used in the "Naismith"  program,
but only in one script.
"""

import datetime
from mlb_data_models import Game
from pprint import pprint
from james import SRS_regress
from supports import dict_search
from mcss import mcss

#Known wins - to be implemented, not yet required for obvious reasons.

#Future games.
x=Game.select().where(Game.scheduled_date>=datetime.datetime.now())
game_dict_list=[dict(zip(['id','scheduled_date','away_team','home_team'],[i.id,i.scheduled_date,i.away_team,i.home_team])) for i in x]

#Analytics component - get ratings (this is ptsaverages and ratings_calculations under the old scheme
#TBD - for now use a dummy - these are the 2017 end of season ranks
ratings=[{'abbreviation':'Ana','rating':0.1},
{'abbreviation':'Ari','rating':0.8},
{'abbreviation':'Atl','rating':-0.7},
{'abbreviation':'Bal','rating':-0.3},
{'abbreviation':'Bos','rating':0.8},
{'abbreviation':'ChC','rating':0.6},
{'abbreviation':'ChW','rating':-0.5},
{'abbreviation':'Cin','rating':-0.7},
{'abbreviation':'Cle','rating':1.5},
{'abbreviation':'Col','rating':0.3},
{'abbreviation':'Det','rating':-0.8},
{'abbreviation':'Fla','rating':-0.5},
{'abbreviation':'Hou','rating':1.2},
{'abbreviation':'Kan','rating':-0.4},
{'abbreviation':'Los','rating':0.9},
{'abbreviation':'Mil','rating':0.1},
{'abbreviation':'Min','rating':0.2},
{'abbreviation':'NYM','rating':-0.9},
{'abbreviation':'NYY','rating':1.3},
{'abbreviation':'Oak','rating':-0.4},
{'abbreviation':'Phi','rating':-0.7},
{'abbreviation':'Pit','rating':-0.4},
{'abbreviation':'Sdg','rating':-1.3},
{'abbreviation':'Sea','rating':0.0},
{'abbreviation':'Sfo','rating':-0.9},
{'abbreviation':'StL','rating':0.2},
{'abbreviation':'Tam','rating':0.1},
{'abbreviation':'Tex','rating':0.0},
{'abbreviation':'Tor','rating':-0.3},
{'abbreviation':'Was','rating':0.6}]

for i,x in enumerate(ratings):
    x['team_id']=i+1

#End of manual ratings.

#Build a function of a function (I think decorators do this) - research later.
def get_rating(_ratings,id):
    return dict_search(_ratings,'team_id',id,'rating')

#monte_carlo_calculation component
for x in game_dict_list:
    x['differential']=get_rating(ratings,x['home_team'])-get_rating(ratings,x['away_team'])
    x['home_win_probability']=SRS_regress(x['differential'])

#simulation component
dir()
game_dict_list
import numpy as np
import random
for x in game_dict_list:
    if x['home_win_probability']<=random.uniform(0,1):
        print home
    else:
        print away
        
for x in game_dict_list:
    if x['home_win_probability']<=random.uniform(0,1):
        print 'home'
    else:
        print 'away'
        
win_matrix=np.zeros(30,30)
win_matrix=np.zeros((30,30))
for x in game_dict_list:
    if x['home_win_probability']<=random.uniform(0,1):
        win_matrix[x['home_team'],x['away_team']]+=1
    else:
        win_matrix[x['away_team'],x['home_team']]+=1
        
for x in game_dict_list:
    if x['home_win_probability']<=random.uniform(0,1):
        win_matrix[x['home_team']-1,x['away_team']-1]+=1    else:
        win_matrix[x['away_team']-1,x['home_team']-1]+=1
        
for x in game_dict_list:
    if x['home_win_probability']<=random.uniform(0,1):
        win_matrix[x['home_team']-1,x['away_team']-1]+=1    
    else:
        win_matrix[x['away_team']-1,x['home_team']-1]+=1
        
win_matriz
win_matrix
raw_total_wins=np.sum(win_matrix,axis=0)
raw_total_wins
raw_total_wins.tolist()
raw_total_wins
raw_total_wins_list=raw_total_wins.tolist()
for i,x in enumerate(id_dict_list):
    x['proj_win_total']=raw_total_wins_list[i]
    
dir()
ratings
