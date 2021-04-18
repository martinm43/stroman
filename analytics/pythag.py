# coding: utf-8
"""
This file attempts to calculate "Pythagorean wins" using pts scored for and
against a team in a given season. The default exponent is set to that 
used by Basketball Reference, which compares favourably to the range given in 
Basketball on Paper (Oliver)
"""
from pprint import pprint
import time
import sys
from tabulate import tabulate


def pythagorean_wins(
    Game,
    team_id_num,
    win_exp=1.83, #baseball
    numgames=162,#baseball
    mincalcdatetime=0.0,
    maxcalcdatetime=999999999999.9,
):
    """


    Parameters
    ----------
    Game : ORM object from the
            nba_playoff_odds.nba_database.nba_data_models file
    team_id_num : team id (1=ATL,30=WAS)
    win_exp : Exponent used in pythagorean_wins calculation. The default is 14.
    numgames : number of games to apply the pythagorean win percentage to
                The default is 82.
    mincalcdatetime : minimum Unix timestamp for querying Game object
                        i.e. the first game
    maxcalcdatetime : maximum Unix timestamp for querying Game object
                        i.e. the last game

    Returns
    -------
    # of games the team should have won over the given time period
    given the number of games.

    """
    team_id = str(team_id_num)
    pts = Game.select(Game.away_team_runs).where(
        Game.away_team_id == team_id,
        Game.epochtime >= mincalcdatetime,
        Game.epochtime <= maxcalcdatetime,
    )
    #team_away_team_runs = sum([p.away_team_runs if p.away_team_runs is not None else 0 for p in pts])
    team_away_team_runs = sum([p.away_team_runs for p in pts])
    pts = Game.select(Game.home_team_runs).where(
        Game.home_team_id == team_id,
        Game.epochtime >= mincalcdatetime,
        Game.epochtime <= maxcalcdatetime,
    )
    #team_home_team_runs = sum([p.home_team_runs if p.home_team_runs is not None else 0 for p in pts])
    team_home_team_runs = sum([p.home_team_runs for p in pts])
    team_team_runs_for = team_away_team_runs + team_home_team_runs
    team_team_runs_against_home = Game.select(Game.away_team_runs).where(
        Game.home_team_id == team_id,
        Game.epochtime >= mincalcdatetime,
        Game.epochtime <= maxcalcdatetime,
    )
    team_team_runs_against_away = Game.select(Game.home_team_runs).where(
        Game.away_team_id == team_id,
        Game.epochtime >= mincalcdatetime,
        Game.epochtime <= maxcalcdatetime,
    )
    team_team_runs_against_home = sum(
         [p.away_team_runs for p in team_team_runs_against_home]
    #    [p.away_team_runs if p.away_team_runs is not None else 0 for p in team_team_runs_against_home]
    )
    team_team_runs_against_away = sum(
         [p.home_team_runs for p in team_team_runs_against_away]
    #    [p.home_team_runs if p.home_team_runs is not None else 0 for p in team_team_runs_against_away]
    )
    team_team_runs_against = team_team_runs_against_away + team_team_runs_against_home

    if team_team_runs_against > 0 and team_team_runs_for > 0:
        return (
            numgames
            * team_team_runs_for ** win_exp
            / (team_team_runs_for ** win_exp + team_team_runs_against ** win_exp)
        )
    else:
        return 0


def league_pythagorean_wins(
    GAME_ORM, mincalcdatetime, maxcalcdatetime, 
    win_exp=1.83, 
    numgames=162
):
    """


    Parameters
    ----------
    GAME_ORM : The Game ORM object
    mincalcdatetime : Minimum Unix timestamp for league pythagorean calculation
    maxcalcdatetime : Maximum Unix timestamp for league pythagorean calculation
    win_exp : Pythagorean win coefficient (default is 14)
    numgames : number of games to apply the pythagorean win expectation to (82)

    Returns
    -------
    List of the pythagorean win expectations

    """
    results_list = []
    for i in range(1, 31):
        results_list.append(
            [
                i,
                pythagorean_wins(
                    GAME_ORM,
                    i,
                    win_exp=win_exp,
                    numgames=numgames,
                    mincalcdatetime=mincalcdatetime,
                    maxcalcdatetime=maxcalcdatetime,
                ),
            ]
        )
    return sorted(results_list, key=lambda x: x[1])

