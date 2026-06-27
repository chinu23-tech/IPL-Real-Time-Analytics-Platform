def generate_orange_cap(
    season_results
):

    batters = {}

    for match in season_results:

        for innings_key in [
            "innings1_stats",
            "innings2_stats"
        ]:

            if innings_key not in match:
                continue

            stats = match[innings_key]

            for batter, data in stats.batters.items():

                if batter not in batters:

                    batters[batter] = 0

                batters[batter] += (
                    data["runs"]
                )

    return sorted(
        batters.items(),
        key=lambda x: x[1],
        reverse=True
    )
def generate_purple_cap(
    season_results
):

    bowlers = {}

    for match in season_results:

        for innings_key in [
            "innings1_stats",
            "innings2_stats"
        ]:

            if innings_key not in match:
                continue

            stats = match[innings_key]

            for bowler, data in stats.bowlers.items():

                if bowler not in bowlers:

                    bowlers[bowler] = 0

                bowlers[bowler] += (
                    data["wickets"]
                )

    return sorted(
        bowlers.items(),
        key=lambda x: x[1],
        reverse=True
    )