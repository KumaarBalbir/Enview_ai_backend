import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('our_database.db')
cursor = conn.cursor()

# Create tables for events and alerts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY,
        timestamp TEXT,
        is_driving_safe INTEGER,
        vehicle_id TEXT,
        location_type TEXT
    )
''')

# Create a table for alerts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        alert_id INTEGER PRIMARY KEY,
        timestamp TEXT,
        vehicle_id TEXT,
        location_type TEXT
    )
''')

# Create a table for location thresholds
cursor.execute('''
    CREATE TABLE IF NOT EXISTS location_thresholds (
        location_type TEXT PRIMARY KEY,
        threshold INTEGER
    )
''')

# Insert default thresholds (can be done initially or as needed)
cursor.executemany('''
    INSERT OR IGNORE INTO location_thresholds (location_type, threshold)
    VALUES (?, ?)
''', [
    ('highway', 4),
    ('city_center', 3),
    ('commercial', 2),
    ('residential', 1)
])

# Commit the changes and close the connection
conn.commit()
conn.close()
