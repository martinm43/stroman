# -*-coding:utf8;-*-
# qpy:2
# qpy:console

# Choose working directory.
from .mlb_models import Games
import time, datetime
import numpy as np

###################
# Time Conversion #
###################


def epochtime(datetime_obj):
    """
    Convert time in MON DAY YEAR format to a UNIX timestamp

    Input: datetime object (datetime.datetime)
    Output: Unix timestamp
    """
    return time.mktime(datetime_obj.timetuple())


def prettytime(timestamp):
    """
    Convert time since epoch to date
    Input: Unix timestamps
    Output: a datetime object (datetime.datetime)
    """
    return datetime.datetime.fromtimestamp(timestamp)


#####################
# String Conversion #
#####################


def team_abbreviation(team_alphabetical_id):
    """
    Converts team numerical ids into team names.
    """
    from .mlb_models import Teams
    #print(team_alphabetical_id)
    s_query = Teams.select(Teams.abbreviation).where(
        Teams.team_id == team_alphabetical_id
    )
    s_result = s_query[0]
    return s_result.abbreviation


# def full_name_to_id(full_team_name):
#     """
#     Converts 'normal team names', provides the rest of the data needed for processing
#     Team id

#     Input: a string representing the team's name
#     Output: a team id - 
#     """
#     # Adjusting for previous team names/previous team locations.
#     # if full_team_name == "New Jersey Nets":
#     #     full_team_name = "Brooklyn Nets"
#     # if full_team_name == "Seattle SuperSonics":
#     #     full_team_name = "Oklahoma City Thunder"
#     # if full_team_name == "Washington Bullets":
#     #     full_team_name = "Washington Wizards"
#     # if full_team_name == "Vancouver Grizzlies":
#     #     full_team_name = "Memphis Grizzlies"

#     from .nba_data_models import ProApiTeams

#     s_query = ProApiTeams.select(ProApiTeams.bball_ref).where(
#         ProApiTeams.full_team_name == full_team_name
#     )

#     s_result = s_query[0]
#     return s_result.bball_ref


def abbrev_to_id(team_abbrev):
    """
    Converts 'normal team names', provides the rest of the data needed for processing
    Team id
    Input: team abbreviation e.g. "ARI"
    Output: numerical id e.g. "1"
    """
    from .mlb_models import Teams
    #print(team_abbrev)
    
    if team_abbrev == "FLA":
        team_abbrev = "MIA"
    if team_abbrev == "TBD":
        team_abbrev = "TBR"
    if team_abbrev == "ANA" or team_abbrev == "CAL":
        team_abbrev = "LAA"
    if team_abbrev == "MON":
        team_abbrev = "WSN"
    s_query = Teams.select(Teams.team_id).where(
        Teams.abbreviation == team_abbrev
    )
    s_result = s_query[0]
    return s_result.team_id


# def id_to_name(team_id):
#     """
#     Converts a team id to a full team name.
#     Input: team id e.g. "30"
#     Output: team name e.g. "Washington Wizards"
#     """
#     from .nba_data_models import ProApiTeams

#     s_query = ProApiTeams.select(ProApiTeams.team_name).where(
#         ProApiTeams.bball_ref == team_id
#     )
#     s_result = s_query[0]
#     return s_result.team_name


# ################################
# # Getting Information On Games #
# ################################


def games_query(start_datetime, end_datetime):
    """
    Input: datetime objects
    Output: [away_team, away_team_runs, home_team, home_team_runs] list
    """
    start_epochtime = epochtime(start_datetime)
    end_epochtime = epochtime(end_datetime)
    played_games = (
        Games.select()
        .where(
            Games.epochtime < end_epochtime,
            Games.epochtime > start_epochtime,
            ((Games.away_team_runs > 0)|(Games.home_team_runs > 0)),
        )
        .order_by(Games.epochtime)
    )

    played_games = [
        [g.away_team_id, g.away_team_runs, g.home_team_id, g.home_team_runs] for g in played_games
    ]
    return played_games


def season_query(season_year):
    """
    Input: a season year
    Output: [away_team, away_team_runs, home_team, home_team_runs, epochtime, season_year] list
    """

    played_games = (
        Games.select()
        .where(Games.year == season_year, ((Games.away_team_runs > 0)|(Games.home_team_runs > 0)))
        .order_by(Games.epochtime)
    )

    played_games = [
        [
            g.away_team_id,
            g.away_team_runs,
            g.home_team_id,
            g.home_team_runs,
            g.epochtime,
            season_year,
        ]
        for g in played_games
    ]

    return played_games


def games_won_query(played_games, return_format="list"):
    """
    Input: [away_team, away_team_runs, home_team, home_team_runs] list
    Output: a list of lists, a list, or a matrix
    """
    winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
    winrows = []
    if return_format == "list_of_lists":
        winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
        winrows = []
        for i in range(1, 31):
            winrows.append([winlist.count(i)])
        return_value = winrows
    elif return_format == "list":
        winlist = [x[0] if x[1] > x[3] else x[2] for x in played_games]
        winrows = []
        for i in range(1, 31):
            winrows.append(winlist.count(i))
        return_value = winrows
    elif return_format == "matrix":
        win_matrix = np.zeros((30, 30))
        for x in played_games:
            if x[1] > x[3]:
                win_matrix[x[0] - 1, x[2] - 1] += 1
            elif x[3] > x[1]:
                win_matrix[x[2] - 1, x[0] - 1] += 1
        return win_matrix
    else:
        print("invalid option")
        return_value = 0
    return return_value


