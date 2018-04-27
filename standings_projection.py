"""
This script writes out a list of games to be played in the mlb season along with their
binomial win probabilities.
"""

import csv
import json
import datetime
from mlb_data_models import Game
from pprint import pprint
from james import SRS_regress, runs_regress
from supports import dict_search
from mcss import mcss

#Future games.
x=Game.select().where(Game.scheduled_date>=datetime.datetime.now())
game_dict_list=[dict(zip(['id','scheduled_date','away_team','home_team'],[i.id,i.scheduled_date,i.away_team,i.home_team])) for i in x]

#Analytics component - get ratings (this is ptsaverages and ratings_calculations under the old scheme
#TBD - for now use a dummy - these are the 2017 end of season ranks
ratings=[{'abbreviation':'Ana'},
{'abbreviation':'Ari'},
{'abbreviation':'Atl'},
{'abbreviation':'Bal'},
{'abbreviation':'Bos'},
{'abbreviation':'ChC'},
{'abbreviation':'ChW'},
{'abbreviation':'Cin'},
{'abbreviation':'Cle'},
{'abbreviation':'Col'},
{'abbreviation':'Det'},
{'abbreviation':'Fla'},
{'abbreviation':'Hou'},
{'abbreviation':'Kan'},
{'abbreviation':'Los'},
{'abbreviation':'Mil'},
{'abbreviation':'Min'},
{'abbreviation':'NYM'},
{'abbreviation':'NYY'},
{'abbreviation':'Oak'},
{'abbreviation':'Phi'},
{'abbreviation':'Pit'},
{'abbreviation':'Sdg'},
{'abbreviation':'Sea'},
{'abbreviation':'Sfo'},
{'abbreviation':'StL'},
{'abbreviation':'Tam'},
{'abbreviation':'Tex'},
{'abbreviation':'Tor'},
{'abbreviation':'Was'}]

file_ratings=[]

#Burke/neo SRS ratings
filename='burke_vector.csv'
regression_function=SRS_regress
#Run differential ratings
#filename='run_diff_vector.csv'
#regression_function=runs_regress

with open(filename,'rb') as fin:
    rankdata=csv.reader(fin)
    for row in rankdata:
        file_ratings.append(row)
    fin.close

pprint(file_ratings)

for i,x in enumerate(ratings):
    x['team_id']=i+1
    x['rating']=float(file_ratings[i][0])

pprint(ratings)
#End of manual ratings.

#Build a function of a function (I think decorators do this) - research later.
def get_rating(_ratings,id):
    return dict_search(_ratings,'team_id',id,'rating')

#monte_carlo_calculation component
for x in game_dict_list:
    x['differential']=get_rating(ratings,x['home_team'])-get_rating(ratings,x['away_team'])
    x['home_win_probability']=regression_function(x['differential'])

win_matrix=mcss(game_dict_list)

#debug: write to a file
debug_json_list=game_dict_list
for x in debug_json_list:
    x.pop('scheduled_date',None)

with open('test_dicts','w') as fout:
    json.dump(debug_json_list,fout)

