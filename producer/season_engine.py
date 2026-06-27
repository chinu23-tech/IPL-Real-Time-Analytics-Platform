import random

TEAMS = [
    "RCB",
    "MI",
    "CSK",
    "KKR",
    "SRH",
    "DC",
    "PBKS",
    "RR",
    "GT",
    "LSG"
]

points_table = {}

for team in TEAMS:

    points_table[team] = {

        "played": 0,
        "won": 0,
        "lost": 0,
        "points": 0,

        "runs_scored": 0,
        "runs_conceded": 0,

        "overs_faced": 0,
        "overs_bowled": 0,

        "nrr": 0
    }


def generate_fixture():

    return random.sample(
        TEAMS,
        2
    )


def update_points_table(
    winner,
    loser,
    winner_score,
    loser_score
):

    points_table[winner]["played"] += 1
    points_table[winner]["won"] += 1
    points_table[winner]["points"] += 2

    points_table[loser]["played"] += 1
    points_table[loser]["lost"] += 1

    points_table[winner]["runs_scored"] += winner_score
    points_table[winner]["runs_conceded"] += loser_score

    points_table[loser]["runs_scored"] += loser_score
    points_table[loser]["runs_conceded"] += winner_score


def calculate_nrr():

    for team in points_table:

        scored = points_table[team]["runs_scored"]

        conceded = points_table[team]["runs_conceded"]

        points_table[team]["nrr"] = round(
            (scored - conceded) / 100,
            3
        )


def get_points_table():

    calculate_nrr()

    return sorted(
        points_table.items(),
        key=lambda x: (
            x[1]["points"],
            x[1]["nrr"]
        ),
        reverse=True
    )
import random

def generate_league_fixtures():

    fixtures = []

    teams = TEAMS.copy()

    for i in range(70):

        team1, team2 = random.sample(
            teams,
            2
        )

        fixtures.append(
            (team1, team2)
        )

    return fixtures
def simulate_season(
    simulate_match_func,
    teams_data
):

    fixtures = generate_league_fixtures()

    season_results = []

    for match_no, (team1, team2) in enumerate(fixtures, start=1):

        print(
            f"Simulating Match {match_no}: "
            f"{team1} vs {team2}"
        )

        result = simulate_match_func(
            match_no,
            team1,
            team2,
            teams_data
        )

        season_results.append(result)

        if result["winner"] != "TIE":

            loser = (
                team2
                if result["winner"] == team1
                else team1
            )

            winner_score = (
                result["team1_score"]
                if result["winner"] == team1
                else result["team2_score"]
            )

            loser_score = (
                result["team2_score"]
                if result["winner"] == team1
                else result["team1_score"]
            )

            update_points_table(
                result["winner"],
                loser,
                winner_score,
                loser_score
            )

    return season_results
def simulate_playoffs(
    points_table_data,
    simulate_match_func,
    teams_data
):

    top4 = [
        team
        for team, data
        in points_table_data[:4]
    ]

    team1 = top4[0]
    team2 = top4[1]
    team3 = top4[2]
    team4 = top4[3]

    # Qualifier 1
    q1 = simulate_match_func(
        1001,
        team1,
        team2,
        teams_data
    )

    q1_winner = q1["winner"]

    q1_loser = (
        team2
        if q1_winner == team1
        else team1
    )

    # Eliminator
    eliminator = simulate_match_func(
        1002,
        team3,
        team4,
        teams_data
    )

    elim_winner = eliminator["winner"]

    # Qualifier 2
    q2 = simulate_match_func(
        1003,
        q1_loser,
        elim_winner,
        teams_data
    )

    q2_winner = q2["winner"]

    # Final
    final = simulate_match_func(
        1004,
        q1_winner,
        q2_winner,
        teams_data
    )

    champion = final["winner"]

    return {

        "qualifier1": q1,

        "eliminator": eliminator,

        "qualifier2": q2,

        "final": final,

        "champion": champion
    }