def future_games_query(season_datetime, season_year):
    """
    Returns all games past a given datetime for a given season
    including games on that date.
    Inputs: season_datetime, a datetime object
        season_year, the year the season ends in
    Outputs: pending games past that date as a list of away team,
    home team pairs
    """
    season_epochtime = epochtime(season_datetime)
    query = Games.select().where(
        Games.epochtime >= season_epochtime, Games.year == season_year
    )
    matches = [[x.away_team_id, x.home_team_id] for x in query]
    return matches


def form_query(team_id):
    """
    Return the form in the last five games for the given team


    Parameters
    ----------
    team_id : standard integer id

    Returns
    -------
    A string representing the current form of the team

    """
    import os

    os.system("")  # required to trigger colouring of text
    COLOR = {
        "HEADER": "\033[95m",
        "GREEN": "\033[92m",
        "RED": "\033[91m",
        "ENDC": "\033[0m",
    }
    q = Games.select().where(
        ((Games.away_team_id == team_id) | (Games.home_team_id == team_id))
        & ((Games.away_team_runs > 0)|(Games.home_team_runs > 0))
    )
    x = [[z.away_team_id, z.away_team_runs, z.home_team_id, z.home_team_runs] for z in q[-5:]]
    winstring = ""
    for g in x:
        #print(g)
        if g[1] > g[3]:
            if g[0] == team_id:
                winstring += COLOR["GREEN"] + "W" + COLOR["ENDC"]
            else:
                winstring += COLOR["RED"] + "L" + COLOR["ENDC"]
        if g[3] > g[1]:
            if g[0] == team_id:
                winstring += COLOR["RED"] + "L" + COLOR["ENDC"]
            else:
                winstring += COLOR["GREEN"] + "W" + COLOR["ENDC"]
    return winstring


# #############################################
# # Getting ratings for a given team
# #############################################
def team_elo_rating(team_id, epochtime):
    """
    Get the most recent Elo rating for a team given a date and the team_id

    Parameters
    ----------
    team_id : integer team ID 1-30
    epochtime : Unix time in seconds since epoch

    Returns
    -------
    rtg : most recent Elo rating

    """

    from .mlb_models import MlbTeamEloData

    rtg_iterable = (
        MlbTeamEloData.select()
        .where(MlbTeamEloData.team_id == team_id, MlbTeamEloData.datetime<= epochtime)
        .order_by(MlbTeamEloData.datetime.desc())
        .limit(1)
    )
    rtg = [x.elo_rating for x in rtg_iterable]
    rtg = rtg[0]
    return rtg


def elo_ratings_list(epochtime):
    """


    Parameters
    ----------
    epochtime : Unix time in seconds since epoch

    Returns
    -------
    ratings_list : list of most recent team ratings to date

    """
    ratings_list = []
    for i in range(1, 31):
        ratings_list.append(team_elo_rating(i, epochtime))
    return ratings_list


def new_team_elo_rating(team_id, epochtime):
    """
    Get the most recent Elo rating for a team given a date and the team_id

    Parameters
    ----------
    team_id : integer team ID 1-30
    epochtime : Unix time in seconds since epoch

    Returns
    -------
    rtg : most recent Elo rating

    """

    from .mlb_models import Ratings

    rtg_iterable = (
        Ratings.select()
        .where(Ratings.team_id == team_id, Ratings.epochtime<= epochtime)
        .order_by(Ratings.epochtime.desc())
        .limit(1)
    )
    rtg = [x.elo_rating for x in rtg_iterable]
    #print(rtg)
    try:
        rtg = rtg[0]
        return rtg
    except IndexError as e:
        print("ratings don't exist for team "+str(team_id))
        return 0


def new_elo_ratings_list(epochtime):
    """


    Parameters
    ----------
    epochtime : Unix time in seconds since epoch

    Returns
    -------
    ratings_list : list of most recent team ratings to date

    """
    ratings_list = []
    for i in range(1, 31):
        ratings_list.append(new_team_elo_rating(i, epochtime))
    return ratings_list

def new_team_srs_rating(team_id, epochtime):
    """
    Get the most recent srs rating for a team given a date and the team_id

    Parameters
    ----------
    team_id : integer team ID 1-30
    epochtime : Unix time in seconds since epoch

    Returns
    -------
    rtg : most recent srs rating

    """

    from .mlb_models import SRS

    rtg_iterable = (
        SRS.select()
        .where(SRS.team_id == team_id, SRS.epochtime<= epochtime)
        .order_by(SRS.epochtime.desc())
        .limit(1)
    )
    rtg = [x.srs_rating for x in rtg_iterable]
    #print(rtg)
    try:
        rtg = rtg[0]
        return rtg
    except IndexError as e:
        print("ratings don't exist for team "+str(team_id))
        return 0

def new_srs_ratings_list(epochtime):
    """


    Parameters
    ----------
    epochtime : Unix time in seconds since epoch

    Returns
    -------
    ratings_list : list of most recent team ratings to date

    """
    ratings_list = []
    for i in range(1, 31):
        ratings_list.append(new_team_srs_rating(i, epochtime))
    return ratings_list


