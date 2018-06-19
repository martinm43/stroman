# coding: utf-8
# %load mcss_ext_test.py
"""
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django
"""

from __future__ import print_function, division

from mcss_ext2 import simulations_result_vectorized
from pprint import pprint
from mlb_data_models import Team

team_results=simulations_result_vectorized()
teams=Team.select()

teams_dict = [dict(zip(['mlbgames_name','division'],[i.mlbgames_name,i.division])) for i in teams]
for i,d in enumerate(teams_dict):
    d['% Division'] = team_results[i][0]
    d['% Wild Card'] = team_results[i][1]
    d['Avg. Wins'] = team_results[i][2]
    
pprint(teams_dict)
