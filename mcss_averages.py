"""
A bunch of functions that I use to do Monte Carlo simulations of issues
This function returns "raw projected wins". A good teaser.
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
    import sys
    import json
    import numpy as np
    from pprint import pprint
    from mlb_data_models import Team,database

    cursor=database.execute_sql('select distinct division from teams;')
    list_of_divisions=[row[0] for row in cursor]

    league_teams=Team.select(Team.team_name,Team.id,Team.division,Team.league)
    league_teams=[dict(zip(['team_name','team_id','division','league'],[x.team_name,x.id,x.division,x.league])) for x in league_teams]

    with open('test_dicts','r') as fin:
        test_dict=json.load(fin)

    ite=int(sys.argv[1])

#    mc_sim_matrix=np.zeros((30,ite))  

#    for i in range(0,ite):
#        result=np.sum(mcss(test_dict),axis=0)
#        mc_sim_matrix[:,i]=result

#    sim_results=np.average(mc_sim_matrix,axis=1)

    sim_results=np.zeros(30)
    for i in range(0,ite):
        sim_results+=np.sum(mcss(test_dict),axis=0)

    sim_results=np.divide(sim_results,ite)

    for x in league_teams:
        x['total_wins']=sim_results[x['team_id']-1]

    league_teams = sorted(league_teams, key=lambda k: -k['total_wins'])

    for i in league_teams:
        print(i['team_name'],i['total_wins'])