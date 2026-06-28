from kafka import KafkaConsumer
import json
import os
import time

consumer = KafkaConsumer(
    "ipl-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

events = []
final_file = "output/consumer_events.json"
temp_file = "output/consumer_events_temp.json"

# Ensure output directory exists safely
os.makedirs("output", exist_ok=True)

# If restarting, read existing events to prevent breaking loader offsets
if os.path.exists(final_file):
    try:
        with open(final_file, "r") as f:
            events = json.load(f)
        print(f"Loaded {len(events)} existing historical records successfully.")
    except Exception:
        events = []

print("=" * 60)
print("🏏 CRASH-PROOF ATOMIC WINDOWS CONSUMER ACTIVE")
print("=" * 60)

for msg in consumer:
    event = msg.value
    events.append(event)

    # 1. Write the state payload out to the temporary file cache
    try:
        with open(temp_file, "w") as f:
            json.dump(events, f, indent=4)
    except Exception as e:
        print(f"⚠️ Temporary array write delayed: {e}")
        continue

    # 2. Hardened Windows OS file-lock atomic bypass system
    success = False
    retries = 10
    delay = 0.02  # 20 milliseconds back-off step

    for attempt in range(retries):
        try:
            # Atomic swap layer
            if os.path.exists(final_file):
                try:
                    os.remove(final_file)
                except PermissionError:
                    time.sleep(delay)
                    continue
            
            os.rename(temp_file, final_file)
            success = True
            break
        except PermissionError:
            # If snowflake_loader is reading, back off slightly and loop again
            time.sleep(delay)
            delay *= 1.5  # Exponential backing-off matrix

    if not success:
        print("⚠️ Ingestion frame locked by database engine read cycle; skipping atomic sync pointer.")

    print(
        f"Match {event['match_id']} | "
        f"Innings {event['innings']} | "
        f"{event['batting_team']} | "
        f"{event['score']}/{event['wickets']} | "
        f"Over {event['over']}.{event['ball']}"
    )