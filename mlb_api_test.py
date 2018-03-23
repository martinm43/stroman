from __future__ import print_function 
import mlbgame
from datetime import datetime, timedelta

game_d=datetime.today()-timedelta(days=1)

print("Getting games from "+game_d.strftime("%Y %m %d"))

month = mlbgame.games(game_d.year,game_d.month,game_d.day)
games = mlbgame.combine_games(month)
for game in games: 
    print(game)
