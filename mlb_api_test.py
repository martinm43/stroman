"""
Testing the MLB Gameday API from Python
for the purposes of importing daily gameplay data 
for personal use.
"""
#imports
import mlbgame

#test constants
game_year=2017
game_month=9
game_day=1

day = mlbgame.games(game_year, game_month, game_day)
games = mlbgame.combine_games(day)
print(dir(games[0]))
game_id=games[0].game_id
print(game_id)
game_away_team=games[0].away_team
game_home_team=games[0].home_team
game_away_runs=games[0].away_team_runs
game_home_runs=games[0].home_team_runs
