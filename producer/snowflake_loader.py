import json
import snowflake.connector

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

with open(
    "output/consumer_events.json",
    "r"
) as f:

    events = json.load(f)

rows = []

for event in events:

    rows.append(
        (
            event.get("match_id"),
            event.get("innings"),
            event.get("batting_team"),
            event.get("bowling_team"),
            event.get("over"),
            event.get("ball"),
            event.get("striker"),
            event.get("bowler"),
            event.get("runs", 0),
            event.get("score"),
            event.get("wickets"),
            event.get("event", "RUN"),
            event.get("wicket_type")
        )
    )

print(f"Preparing to load {len(rows)} rows...")

cursor.executemany(
    """
    INSERT INTO IPL_SIMULATOR_EVENTS
    (
        MATCH_ID,
        INNINGS,
        BATTING_TEAM,
        BOWLING_TEAM,
        OVER_NO,
        BALL_NO,
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
        %s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,
        %s,%s,%s
    )
    """,
    rows
)

conn.commit()

print(f"Loaded {len(rows)} events")

cursor.close()
conn.close()