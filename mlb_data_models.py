from peewee import *

database = SqliteDatabase('mlb_data.sqlite', **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Team(BaseModel):
    abbreviation = TextField(null=True)
    city = TextField(null=True)  # for weather matching purposes
    league = TextField(null=True)
    division = TextField(null=True)
    team = IntegerField(db_column='team_id', null=True)
    team_name = TextField(null=True)
    stadium_type = TextField(null=True)
    mlbgames_name = TextField(null=True)

    class Meta:
        db_table = 'teams'


class Game(BaseModel):  # initialize with default values
    away_team_name = TextField(null=True)
    home_team_name = TextField(null=True)
    away_team = IntegerField(null=True)
    home_team = IntegerField(null=True)
    away_runs = IntegerField(null=True)
    home_runs = IntegerField(null=True)
    away_pitcher_id = IntegerField(null=True)
    home_pitcher_id = IntegerField(null=True)
    scheduled_date = DateTimeField(null=True)
    mlbgame_away_team_name = TextField(null=True)
    mlbgame_home_team_name = TextField(null=True)
    mlbgame_id_str = TextField(null=True)
    is_postphoned = IntegerField(null=True)

    class Meta:
        db_table = 'games'


class SRSRating(BaseModel):  # initialize with default values
    rating_date = DateTimeField(null=True)
    team_id = IntegerField(null=True)
    rating = FloatField(null=True)

    class Meta:
        db_table = 'SRS_ratings'
