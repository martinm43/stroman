# coding: utf-8
# %load mcss_ext_test.py
"""
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django
"""

from __future__ import print_function, division

from tabulate import tabulate
from mcss_ext2 import simulations_result_vectorized
from pprint import pprint
from mlb_data_models import Team

team_results=simulations_result_vectorized()
teams=Team.select()

teams_dict = [dict(zip(['Team','Division'],[i.mlbgames_name,i.division])) for i in teams]
for i,d in enumerate(teams_dict):
    d['Win Division'] = round(team_results[i][0]*100.0,1)
    d['Win Wild Card'] = round(team_results[i][1]*100.0,1)
    d['Avg. Wins'] = team_results[i][2]
    d['Make Playoffs'] = d['Win Division'] + d['Win Wild Card']
    
teams_dict.sort(key=lambda x: (x['Division'],-x['Avg. Wins']))

team_tuples = [(d['Division'],d['Team'],d['Avg. Wins'],\
        d['Win Division'],d['Win Wild Card'],d['Make Playoffs']) for d in teams_dict]

results_table = tabulate(team_tuples, headers=['Division','Team','Avg. Wins',\
                            'Win Division','Win Wild Card','Make Playoffs'],\
                        tablefmt='rst')

print(results_table)
