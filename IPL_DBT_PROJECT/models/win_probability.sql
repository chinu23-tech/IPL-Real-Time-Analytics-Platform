{{ config(materialized='table') }}

SELECT
    MATCH_ID,
    INNINGS,
    OVER,
    RUNS_SCORED,
    WICKETS,
    ROUND(
        (RUNS_SCORED * 1.0) /
        NULLIF((RUNS_SCORED + (WICKETS * 10)), 0),
        4
    ) AS WIN_PROBABILITY
FROM CRICKET_DB.GOLD.WIN_PROBABILITY