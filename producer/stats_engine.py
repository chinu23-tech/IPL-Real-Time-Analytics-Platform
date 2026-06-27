class MatchStats:

    def __init__(self):

        self.team_score = 0
        self.team_wickets = 0

        self.batters = {}

        self.bowlers = {}

    # --------------------
    # TEAM STATS
    # --------------------

    def add_team_runs(self, runs):

        self.team_score += runs

    def add_wicket(self):

        self.team_wickets += 1

    def current_run_rate(self, overs):

        if overs == 0:
            return 0

        return round(
            self.team_score / overs,
            2
        )

    # --------------------
    # BATTER STATS
    # --------------------

    def update_batter(self, batter, runs):

        if batter not in self.batters:

            self.batters[batter] = {
                "runs": 0,
                "balls": 0,
                "fours": 0,
                "sixes": 0,
                "strike_rate": 0
            }

        self.batters[batter]["runs"] += runs
        self.batters[batter]["balls"] += 1

        if runs == 4:
            self.batters[batter]["fours"] += 1

        if runs == 6:
            self.batters[batter]["sixes"] += 1

        balls = self.batters[batter]["balls"]

        self.batters[batter]["strike_rate"] = round(
            (
                self.batters[batter]["runs"]
                / balls
            ) * 100,
            2
        )

    # --------------------
    # BOWLER STATS
    # --------------------

    def update_bowler(
        self,
        bowler,
        runs,
        wicket=False
    ):

        if bowler not in self.bowlers:

            self.bowlers[bowler] = {
                "runs_conceded": 0,
                "balls": 0,
                "wickets": 0,
                "dot_balls": 0,
                "economy": 0
            }

        self.bowlers[bowler]["runs_conceded"] += runs

        self.bowlers[bowler]["balls"] += 1

        if runs == 0:
            self.bowlers[bowler]["dot_balls"] += 1

        if wicket:
            self.bowlers[bowler]["wickets"] += 1

        overs = self.bowlers[bowler]["balls"] / 6

        if overs > 0:

            self.bowlers[bowler]["economy"] = round(
                self.bowlers[bowler]["runs_conceded"]
                / overs,
                2
            )

    # --------------------
    # ORANGE CAP
    # --------------------

    def orange_cap(self):

        if not self.batters:
            return None

        return max(
            self.batters.items(),
            key=lambda x: x[1]["runs"]
        )

    # --------------------
    # PURPLE CAP
    # --------------------

    def purple_cap(self):

        if not self.bowlers:
            return None

        return max(
            self.bowlers.items(),
            key=lambda x: x[1]["wickets"]
        )

    # --------------------
    # BATTING CARD
    # --------------------

    def print_batting_card(self):

        print("\nBATTING CARD")

        for batter, data in self.batters.items():

            print(
                f"{batter} "
                f"{data['runs']}({data['balls']}) "
                f"SR:{data['strike_rate']}"
            )

    # --------------------
    # BOWLING CARD
    # --------------------

    def print_bowling_card(self):

        print("\nBOWLING CARD")

        for bowler, data in self.bowlers.items():

            overs = round(
                data["balls"] / 6,
                1
            )

            print(
                f"{bowler} "
                f"O:{overs} "
                f"R:{data['runs_conceded']} "
                f"W:{data['wickets']} "
                f"ECO:{data['economy']}"
            )