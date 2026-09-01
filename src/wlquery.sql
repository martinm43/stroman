SELECT
    team,

    SUM(wins) || '-' || SUM(losses) AS record,

    SUM(home_wins) || '-' || SUM(home_losses) AS home_record,

    SUM(away_wins) || '-' || SUM(away_losses) AS away_record,

    SUM(runs_for) - SUM(runs_against) AS run_diff

FROM (
    SELECT
        home_team AS team,
        home_team_runs > away_team_runs AS wins,
        home_team_runs < away_team_runs AS losses,

        home_team_runs > away_team_runs AS home_wins,
        home_team_runs < away_team_runs AS home_losses,

        0 AS away_wins,
        0 AS away_losses,

        home_team_runs AS runs_for,
        away_team_runs AS runs_against
    FROM games
    WHERE year = 2026
    UNION ALL

    SELECT
        away_team AS team,
        away_team_runs > home_team_runs AS wins,
        away_team_runs < home_team_runs AS losses,

        0 AS home_wins,
        0 AS home_losses,

        away_team_runs > home_team_runs AS away_wins,
        away_team_runs < home_team_runs AS away_losses,

        away_team_runs AS runs_for,
        home_team_runs AS runs_against
    FROM games
    WHERE year = 2026
)
GROUP BY team
ORDER BY
    SUM(wins) DESC,
    run_diff DESC;
