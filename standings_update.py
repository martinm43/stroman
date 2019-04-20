"""
Gets data from the mlbgame api
and then updates the existing db entries

Need to doublecheck/tune algo
"""



import sys
from datetime import datetime, timedelta

import mlbgame
from supports import teams_index_matcher
from mlb_data_models import Game, Team
from pprint import pprint

start_date = datetime(2012,3,28) #start date (sometime in March)
end_date = datetime(2012,10,28) #end date (end of season typically oct 1)

game_d = start_date

while game_d <= end_date:

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

    for g in game_list:
        game_scheduled_date = datetime.strptime(
            g['scheduled_date'], '%Y-%m-%d')
        game_season_year = game_scheduled_date.year
        #Code to determine if the data entered already exists in database and 
        #not duplicate it
        existing_query = Game.select().where(Game.away_team == g['away_team'],
                            Game.home_team == g['home_team'],
                            Game.scheduled_date == game_scheduled_date,
                            Game.away_runs == g['away_runs'],
                            Game.home_runs == g['home_runs'])
        existing_query_results_sample = [g for g in existing_query]
        #print(len(existing_query_results_sample)) - debug print
        if len(existing_query_results_sample) > 0: #entry already exists
            print('Entry for '+g['mlbgame_away_team_name']+\
                    ' at '+g['mlbgame_home_team_name']+' on '+\
                    g['scheduled_date']+' exists in database, updating entry')
            Game.update(
                away_runs=g['away_runs'],
                home_runs=g['home_runs']).where(
                    Game.scheduled_date == game_scheduled_date,
                    Game.is_postphoned == 0,
                Game.away_team == g['away_team'],
                Game.home_team == g['home_team']).execute() 
        else:
            Game.replace(
                away_runs = g['away_runs'],
                home_runs = g['home_runs'],
                scheduled_date = game_scheduled_date,
                away_team = g['away_team'],
                away_team_name = g['mlbgame_away_team_name'],
                home_team = g['home_team'],
                home_team_name = g['mlbgame_home_team_name'],
                season_year = game_season_year).execute() 

        # "replace" is the upsert functionality of peewee  

    game_d = game_d + timedelta(days=1)
