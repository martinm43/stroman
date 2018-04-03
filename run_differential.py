"""
ptsaverages

This script calculates the "average margin of victory" based on a date
period and the start date/end date for analysis.

AUTO mode will be triggered by using AUTO after the script.

Human inputs that need to be automated: Automatic input

Maximum margin of victory: 15
Start date: 4 weeks before analysis
End date: Current day

Also does "pythagorean win expectation"

"""
import sqlite3
import os
import csv
from pprint import pprint
import numpy as np
from datetime import datetime,timedelta
from mlb_data_models import Game, Team
from supports import list_to_csv, id_to_mlbgames_name

#define factor
pythag_factor=1.83 # As used by baseball reference.

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


# Create a 30x8 vector: rows are teams, columns are "RUNS SCORED", "RUNS ALLOWED", "GAMES PLAYED", 
# "AVERAGE RUNS SCORED", "AVERAGE RUNS ALLOWED", "AVERAGE RUN DIFFERENTIAL", "RUN DIFFERENTIAL"
# "PYTHAGOREAN_WINS"
diff_matrix=np.zeros((30,8))
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
    diff_matrix[i,7]=diff_matrix[i,0]**pythag_factor/(diff_matrix[i,0]**pythag_factor+diff_matrix[i,1]**pythag_factor)

#p#print(diff_matrix)

diff_list=diff_matrix.tolist()

pprint(diff_list)

#Print to screen.

print('Listing run differentials:')
for i,x in enumerate(diff_list):
    print('The '+id_to_mlbgames_name(i+1)+' have a run differential of '+'{0}'.format(x[6])+\
          ', scoring '+'{0}'.format(x[0])+' runs while allowing '+\
          '{0}'.format(x[1])+' runs.')
print('Listing pythagorean win expectancies: ')
for i,x in enumerate(diff_list):
    print(id_to_mlbgames_name(i+1)+': '+'{:.1f}'.format(x[7]*162))

#Write list of point differentials to a file for use by other programs
#csvfile_out = open(wkdir+'run_diff_vector.csv','wb')
#csvwriter = csv.writer(csvfile_out)
vector_of_means=[[x[6]] for x in diff_list]
#print(vector_of_means)
#for row in vector_of_means:
#    csvwriter.writerow(row)
#csvfile_out.close()
list_to_csv('run_diff_vector.csv',vector_of_means)
