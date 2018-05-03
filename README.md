STROMAN

Named after the cocky Blue Jays pitcher, this is a rudimentary set 
of scripts based on the mlbgames api and other work I've done 
for NBA data analysis. 

The main creative work this builds upon as stated above is Carl Panzarino's
mlbgame, using the MLB license, located at https://github.com/panzarino/mlbgame/blob/master/LICENSE

Using an MIT license

* Create a "future games" worksheet something like that for the NBA
* Create a table and output file for the big simulation (mcss)
* Update pitching data (starting with pitcher names) in table.
* Add in a random quote at the end of the log file when complete.
* Playoff predictions and the like should start no earlier than 20%, no later than 25% into season.
* GUI for updating missed/postphoned games, could be as easy as an Excel sheet/python script combination.

Filelist (to be updated):

1. full_ratings_calculations.py
Calculates net ratings, Pythagorean win 
expectation, and adjusted net rating.

2. james.py
Performes binomial regression based on run
differential and adjusted net rating.

3. global_update.py
Updates multiple games (N days in the past via command line update)

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

9. season_games_splitter.py
Splits the season based on games played and games to be 
played.

10. supports.py
A set of assistant scripts for other main scripts in this 
library/repo/whatever. Contains scripts for calculating
current ratings and the binomial win probabilities in future
games. Also contains a function that converts the list of
binomial win probabilities into a "head to head matrix"

11. table_initializer.py
Brief script that creates the tables in the MLB database.

12. tiebreaker.py
Function containing tiebreaker logic based 
on dicts containing team records and head to heads. Current time of development (may)
is a bit too early to start thinking about tiebreaker logic for playoffs.

13. missing_read.py
Reads missing games (games that have not yet been played) from an excel worksheet.
Worksheet is a work in progress, development paused.

14. missing_write.py
Writes missing games to excel worksheet (in progress). 
Note that there is the possibility that our update dates 
might be the reason for the win discrepancy.
The goal here is not to track specific wins and losses at this point, but to
assess team performance using raw stats.



