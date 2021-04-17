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

    class Meta:
        table_name = 'teams'

