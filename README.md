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
Performs Monte Carlo simulation and calculates:
* head to head records
* league wins
* division wins

mcss_averages.py
Reads a dict of games to be played with their binomial 
win probabilities and produces an average number of wins 
for each team.

mlb_array.py
Parses the attached xls schedule in order to create a 
season schedule and insert it into the database.

mlb_data_models.py
Contains ORM models for the MLB database.

mlb_manual.py - TO BE DELETED
Script for entering MLB data manually from an Excel 
sheet.

season_games_splitter.py
Splits the season based on games played and games to be 
played.

standings_projection.py
Takes in a set of rankings (TBD) and writes out a set of 
dicts to a json file containing future win probabilities

supports.py
A set of assistant scripts for other main scripts in this 
library/repo/whatever.

table_initializer.py
Brief script that creates the tables in the MLB database.

tiebreaker.py
Function containing tiebreaker logic based 
on dicts (in progress)

To be done apr 16:

check how/if burke ratngs are calculated properly or use run differential
incorporate known wins into "mcss" files.
