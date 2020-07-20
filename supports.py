from models import Teams

def team_identifier(abbrev_str):
    x = Teams.select().where(Teams.abbreviation == abbrev_str)
    return x[0].id
