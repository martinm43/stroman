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
from pprint import pprint
import numpy as np
from datetime import datetime,timedelta
from mlb_data_models import Game

#needs to be adjusted for baseball
home_team_adv = 2.0

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#New automated code
analysis_start_date = datetime.now()-timedelta(weeks=4) #4 weeks prior, 7 days in a week, 86400 sec in a day
analysis_end_date = datetime.now()

#No limit on margin of victory
#No margin required for baseball. 30-3 outcomes are
#rare and good.

list_of_means = []
vector_of_means = []

games=Game.select().where(Game.scheduled_date>=analysis_start_date,Game.scheduled_date<=analysis_end_date-timedelta(days=1))
games=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in games]

# Create a 30x7 vector: rows are teams, columns are "RUNS SCORED", "RUNS ALLOWED", "GAMES PLAYED", 
# "AVERAGE RUNS SCORED", "AVERAGE RUNS ALLOWED", "AVERAGE RUN DIFFERENTIAL", "RUN DIFFERENTIAL"
diff_matrix=np.zeros((30,7))
for g in games:
    #Away team.
    diff_matrix[g[0]-1,0]+=g[1]
    diff_matrix[g[0]-1,1]+=g[3]
    diff_matrix[g[0]-1,2]+=1
    #Home team.
    diff_matrix[g[2]-1,0]+=g[3]
    diff_matrix[g[2]-1,1]+=g[1]
    diff_matrix[g[2]-1,2]+=1

for i in range(0,len(diff_matrix)):
    diff_matrix[i,3]=diff_matrix[i,0]/diff_matrix[i,2]
    diff_matrix[i,4]=diff_matrix[i,1]/diff_matrix[i,2]
    diff_matrix[i,5]=diff_matrix[i,3]-diff_matrix[i,4]
    diff_matrix[i,6]=diff_matrix[i,5]*diff_matrix[i,2]

pprint(diff_matrix)

list_of_means.sort(key = lambda x:x['team_mean'], reverse = True)

#Write list of point differentials to a file for use by other programs
csvfile_out = open(wkdir+'run_diff_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in vector_of_means:
    csvwriter.writerow(row)
csvfile_out.close()
