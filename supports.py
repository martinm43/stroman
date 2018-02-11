from mlb_data_models import Team, Game, SRSRating

def abbrev_to_id(abbrev):
    x=Team.select().where(Team.abbreviation==abbrev)
    return [i.id for i in x][0]

if __name__=="__main__":
    #test abbrev to id
    print(abbrev_to_id('Ana'))
