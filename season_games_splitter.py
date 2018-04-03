"""
Season Games Splitter

This program splits the season into "games that have already been played"
and determines which games have already been won.

--MA Miller

"""


#Replace Excel Program with Python routine.
import sqlite3
import os,sys,time
from pprint import pprint
from datetime import datetime, timedelta
from mlb_data_models import Game
wkdir = os.path.dirname(os.path.realpath(__file__))+'/'

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

#Need to add 'and not postphoned'.
played_games=Game.select().where(Game.scheduled_date<datetime.today()-timedelta(days=1)).order_by(Game.scheduled_date) 
played_games=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in played_games]
pprint(played_games)

winlist=[x[0] if x[1]>x[3] else x[2] for x in played_games]

winrows=[]
for i in range(1,31):
    winrows.append([winlist.count(i)])

#Split data into games that have already occured and games that are to occur. Also grab a set of games
#for the model
futuredata=Game.select().where(Game.scheduled_date>=datetime.today()-timedelta(days=1)).order_by(Game.scheduled_date) 
futuredata=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in futuredata]
pastdata=Game.select().where(Game.scheduled_date<datetime.today()-timedelta(days=1)).order_by(Game.scheduled_date) 
pastdata=[[g.away_team,g.away_runs,g.home_team,g.home_runs] for g in pastdata]
print('Number of games to be played: '+str(len(futuredata)))
print('Number of games already played: '+str(len(pastdata)))

#Write out the results
list_to_csv(wkdir+'outfile_wins.csv',winrows)
list_to_csv(wkdir+'outfile_future_games.csv',futuredata)

