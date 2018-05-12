STROMAN

Named after the cocky Blue Jays pitcher, this is a rudimentary set 
of scripts based on the mlbgames api and other work I've done 
for NBA data analysis. 

The main creative work this builds upon as stated above is Carl Panzarino's
mlbgame, using the MLB license, located at https://github.com/panzarino/mlbgame/blob/master/LICENSE

Using an MIT license

* Create a "future games" worksheet something like that for the NBA
* Update pitching data (starting with pitcher names) in table.
* Add in a random quote at the end of the log file when complete.
* Playoff predictions and the like should start no earlier than 20%, no later than 25% into season.
* GUI for updating missed/postphoned games, could be as easy as an Excel sheet/python script combination.

Filelist (to be updated) (linted save for C0103, variable names):
1. full_ratings_calculations.py - linted save for naming styles
Calculates net ratings, Pythagorean win 
expectation, and adjusted net rating.

2. james.py - linted save for naming styles
Performes binomial regression based on run
differential and adjusted net rating.

3. global_update.py - fully linted
Updates multiple games (N days in the past via command line update)

3. mcss.py - linted save for variable names
Performs Monte Carlo simulation and calculates:
* head to head records
* league wins
* division wins

4. mcss_averages.py - linted save for variable names
Reads a dict of games to be played with their binomial 
win probabilities and produces an average number of wins 
for each team.

5. mlb_array.py - linted save for variable names
Parses the attached xls schedule in order to create a 
season schedule and insert it into the database.

6. mlb_data_models.py - linting is a tool, not a religious institution. 
                      - not going to lint this file!
Contains ORM models for the MLB database.

7. supports.py - linted save for variable names
A set of assistant scripts for other main scripts in this 
library/repo/whatever. Contains scripts for calculating
current ratings and the binomial win probabilities in future
games. Also contains a function that converts the list of
binomial win probabilities into a "head to head matrix"

8. table_initializer.py - linted
Brief script that creates the tables in the MLB database.

9. tiebreaker.py - linted save for variable names
Function containing tiebreaker logic based 
on dicts containing team records and head to heads. Current time of development (may)
is a bit too early to start thinking about tiebreaker logic for playoffs.

10. missing_read.py - linted save for variable names
Reads missing games (games that have not yet been played) from an excel worksheet.
Worksheet is a work in progress, development paused.

11. missing_write.py - linted save for variable names
Writes missing games to excel worksheet (in progress). 
Note that there is the possibility that our update dates 
might be the reason for the win discrepancy.
The goal here is not to track specific wins and losses at this point, but to
assess team performance using raw stats.



