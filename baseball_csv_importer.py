"""
TO BE EDITED:
 For parsing .csv files obtained from the Sports-Reference website.
 All data belongs to Sports Reference LLC themselves, an excellent site you 
 should consider supporting if you like this stuff.
 
"""
from pprint import pprint
import pandas as pd
from datetime import datetime

from mlb_models import Games, database

SQLITE_MAX_VARIABLE_NUMBER = 100

for season_year_start in range(1977,1976,-1):

    df = pd.read_csv("data/"+str(season_year_start)+"Games.csv")
    df = df.rename(columns={"R":"HomeTeamRuns","RA":"AwayTeamRuns","Unnamed: 2":"dummy"})
    df = df.drop(columns=["Gm#","dummy"])
    # Convert date into standard date object
    df["Date"] = df["Date"].astype(str)
    df["Date"] = df["Date"].map(lambda x: str(x)[:-1])
    df["Date"] = pd.to_datetime(df["Date"],format='%Y%m%d', errors='ignore')
    df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d"))
    #Create unique index
    df["id"] = df["Index"]+df["year"]*10000
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
    
    season_dict_list=[]
    for key,value in season_dicts.items():
        season_dict_list.append(value)
    
    print("Sample dict to be entered:")
    pprint(season_dict_list[0])
    
    #Games.insert_many(season_dict_list).on_conflict_replace().execute()
    
    with database.atomic() as txn:
        size = (SQLITE_MAX_VARIABLE_NUMBER // len(season_dict_list[0])) - 1
        # remove one to avoid issue if peewee adds some variable
        for i in range(0, len(season_dict_list), size):
            Games.insert_many(
                season_dict_list[i : i + size]
            ).on_conflict_replace().execute()
