import json
import time
import snowflake.connector
import traceback

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

# Start Clean
cursor.execute("TRUNCATE TABLE IPL_SIMULATOR_EVENTS")
conn.commit()

print("=" * 60)
print("🏏 Snowflake Live Loader Started (Hardened Tournament Loop)")
print("=" * 60)

loaded = 0

while True:
    try:
        with open("output/consumer_events.json", "r") as f:
            events = json.load(f)

        new_events = events[loaded:]

        if len(new_events) == 0:
            time.sleep(1)  # Increased check sleep to prevent thread lock
            continue

        for event in new_events:
            # Safe parsing to guarantee the loader never crashes on structural data gaps
            match_id = event.get("match_id")
            innings = event.get("innings")
            over_no = event.get("over")
            ball_no = event.get("ball")
            
            # Skip corrupted row markers if any exist during rapid file changes
            if match_id is None or innings is None:
                loaded += 1
                continue

            cursor.execute(
                """
                INSERT INTO IPL_SIMULATOR_EVENTS
                (
                    MATCH_ID, INNINGS, OVER_NO, BALL_NO, BATTING_TEAM, BOWLING_TEAM,
                    STRIKER, NON_STRIKER, BOWLER, RUNS, SCORE, WICKETS, EVENT, WICKET_TYPE
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    match_id,
                    innings,
                    over_no,
                    ball_no,
                    event.get("batting_team"),
                    event.get("bowling_team"),
                    event.get("striker"),
                    event.get("non_striker"),
                    event.get("bowler"),
                    int(event.get("runs", 0)),
                    int(event.get("score", 0)),
                    int(event.get("wickets", 0)),
                    event.get("event", "RUN"),
                    event.get("wicket_type")
                )
            )
            loaded += 1

        conn.commit()
        print(f"✅ Batch Sync Complete. Total Balls Processed: {loaded}")
        time.sleep(0.5)

    except (FileNotFoundError, json.JSONDecodeError):
        time.sleep(0.5)  # Wait safely for the consumer to finish writing the file
    except Exception as e:
        print(f"⚠️ Caught ingestion gap: {e}")
        traceback.print_exc()
        time.sleep(1)