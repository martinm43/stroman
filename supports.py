"""
Gets data from the mlbgame api
and then updates the existing db entries

Need to doublecheck/tune algo
"""
from mlb_data_models import Team

def teams_index_matcher(teams_index,namestr):
    team_ind=[t['team_id'] for t in teams_index if t['mlbgames_name']==namestr][0]
    print(team_ind)
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

def id_to_mlbgames_name(id):
    from mlb_data_models import Team
    t=Team.select().where(Team.id==id)
    t=[x.mlbgames_name for x in t][0]
    return t


if __name__=="__main__":
    #test abbrev to id
    print(abbrev_to_id('Ana'))
