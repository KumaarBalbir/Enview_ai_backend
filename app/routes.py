from flask import Blueprint, jsonify, request
import sqlite3

# Create blueprints
event_blueprint = Blueprint("event", __name__)
alert_blueprint = Blueprint("alert", __name__)

# Function to create a database connection


def get_db_connection():
    conn = sqlite3.connect('our_database.db')
    conn.row_factory = sqlite3.Row
    return conn


@event_blueprint.route("/event", methods=["POST"])
def add_event():
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (timestamp, is_driving_safe, vehicle_id, location_type) 
            VALUES (?, ?, ?, ?)
        ''', (data["timestamp"], data["is_driving_safe"], data["vehicle_id"], data["location_type"]))
        conn.commit()
    return jsonify({"message": "Event added successfully"}), 201


@alert_blueprint.route("/alert/<alert_id>", methods=["GET"])
def get_alert(alert_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM alerts WHERE alert_id = ?
        ''', (alert_id,))
        alert = cursor.fetchone()
        if alert:
            return jsonify({
                "alert_id": alert['alert_id'],
                "timestamp": alert['timestamp'],
                "vehicle_id": alert['vehicle_id'],
                "location_type": alert['location_type']
            })
        else:
            return jsonify({"message": "Alert not found"}), 404
