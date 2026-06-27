from kafka import KafkaConsumer
import json
import os

# ==========================================
# KAFKA CONSUMER
# ==========================================

consumer = KafkaConsumer(
    "ipl-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(
        m.decode("utf-8")
    )
)

events = []

print("=" * 60)
print("🏏 IPL LIVE CONSUMER STARTED")
print("=" * 60)

# ==========================================
# LISTEN FOREVER
# ==========================================

for msg in consumer:

    event = msg.value

    events.append(event)

    # --------------------------------------
    # SAVE EVERY BALL IMMEDIATELY
    # --------------------------------------

    temp_file = "output/consumer_events_temp.json"

    with open(
        temp_file,
        "w"
    ) as f:

        json.dump(
            events,
            f,
            indent=4
        )

    os.replace(
        temp_file,
        "output/consumer_events.json"
    )

    # --------------------------------------
    # TERMINAL OUTPUT
    # --------------------------------------

    print(
        f"Match {event['match_id']} | "
        f"Innings {event['innings']} | "
        f"{event['batting_team']} | "
        f"{event['score']}/{event['wickets']} | "
        f"Over {event['over']}.{event['ball']}"
    )

print("=" * 60)
print("Consumer Stopped")
print("=" * 60)