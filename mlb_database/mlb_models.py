from peewee import *

database = SqliteDatabase('mlb_data.sqlite')

# class TextField(object):
#     def __init__(self, *_, **__): 
#         pass

class BaseModel(Model):
    class Meta:
        database = database

class Games(BaseModel):
    attendance = FloatField(null=True)
    away_team = TextField(null=True)
    away_team_runs = IntegerField(null=True)
    c_li = FloatField(null=True)
    d_n = TextField(null=True)  # str
    game_date = TextField(null=True)
    gb = TextField(null=True)  # str
    home_game = BooleanField(null=True)
    home_streak = TextField(null=True)  # str
    home_team = TextField(null=True)
    home_team_runs = IntegerField(null=True)
    home_wl = TextField(null=True)  # str
    inn = IntegerField(null=True)
    loss = TextField(null=True)  # str
    orig_scheduled = FloatField(null=True)
    save = TextField(null=True)  # str
    team_rank = IntegerField(null=True)
    time = TextField(null=True)  # str
    w_l = TextField(null=True)
    win = TextField(null=True)  # str
    year = IntegerField(null=True)
    epochtime = FloatField(null=True)
    away_team_id = IntegerField(null=True)
    home_team_id = IntegerField(null=True)

    class Meta:
        table_name = 'games'

class Teams(BaseModel):
    abbreviation = TextField(null=True)
    city = TextField(null=True)
    division = TextField(null=True)
    league = TextField(null=True)
    mlbgames_name = TextField(null=True)
    stadium_type = TextField(null=True)
    state = BareField(null=True)
    team_id = IntegerField(null=True)
    team_name = TextField(null=True)
    primary_color = TextField(null=True)
    legacy_divisions_1 = TextField(null=True) #1998 to 2012
    legacy_divisions_2 = TextField(null=True) #1994 to 1997
    legacy_divisions_3 = TextField(null=True) #1977 to 1993

    class Meta:
        table_name = 'teams'

class MlbTeamEloData(BaseModel):
    current_abbreviation = TextField(null=True)
    datetime = FloatField(null=True)
    elo_rating = FloatField(null=True)
    season_year = IntegerField(null=True)
    team_abbreviation = TextField(null=True)
    team_id = IntegerField(null=True)

    class Meta:
        table_name = 'mlb_team_elo_data'

