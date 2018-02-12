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
    import numpy as np
    from pprint import pprint
    from mlb_data_models import Team,database

    cursor=database.execute_sql('select distinct division from teams;')
    list_of_divisions=[row[0] for row in cursor]

    division_teams=Team.select(Team.team_name,Team.id,Team.division)
    division_teams=[dict(zip(['team_name','team_id','division'],[x.team_name,x.id,x.division])) for x in division_teams]

    with open('test_dicts','r') as fin:
        test_dict=json.load(fin)

    win_matrix=mcss(test_dict)

    total_wins=np.sum(win_matrix,axis=0)
    for x in division_teams:
        x['total_wins']=total_wins[x['team_id']-1]

    pprint(division_teams)
