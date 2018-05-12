"""
A bunch of functions that I use to do Monte Carlo simulations of issues
This function returns "raw projected wins". A good teaser.
"""
from __future__ import division, print_function
from tabulate import tabulate
import numpy as np

if __name__ == '__main__':
    from datetime import datetime
    import os
    import sys
    from mlb_data_models import Team, database
    from supports import games_won_to_date, future_games_dicts, mcss

    wkdir = os.path.join(os.path.dirname(__file__))
    games_won = games_won_to_date()

    cursor = database.execute_sql('select distinct division from teams;')
    list_of_divisions = [row[0] for row in cursor]

    league_teams = Team.select(
        Team.team_name,
        Team.id,
        Team.division,
        Team.league)
    league_teams = [dict(zip(['team_name', 'team_id', 'division', 'league'], [
        x.team_name, x.id, x.division, x.league])) for x in league_teams]

    # pprint(test_dict)
    try:
        ite = int(sys.argv[1])
    except IndexError:
        print('Running from Ipython or some other place - assuming debug length of 1000')
        ite = 1000

    binomial_win_probabilities = future_games_dicts()
    if binomial_win_probabilities == 1:
        print('Error occurred while calculating \
              future binomial win probabilities')
        sys.exit(1)

    sim_results = np.zeros(30)
    for i in range(0, ite):
        sim_results += np.sum(mcss(binomial_win_probabilities), axis=0)

    sim_results = np.divide(sim_results, ite) + np.asarray(games_won)

    for x in league_teams:
        x['total_wins'] = sim_results[x['team_id'] - 1]

    league_teams = sorted(league_teams, key=lambda k: -k['total_wins'])

###############################
# Writing the table to screen #
###############################

# Sort

league_teams.sort(key=lambda x: (x['division'], -x['total_wins']))

# Format

for x in league_teams:
    x['total_wins'] = round(x['total_wins'], 1)

# Preview
# pprint(league_teams)

# division, team name, total wins as list of tuples then pass headers
league_teams = [(x['division'], x['team_name'], x['total_wins'])
                for x in league_teams]
averages_table = tabulate(
    league_teams,
    headers=[
        'Division',
        'Team',
        'Projected Wins'],
    tablefmt='rst')

print(averages_table)

#####################
# Print to Log File #
#####################

# Repeat commands above but write the information to a file.

file_out = open(
    wkdir +
    'Monte_Carlo_Average_Wins_' +
    datetime.now().strftime('%Y-%m-%d') +
    '_' +
    str(ite) +
    '_iter.txt',
    'wb')

file_out.write(
    'Summary of Results, ' +
    datetime.now().strftime('%Y-%m-%d') +
    ' ' +
    str(ite) +
    ' iterations \n\n')

file_out.write(averages_table)

file_out.close()

print("Writing to file completed successfully.")
