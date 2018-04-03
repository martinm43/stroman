"""
Main file for running the Future Games Projector, Standings Projector, and
Playoff Odds Calculator sub-scripts.
"""
import os

def standings_generation():
    "This function runs all the sub-scripts for the program"
    working_directory = os.path.dirname(os.path.realpath(__file__))+'/'
    #clean up data
    execfile(working_directory+'nba_api_team_indexer.py')
    #obtain relevant data for future projections
    execfile(working_directory+'season_games_splitter.py')
    #perform analytics calculations
    execfile(working_directory+'analytics/ptsaverages.py')
    execfile(working_directory+'ratings_calculations.py')
    execfile(working_directory+'monte_carlo_calculations.py')
    #monte carlo simulation
    execfile(working_directory+'monte_carlo_standings_simulator.py')

#if __name__ == '__main__':
#    print 'Standings Projector and Playoffs Odds Calculator, v1.0'
#    print 'MA Miller, 2017'
#    standings_generation()
