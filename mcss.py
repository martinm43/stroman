# coding: utf-8
get_ipython().magic(u'load mcss.py')
# %load mcss.py
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

#define a "percentization function":
def format_percent(percent_float):
    return str(percent_float) + '%'

team_results=simulations_result_vectorized()
teams=Team.select()

teams_dict = [dict(zip(['Team','Division'],[i.mlbgames_name,i.division])) for i in teams]
for i,d in enumerate(teams_dict):
    d['Win Division'] = round(team_results[i][0]*100.0,1)
    d['Win Wild Card'] = round(team_results[i][1]*100.0,1)
    d['Avg. Wins'] = round(team_results[i][2],1)
    d['Make Playoffs'] = d['Win Division'] + d['Win Wild Card']
    #Convert into percentages for printing
    d['Win Division'] = format_percent(d['Win Division'])
    d['Win Wild Card'] = format_percent(d['Win Wild Card'])
    d['Make Playoffs'] = format_percent(d['Make Playoffs'])

teams_dict.sort(key=lambda x: (x['Division'],-x['Avg. Wins']))

team_tuples = [(d['Division'],d['Team'],d['Avg. Wins'],        d['Win Division'],d['Win Wild Card'],d['Make Playoffs']) for d in teams_dict]

results_table = tabulate(team_tuples, headers=['Division','Team','Avg. Wins',                            'Win Division','Win Wild Card','Make Playoffs'],                        tablefmt='rst',numalign='left')

print(results_table)
query=Team.select()
divisions = [t.division for t in query]
divisions = list(set(divisions))
