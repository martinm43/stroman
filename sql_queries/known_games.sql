string SQLStatement("SELECT away_team, away_runs, home_team, home_runs "
                       "FROM games WHERE (scheduled_date < datetime('now')) 
"
                       "AND NOT (away_runs=0 and home_runs=0);
