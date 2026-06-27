import json
import time
import snowflake.connector

# ==========================================
# SNOWFLAKE CONNECTION
# ==========================================

conn = snowflake.connector.connect(
    account="PJGGWMP-ZH63080",
    user="CHINU6371",
    password="6371486849@Chinu",
    warehouse="COMPUTE_WH",
    database="CRICKET_DB",
    schema="RAW",
    role="ACCOUNTADMIN"
)

cursor = conn.cursor()

# ==========================================
# START CLEAN
# ==========================================

cursor.execute(
    "TRUNCATE TABLE IPL_SIMULATOR_EVENTS"
)

conn.commit()

print("=" * 60)
print("🏏 Snowflake Live Loader Started")
print("=" * 60)

loaded = 0

# ==========================================
# LIVE LOOP
# ==========================================

while True:

    try:

        with open(
            "output/consumer_events.json",
            "r"
        ) as f:

            events = json.load(f)

        # Only load new events
        new_events = events[loaded:]

        if len(new_events) == 0:

            time.sleep(0.2)
            continue

        for event in new_events:

            cursor.execute(
                """
                INSERT INTO IPL_SIMULATOR_EVENTS
                (
                    MATCH_ID,
                    INNINGS,
                    OVER_NO,
                    BALL_NO,
                    BATTING_TEAM,
                    BOWLING_TEAM,
                    STRIKER,
                    BOWLER,
                    RUNS,
                    SCORE,
                    WICKETS,
                    EVENT,
                    WICKET_TYPE
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    event.get("match_id"),
                    event.get("innings"),
                    event.get("over"),
                    event.get("ball"),
                    event.get("batting_team"),
                    event.get("bowling_team"),
                    event.get("striker"),
                    event.get("bowler"),
                    event.get("runs", 0),
                    event.get("score"),
                    event.get("wickets"),
                    event.get("event", "RUN"),
                    event.get("wicket_type")
                )
            )

            loaded += 1

            print(
                f"Loaded Ball : "
                f"Match {event['match_id']} | "
                f"{event['over']}.{event['ball']} | "
                f"{event['score']}/{event['wickets']}"
            )

        conn.commit()

        time.sleep(0.2)

    except FileNotFoundError:

        time.sleep(0.2)

    except json.JSONDecodeError:

        time.sleep(0.2)

    except Exception as e:

        print(e)

        time.sleep(0.2)