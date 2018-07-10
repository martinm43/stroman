"""
These scripts are functions commonly reused in other files.
"""
from __future__ import division, print_function

from datetime import datetime, timedelta
import random

import numpy as np

from pprint import pprint

from james import SRS_regress
from mlb_data_models import Team, Game, SRSRating, database

def big_inserter(
        db,
        SQLITE_MAX_VARIABLE_NUMBER,
        PeeweeClassObject,
        list_of_dicts):
    """
    Inserts a long list of dicts into the main matrix
    """
    with db.atomic() as txn: #pylint:disable=W0612
        size = (SQLITE_MAX_VARIABLE_NUMBER // len(list_of_dicts[0])) - 1
        # remove one to avoid issue if peewee adds some variable
        for i in range(0, len(list_of_dicts), size):
            PeeweeClassObject.insert_many(
                list_of_dicts[i:i + size]).upsert().execute()
        return

def teams_index_matcher(teams_index, namestr):
    """
    Returns the mlbgames name from a dict into a numerical id
    """
    team_ind = [t['team_id']
                for t in teams_index if t['mlbgames_name'] == namestr][0]
    return team_ind


def abbrev_to_id(abbrev):
    """
    Converts team abbreviations into numerical ids
    """
    x = Team.select().where(Team.abbreviation == abbrev)
    return [i.id for i in x][0]


def mlbgames_name_to_id(mlbgames_name):
    """
    Converts the mlbgames name into a numerical id (starts at 1)
    """
    x = Team.select().where(Team.mlbgames_name == mlbgames_name)
   # print(x)
    return [i.id for i in x][0]


def dict_search(list_of_dicts, key1, key_value1, key2):
    """
    Searches for a value in a dict and returns the other value
    e.g. search for team_id=1 and return team_name=Angels
    """
    x = [i for i in list_of_dicts if i[key1] == key_value1]
    if x == []:
        print('Value not found, check input')
        return_value = x
    else:
        return_value = x[0][key2]
    return return_value


def list_to_csv(csvfile, list_of_lists):
    """
    Converts a list into a csv file.
    """
    import csv
    csvfile_out = open(csvfile, 'wb')
    csvwriter = csv.writer(csvfile_out)
    for row in list_of_lists:
        # Only need to print the visiting and home team scores and names.
        csvwriter.writerow(row)
    csvfile_out.close()
    return 1


def id_to_mlbgames_name(team_id, verbose=False):
    """
    Converts numerical id to the name used by mlbgames API
    """
    t = Team.select().where(Team.id == team_id)
    if not verbose:
        t = [x.mlbgames_name for x in t][0]
    else:
        t = [[x.mlbgames_name, x.division] for x in t][0]
    return t

def games_won_to_date():

    start_datetime = datetime(2018,03,15)
    end_datetime = datetime.today() - timedelta(days=1)
    games_query_result = games_query(start_datetime,end_datetime)
    return games_query_result



def games_query(start_datetime,end_datetime,return_format="list"):
    """
    Returns the number of games won to date in either a straight
    numerical list, a list of dicts, or a head to head matrix
    """
    played_games = Game.select().where(
        Game.scheduled_date < end_datetime,
        Game.scheduled_date > start_datetime).order_by(Game.scheduled_date)

    played_games = [[g.away_team, g.away_runs, g.home_team, g.home_runs]
                    for g in played_games]
    winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
    winrows = []
    if return_format == 'list_of_lists':
        winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
        winrows = []
        for i in range(1, 31):
            winrows.append([winlist.count(i)])
        return_value = winrows
    elif return_format == 'list':
        winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
        winrows = []
        for i in range(1, 31):
            winrows.append(winlist.count(i))
        return_value = winrows
    elif return_format == 'matrix':
        win_matrix = np.zeros((30, 30))
        for x in played_games:
            if x[1] > x[3]:
                win_matrix[x[0] - 1, x[2] - 1] += 1
            elif x[3] > x[1]:
                win_matrix[x[2] - 1, x[0] - 1] += 1
        return win_matrix
    else:
        print('invalid option')
        return_value = 0
    return return_value

def future_games_dicts():
    """
    Returns a list of dicts of future games (used in all the mcss files)
    """

    # dummy variable to represent the query (retrieve ratings for current day)
    #x = SRSRating.select().where(
    #    SRSRating.rating_date == datetime.now(). replace(
    #        hour=0, minute=0, second=0, microsecond=0)).order_by(
    #            SRSRating.team_id)
    #
    # retrieve ratings for current day

    query_result = database.execute_sql("select t.id, s.rating from teams as t \
                             inner join SRS_Ratings as s \
                             on s.team_id=t.id \
                             where s.rating <> 0 and s.rating_date = (\
                                    select rating_date from SRS_ratings order by rating_date desc limit 1 ) \
                             order by t.id asc;")

    # Ported from old "standings_calculations" file
    ratings_dict_list = [{'abbreviation': 'Ana'},
                         {'abbreviation': 'Ari'},
                         {'abbreviation': 'Atl'},
                         {'abbreviation': 'Bal'},
                         {'abbreviation': 'Bos'},
                         {'abbreviation': 'ChC'},
                         {'abbreviation': 'ChW'},
                         {'abbreviation': 'Cin'},
                         {'abbreviation': 'Cle'},
                         {'abbreviation': 'Col'},
                         {'abbreviation': 'Det'},
                         {'abbreviation': 'Fla'},
                         {'abbreviation': 'Hou'},
                         {'abbreviation': 'Kan'},
                         {'abbreviation': 'Los'},
                         {'abbreviation': 'Mil'},
                         {'abbreviation': 'Min'},
                         {'abbreviation': 'NYM'},
                         {'abbreviation': 'NYY'},
                         {'abbreviation': 'Oak'},
                         {'abbreviation': 'Phi'},
                         {'abbreviation': 'Pit'},
                         {'abbreviation': 'Sdg'},
                         {'abbreviation': 'Sea'},
                         {'abbreviation': 'Sfo'},
                         {'abbreviation': 'StL'},
                         {'abbreviation': 'Tam'},
                         {'abbreviation': 'Tex'},
                         {'abbreviation': 'Tor'},
                         {'abbreviation': 'Was'}]


    x=[] #get empty list
    for t_id, t_rating in query_result:
        x_dict={}
        x_dict['team_id'] = t_id
        x_dict['rating'] = t_rating
        x.append(x_dict)


    #x dict {'team_id':,'rating':}
    ratings_dict_list=x

    # pprint(ratings_dict_list)

    # Get the list of games.
    query = Game.select().where(Game.scheduled_date >= datetime.now())
    game_dict_list = [dict(zip(['id', 'scheduled_date', 'away_team', 'home_team'], [
        i.id, i.scheduled_date, i.away_team, i.home_team])) for i in query]

    # Build a function of a function (I think decorators do this) - research
    # later.
    def get_rating(_ratings, team_id):
        """
        Specific search of a list of dictionaries for their
        team rating from the team id
        """
        return dict_search(_ratings, 'team_id', team_id, 'rating')

    regression_function = SRS_regress

    # monte_carlo_calculation component
    for x in game_dict_list:
        x['differential'] = get_rating(ratings_dict_list, x['home_team'])\
            - get_rating(ratings_dict_list, x['away_team'])
        x['home_win_probability'] = regression_function(x['differential'])

    return game_dict_list


def mcss(game_dict_list):
    """Function takes in a list of dicts of games with the home team's win probability"""
    win_matrix = np.zeros((30, 30))
    for x in game_dict_list:
        if x['home_win_probability'] <= random.uniform(0, 1):
            win_matrix[x['home_team'] - 1, x['away_team'] - 1] += 1
        else:
            win_matrix[x['away_team'] - 1, x['home_team'] - 1] += 1
    return win_matrix

def future_games_list():
    # return away, home, odds (diff is home - away)
    dict_list = future_games_dicts()
    fg_list=[]
    for d in dict_list:
        fg=[]
        fg.append(d['away_team'])
        fg.append(d['home_team'])
        fg.append(d['home_win_probability'])
        fg_list.append(fg)
    return fg_list

if __name__ == '__main__':
    print('1')
    pprint(future_games_dicts())
