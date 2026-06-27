import json
import time
from kafka import KafkaProducer

# ==========================================
# CONFIGURATION
# ==========================================

BALL_DELAY = 2          # seconds between every ball
OVER_DELAY = 8          # seconds after every over
INNINGS_DELAY = 20      # innings break
MATCH_DELAY = 30        # break between matches

# ==========================================
# KAFKA PRODUCER
# ==========================================

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# ==========================================
# LOAD MATCH DATA
# ==========================================

with open(
    "output/season_results.json",
    "r"
) as f:

    season_results = json.load(f)

print("=" * 60)
print("🏏 IPL LIVE STREAM STARTED")
print("=" * 60)

total_events = 0

previous_match = None
previous_innings = None

# ==========================================
# STREAM MATCHES
# ==========================================

for match in season_results:

    for event in match["events"]:

        # ----------------------------------
        # MATCH BREAK
        # ----------------------------------

        if (
            previous_match is not None
            and previous_match != event["match_id"]
        ):

            print("\n" + "=" * 60)
            print(f"✅ Match {previous_match} Completed")
            print("Starting Next Match...")
            print("=" * 60)

            time.sleep(MATCH_DELAY)

        # ----------------------------------
        # INNINGS BREAK
        # ----------------------------------

        if (
            previous_innings is not None
            and previous_innings != event["innings"]
        ):

            print("\n")
            print("-" * 50)
            print("🏏 Innings Break")
            print("-" * 50)

            time.sleep(INNINGS_DELAY)

        # ----------------------------------
        # SEND EVENT
        # ----------------------------------

        producer.send(
            "ipl-events",
            event
        )

        producer.flush()

        total_events += 1

        print(
            f"Match {event['match_id']} | "
            f"Innings {event['innings']} | "
            f"{event['batting_team']} | "
            f"{event['score']}/{event['wickets']} | "
            f"Over {event['over']}.{event['ball']}"
        )

        # ----------------------------------
        # OVER BREAK
        # ----------------------------------

        if event["ball"] == 6:

            print("🔄 Over Completed\n")
            time.sleep(OVER_DELAY)

        else:

            time.sleep(BALL_DELAY)

        previous_match = event["match_id"]
        previous_innings = event["innings"]

# ==========================================
# FINISH
# ==========================================

producer.flush()

print("\n")
print("=" * 60)
print(f"🏆 IPL Season Completed")
print(f"Total Events Streamed : {total_events}")
print("=" * 60)