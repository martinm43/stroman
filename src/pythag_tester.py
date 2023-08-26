"""
A script for checking whether the pythagorean odds
you calculated make sense. 

"""

if __name__=="__main__":
    from analytics.pythag import pythagorean_wins
    from mlb_database.mlb_models import Games
    from mlb_database.queries import epochtime, team_abbreviation
    from datetime import datetime
    start_epoch = epochtime(datetime(2001,3,1))
    end_epoch = epochtime(datetime(2001,11,30))
  
    for team_id in range(1,31):
        z = pythagorean_wins(Games, team_id, mincalcdatetime=start_epoch,maxcalcdatetime=end_epoch)
        print(team_abbreviation(team_id))
        print(z)
