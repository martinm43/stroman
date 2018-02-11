from mlb_data_models import Team, Game, SRSRating

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
