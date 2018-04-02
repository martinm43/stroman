"""
ptsaverages

This script calculates the "average margin of victory" based on a date
period and the start date/end date for analysis.

AUTO mode will be triggered by using AUTO after the script.

Human inputs that need to be automated: Automatic input

Maximum margin of victory: 15
Start date: 4 weeks before analysis
End date: Current day

"""
import sqlite3
import os
import csv
import time
from pprint import pprint
from dbtools.access_nba_data import epochtime
import numpy as np
from datetime import datetime,timedelta
from mlb_data_models import Game

#needs to be adjusted for baseball
home_team_adv = 2.0

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#New automated code
analysis_start_date = datetime.now()-timedelta(weeks=4) #4 weeks prior, 7 days in a week, 86400 sec in a day
analysis_end_date = datetime.now()

"""
teamdict = [{'team_id':'1', 'team_name':'ATL', 'conf':'E'},
            {'team_id':'2', 'team_name':'BOS', 'conf':'E'},
            {'team_id':'3', 'team_name':'BRK', 'conf':'E'},
            {'team_id':'4', 'team_name':'CHA', 'conf':'E'},
            {'team_id':'5', 'team_name':'CHI', 'conf':'E'},
            {'team_id':'6', 'team_name':'CLE', 'conf':'E'},
            {'team_id':'7', 'team_name':'DAL', 'conf':'W'},
            {'team_id':'8', 'team_name':'DEN', 'conf':'W'},
            {'team_id':'9', 'team_name':'DET', 'conf':'E'},
            {'team_id':'10', 'team_name':'GSW', 'conf':'W'},
            {'team_id':'11', 'team_name':'HOU', 'conf':'W'},
            {'team_id':'12', 'team_name':'IND', 'conf':'E'},
            {'team_id':'13', 'team_name':'LAC', 'conf':'W'},
            {'team_id':'14', 'team_name':'LAL', 'conf':'W'},
            {'team_id':'15', 'team_name':'MEM', 'conf':'W'},
            {'team_id':'16', 'team_name':'MIA', 'conf':'E'},
            {'team_id':'17', 'team_name':'MIL', 'conf':'E'},
            {'team_id':'18', 'team_name':'MIN', 'conf':'W'},
            {'team_id':'19', 'team_name':'NOP', 'conf':'W'},
            {'team_id':'20', 'team_name':'NYK', 'conf':'E'},
            {'team_id':'21', 'team_name':'OKC', 'conf':'W'},
            {'team_id':'22', 'team_name':'ORL', 'conf':'E'},
            {'team_id':'23', 'team_name':'PHI', 'conf':'E'},
            {'team_id':'24', 'team_name':'PHX', 'conf':'W'},
            {'team_id':'25', 'team_name':'POR', 'conf':'W'},
            {'team_id':'26', 'team_name':'SAC', 'conf':'W'},
            {'team_id':'27', 'team_name':'SAS', 'conf':'W'},
            {'team_id':'28', 'team_name':'TOR', 'conf':'E'},
            {'team_id':'29', 'team_name':'UTA', 'conf':'W'},
            {'team_id':'30', 'team_name':'WAS', 'conf':'E'}]
"""

#No limit on margin of victory
#No margin required for baseball. 30-3 outcomes are
#rare and good.

list_of_means = []
vector_of_means = []

"""
for i in range(1, 31):
    team_dict={}
    team_id=str(i)
    #Incorporating Date Limits
    #Replace with a peewee statement, but I need Peewee Select Case
    str_input = 'SELECT CASE WHEN away_team='+team_id+\
           ' THEN away_pts-home_pts'\
           ' WHEN home_team'+team_id+\
           ' THEN home_pts-away_pts'\
           ' END FROM bballref_scores WHERE\
           (away_team_id='+team_id+\
           ' OR home_team'+team_id+') AND '+\
           '(scheduled_date >= '+analysis_start_date\
           ' AND scheduled_date <= '+analysis_end_date)+');'

    if str_input.find('drop') == -1:
        query_result = c.execute(str_input).fetchall()

    query_result = [q[0] for q in query_result]

    #filter out huge results
    scores = np.asarray(query_result)

    scores = score_bound(scores,score_cut)

    team_name = [row['team_name'] for row in teamdict if row['team_id'] == team_id][0]
    print('The '+team_name+' have an average run differential of '+'{:1.4}'.format(scores.mean()))
    team_dict['team_name'] = team_name
    team_dict['team_mean'] = scores.mean()
    list_of_means.append(team_dict)
    vector_of_means.append([scores.mean()])
    team_dict = {}

conn.close()
"""

list_of_means.sort(key = lambda x:x['team_mean'], reverse = True)

#Write list of point differentials to a file for use by other programs
csvfile_out = open(wkdir+'run_diff_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in vector_of_means:
    csvwriter.writerow(row)
csvfile_out.close()
