from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


app = Flask(__name__)

# Configuration for InfluxDB
token = "i1uzl3uek09fFXKW6t8131GmFFKkUG-WESrM3-L4zKDbaOoocHqx4VSpen3UyzKVxAZW3Ujr19gpgUWFvwrYYg=="
org = "cern"
bucket = "sensor"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    point = (
        Point("sensor_data")
        .tag("sensor", "arduino")
        .field("temperature", float(data["temperature"]))
        .field("gas", float(data["gas"]))
        .field("sound", float(data["sound"]))
        .field("magnetic", int(data["magnetic"]))
        .time(datetime.utcnow(), WritePrecision.NS)
    )
    try:
        write_api.write(bucket=bucket, org=org, record=point)
        return jsonify({"message": "Data received"}), 200
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")
        return jsonify({"message": "Failed to write data", "error": str(e)}), 403


if __name__ == "__main__":
    app.run(debug=True, port=5001)