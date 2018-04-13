STROMAN

Named after the cocky Blue Jays pitcher, this is a rudimentary set 
of scripts based on the mlbgames api and other work I've done 
for NBA data analysis. 

The main creative work this builds upon as stated above is Carl Panzarino's
mlbgame, using the MLB license, located at https://github.com/panzarino/mlbgame/blob/master/LICENSE

(c) of some kind - TBD - Martin Miller

TBD soon, RQ INT means requires internet, a lot of these are just raw ideas:

* Parse the "unable to find data for..." statements and update the Games table to say "Game Postphoned"
* Update pitching data (starting with pitcher names) in table
* Add in a random quote at the end of the log file when complete

TBD later:
Playoff predictions and the like should start no earlier than 20%, no later than 25% into season

Filelist:

full_ratings_calculations.py
Calculates net ratings, Pythagorean win 
expectation, and adjusted net rating.

james.py
Performes binomial regression based on run
differential and adjusted net rating.

last_day_update.py
Updates the mlb database based on the 
previous day's games.

long_dict_inserter.py
A function created for the purpose of 
inserting long lists of dicts into SQLite
databases

mcss.py


mcss_averages.py
Reads a dict of games to be played with their binomial 
win probabilities and produces an average number of wins 
for each team.

mcss_basic.py


mlb_api_test.py


mlb_array.py


mlb_data_models.py
Contains ORM models for the MLB database.

mlb_manual.py


season_games_splitter.py


standings_projection.py


supports.py
A set of assistant scripts for other main scripts in this 
library/repo/whatever.

table_initializer.py


tiebreaker.py
Function containing tiebreaker logic based 
on dicts (in progress)

