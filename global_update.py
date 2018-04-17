"""
Gets data from the mlbgame api
and then updates the existing db entries

Need to doublecheck/tune algo
"""

from __future__ import print_function 
import mlbgame
from datetime import datetime, timedelta
from supports import teams_index_matcher
from mlb_data_models import Game, Team
from pprint import pprint
import sqlite3
import sys

max_days_back=int(sys.argv[1])

for i in range(1,max_days_back):
    game_d=datetime.today()-timedelta(days=i)

    print("Getting games from "+game_d.strftime("%Y-%m-%d"))

    month = mlbgame.games(game_d.year,game_d.month,game_d.day)
    games = mlbgame.combine_games(month)

    game_list=[]

    #Following segment is based on the solution
    #provided by Trevor V in the Github.
    #Tries to see if a game has data available, processes it.
    #If not, returns an error and the unique "mlbid" of the game
    #that has ostensibly been PPD.

    for game in games: 
        try: 
            stats = mlbgame.team_stats(game.game_id) 
            home_team = game.home_team 
            away_team = game.away_team 
            print('Processing {0} ({1}) at {2} ({3})'.\
                  format(away_team, stats.away_batting.r,\
                  home_team, stats.home_batting.r))
            game_dict={'mlbgame_away_team_name':away_team,\
                'away_runs':stats.away_batting.r,\
                    'mlbgame_home_team_name':home_team,\
                    'home_runs':stats.home_batting.r,\
                    'mlbgame_id_str':game.game_id,\
                    'scheduled_date':game_d.strftime('%Y-%m-%d')}
            game_list.append(game_dict)
        except ValueError:
            print('Unable to find data for game_id: {0}'.format(game.game_id))

    #adhoc team processing
    teams_index=Team.select(Team.id,Team.mlbgames_name).execute()
    teams_index=[{'team_id':t.id,'mlbgames_name':t.mlbgames_name} for t in teams_index]

    for g in game_list:
        g['away_team']=teams_index_matcher(teams_index,g['mlbgame_away_team_name'])
        g['home_team']=teams_index_matcher(teams_index,g['mlbgame_home_team_name'])

    print('Processing complete. Adding games into database')

    for g in game_list:
        game_scheduled_date=datetime.strptime(g['scheduled_date'],'%Y-%m-%d')
        Game.update(away_runs=g['away_runs'],home_runs=g['home_runs']).\
            where(Game.scheduled_date==game_scheduled_date,\
                    Game.is_postphoned==0,\
                    Game.away_team==g['away_team'],Game.home_team==g['home_team']).execute()
