"""
Script that calculates Elo for the entire available NBA history,
ERASES THE PREVIOUS RESULTS, and stores the result the main SQLite database.

Inputs: 
    None explicit (parameters calculated from other scripts)
    
Outputs:
    None
    Prints summary of best and worst teams in each season
    Writes the results to database


"""
from mlb_database.queries import season_query, prettytime, team_abbreviation
from mlb_database.mlb_models import database, Games, MlbTeamEloData
from pprint import pprint
from math import exp
from random import randint
import numpy as np

# default rating is 0.01, multiplied by 10^6 for readability.
DEFAULT_RATING = 0.01


def predicted_rd_formula(a, b):
    """
    Parameters
    ----------
    a : Elo rating of team a
    b : Elo rating of team b.

    Returns
    -------
    DoS : difference over sum estimate

    Constants
    ---------
    mean and stddev taken from results of points_analysis.py

    """
    mean = 0.19020
    stddev = 2.3966
    DoS = -1 + 2 / (1 + exp((b - a - mean) / stddev))
    return DoS


def season_elo_calc(_analysis_list, previous_ratings=None, new_season=True):
    """
    Based on a series of games provided in
    [away id, away pts, home id, home pts]
    format, previous ratings (if applicable),
    and if a previous iteration is being used
    return both the final ratings and a continuous set of ratings
    for the entire season.

    Parameters
    ----------
    _analysis_list : TYPE
        DESCRIPTION.
    previous_ratings : TYPE, optional
        DESCRIPTION. The default is None.
    new_season : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    season_elo_ratings_list : TYPE
        DESCRIPTION.
    list_of_ratings : TYPE
        DESCRIPTION.

    """

    default_rating = DEFAULT_RATING  # 1 gives good results.
    rating_scaling = 1000  # 10 gives good spread x 100 for scoring diff
    
    default_K = default_rating / rating_scaling

    if new_season == True:
        season_elo_ratings_list = default_rating * np.ones((30, 1))
    else:
        season_elo_ratings_list = previous_ratings

    # create a list of ratings to return and store the first ratings set
    list_of_ratings = []
    initial_date = _analysis_list[0][4]  # first entry, first date
    year = analysis_list[0][5]
    for i, z in enumerate(season_elo_ratings_list):
        rd = {}  # ratings_dict
        rd["team_id"] = i + 1
        rd["team_abbreviation"] = team_abbreviation(rd["team_id"])
        rd["elo_rating"] = z[0] * 100000
        rd["datetime"] = initial_date
        rd["season_year"] = year
        list_of_ratings.append(rd)

    for g in _analysis_list:

        # get previous elo ratings
        away_rating = season_elo_ratings_list[g[0] - 1]
        home_rating = season_elo_ratings_list[g[2] - 1]
        # get expected DoS value, compare it to the real one
        expected_rd = predicted_rd_formula(away_rating, home_rating)
        actual_rd = g[1] - g[3]
        rd_difference = actual_rd - expected_rd
        # adjust ratings
        change_factor = default_K * rd_difference
        season_elo_ratings_list[g[0] - 1] = (
            season_elo_ratings_list[g[0] - 1] + change_factor
        )
        season_elo_ratings_list[g[2] - 1] = (
            season_elo_ratings_list[g[2] - 1] - change_factor
        )



        # add the date and then add the new ratings to the list of ratings
        cur_date = g[4]
        list_of_ratings.append(
            {
                "team_id": g[0],
                "elo_rating": season_elo_ratings_list[g[0] - 1][0] * 100000,
                "datetime": cur_date,
                "season_year": year,
                "team_abbreviation": team_abbreviation(g[0]),
            }
        )
        list_of_ratings.append(
            {
                "team_id": g[2],
                "elo_rating": season_elo_ratings_list[g[2] - 1][0] * 100000,
                "datetime": cur_date,
                "season_year": year,
                "team_abbreviation": team_abbreviation(g[2]),
            }
        )

    print(
        "Final set of Elo ratings after season "
        + str(year)
        + " presented below."
    )

    return season_elo_ratings_list, list_of_ratings


def year_to_year_ratings(
    season_elo_ratings_list, reset_factor=0.25, reset_value=DEFAULT_RATING
):
    """
    Take a set of ratings from the previous year,
    and based on a reset factor and a value to be
    reset to, adjust them for use in a new year.

    Note that rating is unscaled here.

    Parameters
    ----------
    season_elo_ratings_list : TYPE
        DESCRIPTION.
    reset_factor : TYPE, optional
        DESCRIPTION. The default is 0.25.
    reset_value : TYPE, optional
        DESCRIPTION. The default is the default rating.

    Returns
    -------
    new_ratings : TYPE
        DESCRIPTION.

    """
    previous_ratings = np.array(season_elo_ratings_list)
    # print(previous_ratings)
    new_ratings = previous_ratings * (
        1 - reset_factor
    ) + reset_factor * reset_value * np.ones((30, 1))
    new_ratings.tolist()
    new_ratings = [r for r in new_ratings]
    return new_ratings


def results_summary(season_elo_ratings_list, scaling=100000):
    """
    Based on a set of ratings (in team, rating, year format)
    print out the best and worst teams for that season.

    Parameters
    ----------
    season_elo_ratings_list : TYPE
        DESCRIPTION.
    scaling : TYPE, optional
        DESCRIPTION. The default is 100000.

    Returns
    -------
    None.

    """
    print_list = []

    for i, r in enumerate(season_elo_ratings_list):
        rtg = float(r[0] * scaling)
        team = team_abbreviation(i + 1)
        print_list.append([rtg, team])

    print_list = sorted(print_list, key=lambda x: -x[0])
    top_list = print_list[0:10]
    bottom_list = print_list[22:30]
    print("Top 10 teams for the season ending in " + str(year) + ":")
    for t in top_list:
        rating = "%.1f" % t[0]
        print(t[1] + ": " + rating)
    print("Bottom 10 teams for the season ending in " + str(year) + ":")
    for t in bottom_list:
        rating = "%.1f" % t[0]
        print(t[1] + ": " + rating)
    spread = print_list[0][0] - print_list[29][0]
    spread_string = "%.1f" % spread
    print("Max spread is: " + spread_string)

    return


if __name__ == "__main__":

    # x = Games.select().order_by(Games.year.asc()).get()
    # start_year = x.year
    # x = Games.select().order_by(Games.year.desc()).get()
    # end_year = x.year + 1
    start_year = 1977
    end_year = 2023


    # master_results - capture all ratings over all seasons.
    master_results = []

    reset_factor = 0.75  # 1: every season is new. #0: every season is a continuation
    reset_value = DEFAULT_RATING  # identical to default value
    for year in range(start_year, end_year):

        if year == start_year:
            analysis_list = season_query(year)
            season_elo_ratings_list, ratings = season_elo_calc(analysis_list)
            results_summary(season_elo_ratings_list)
        else:
            analysis_list = season_query(year)
            season_elo_ratings_list, ratings = season_elo_calc(
                analysis_list, season_elo_ratings_list, new_season=False
            )
            results_summary(season_elo_ratings_list)
        season_elo_ratings_list = year_to_year_ratings(
            season_elo_ratings_list, reset_factor=reset_factor, reset_value=reset_value
        )
        master_results.append(ratings)

    with database.atomic():
        MlbTeamEloData.delete().execute()  # clear previous table
        for dl in master_results:
            MlbTeamEloData.insert_many(dl).execute()
