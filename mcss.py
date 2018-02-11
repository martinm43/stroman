"""
This script will implement the same strategy used in the "Naismith"  program,
but only in one script.
"""

import datetime
from mlb_data_models import Game
from pprint import pprint
from james import SRS_regress
from supports import dict_search

#Known wins - to be implemented, not yet required for obvious reasons.

#Future games.
x=Game.select().where(Game.scheduled_date>=datetime.datetime.now())
#id,scheduled_date,away_team,home_team
x=[[i.id,i.scheduled_date,i.away_team,i.home_team] for i in x]
pprint(x)

#
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

#Build a function of a function (I think decorators do this).
def get_rating(_ratings,id):
    return dict_search(_ratings,'team_id',id,'rating')



