"""
These scripts are "helper scripts" largely for the purpose
of converting between various forms of team identifications
using the "Team" table in the database.
"""
from mlb_data_models import Team, Game
from datetime import datetime, timedelta

def teams_index_matcher(teams_index,namestr):
    team_ind=[t['team_id'] for t in teams_index if t['mlbgames_name']==namestr][0]
    return team_ind

def abbrev_to_id(abbrev):
    x=Team.select().where(Team.abbreviation==abbrev)
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
        for i in range(1,31):
            winrows.append([winlist.count(i)])
    elif return_format=='list':
         for i in range(1,31):
            winrows.append(winlist.count(i))       
    return winrows

if __name__=="__main__":
    #test abbrev to id
    print(abbrev_to_id('Ana'))
