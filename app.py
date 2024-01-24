"""Module docstring:This module fetches data from the opensensemap api for the 3 given sensors and makes a temperature average of the 3."""

from datetime import datetime, timedelta
from flask import Flask, jsonify
import requests

app = Flask(__name__)

def fetch_temperature_data():
    """Function docstring: The fucntion fetches the temp data, checks that it's no older than 1 hour and makes an average."""
    sense_box_ids = ["6007eb18942e57001bbead04", "60ff9649482ba8001ca9c072", "5f16ff68e8f87e001c0ec82f"]
    temperatures = []

    for box_id in sense_box_ids:
        try:
            response = requests.get(f"https://api.opensensemap.org/boxes/{box_id}?format=json", timeout=10)
            if response.status_code == 200:
                data = response.json()
                for sensor in data['sensors']:
                    if sensor['title'] == 'Temperatur' and 'lastMeasurement' in sensor:
                        measurement = sensor['lastMeasurement']
                        timestamp = datetime.strptime(measurement['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        if datetime.utcnow() - timestamp <= timedelta(hours=1):
                            temperatures.append(float(measurement['value']))
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    return sum(temperatures) / len(temperatures) if temperatures else None

@app.route('/version')
def version():
    """Return the version of the application."""
    return jsonify({"version": "0.0.1"})

@app.route('/temperature')
def temperature():
    """Return the average temperature."""
    try:
        avg_temp = fetch_temperature_data()
        return jsonify({"average_temperature": avg_temp})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
