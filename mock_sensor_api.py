from flask import Flask, jsonify

app = Flask(__name__)

# Mock sensor location
sensor_location = {
    'x': 0.7,
    'y': 0.6,
    'z': 0.8
}


@app.route('/api/sensor/location', methods=['GET'])
def get_sensor_location():
    return jsonify(sensor_location)


if __name__ == '__main__':
    app.run(debug=True)
