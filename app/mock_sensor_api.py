from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Mock sensor location
chair_current_location = {
    'x': [-0.5, 0],
    'y': [1.8, 2.4]
}


@app.route('/api/sensor/location', methods=['GET'])
def get_sensor_location():
    return jsonify(chair_current_location)


@app.route('/api/chair/location', methods=['GET'])
def get_current_chair_location():
    sensor_endpoint = 'http://127.0.0.1:5000/api/sensor/location'
    response = requests.get(sensor_endpoint)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        # Return an error message if the request to the sensor API failed
        return jsonify({'error': 'Failed to retrieve sensor location'}), 500


if __name__ == '__main__':
    app.run(debug=True)
