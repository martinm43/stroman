"""
A bunch of functions that I use to do Monte Carlo simulations of issues
Performs Monte Carlo simulation using MLB
schedule and then determines playoff teams.

Tiebreaker logic to be developed. 
Other functionality (such as processing daily updates)
are far more important.

MAM

"""

import random
import numpy as np

if __name__=='__main__':
    import json
    import numpy as np
    from pprint import pprint
    from mlb_data_models import Team,database
    import sys
    from supports import games_won_to_date, future_games_dicts, mcss

    sim_results=[]

    cursor=database.execute_sql('select distinct division from teams;')
    list_of_divisions=[row[0] for row in cursor]

    league_teams=Team.select(Team.team_name,Team.id,Team.division,Team.league)
    league_teams=[dict(zip(['team_name','team_id','division','league'],[x.team_name,x.id,x.division,x.league])) for x in league_teams]

    try:
        ite=int(sys.argv[1])
    except IndexError:
        ite=1
        print('Debug run, using 1 iterations')

    binomial_win_probabilities=future_games_dicts()
    if binomial_win_probabilities==1:
        print('Error occurred while calculating ' \
              'future binomial win probabilities')
        sys.exit(1)
        
    for i_ite in range(0,ite):
        win_matrix=mcss(binomial_win_probabilities)
        known_wins=games_won_to_date(return_format='matrix')
        win_matrix+=known_wins
        total_wins=np.sum(win_matrix,axis=0)
        #Raw win totals.
        for x in league_teams:
            x['total_wins']=total_wins[x['team_id']-1]

        #pprint(league_teams)
        #Division win totals and eventually division leaders
        for d in list_of_divisions:
            dt=[x for x in league_teams if x['division']==d]
            for t in dt:
                other_division_team_ids=[x['team_id'] for x in dt if x['team_id']!=t['team_id']]
                other_league_team_ids=[x['team_id'] for x in league_teams if x['league']==t['league']]
                division_wins=sum([win_matrix[i-1,t['team_id']-1] for i in other_division_team_ids])
                t['division_wins']=division_wins
                league_wins=sum([win_matrix[i-1,t['team_id']-1] for i in other_league_team_ids])
                t['league_wins']=league_wins

            #sort list of dicts             
            new_dt=sorted(dt, key=lambda k: (-k['total_wins'],-k['division_wins'],-k['league_wins']))
            for i,d in enumerate(new_dt):
                d['div_rank']=i+1
                if d['div_rank']==1:
                    d['div_winner']=True
                else:
                    d['div_winner']=False

        #print('Iteration number '+str(i_ite)+':')
        sim_results.append(league_teams)
    #pprint(sim_results[0])
    al_wc=[x for x in sim_results[0] if (x['div_winner']==False and x['league']=='AL')]
    al_wc.sort(key=lambda x:-x['total_wins'])
    nl_wc=[x for x in sim_results[0] if (x['div_winner']==False and x['league']=='NL')]
    nl_wc.sort(key=lambda x:-x['total_wins'])
    pprint(al_wc[0:2])
    pprint(nl_wc[0:2])
