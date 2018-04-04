"""
Main file for running the Future Games Projector, Standings Projector, and
Playoff Odds Calculator sub-scripts.
"""
from __future__ import print_function
import os

def standings_generation():
    "This function runs all the sub-scripts for the program"
    working_directory = os.path.dirname(os.path.realpath(__file__))+'/'
    #obtain relevant data for future projections
    execfile(working_directory+'season_games_splitter.py')
    #perform analytics calculations
    execfile(working_directory+'run_differential.py')
    execfile(working_directory+'ratings_calculations.py')
    #prepare to perform monte carlo calculations
    #execfile(working_directory+'monte_carlo_calculations.py')
    #perform the monte carlo simulation
    #execfile(working_directory+'monte_carlo_standings_simulator.py')

if __name__ == '__main__':
    print('Standings Projector and Playoffs Odds Calculator, v2.0')
    print('Now adapted for baseball. ')
    print('MA Miller, 2017')
    standings_generation()
