from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Mock sensor location
chair_current_location = {
    'x': [-0.5, 0],
    'y': [1.8, 2.4]
}


@app.route('/')
def index():
    return "Real-time Sensor Location System"


@socketio.on('connect')
def handle_connect():
    emit_sensor_location()


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def emit_sensor_location():
    socketio.emit('sensor_location', chair_current_location)


@app.route('/api/chair/location', methods=['GET'])
def get_current_chair_location():
    return jsonify(chair_current_location)


if __name__ == '__main__':
    socketio.run(app, debug=True)
