STROMAN

Named after the cocky Blue Jays pitcher, this is a rudimentary set 
of scripts based on the mlbgames api and other work I've done 
for NBA data analysis. 

The main creative work this builds upon as stated above is Carl Panzarino's
mlbgame, using the MLB license, located at https://github.com/panzarino/mlbgame/blob/master/LICENSE

Using an MIT license

Future Tasks:
* Integrate mcss code into mcss_python.py ("do the heavy lifting in C++, while maintaining the Python interface")
  - to this task, see also "python-cpp" repo

Ratings Calculation File (common to previous NBA work and current MLB work):
R1. analytics/burke_solver.py
Takes in a list of games (away team, away runs, home team, home runs) and calculates a 
functional equivalent of Simple Rating SYstem (point differential adjusted for Strength of Schedule).
Unlike the NBA equivalent there is no "cutoff".

Filelist (to be updated) (linted save for C0103, variable names):
1. full_ratings_calculations.py - linted save for naming styles
Calculates net ratings, Pythagorean win 
expectation, and adjusted net rating.

2. james.py - linted save for naming styles
Performes binomial regression based on run
differential and adjusted net rating.

3. global_update.py - fully linted
Updates multiple games (N days in the past via command line update)

3. mcss_python.py - linted save for variable names
Performs Monte Carlo simulation and calculates:
* head to head records
* league wins
* division wins
Currently incorrect - attempting to troubleshoot incorrect math/replace with C++ module

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

10. cpp_setup.py
Setup file for creating the cython-based C++ library for monte carlo standings simulation.

C/C++ Files
Requires armadillo and sqlite3

Intention is to try and write some of the files (mcss, mcss_averages, and full
ratings calculations) in C++

1. mcss_average 
Obtains known wins, then simulates the rest of the season 100,000 times and determines the
average number of wins for the rest of the season. Teams are then sorted by division and 
total wins.

2. mcss
Calculates the playoff odds for each team, accounting for wildcards (but not accounting for end of season tie logic)

3. mcss.h
Header file containing necessary classes, functions, and structures

Compared to its similar file:
"time python mcss_average.py 10000" - 1m 18.743s
"time bash -c "./mcss_average"" - 7.267s, 11x faster.

Cython

1. cpp_setup.pyx
Cython file for linking the cpp function
