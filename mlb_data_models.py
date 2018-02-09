from peewee import *

database = SqliteDatabase('mlb_data.sqlite', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Teams(BaseModel):
    abbreviation = TextField(null=True)
    city = TextField(null=True) #for weather matching purposes
    league = TextField(null=True)
    division = TextField(null=True)
    team = IntegerField(db_column='team_id', null=True)
    team_name = TextField(null=True)

    class Meta:
        db_table = 'teams'

class Games(BaseModel): #initialize with default values
    away_team = TextField(null=True)
    home_team = TextField(null=True)

    class Meta:
        db_table = 'teams'

