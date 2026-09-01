SELECT
    team,

    SUM(wins) || '-' || SUM(losses) AS record,

    SUM(home_wins) || '-' || SUM(home_losses) AS home_record,

    SUM(away_wins) || '-' || SUM(away_losses) AS away_record,

    SUM(runs_for) - SUM(runs_against) AS run_diff

FROM (
    SELECT
        home_team AS team,
        home_runs > away_runs AS wins,
        home_runs < away_runs AS losses,

        home_runs > away_runs AS home_wins,
        home_runs < away_runs AS home_losses,

        0 AS away_wins,
        0 AS away_losses,

        home_runs AS runs_for,
        away_runs AS runs_against
    FROM games

    UNION ALL

    SELECT
        away_team AS team,
        away_runs > home_runs AS wins,
        away_runs < home_runs AS losses,

        0 AS home_wins,
        0 AS home_losses,

        away_runs > home_runs AS away_wins,
        away_runs < home_runs AS away_losses,

        away_runs AS runs_for,
        home_runs AS runs_against
    FROM games
)
GROUP BY team
ORDER BY
    SUM(wins) DESC,
    run_diff DESC;
