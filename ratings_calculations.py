"""
Ratings_Calculations

This script calculates the Burke ratings for MLB teams over a given time period with a given 
maximum/minimum margin of victory and average home team advantage for use in the projections
scripts. 

Automation requirements

Human input: Automatic input

End date for analysis: current date
Maximum margin of victory: 15
Average home court advantage: 2

"""

import csv,os
import time
from supports import id_to_mlbgames_name
from mlb_data_models import Team, Game
import sqlite3
from datetime import datetime, timedelta

wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

#Handling Burke solver's dependence on scipy.
burke_solve=0
from analytics.burke_solver import burke_calc
try:
    import scipy.optimize
    from analytics.burke_solver import burke_calc
    burke_solve=1
except ImportError:
    print('Burke solution method not available')

srsdata=[]

filename='MLB_data.sqlite'
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()



###END OF V2.0 EDITS ###################################################

if burke_solve==1:
    #Calculate Burke SRS
    
    #New automated code.
    analysis_start_date=datetime.now()-timedelta(weeks=4) #N weeks*days*seconds
    analysis_end_date=datetime.now()
    max_MOV=100.0 #quick fix.
    home_team_adv=0.0

#    nba_api_srsdata_query_str='SELECT away_team_id, away_PTS, home_team_id, home_PTS\
#                             from bballref_scores WHERE datetime >= '+str(analysis_start_date)+' AND datetime <= '+str(analysis_end_date)+' AND \
#                             away_pts>0'
#    nba_api_srsdata=c.execute(nba_api_srsdata_query_str).fetchall()
#    srsdata=nba_api_srsdata
#    burke_data=[[s[2],s[0],s[3],s[1]] for s in srsdata if s[1] is not None]

    games=Game.select().where(Game.scheduled_date>=analysis_start_date,Game.scheduled_date<=analysis_end_date-timedelta(days=1))
    games=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in games]
    burke_data=[[g[2],g[0],g[3],g[1]] for g in games]

    burkelist=burke_calc(burke_data,impmode=None,max_MOV=max_MOV,home_team_adv=home_team_adv,win_floor=0.0)
    burkelist=[[b] for b in burkelist]
else:
    burkelist=None
#Debug
print('Printing Burke Ratings (ratings based on strength of schedule and any perceived home field advantage).')
if burkelist!=None:
  for i, burke_value in enumerate(burkelist):
      print('The Burke rating of the '+id_to_mlbgames_name(i+1)+' is '+str(burke_value[0]))
else:
  print('Burke calculations not performed, skipping')

if burke_solve==1:
    #write out burke vector
    csvfile_out = open(wkdir+'burke_vector.csv','wb')
    csvwriter = csv.writer(csvfile_out)
    for row in burkelist:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()


#### Close connection ####
conn.close()
