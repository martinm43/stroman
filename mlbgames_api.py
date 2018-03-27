from __future__ import print_function 
import mlbgame
from datetime import datetime, timedelta
from mlb_data_models import Game
from pprint import pprint

game_d=datetime.today()-timedelta(days=1)

print("Getting games from "+game_d.strftime("%Y-%m-%d"))

month = mlbgame.games(game_d.year,game_d.month,game_d.day)
games = mlbgame.combine_games(month)

#Does not work for spring training games. Should test
#on March 28.
#for g in games: 
#    pprint([g.away_team,g.away_team_runs,\
#            g.home_team,g.home_team_runs])

#print('Game properties')
#print(dir(games[0]))

game_list=[]

print('Attempting to use the solution to the issue on SO provided by Trevor V')

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
              'mlbgame_id_str':game.game_id}
        #pprint(game_dict)
        game_list.append(game_dict)
    except ValueError:
        print('Unable to find data for game_id: {0}'.format(game.game_id))

print('Processing complete. Adding games into database')
Game.insert_many(game_list).upsert().execute()
