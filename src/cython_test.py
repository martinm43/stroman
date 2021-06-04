"""
Endfile for testing integration with the mcss.cpp shared library
Using the python library developed using C++ to rapidly speed up how standings are printed and presented
and allow for integration with more 'modern' interfaces -think flask or Django

"""

# Future import first

from predict.cython_mcss.mcss_ext2 import simulations_result_vectorized
from mlb_database.mlb_models import Teams
from mlb_database.queries import elo_ratings_list, epochtime
from datetime import datetime, timedelta

from pprint import pprint


def playoff_odds_calc(start_datetime, end_datetime, season_year, ratings_mode="Elo"):
    """

    Given a start, end, season_year, and a ratings calculation method
    with some other factors, determine the odds of every team of making
    the playoffs at any given time.

    Parameters
    ----------
    start_datetime : start of period to be used for analysis (Unix timestamp)
    end_datetime : end of period to be used for analysis (Unix timestamp)
    season_year : year that season nominally ends in
                (e.g. if season ends in 2021, use 2021)
    ratings_mode : Elo or SRS. Default mode is Elo.

    Returns
    -------
    a list of 2-item lists for each team (first item ATL, last item WAS)
    each list consists of [playoff odds,average wins]

    """

    #from predict.cython_mcss.mcss_ext2 import simulations_result_vectorized
    from analytics.SRS import SRS
    from analytics.morey import SRS_regress, Elo_regress

    from mlb_database.queries import games_query, games_won_query, future_games_query

    # Test results/inputs
    if end_datetime < start_datetime:
        print("Start date is after end date, please check inputs")
        return 1

    predict_date = end_datetime
    predict_season_year = season_year

    # Get List Of Known Wins
    games_list = games_query(start_datetime, end_datetime)
    games_won_list_cpp = games_won_query(games_list, return_format="matrix").tolist()

    # Get team data.
    teams_list = Teams.select().order_by(Teams.team_id)
    teams_list = [
        [x.team_id, x.team_name, x.abbreviation, x.division, x.league]
        for x in teams_list
    ]

    # Team Name/Division Fixes
    for x in teams_list:
        if x[0] == 13 and season_year <= 2012: #Houston
            x[4] = "NL"
            x[3] = "NL Central"
            
        if x[0] == 16 and season_year <= 1997: #Milwaukee
            x[4] = "AL"
            x[3] = "AL Central"
        
        if x[0] == 11 and season_year <= 1997: #Detroit
            x[3] = "AL East"
        
        if x[0] == 30 and season_year <= 2004: #The Expos should never have left
            x[1] = "Montreal Expos"
            x[2] = "MON"

        if season_year <= 1993:
            if x[0] in [9,11,16]: #to AL East
                x[3] = "AL East"
            if x[0] in [7,14,17]: #to AL West
                x[3] = "AL West"
            if x[0] in [26,6,22]: #to NL East
                x[3] = "NL East"
            if x[0] in [13,8,3]: #to NL West
                x[3] = "NL West"    


    #pprint(teams_list)

    # Get future games (away_team, home_team, home_team_win_probability)

    future_games_list = future_games_query(predict_date, predict_season_year)

    if ratings_mode == "SRS":
        # Get Team Ratings (and create Team object list)
        ratings_list = SRS(
            games_query(start_datetime, end_datetime)
        ).tolist()  # get ratings for that time.

        for i, x in enumerate(teams_list):
            x.append(ratings_list[i])
            for j in range(1, 5):  # "all strings"
                x[j] = x[j].encode("utf-8")

        for x in future_games_list:
            away_team_rating = teams_list[x[0] - 1][5]
            home_team_rating = teams_list[x[1] - 1][5]
            SRS_diff = home_team_rating - away_team_rating
            x.append(SRS_regress(SRS_diff))

    if ratings_mode == "Elo":
        ratings_list = elo_ratings_list(epochtime(end_datetime))
        for i, x in enumerate(teams_list):
            x.append(ratings_list[i])
            for j in range(1, 5):  # "all strings"
                x[j] = x[j].encode("utf-8")

        for x in future_games_list:
            away_team_rating = teams_list[x[0] - 1][5]
            home_team_rating = teams_list[x[1] - 1][5]
            Elo_diff = home_team_rating - away_team_rating
            x.append(Elo_regress(Elo_diff))

    print(type(games_won_list_cpp))
    print(type(future_games_list))

    #team_results = simulations_result_vectorized(games_won_list_cpp, future_games_list, teams_list,season_year)
    team_results = simulations_result_vectorized(season_year)
    # Return (top 8 odds, average wins, top 6 odds, and play in tournament odds).
    # team_results = [
    #     [x[0] * 100.0, x[1], x[2] * 100.0, x[3] * 100.0, 100.0*(x[0]+x[2]+x[3])] for x in team_results
    # ]
    return team_results #team_results


if __name__ == "__main__":

    from random import randint
    season_year = randint(1977,2020)  # year in which season ends
    print("Testing year: "+str(season_year))
    start_datetime = datetime(season_year, 3, 22)  # start of season
    end_datetime = datetime(season_year,8,1) # a few weeks or months in
    # in-season option: end_datetime = datetime.today()-timedelta(days=1)

    ratings_mode = "SRS"
    results = playoff_odds_calc(
        start_datetime, end_datetime, season_year, ratings_mode=ratings_mode)
    print(results)
