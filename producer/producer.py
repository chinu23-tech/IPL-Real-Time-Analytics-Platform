import json
import time

from teams import TEAMS

from match_engine import (
    simulate_match
)

from season_engine import (
    simulate_season,
    get_points_table,
    simulate_playoffs
)
from analytics_engine import (
    generate_orange_cap,
    generate_purple_cap
)

print("=" * 60)
print("IPL SEASON SIMULATION")
print("=" * 60)

# -----------------------
# SIMULATE SEASON
# -----------------------

season_results = simulate_season(
    simulate_match,
    TEAMS
)
orange_cap = generate_orange_cap(
    season_results
)

purple_cap = generate_purple_cap(
    season_results
)

# -----------------------
# SAVE SEASON RESULTS
# -----------------------

with open(
    "output/season_results.json",
    "w"
) as f:

    json.dump(
        season_results,
        f,
        indent=4,
        default=str
    )

# -----------------------
# POINTS TABLE
# -----------------------

table = get_points_table()
points_json = []

for team, data in table:

    points_json.append(
        {
            "team": team,
            **data
        }
    )

with open(
    "output/points_table.json",
    "w"
) as f:

    json.dump(
        points_json,
        f,
        indent=4
    )

print("\n")
print("=" * 60)
print("IPL POINTS TABLE")
print("=" * 60)

for position, (team, data) in enumerate(
    table,
    start=1
):

    print(
        f"{position}. "
        f"{team} | "
        f"Pts: {data['points']} | "
        f"NRR: {data['nrr']}"
    )

# -----------------------
# TOP 4
# -----------------------

print("\n")
print("=" * 60)
print("TOP 4 QUALIFIED")
print("=" * 60)

for rank, (team, data) in enumerate(
    table[:4],
    start=1
):

    print(
        f"{rank}. "
        f"{team} "
        f"({data['points']} pts)"
    )

# -----------------------
# PLAYOFFS
# -----------------------

playoffs = simulate_playoffs(
    table,
    simulate_match,
    TEAMS
)

# -----------------------
# CHAMPION
# -----------------------

print("\n")
print("=" * 60)
print("IPL CHAMPION")
print("=" * 60)

print(
    playoffs["champion"]
)

# -----------------------
# SAVE CHAMPION
# -----------------------

with open(
    "output/champion.json",
    "w"
) as f:

    json.dump(
        {
            "champion": playoffs["champion"]
        },
        f,
        indent=4
    )

print("\n")
print("=" * 60)
print("FILES GENERATED")
print("=" * 60)

print("output/season_results.json")
print("output/champion.json")

print("\nSimulation Completed Successfully")
with open(
    "output/orange_cap.json",
    "w"
) as f:

    json.dump(
        orange_cap[:10],
        f,
        indent=4,
        default=str
    )

with open(
    "output/purple_cap.json",
    "w"
) as f:

    json.dump(
        purple_cap[:10],
        f,
        indent=4,
        default=str
    )
