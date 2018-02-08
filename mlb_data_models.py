from peewee import *

database = SqliteDatabase('mlb_data.sqlite', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class MLBTeams(BaseModel):
    abbreviation = TextField(null=True)
    city = TextField(null=True)
    league = TextField(null=True)
    division = TextField(null=True)
    team = IntegerField(db_column='team_id', null=True)
    team_name = TextField(null=True)

    class Meta:
        db_table = 'mlb_teams'

