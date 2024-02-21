import numpy as np

from src.constants import DATA_PROVIDED_TIME
import matplotlib.pyplot as plt


def calculate_jerk(acceleration, dt):
    """
    Calculate the jerk from acceleration data.

    Parameters:
    acceleration (list): List of acceleration values.
    dt (float): Time interval between data points.

    Returns:
    list: Calculated jerk values.
    """
    return np.diff(acceleration) / dt


def analyze_movement(coordinates, chair_location):
    """
    Analyzes and visualizes the movement in X, Y, and Z coordinates including
    location, velocity, acceleration, and jerk.

    Parameters:
    coordinates (dict): A dictionary containing lists of 'x', 'y', and 'z' coordinate values.
    chair_location (dict): A dictionary with 'x' and 'y' keys, each containing a range [min, max].

    Returns:
    None
    """
    dt = DATA_PROVIDED_TIME
    x_values, y_values, z_values = (coordinates.get(key) for key in ['x', 'y', 'z'])

    # Function to calculate velocity and acceleration
    def calculate_velocity_acceleration(values):
        velocity = np.diff(values) / dt
        acceleration = np.diff(velocity) / dt
        return velocity.tolist(), acceleration.tolist()

    # Calculating for each coordinate
    vx, ax = calculate_velocity_acceleration(x_values)
    vy, ay = calculate_velocity_acceleration(y_values)
    vz, az = calculate_velocity_acceleration(z_values)

    # Calculating jerk for each coordinate
    jx = calculate_jerk(ax, dt)
    jy = calculate_jerk(ay, dt)
    jz = calculate_jerk(az, dt)

    # Plotting for X, Y, and Z
    for i, (values, velocity, acceleration, jerk, coord_label) in enumerate(zip(
            (x_values, y_values, z_values),
            (vx, vy, vz),
            (ax, ay, az),
            (jx, jy, jz),
            ('X', 'Y', 'Z'))):
        plt.figure(figsize=(12, 8))

        # Location plot
        plt.subplot(4, 1, 1)
        plt.plot(values[:-2], label=f'{coord_label} Coordinate')  # Exclude the last 2 points for matching dimensions
        plt.title(f'{coord_label} Coordinate')
        plt.xlabel('Frame')
        plt.ylabel(coord_label)
        plt.legend()

        # Velocity plot
        plt.subplot(4, 1, 2)
        plt.plot(velocity[:-1], label=f'{coord_label} Velocity')  # Exclude the last point for matching dimensions
        plt.title(f'{coord_label} Velocity')
        plt.xlabel('Frame')
        plt.ylabel('Velocity (m/s)')
        plt.axhline(y=0, color='b', linestyle='--', label='Zero Velocity')
        plt.legend()

        # Acceleration plot
        plt.subplot(4, 1, 3)
        plt.plot(acceleration, label=f'{coord_label} Acceleration')
        plt.title(f'{coord_label} Acceleration')
        plt.xlabel('Frame')
        plt.ylabel('Acceleration (m/s^2)')
        plt.axhline(y=0, color='b', linestyle='--', label='Zero Acceleration')
        plt.legend()

        # Jerk plot
        plt.subplot(4, 1, 4)
        plt.plot(jerk, label=f'{coord_label} Jerk')
        plt.title(f'{coord_label} Jerk')
        plt.xlabel('Frame')
        plt.ylabel('Jerk (m/s^3)')
        plt.axhline(y=0, color='b', linestyle='--', label='Zero Jerk')
        plt.legend()

        plt.tight_layout()
        plt.show()
