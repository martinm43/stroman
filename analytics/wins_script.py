# coding: utf-8
def get_wins(team_id, season_year, start_datetime, end_datetime):
    """

    Return wins from a given season for a given team.

    Parameters
    ----------
    team_id : team id (1=ATL,30=WAS)
    season_year : season ending in year X
    start_datetime : UNIX timestamp of start of query
    end_datetime : UNIX timestamp of end of query

    Returns
    -------
    dict: away_wins of team, home_wins of team, and overall record.

    """
    from mlb_database.mlb_models import Games
    from mlb_database.queries import team_abbreviation, epochtime

    away_query = Games.select().where(
        Games.year == season_year,
        Games.away_team_id == team_id,
        ((Games.away_team_runs > 0)|(Games.home_team_runs > 0)),
        Games.epochtime >= epochtime(start_datetime),
        Games.epochtime <= epochtime(end_datetime),
    )
    away_results = [[i.away_team_runs, i.home_team_runs] for i in away_query]
    away_wins_total = sum([1 if x[0] > x[1] else 0 for x in away_results])
    away_games_total = len(away_results)
    # home_query = Games.select().where(Games.year == season_year, Games.home_team_id == team_id, Games.home_team_runs > 0)
    home_query = Games.select().where(
        Games.year == season_year,
        Games.home_team_id == team_id,
        ((Games.away_team_runs > 0)|(Games.home_team_runs > 0)),
        Games.epochtime >= epochtime(start_datetime),
        Games.epochtime <= epochtime(end_datetime),
    )
    home_results = [[i.home_team_runs, i.away_team_runs] for i in home_query]
    home_wins_total = sum([1 if x[0] > x[1] else 0 for x in home_results])
    home_games_total = len(home_results)

    away_record = str(away_wins_total) + "-" + str(away_games_total - away_wins_total)
    home_record = str(home_wins_total) + "-" + str(home_games_total - home_wins_total)
    record = (
        str(away_wins_total + home_wins_total)
        + "-"
        + str(away_games_total + home_games_total - away_wins_total - home_wins_total)
    )

    return {"away_record": away_record, "home_record": home_record, "record": record}
