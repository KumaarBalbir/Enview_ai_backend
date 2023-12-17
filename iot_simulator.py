import requests
import json
import datetime


def make_POST_request(url, data):

    # Make a POST request to the /event endpoint
    response = requests.post(url, json=data)

    # Check the response
    if response.status_code == 201:
        print("Hello from IOT Simulator. Successfully added event!\n")
    else:
        print("IOT Simulator, couldn't add event", response.text)


def make_GET_request(url, alert_id):
    url = f'{url}/{alert_id}'

    # Make a POST request to the /event endpoint
    response = requests.get(url)

    # Check the response
    if response.status_code == 200:
        alert_data = response.json()
        print("Hello from Server, this is the alert you requested:\n")
        print("Alert ID:", alert_data['alert_id'])
        print("Timestamp:", alert_data['timestamp'])
        print("Vehicle ID:", alert_data['vehicle_id'])
        print("Location Type:", alert_data['location_type'])
    else:
        print("Server couldn't get alert:", response.text)


if __name__ == "__main__":
    current_time = datetime.datetime.utcnow().isoformat()
    # Replace with IOT data
    data = {
        "timestamp": current_time,
        "is_driving_safe": 0,  # Assuming 0 represents False for is_driving_safe
        "vehicle_id": 12345,
        "location_type": "residential"
    }
    # URL of Flask app
    # Update with server URL(if deployed)
    post_url = 'http://127.0.0.1:5000/event'

    # Update with server URL(if deployed)
    get_url = 'http://127.0.0.1:5000/alert'

    alert_id = 1

    make_POST_request(post_url, data)
    make_GET_request(get_url, alert_id)
