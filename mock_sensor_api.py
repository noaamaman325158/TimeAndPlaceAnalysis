from flask import Flask, jsonify

app = Flask(__name__)

# Mock sensor location
chair_current_location = {
    'x': [-0.5, 0],
    'y': [1.8, 2.4]
}


@app.route('/api/sensor/location', methods=['GET'])
def get_sensor_location():
    return jsonify(chair_current_location)


if __name__ == '__main__':
    app.run(debug=True)
