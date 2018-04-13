"""
Full_Ratings_Calculations

This script calculates the run differentials, pythagorean win expectations, 
and Burke ratings for MLB teams over a given time period with a given 
maximum/minimum margin of victory and average home team advantage for use in the projections
scripts. 

"""
from __future__ import print_function, division

from pprint import pprint
import csv,os
import numpy as np
import tabulate
import json
from supports import id_to_mlbgames_name, list_to_csv
from mlb_data_models import Team, Game
from datetime import datetime, timedelta
from analytics.burke_solver import burke_calc
from collections import OrderedDict
from tabulate import tabulate
from datetime import datetime

#Define constant for pythagorean wins (the pythagorean win exponent)
pythag_factor=1.83
#Change added in order to make file compatible with the Interactive Shell
wkdir = os.path.join(os.path.dirname(__file__))

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
# Create a 30x11 vector: rows are teams, columns are:
#1. "WINS" - to be added
#2. "LOSSES" - to be added
#3. "RUNS SCORED"
#4. "RUNS ALLOWED"
#5. "GAMES PLAYED"
#6.  "AVERAGE RUNS SCORED"
#7. "AVERAGE RUNS ALLOWED"
#8. "AVERAGE RUN DIFFERENTIAL"
#9. "RUN DIFFERENTIAL"
#10. "PYTHAGOREAN_WINS"
#11. "ADJUSTED RATING"

analytics_headers=["Wins","Losses","Runs Scored","Runs Allowed","Games Scheduled",\
                   "Avg. Runs Scored","Avg. Runs Allowed",\
                   "Avg. Run Delta","Run Delta",\
                   "Pythag. Wins","Adj. Rtg."]

#then prepend the team names and division names to the list for sorting

diff_matrix=np.zeros((30,11))
for g in games:
    #two operations required, to increase the net wins and losses for both teams in 
    #each pass. Like if "away runs" greater than home runs then away team won. Advanced logic.
    if g[1]>g[3]:
        diff_matrix[g[0]-1,0]+=1
        diff_matrix[g[2]-1,1]+=1
    elif g[1]<g[3]:
        diff_matrix[g[2]-1,0]+=1
        diff_matrix[g[0]-1,1]+=1
    diff_matrix[g[0]-1,2]+=g[1]
    diff_matrix[g[0]-1,3]+=g[3]
    diff_matrix[g[0]-1,4]+=1
    #Home team.
    diff_matrix[g[2]-1,2]+=g[3]
    diff_matrix[g[2]-1,3]+=g[1]
    diff_matrix[g[2]-1,4]+=1

for i in range(0,len(diff_matrix)):
    diff_matrix[i,5]=diff_matrix[i,2]/diff_matrix[i,4]
    diff_matrix[i,6]=diff_matrix[i,3]/diff_matrix[i,4]
    diff_matrix[i,7]=diff_matrix[i,5]-diff_matrix[i,6]
    diff_matrix[i,8]=diff_matrix[i,7]*diff_matrix[i,4]
    diff_matrix[i,9]=162*diff_matrix[i,2]**pythag_factor/(diff_matrix[i,2]**pythag_factor+diff_matrix[i,3]**pythag_factor)

#Adjusted Rating Calculations (Burke - after Brian Burke - ratings)
burke_data=[[g[2],g[0],g[3],g[1]] for g in games]
burkelist=burke_calc(burke_data,impmode=None,max_MOV=max_MOV,home_team_adv=home_team_adv,win_floor=0.0)
burkelist=[[b] for b in burkelist]
diff_matrix[:,10]=[b[0] for b in burkelist]



diff_list=diff_matrix.tolist()
ratings_list=[]
for i in diff_list:
    ratings_list.append(dict(zip(analytics_headers,i)))

for i,x in enumerate(ratings_list):
    team_name_data=id_to_mlbgames_name(i+1,verbose=True)
    x_team_name=team_name_data[0]
    x_team_division=team_name_data[1]
    x['Team']=x_team_name
    x['Division']=x_team_division
    
ratings_list.sort(key=lambda x:(x['Division'],-x['Wins']))


for rating in ratings_list:
    rating['Wins']=int(rating['Wins'])
    rating['Losses']=int(rating['Losses'])
    rating['Games Scheduled']=int(rating['Games Scheduled'])

#################################
# Writing Out Ratings CSV Files #
#################################
list_to_csv('run_diff_vector.csv',vector_of_means)
list_to_csv('burke_vector.csv',burkelist)
###############################
# Writing the table to screen #
###############################

#Decide what we do want to publish:

table_list=[(i['Team'],i['Division'],i['Wins'],i['Losses'],i['Run Delta'],i['Pythag. Wins'],i['Adj. Rtg.']) for i in ratings_list]

pprint(table_list[0])

ratings_table=tabulate(table_list,headers=['Team','Division','Wins','Losses','Run Delta','Pythag. Wins','Adj. Rtg.'])

print(ratings_table)

#####################
# Print to Log File #
#####################

#Repeat commands above but write the information to a file.

file_out = open(wkdir+'Summary_'+analysis_end_date.strftime('%Y-%m-%d')+'.txt','wb')

file_out.write('Summary of Results, '+analysis_end_date.strftime('%Y-%m-%d')+'\n\n')

file_out.write(ratings_table)

file_out.close()

print("Writing to file completed successfully.")

