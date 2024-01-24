from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

def fetch_temperature_data():
    senseBox_ids = ["6007eb18942e57001bbead04", "60ff9649482ba8001ca9c072", "5f16ff68e8f87e001c0ec82f"]
    temperatures = []

    for box_id in senseBox_ids:
        response = requests.get(f"https://api.opensensemap.org/boxes/{box_id}?format=json")
        if response.status_code == 200:
            data = response.json()
            for sensor in data['sensors']:
                if sensor['title'] == 'Temperatur' and 'lastMeasurement' in sensor:
                    measurement = sensor['lastMeasurement']
                    timestamp = datetime.strptime(measurement['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    if datetime.utcnow() - timestamp <= timedelta(hours=1):
                        temperatures.append(float(measurement['value']))

    return sum(temperatures) / len(temperatures) if temperatures else None



@app.route('/version')
def version():
    return jsonify({"version": "0.0.1"})

@app.route('/temperature')
def temperature():
    try:
        avg_temp = fetch_temperature_data()
        return jsonify({"average_temperature": avg_temp})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
