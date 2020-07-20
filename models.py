from peewee import *

database = SqliteDatabase('mlb_data.sqlite', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SrsRatings(BaseModel):
    rating = FloatField(null=True)
    rating_date = DateTimeField(null=True)
    team_id = IntegerField(null=True)

    class Meta:
        table_name = 'SRS_ratings'

class Games(BaseModel):
    away_pitcher_id = IntegerField(null=True)
    away_runs = IntegerField(null=True)
    away_team = IntegerField(null=True)
    away_team_name = TextField(null=True)
    home_pitcher_id = IntegerField(null=True)
    home_runs = IntegerField(null=True)
    home_team = IntegerField(null=True)
    home_team_name = TextField(null=True)
    is_postphoned = IntegerField(null=True)
    mlbgame_away_team_name = TextField(null=True)
    mlbgame_home_team_name = TextField(null=True)
    mlbgame_id_str = TextField(null=True)
    scheduled_date = DateTimeField(null=True)
    season_year = IntegerField(null=True)

    class Meta:
        table_name = 'games'

class Teams(BaseModel):
    abbreviation = TextField(null=True)
    city = TextField(null=True)
    division = TextField(null=True)
    league = TextField(null=True)
    mlbgames_name = TextField(null=True)
    stadium_type = TextField(null=True)
    state = UnknownField(null=True)  # 
    team_id = IntegerField(null=True)
    team_name = TextField(null=True)

    class Meta:
        table_name = 'teams'

