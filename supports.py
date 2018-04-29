"""
These scripts are functions commonly reused in other files.
"""
from __future__ import division, print_function
from mlb_data_models import Team, Game, SRSRating
from datetime import datetime, timedelta
from james import SRS_regress
import numpy as np
from pprint import pprint
import random

def teams_index_matcher(teams_index,namestr):
    team_ind=[t['team_id'] for t in teams_index if t['mlbgames_name']==namestr][0]
    return team_ind

def abbrev_to_id(abbrev):
    x=Team.select().where(Team.abbreviation==abbrev)
    return [i.id for i in x][0]

def mlbgames_name_to_id(mlbgames_name):
    x=Team.select().where(Team.mlbgames_name==mlbgames_name)
   # print(x)
    return [i.id for i in x][0]

def dict_search(list_of_dicts,key1,key_value1,key2):
    x=[i for i in list_of_dicts if i[key1]==key_value1]
    if x==[]:
        print('Value not found, check input')
        return x
    else:
        return x[0][key2]

def list_to_csv(csvfile,list_of_lists):
    import csv
    csvfile_out = open(csvfile,'wb')
    csvwriter = csv.writer(csvfile_out)
    for row in list_of_lists:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()
    return 1

def id_to_mlbgames_name(id,verbose=False):
    from mlb_data_models import Team
    t=Team.select().where(Team.id==id)
    if verbose==False:
        t=[x.mlbgames_name for x in t][0]
    else:
        t=[[x.mlbgames_name,x.division] for x in t][0]
    return t

def games_won_to_date(return_format='list'):
    played_games=Game.select().where(Game.scheduled_date<datetime.today()-timedelta(days=1)).order_by(Game.scheduled_date) 
    played_games=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in played_games]
    winlist=[x[0] if x[1]>x[3] else x[2] for x in played_games]
    winrows=[]
    if return_format=='list_of_lists':
        winlist=[x[0] if x[1]>x[3] else x[2] for x in played_games]
        winrows=[]
        for i in range(1,31):
            winrows.append([winlist.count(i)])
        return winrows
    elif return_format=='list':
        winlist=[x[0] if x[1]>x[3] else x[2] for x in played_games]
        winrows=[]
        for i in range(1,31):
            winrows.append(winlist.count(i))       
        return winrows
    elif return_format=='matrix':
        win_matrix=np.zeros((30,30))
        for x in played_games:
            if x[1]>x[3]:
                win_matrix[x[0]-1,x[2]-1]+=1    
            elif x[3]>x[1]:
                win_matrix[x[2]-1,x[0]-1]+=1
        return win_matrix
    else:
        print('invalid option')
        return 0

def future_games_dicts():
    """
    Returns a list of dicts of future games (used in all the mcss files)
    """
    #dummy variable to represent the query (retrieve ratings for current day)
    x=SRSRating.select().where(SRSRating.rating_date==datetime.now().\
                   replace(hour=0,minute=0,second=0,microsecond=0)).order_by(SRSRating.team_id)
    
    #retrieve ratings for current day
    ratings=[i.rating for i in x]
    
    if ratings==[]:
        print('Current ratings do not exist yet. Please run full ratings calculations')
        return 1
    
    #Ported from old "standings_calculations" file
    ratings_dict_list=[{'abbreviation':'Ana'},
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
    
    for i,x in enumerate(ratings_dict_list):
        x['team_id']=i+1
        x['rating']=float(ratings[i])

    #pprint(ratings_dict_list)
    
    #Get the list of games.
    query=Game.select().where(Game.scheduled_date>=datetime.now())
    game_dict_list=[dict(zip(['id','scheduled_date','away_team','home_team'],\
              [i.id,i.scheduled_date,i.away_team,i.home_team])) for i in query]
        
    #Build a function of a function (I think decorators do this) - research later.
    def get_rating(_ratings,id):
        return dict_search(_ratings,'team_id',id,'rating')

    regression_function=SRS_regress

    #monte_carlo_calculation component
    for x in game_dict_list:
        x['differential']=get_rating(ratings_dict_list,x['home_team'])\
                          -get_rating(ratings_dict_list,x['away_team'])
        x['home_win_probability']=regression_function(x['differential'])

    return game_dict_list

def mcss(game_dict_list):
    """Function takes in a list of dicts of games with the home team's win probability"""        
    win_matrix=np.zeros((30,30))
    for x in game_dict_list:
        if x['home_win_probability']<=random.uniform(0,1):
            win_matrix[x['home_team']-1,x['away_team']-1]+=1    
        else:
            win_matrix[x['away_team']-1,x['home_team']-1]+=1
    return win_matrix

if __name__=="__main__":
    #test abbrev to id
    pprint(future_games_dicts())
    
    
