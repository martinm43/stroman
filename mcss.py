"""
A bunch of functions that I use to do Monte Carlo simulations of issues
_Performs Monte Carlo simulation using MLB
schedule and then determines playoff teams.

Tiebreaker logic to be developed.
Other functionality (such as processing daily updates)
are far more important.

MAM

"""



if __name__ == '__main__':

    from pprint import pprint
    import os
    import sys
    import numpy as np
    from tabulate import tabulate
    from datetime import datetime
    #from pprint import pprint


    from mlb_data_models import Team, database
    from supports import games_won_to_date, future_games_dicts, mcss

    sim_results = []

    cursor = database.execute_sql('select distinct division from teams;')
    list_of_divisions = [row[0] for row in cursor]

    league_teams = Team.select(
        Team.team_name,
        Team.id,
        Team.division,
        Team.league)
    league_teams = [dict(list(zip(['team_name', 'team_id', 'division', 'league'], [
        x.team_name, x.id, x.division, x.league]))) for x in league_teams]

    # Assign this once to hold it for later use
    header_league_teams = league_teams

    # Holding matrix for major outcomes
    # Rows = team ids
    # Columns = (Division wins, Wildcard places,Total wins)
    playoff_matrix = np.zeros((30, 3))

    try:
        ite = int(sys.argv[1])
    except IndexError:
        ite = 1
        print('Debug run, using ' + str(ite) + ' iteration(s)')

    binomial_win_probabilities = future_games_dicts()
    print(len(binomial_win_probabilities))
    if binomial_win_probabilities == 1:
        print('Error occurred while calculating '
              'future binomial win probabilities')
        sys.exit(1)

    known_wins = games_won_to_date(return_format='matrix')
    wkdir = os.path.join(os.path.dirname(__file__))

    for i_ite in range(0, ite):
        win_matrix = mcss(binomial_win_probabilities)
        win_matrix += known_wins
        total_wins = np.sum(win_matrix, axis=0)
        # Raw win totals.
        for x in league_teams:
            x['total_wins'] = total_wins[x['team_id'] - 1]

        # pprint(league_teams)
        # Division win totals and eventually division leaders
        for d in list_of_divisions:
            dt = [x for x in league_teams if x['division'] == d]
            for t in dt:
                other_division_team_ids = [x['team_id']
                                           for x in dt if x['team_id'] != t['team_id']]
                other_league_team_ids = [
                    x['team_id'] for x in league_teams if x['league'] == t['league']]
                division_wins = sum([win_matrix[i - 1, t['team_id'] - 1]
                                     for i in other_division_team_ids])
                t['division_wins'] = division_wins
                league_wins = sum([win_matrix[i - 1, t['team_id'] - 1]
                                   for i in other_league_team_ids])
                t['league_wins'] = league_wins

            # sort list of dicts
            new_dt = sorted(
                dt, key=lambda k: (-k['total_wins'], -k['division_wins'], -k['league_wins']))
            for i, dt_dict in enumerate(new_dt):
                dt_dict['div_rank'] = i + 1
                #dt_dict['div_winner'] = bool(dt_dict['div_rank'])
                if dt_dict['div_rank'] == 1: #pylint:disable=simplifiable-if-statement
                    dt_dict['div_winner'] = True
                else:
                    dt_dict['div_winner'] = False

        sim_results.append(league_teams)

        # Determine wild card winners
        al_wc = [
            x for x in sim_results[0] if (
                x['div_winner'] is False and x['league'] == 'AL')]
        al_wc.sort(key=lambda x: -x['total_wins'])
        nl_wc = [
            x for x in sim_results[0] if (
                x['div_winner'] is False and x['league'] == 'NL')]
        nl_wc.sort(key=lambda x: -x['total_wins'])
        al_wc_winners = [x['team_id'] for x in al_wc[0:2]]
        nl_wc_winners = [x['team_id'] for x in nl_wc[0:2]]
        for t in league_teams:
            if (t['team_id'] in al_wc_winners) or ( #pylint:disable=simplifiable-if-statement
                    t['team_id'] in nl_wc_winners):
                t['wild_card'] = True
            else:
                t['wild_card'] = False

            # enter into the playoff matrix as per above
            if t['wild_card']:
                playoff_matrix[int(t['team_id']) - 1, 1] += 1
            elif t['div_winner']:
                playoff_matrix[int(t['team_id']) - 1, 0] += 1
            playoff_matrix[int(t['team_id'] - 1), 2] += t['total_wins']

    # Summarizing results.
    header_league_teams = Team.select(
        Team.team_name, Team.id, Team.division, Team.league)
    header_league_teams = [dict(list(zip(['team_name', 'team_id',\
        'division', 'league'], [x.team_name, x.id, x.division, x.league])))\
        for x in header_league_teams]

    for t in header_league_teams:
        t['Wild Card Odds'] = np.sum(
            playoff_matrix[int(t['team_id']) - 1, 1]) / ite
        t['Division Win Odds'] = np.sum(
            playoff_matrix[int(t['team_id']) - 1, 0]) / ite
        t['Playoff Odds'] = t['Wild Card Odds'] + t['Division Win Odds']
        t['Total Wins'] = np.sum(
            playoff_matrix[int(t['team_id']) - 1, 2]) / ite

    #pprint(t)

    # Print out the headers and a table.
    header_league_teams.sort(
        key=lambda x: (
            x['division'], -x['Playoff Odds'], -x['Total Wins']))
    header_league_teams = [
        (x['division'],
         x['team_name'],
         x['Total Wins'],
         x['Wild Card Odds'],
         x['Division Win Odds'],
         x['Playoff Odds']) for x in header_league_teams]
    summary_table = tabulate(
        header_league_teams,
        headers=[
            'Division',
            'Team',
            'Projected Wins',
            'Wild Card Odds',
            'Division Odds',
            'Playoff Odds'],
        tablefmt='rst')
    print(summary_table)

    #####################
    # Print to Log File #
    #####################

    # Repeat commands above but write the information to a file.

    file_out = open(
        wkdir +
        'MCSS_' +
        datetime.now().strftime('%Y-%m-%d') +
        '_' +
        str(ite) +
        '_iter.txt',
        'w')

    file_out.write(
        'Summary of Results, ' +
        datetime.now().strftime('%Y-%m-%d') +
        ' ' +
        str(ite) +
        ' iterations \n\n')

    file_out.write(summary_table)

    file_out.close()

    print("Writing to file completed successfully.")
