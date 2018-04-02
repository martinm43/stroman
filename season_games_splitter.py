"""
Season Games Splitter

This program splits the season into "games that have already been played"
and determines which games have already been won.

Automatic mode is triggered by adding "AUTO" to the script invocation.
In automatic mode, the current season is cut based on the current date 
(Not yet implemented.)

--MA Miller

"""


#Replace Excel Program with Python routine.
import sqlite3
import os,sys,time
from pprint import pprint
#get the conversion function
from datetime import datetime
from dbtools.access_nba_data import epochtime,current_season
from mlb_data_models import Game, Team

#CSV output function
#Part Two: Write out a file containing all games played
def list_to_csv(csvfile,list_of_lists):
    import csv
    csvfile_out = open(csvfile,'wb')
    csvwriter = csv.writer(csvfile_out)
    for row in list_of_lists:
        #Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()
    return 1

#New automated options - brief concept test
season=str(current_season())
cutdate=time.time()

#strings for getting to file locations 
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'
filename='mlb_data.sqlite'

#ISSUE: This is a poor solution to "trying to determine the start date of a season"
#that requires fixing.
season_start=epochtime('Mar 1 '+season)-31536000

#create ballrows list of tuples (all games) using the database
conn=sqlite3.connect(wkdir+filename)
c=conn.cursor()
str_input='select id, scheduled_date, away_team,away_runs,home_team,home_runs \
          from games order by scheduled_date asc'
ballrows=c.execute(str_input).fetchall()

#Dec 29 2016 edit: Obtain an up-to-date list of wins from the nba_py_api_data database
c=conn.cursor()
gameslist=Game.select().where(Game.scheduled_date<datetime.now())
gameslist=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in gameslist]
print(len(gameslist))
pprint(gameslist)
#Hardcoded solution to "incorporating past wins while projecting into the future" problem
winlist=[x[0] if x[1]>x[3] else x[2] for x in gameslist]

winrows=[]
for i in range(1,31):
    winrows.append([winlist.count(i)])

#Split data into games that have already occured and games that are to occur. Also grab a set of games
#for the model
futuredata=[row for row in ballrows if datetime.strptime(row[1][0:10],'%Y-%m-%d')>=datetime.now()]
pastdata=[row for row in ballrows if datetime.strptime(row[1][0:10],'%Y-%m-%d')<datetime.now()]
print('Number of games to be played: '+str(len(futuredata)))
print('Number of games already played: '+str(len(pastdata)))

#Write out the results
list_to_csv(wkdir+'outfile_wins.csv',winrows)
list_to_csv(wkdir+'outfile_future_games.csv',futuredata)

