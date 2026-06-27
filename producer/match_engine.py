import random

from teams import TEAMS
from stats_engine import MatchStats
from config import WICKET_TYPES


def create_match():

    team1, team2 = random.sample(
        list(TEAMS.keys()),
        2
    )

    toss_winner = random.choice(
        [team1, team2]
    )

    decision = random.choice(
        ["BAT", "BOWL"]
    )

    if decision == "BAT":

        batting_team = toss_winner

        bowling_team = (
            team2
            if toss_winner == team1
            else team1
        )

    else:

        bowling_team = toss_winner

        batting_team = (
            team2
            if toss_winner == team1
            else team1
        )

    return {
        "team1": team1,
        "team2": team2,
        "toss_winner": toss_winner,
        "decision": decision,
        "batting_team": batting_team,
        "bowling_team": bowling_team
    }


def initialize_innings(
    batting_team,
    bowling_team
):

    batting_players = TEAMS[
        batting_team
    ]["players"]

    bowling_options = TEAMS[
        bowling_team
    ]["bowlers"]

    return {
        "striker": batting_players[0],
        "non_striker": batting_players[1],
        "next_batter_index": 2,
        "current_bowler": bowling_options[0]
    }


def simulate_innings(
    match_id,
    innings_no,
    batting_team,
    bowling_team,
    teams_data
):

    batters = teams_data[
        batting_team
    ]["players"]

    bowlers = teams_data[
        bowling_team
    ]["bowlers"]

    stats = MatchStats()

    striker = batters[0]
    non_striker = batters[1]

    next_batter = 2

    innings_events = []

    for over in range(1, 21):

        if stats.team_wickets >= 10:
            break

        bowler = bowlers[
            (over - 1)
            % len(bowlers)
        ]

        for ball in range(1, 7):

            if stats.team_wickets >= 10:
                break

            wicket = random.choice(
                [False] * 18 + [True] * 2
            )

            if wicket:

                wicket_type = random.choice(
                    WICKET_TYPES
                )

                stats.add_wicket()

                stats.update_bowler(
                    bowler,
                    0,
                    True
                )

                innings_events.append(
                    {
                        "match_id": match_id,
                        "innings": innings_no,
                        "over": over,
                        "ball": ball,
                        "batting_team": batting_team,
                        "bowling_team": bowling_team,
                        "striker": striker,
                        "bowler": bowler,
                        "event": "WICKET",
                        "wicket_type": wicket_type,
                        "score": stats.team_score,
                        "wickets": stats.team_wickets
                    }
                )

                if next_batter < len(batters):

                    striker = batters[
                        next_batter
                    ]

                    next_batter += 1

                continue

            runs = random.choice(
                [0, 1, 1, 1, 2, 3, 4, 4, 6]
            )

            stats.add_team_runs(
                runs
            )

            stats.update_batter(
                striker,
                runs
            )

            stats.update_bowler(
                bowler,
                runs,
                False
            )

            innings_events.append(
                {
                    "match_id" : match_id,
                    "innings": innings_no,
                    "over": over,
                    "ball": ball,
                    "batting_team": batting_team,
                    "bowling_team": bowling_team,
                    "striker": striker,
                    "bowler": bowler,
                    "runs": runs,
                    "score": stats.team_score,
                    "wickets": stats.team_wickets
                }
            )

            if runs % 2 == 1:

                striker, non_striker = (
                    non_striker,
                    striker
                )

        striker, non_striker = (
            non_striker,
            striker
        )

    return stats, innings_events


def simulate_match(
    match_id,
    team1,
    team2,
    teams_data
):

    first_innings, events1 = (
        simulate_innings(
            match_id,
            1,
            team1,
            team2,
            teams_data
        )
    )

    second_innings, events2 = (
        simulate_innings(
            match_id,
            2,
            team2,
            team1,
            teams_data
        )
    )

    if (
        first_innings.team_score >
        second_innings.team_score
    ):

        winner = team1

    elif (
        second_innings.team_score >
        first_innings.team_score
    ):

        winner = team2

    else:

        winner = "TIE"

    # --------------------
    # MAN OF THE MATCH
    # --------------------

    mom = None
    highest_runs = 0

    for batter, data in (
        first_innings.batters.items()
    ):

        if data["runs"] > highest_runs:

            highest_runs = data["runs"]
            mom = batter

    for batter, data in (
        second_innings.batters.items()
    ):

        if data["runs"] > highest_runs:

            highest_runs = data["runs"]
            mom = batter

    return {
        "match_id": match_id,

        "team1": team1,
        "team2": team2,

        "team1_score":
            first_innings.team_score,

        "team2_score":
            second_innings.team_score,

        "winner":
            winner,

        "man_of_match":
            mom,
        "margin": abs(
             first_innings.team_score - second_innings.team_score
        ),
        "events":
            events1 + events2,

        "innings1_stats":
            first_innings,

        "innings2_stats":
            second_innings
    }