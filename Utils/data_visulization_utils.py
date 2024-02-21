from constants import DATA_PROVIDED_TIME
import matplotlib.pyplot as plt

def analyze_movement(coordinates, chair_location):
    x_values = coordinates.get('x', [])
    y_values = coordinates.get('y', [])

    dt = DATA_PROVIDED_TIME
    vx = [(x_values[i + 1] - x_values[i]) / dt for i in range(len(x_values) - 1)]
    vy = [(y_values[i + 1] - y_values[i]) / dt for i in range(len(y_values) - 1)]

    ax = [(vx[i + 1] - vx[i]) / dt for i in range(len(vx) - 1)]
    ay = [(vy[i + 1] - vy[i]) / dt for i in range(len(vy) - 1)]

    chair_x_range = chair_location.get('x', [])
    chair_y_range = chair_location.get('y', [])

    # Plotting
    plt.figure(figsize=(12, 8))

    # X Coordinate
    plt.subplot(3, 1, 1)
    plt.plot(x_values, label='X Coordinate')
    plt.title('X Coordinate')
    plt.xlabel('Frame')
    plt.ylabel('X')
    plt.axhline(y=chair_x_range[0], color='r', linestyle='--', label='Chair X Lower Bound')
    plt.axhline(y=chair_x_range[1], color='g', linestyle='--', label='Chair X Upper Bound')
    plt.legend()

    # X Velocity
    plt.subplot(3, 1, 2)
    plt.plot(vx, label='X Velocity')
    plt.title('X Velocity')
    plt.xlabel('Frame')
    plt.ylabel('Velocity (m/s)')
    plt.axhline(y=0, color='b', linestyle='--', label='Zero Velocity')
    plt.legend()

    # X Acceleration
    plt.subplot(3, 1, 3)
    plt.plot(ax, label='X Acceleration')
    plt.title('X Acceleration')
    plt.xlabel('Frame')
    plt.ylabel('Acceleration (m/s^2)')
    plt.axhline(y=0, color='b', linestyle='--', label='Zero Acceleration')
    plt.legend()

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 8))

    # Y Coordinate
    plt.subplot(3, 1, 1)
    plt.plot(y_values, label='Y Coordinate')
    plt.title('Y Coordinate')
    plt.xlabel('Frame')
    plt.ylabel('Y')
    plt.axhline(y=chair_y_range[0], color='r', linestyle='--', label='Chair Y Lower Bound')
    plt.axhline(y=chair_y_range[1], color='g', linestyle='--', label='Chair Y Upper Bound')
    plt.legend()

    # Y Velocity
    plt.subplot(3, 1, 2)
    plt.plot(vy, label='Y Velocity')
    plt.title('Y Velocity')
    plt.xlabel('Frame')
    plt.ylabel('Velocity (m/s)')
    plt.axhline(y=0, color='b', linestyle='--', label='Zero Velocity')
    plt.legend()

    # Y Acceleration
    plt.subplot(3, 1, 3)
    plt.plot(ay, label='Y Acceleration')
    plt.title('Y Acceleration')
    plt.xlabel('Frame')
    plt.ylabel('Acceleration (m/s^2)')
    plt.axhline(y=0, color='b', linestyle='--', label='Zero Acceleration')
    plt.legend()

    plt.tight_layout()
    plt.show()