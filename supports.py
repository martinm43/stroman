"""
Gets data from the mlbgame api
and then updates the existing db entries

Need to doublecheck/tune algo
"""
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

if __name__=="__main__":
    #test abbrev to id
    print(abbrev_to_id('Ana'))
