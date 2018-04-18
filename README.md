STROMAN

Named after the cocky Blue Jays pitcher, this is a rudimentary set 
of scripts based on the mlbgames api and other work I've done 
for NBA data analysis. 

The main creative work this builds upon as stated above is Carl Panzarino's
mlbgame, using the MLB license, located at https://github.com/panzarino/mlbgame/blob/master/LICENSE

(c) of some kind - TBD - Martin Miller

TBD soon, RQ INT means requires internet, a lot of these are just raw ideas:

* Process known wins into the "mcss matrix"
* Update pitching data (starting with pitcher names) in table
* Add in a random quote at the end of the log file when complete
* Playoff predictions and the like should start no earlier than 20%, no later than 25% into season
* GUI for updating missed/postphoned games, could be as easy as an Excel sheet/python script combination

Filelist:

1. full_ratings_calculations.py
Calculates net ratings, Pythagorean win 
expectation, and adjusted net rating.

2. james.py
Performes binomial regression based on run
differential and adjusted net rating.

3. last_day_update.py
Updates the mlb database based on the 
previous day's games.

4. long_dict_inserter.py
A function created for the purpose of 
inserting long lists of dicts into SQLite
databases

5. mcss.py
Performs Monte Carlo simulation and calculates:
* head to head records
* league wins
* division wins

6. mcss_averages.py
Reads a dict of games to be played with their binomial 
win probabilities and produces an average number of wins 
for each team.

7. mlb_array.py
Parses the attached xls schedule in order to create a 
season schedule and insert it into the database.

8. mlb_data_models.py
Contains ORM models for the MLB database.

9. mlb_manual.py - TO BE DELETED
Script for entering MLB data manually from an Excel 
sheet.

10. season_games_splitter.py
Splits the season based on games played and games to be 
played.

11. standings_projection.py
Takes in a set of rankings (TBD) and writes out a set of 
dicts to a json file containing future win probabilities

12. supports.py
A set of assistant scripts for other main scripts in this 
library/repo/whatever.

13. table_initializer.py
Brief script that creates the tables in the MLB database.

14. tiebreaker.py
Function containing tiebreaker logic based 
on dicts (in progress)


