"""
Full_Ratings_Calculations

This script calculates the run differentials, pythagorean win expectations, 
and Burke ratings for MLB teams over a given time period with a given 
maximum/minimum margin of victory and average home team advantage for use in the projections
scripts. 

"""

import csv,os
import time
import numpy as np
from supports import id_to_mlbgames_name, list_to_csv
from mlb_data_models import Team, Game
import sqlite3
from datetime import datetime, timedelta
from analytics.burke_solver import burke_calc

#Define constant for pythagorean wins (the pythagorean win exponent)
pythag_factor=1.83
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#Times and constants
analysis_start_date=datetime.now()-timedelta(weeks=4) #N weeks*days*seconds
analysis_end_date=datetime.now()
max_MOV=100.0 #Maximum margin of victory set far above what is possible
home_team_adv=0.0

##################
# DATA SELECTION #
##################

games=Game.select().where(Game.scheduled_date>=analysis_start_date,Game.scheduled_date<=analysis_end_date-timedelta(days=1))
games=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in games]

#############
# ANALYTICS #
#############

#Basic run-based calculations
# Create a 30x9 vector: rows are teams, columns are:
# . "WINS" - to be added
# . "LOSSES" - to be added
#1. "RUNS SCORED"
#2. "RUNS ALLOWED"
#3. "GAMES PLAYED"
#4.  "AVERAGE RUNS SCORED"
#5. "AVERAGE RUNS ALLOWED"
#6. "AVERAGE RUN DIFFERENTIAL"
#7. "RUN DIFFERENTIAL"
#8. "PYTHAGOREAN_WINS"
#9. "ADJUSTED RATING"

#then append the division names to the list for sorting
diff_matrix=np.zeros((30,9))
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

#Adjusted Rating Calculations (Burke - after Brian Burke - ratings)
burke_data=[[g[2],g[0],g[3],g[1]] for g in games]
burkelist=burke_calc(burke_data,impmode=None,max_MOV=max_MOV,home_team_adv=home_team_adv,win_floor=0.0)
burkelist=[[b] for b in burkelist]
diff_matrix[:,8]=[b[0] for b in burkelist]



diff_list=diff_matrix.tolist()

print(diff_list)

######################
# PRINTING TO SCREEN #
######################

print('Listing run differentials:')
for i,x in enumerate(diff_list):
    print('The '+id_to_mlbgames_name(i+1)+' have a run differential of '+'{0}'.format(x[6])+\
          ', scoring '+'{0}'.format(x[0])+' runs while allowing '+\
          '{0}'.format(x[1])+' runs.')
print('Listing pythagorean win expectancies: ')
for i,x in enumerate(diff_list):
    print(id_to_mlbgames_name(i+1)+': '+'{:.1f}'.format(x[7]*162))


print('Printing Burke Ratings (ratings based on strength of schedule and any perceived home field advantage).')
for i, burke_value in enumerate(burkelist):
  print('The Burke rating of the '+id_to_mlbgames_name(i+1)+' is '+'{:.1f}'.format(burke_value[0]))

##################################
# WRITING TO TEMPORARY CSV FILES #
##################################

#write out burke vector
csvfile_out = open(wkdir+'burke_vector.csv','wb')
csvwriter = csv.writer(csvfile_out)
for row in burkelist:
    #Only need to print the visiting and home team scores and names.
    csvwriter.writerow(row)
csvfile_out.close()

vector_of_means=[[x[6]] for x in diff_list]
list_to_csv('run_diff_vector.csv',vector_of_means)
