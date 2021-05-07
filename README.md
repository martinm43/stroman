# Stroman

A Python/C++ program to calculate basic statistics about baseball seasons and 
to determine the playoff picture at any given time since 1977 
(free agency/true desegregation). It was named after my favourite pitcher for 
the Toronto Blue Jays and now New York Mets, Marcus Stroman.

## <u>**The Files, and What they Do**</u>
**baseball_csv_importer.py**  -- processes the .csv files supplied by the ben_kite 
baseball_data library. Minor changes have been made to that library in order to 
facilitate the acquisition of historical data

        
**points_analysis.py** -- used to calculate the parameters of a normal 
distribution of runs in baseball  

**info_table.py** - provides critical information for a given baseball season,
given start date and end date. Useful if you want to see "performance over 
second half" or something similar

**elo_calculator.py** - Calculates the Elo model for baseball from 1977 to 2020
(current end of the dataset)

**team_elo_history_plots.py** - Plots Elo history for every team.

**elo_model_check.py** - Checks to see if the Elo model would have predicted
the correct winner for each game for every season.

**prediction_table.py** - Uses a Monte Carlo simulation model to predict the 
odds of making a variety of relevant playoff spots - see below explanation.

**plot_season_odds.py** - Plots the odds of each team in a random division 
since 1977 making the playoffs, using time-period-correct criteria.

## <u>**Monte Carlo Model Explanation**</u>

The basic idea is - use one of the two models (either Elo at game date, or SRS 
calculated using the games up to that date) and simulate the rest of the games
in the season using a regression model. Then sort the results in such a way that 
certain spots will be occupied by certain playoff teams. E.G. if there were 7 
AL East/AL West teams and 7 NL East/7 NL West teams and after you played a season
and sorted them according to their division name string then by wins you'd get:

AL East ... Team .. MAX_AL_EAST_WINS

(6 teams)

AL West ... Team .. MAX_AL_WEST_WINS

(6 teams)   

NL East .. Team .. MAX_NL_EAST_WINS

(6 teams)

NL West .. Team .. MAX_NL_WEST_WINS

(6 teams)

In later seasons there is logic that selects, for example:

* the "max 2 teams that did not win their division in the AL"
* the "max 2 teams that did not win their division or be runner ups" (yes, that last one is the logic used in the 2020 'season')

The specific places in the array used to choose the winners and wild-cards 
(and 2020 runner ups) changes based on # of teams in the league. 

## <u>**Dependencies and Requirements/Caveats**</u>

Python requirements:  
the nba_py library (only for update_nba_api)  
peewee (version 3.11+)
numpy, scipy, and cython  

C++ requirements for compiling Monte Carlo cython extension (on Linux):  
libarmadillo-dev   
libsqlite3-dev  

Note that gcc-11 and clang-12 are not yet tested.

On Windows in order to build the Monte Carlo simulation extension, you will require:

Microsoft Visual C++ as described in the .vsconfig file (tested with VC.141.x86.64)
Armadillo libraries have been included for this purpose (see below Attribution)  
Note that the program runs much slower under Windows:

info_table: about 3 seconds on Linux, about 9 seconds on Windows  
prediction_table: about 0.7 seconds on Linux, about 2.1 seconds on Windows  
plot_season_odds: about 1.2 on Linux, about 4.2 seconds on Windows  

Windows users with access to WSL or WSL2 should consider running the program under those virtualization options as it will most likely run much faster.  

## <u>To Do</u>
- Update the dependencies
- Final (?) update of readme




