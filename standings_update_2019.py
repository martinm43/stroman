"""
Gets data from the mlbgame api
and then updates the existing db entries

Need to doublecheck/tune algo
"""



import sys
from datetime import datetime, timedelta

import mlbgame
from supports import teams_index_matcher
from mlb_data_models import Game, Team
from pprint import pprint

from lxml import etree

start_date = datetime(2019,4,1) #start date (sometime in March)
end_date = datetime(2019,4,1) #end date (end of season typically oct 1)

game_d = start_date

while game_d <= end_date:

    print("Getting games from " + game_d.strftime("%Y-%m-%d"))

    month = mlbgame.games(game_d.year, game_d.month, game_d.day)
    games = mlbgame.combine_games(month)

    game_list = []
    pprint(games)
    print(dir(games[0]))
    box_score = mlbgame.data.get_box_score(games[0].game_id)
    bs = etree.parse(box_score).getroot()
    dir(bs)
    game_d = game_d + timedelta(days=1)
