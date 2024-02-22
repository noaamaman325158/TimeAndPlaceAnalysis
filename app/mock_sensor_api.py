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
    """
    Endpoint to get the sensor's current location.

    This route returns the current  location of the chair in the format:
    {
        'x': [min_x, max_x],
        'y': [min_y, max_y]
    }

    :return: JSON object with the sensor's current location.
    """
    return jsonify(chair_current_location)


@app.route('/api/chair/location', methods=['GET'])
def get_current_chair_location():
    """
    Endpoint to get the current location of the chair.

    This route fetches the sensor location from the '/api/sensor/location' endpoint
    and returns it. In case of failure to retrieve the sensor location,
    it returns an error message with a 500 status code.

    :return: JSON object with the chair's current location if successful,
             otherwise JSON object with error message.
    """
    sensor_endpoint = 'http://127.0.0.1:5000/api/sensor/location'
    response = requests.get(sensor_endpoint)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to retrieve sensor location'}), 500


if __name__ == '__main__':
    app.run(debug=True)
