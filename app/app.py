from flask import Flask
from routes import event_blueprint, alert_blueprint
import datetime
import sqlite3
import time
import threading

app = Flask(__name__)
app.register_blueprint(event_blueprint)
app.register_blueprint(alert_blueprint)

# define the time interval in minutes
TIME_INTERVAL = 1


# Function to print the contents of the events table
def print_events():
    conn = sqlite3.connect('our_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()

    print("Events Table:")
    for event in events:
        print(event)


# Function to print the contents of the alerts table
def print_alerts():
    conn = sqlite3.connect('our_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts")
    alerts = cursor.fetchall()
    conn.close()

    print("Alerts Table:")
    for alert in alerts:
        print(alert)


# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect('our_database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Function to apply rule engine and generate alerts
def apply_rule_engine():
    now = datetime.datetime.utcnow()
    minute_interval_ago = now - datetime.timedelta(minutes=TIME_INTERVAL)

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Fetch thresholds from the database
        cursor.execute(
            'SELECT location_type, threshold FROM location_thresholds')
        location_thresholds_dict = {row[0]: row[1]
                                    for row in cursor.fetchall()}

        # Fetch all events that happened within the last TIME_INTERVAL minutes
        cursor.execute('''
              SELECT * FROM events 
              WHERE timestamp >= ?
          ''', (minute_interval_ago,))

        events_min_interval_ago = cursor.fetchall()

        # Count the number of events per vehicle and location
        vehicle_location_count = {}
        for event in events_min_interval_ago:
            event_is_driving_safe = event['is_driving_safe']
            event_vehicle_id = event['vehicle_id']
            event_location_type = event['location_type']
            if event_is_driving_safe == 0:
                key = (event_vehicle_id, event_location_type)
                if key in vehicle_location_count:
                    vehicle_location_count[key] += 1
                else:
                    vehicle_location_count[key] = 1

        for key, count in vehicle_location_count.items():
            vehicle_id = key[0]
            location = key[1]
            threshold_limit = location_thresholds_dict[location]
            if count >= threshold_limit:
                current_time = datetime.datetime.now().isoformat()
                cursor.execute('''
                    INSERT INTO alerts (timestamp, vehicle_id, location_type) 
                    VALUES (?, ?, ?)
                ''', (current_time, vehicle_id, location))
                conn.commit()
                print(f"Alert generated for {location} at {now}")
            else:
                pass  # TODO implement what to do if there is no violation of driving in given TIME_INTERVAL


# Run the rule engine every TIME_INTERVAL minutes (for demonstration purposes)
def run_rule_engine():
    while True:
        apply_rule_engine()
        # Sleep for TIME_INTERVAL minutes before running the rule engine again
        time.sleep(TIME_INTERVAL * 60)  # Sleep in seconds, so multiply by 60


if __name__ == "__main__":

    # Call the functions to print the contents of the tables
    # print_events()
    # print_alerts()

    # Start the rule engine in a separate thread
    rule_engine_thread = threading.Thread(target=run_rule_engine)
    rule_engine_thread.start()

    app.run(debug=False)
