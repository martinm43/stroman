#Updating the SQL Server, using upsert functionality taken from:
#https://stackoverflow.com/questions/43899189/access-database-upsert-with-pyodbc
#Obtain the data required.


import sys
import pyodbc
from datetime import datetime, timedelta
import mlbgame
from supports import teams_index_matcher
from pprint import pprint
from mlb_data_models import Game, Team

try:
    MAX_DAYS_BACK = int(sys.argv[1])
except IndexError:
    print('Insufficient variables provided, assuming number of days is 1')
    MAX_DAYS_BACK = 1

#Connect to the server.
cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                      "Server=Owner-PC;"
                      "Database=MS_mlb_data;"
                      "Trusted_Connection=yes;")

crsr = cnxn.cursor()

for i in range(1, MAX_DAYS_BACK+1):
    game_d = datetime.today() - timedelta(days=i)

    print("Getting games from " + game_d.strftime("%Y-%m-%d"))

    month = mlbgame.games(game_d.year, game_d.month, game_d.day)
    games = mlbgame.combine_games(month)

    game_list = []

    # Following segment is based on the solution
    # provided by Trevor V in the Github.
    # Tries to see if a game has data available, processes it.
    # If not, returns an error and the unique "mlbid" of the game
    # that has ostensibly been PPD.

    for game in games:
        try:
            stats = mlbgame.team_stats(game.game_id)
            home_team = game.home_team
            away_team = game.away_team
            print('Processing {0} ({1}) at {2} ({3})'.
                  format(away_team, stats.away_batting.r, #pylint:disable=no-member
                         home_team, stats.home_batting.r)) #pylint:disable=no-member
            game_dict = {'mlbgame_away_team_name': away_team,
                         'away_runs': stats.away_batting.r, #pylint:disable=no-member
                         'mlbgame_home_team_name': home_team,
                         'home_runs': stats.home_batting.r, #pylint:disable=no-member
                         'mlbgame_id_str': game.game_id,
                         'scheduled_date': game_d.strftime('%Y-%m-%d')}
            game_list.append(game_dict)
        except ValueError:
            print('Unable to find data for game_id: {0}'.format(game.game_id))

    # adhoc team processing
    teams_index = Team.select(Team.id, Team.mlbgames_name).execute() #pylint:disable=no-value-for-parameter
    teams_index = [{'team_id': t.id, 'mlbgames_name': t.mlbgames_name}
                   for t in teams_index]

    for g in game_list:
        g['away_team'] = teams_index_matcher(
            teams_index, g['mlbgame_away_team_name'])
        g['home_team'] = teams_index_matcher(
            teams_index, g['mlbgame_home_team_name'])

    print('Processing complete. Adding games into database')

#Begin UPDATE OR INSERT process with the data obtained.

    for g in game_list:

        away_runs=g['away_runs']
        home_runs=g['home_runs']
        scheduled_date=g['scheduled_date']
        away_team=g['away_team']
        home_team=g['home_team']
        #Update type statement.
        sql_update = "UPDATE [games] SET away_runs = " + str(away_runs) +","\
                             "home_runs = " + str(home_runs) +\
                             " WHERE scheduled_date = '"+ str(scheduled_date) +"'"+\
                             " AND away_team = " + str(away_team) +\
                             " and home_team = " + str(home_team)

        print(sql_update)
  
        crsr.execute(sql_update)
        crsr.commit() 

print("Update complete!")