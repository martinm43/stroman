"""
A bunch of functions that I use to do Monte Carlo simulations of issues
"""

import random
import numpy as np

def mcss(game_dict_list):
    """Function takes in a list of dicts of games with the home team's win probability"""        
    win_matrix=np.zeros((30,30))
    for x in game_dict_list:
        if x['home_win_probability']<=random.uniform(0,1):
            win_matrix[x['home_team']-1,x['away_team']-1]+=1    
        else:
            win_matrix[x['away_team']-1,x['home_team']-1]+=1
    return win_matrix
    
if __name__=='__main__':
    import json
    from pprint import pprint
    from mlb_data_models import Team,database

    cursor=database.execute_sql('select distinct division from teams;')
    list_of_divisions=[row[0] for row in cursor]

    for d in list_of_divisions:
        division_teams=Team.select(Team.team_name,Team.id).where(Team.division==d).get()
        pprint(division_teams)

    with open('test_dicts','r') as fin:
        test_dict=json.load(fin)
