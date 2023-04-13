"""
TO BE EDITED:
 For parsing .csv files obtained from the Sports-Reference website.
 All data belongs to Sports Reference LLC themselves, an excellent site you 
 should consider supporting if you like this stuff.
 
"""
from pprint import pprint
import pandas as pd
from datetime import datetime

from mlb_database.mlb_models import Games, database
from mlb_database.queries import abbrev_to_id

SQLITE_MAX_VARIABLE_NUMBER = 100


start_year = 2023
end_year = 2022
season_dict_list=[]
for season_year_start in range(start_year,end_year,-1):

    df = pd.read_csv("data/"+str(season_year_start)+"Games.csv", thousands=',')
    df = df.rename(columns={"R":"HomeTeamRuns","RA":"AwayTeamRuns","Unnamed: 2":"dummy"})
    df = df.drop(columns=["Gm#","dummy"])
    # Convert date into standard date object
    df["Date"] = df["Date"].astype(str)
    df["Date"] = df["Date"].map(lambda x: str(x)[:-1])
    df["Date"] = pd.to_datetime(df["Date"],format='%Y%m%d', errors='ignore')
    #Create the epochtime and then convert the date
    df["epochtime"] = df["Date"].astype('int64')//1e9
    df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    #Create unique index
    df["id"] = df["Index"]+df["year"]*10000
    df["away_team_id"] = df["AwayTeam"].apply(lambda x: abbrev_to_id(x))
    df["home_team_id"] = df["HomeTeam"].apply(lambda x: abbrev_to_id(x))
    #Renamings to match peewee
    df["home_team"]=df["HomeTeam"]
    df["away_team"]=df["AwayTeam"]
    df["home_team_runs"]=df["HomeTeamRuns"]
    df["away_team_runs"]=df["AwayTeamRuns"]
    df["home_wl"]=df["HomeWL"]
    df["inn"]=df["Inn"]
    df["gb"]=df["GB"]
    df["win"]=df["Win"]
    df["loss"]=df["Loss"]
    df["save"]=df["Save"]
    df["time"]=df["Time"]
    df["attendance"]=df["Attendance"]
    df["c_li"]=df["cLI"]
    df["home_streak"]=df["HomeStreak"]
    df["home_game"]=df["HomeGame"]
    df["team_rank"]=df["Rank"]
    df["game_date"]=df["Date"]
    df["w_l"]=df["W/L"]
    df["d_n"]=df["D/N"]
    df["orig_scheduled"]=df["Orig. Scheduled"]
    df= df.drop(columns=["Index","W/L","D/N","Rank","Date","Orig. Scheduled",\
                         "HomeTeam","AwayTeam","HomeTeamRuns","AwayTeamRuns",\
                             "Inn","HomeWL","GB","Win","Loss","Save","Time",\
                                 "Attendance","cLI","HomeStreak","HomeGame"])
        
    season_dicts = df.T.to_dict()
    types = [type(z) for z in season_dicts[0].values()]
    
    # For deleting current year data
    # print("Number of entries: "+str(len(season_dicts)))
    # print("Preparing to delete entries.")
    # q = BballrefScores.delete().where(BballrefScores.id > 20210000)
    # q.execute()
    # print("Entries cleared, restoring entries.")
    
    
    for key,value in season_dicts.items():
        season_dict_list.append(value)
    
    print("Year "+str(season_year_start)+" is now complete")
    
    #Games.insert_many(season_dict_list).on_conflict_replace().execute()
    
with database.atomic() as txn:
    size = (SQLITE_MAX_VARIABLE_NUMBER // len(season_dict_list[0])) - 1
    # remove one to avoid issue if peewee adds some variable
    for i in range(0, len(season_dict_list), size):
        Games.insert_many(
            season_dict_list[i : i + size]
        ).on_conflict_replace().execute()

#For games not yet played, set home runs and away runs equal to 0
Games.update(away_team_runs=0).where(Games.home_team_runs=="Game Preview, and Matchups").execute()
Games.update(home_team_runs=0).where(Games.home_team_runs=="Game Preview, and Matchups").execute()
