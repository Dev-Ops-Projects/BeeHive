"""Module docstring: This module fetches data from the opensensemap api for the 3 given sensors 
and makes a temperature average of the 3."""

import os
from datetime import datetime, timedelta
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Define the senseBox IDs as environment variables or provide default values
SENSE_BOX_IDS = [
    os.getenv("SENSE_BOX_ID_1", "6007eb18942e57001bbead04"),
    os.getenv("SENSE_BOX_ID_2", "60ff9649482ba8001ca9c072"),
    os.getenv("SENSE_BOX_ID_3", "5f16ff68e8f87e001c0ec82f")
]

def fetch_temperature_data():
    """Fetch temperature data and return the average if data is no older than 1 hour."""
    temperatures = []

    for box_id in SENSE_BOX_IDS:
        temperatures.extend(get_temperatures_for_box(box_id))

    return sum(temperatures) / len(temperatures) if temperatures else None


def get_temperatures_for_box(box_id):
    """Helper function to get temperatures for a single box."""
    try:
        url = f"https://api.opensensemap.org/boxes/{box_id}?format=json"
        response = requests.get(url, timeout=10)
        return parse_sensor_data(response) if response.status_code == 200 else []
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []


def parse_sensor_data(response):
    """Parse sensor data from response to extract temperatures."""
    temperatures = []
    data = response.json()
    for sensor in data['sensors']:
        if sensor['title'] == 'Temperatur' and 'lastMeasurement' in sensor:
            measurement = sensor['lastMeasurement']
            timestamp = datetime.strptime(measurement['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if datetime.utcnow() - timestamp <= timedelta(hours=1):
                temperatures.append(float(measurement['value']))
    return temperatures


@app.route('/version')
def version():
    """Return the version of the application."""
    return jsonify({"version": "0.0.1"})


@app.route('/temperature')
def temperature():
    """Return the average temperature."""
    avg_temp = fetch_temperature_data()
    if avg_temp is None:
        return jsonify({"error": "Data fetch failed"}), 500
    return jsonify({"average_temperature": avg_temp})



if __name__ == '__main__':
    app.run(debug=False)
