"""
This script creates the sqlite database containing the tables defined in
nba_data_models
"""

from mlb_data_models import Team, Game, SRSRating

Team.create_table(True)
Game.create_table(True)
SRSRating.create_table(True)