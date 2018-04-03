"""
This function is intended to take the 'key stats' of two teams
and apply tiebreaker logic to determine who wins.

Note that, per MLB, should two teams be tied for a division title 
or the wild card, a 'play in game' is required regardless of whether both
teams would make it in.

Simulating that logic poses an intense challenge, and at the time of writing
(April 2018) it is not an immediate concern.

"""

def tiebreaker(team_1_dict,team_2_dict,win_matrix):
    pprint(team_1_dict)
    pprint(team_2_dict)
    pprint(win_matrix)
    team_1_id=team_1_dict['team_id']
    team_2_id=team_2_dict['team_id']
    #1: head to head
    if win_matrix[team_1_id-1][team_2_id-1]>win_matrix[team_2_id-1][team_1_id-1]:
        return 1
    elif win_matrix[team_2_id-1][team_1_id-1]>win_matrix[team_1_id-1][team_2_id-1]:
        return 2 
    #2: division
    elif team_1_dict['division_wins']>team_2_dict['division_wins']:
        return 1
    elif team_2_dict['division_wins']>team_1_dict['division_wins']:
        return 2 
    #3: league
    elif team_1_dict['league_wins']>team_2_dict['league_wins']:
        return 1
    elif team_2_dict['league_wins']>team_1_dict['league_wins']:
        return 2 
    return 0
    
if __name__=='__main__':
    import numpy
    from pprint import pprint
    #Create test team brackets
    x1={'team_id':1,'division_wins':31.0,'total_wins':90,'league_wins':62}
    x2={'team_id':2,'division_wins':33.0,'total_wins':90,'league_wins':63}
    #randomly generate the win matrix
    win_matrix=numpy.random.randint(0,7,(30,30))
    pprint(win_matrix)
    pprint(tiebreaker(x1,x2,win_matrix))
