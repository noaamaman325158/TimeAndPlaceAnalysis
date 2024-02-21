from constants import DATA_PROVIDED_TIME
import matplotlib.pyplot as plt


def analyze_movement(coordinates, chair_location):
    """
    Analyzes and visualizes the movement in X, Y, and Z coordinates.

    This function calculates and plots the location, velocity, and acceleration for each
    of the X, Y, and Z coordinates. It plots these values in separate figures.
    Chair location boundaries are marked in the X and Y coordinate plots.

    Parameters:
    coordinates (dict): A dictionary containing lists of 'x', 'y', and 'z' coordinate values.
    chair_location (dict): A dictionary with 'x' and 'y' keys, each containing a range [min, max].

    Returns:
    None
    """
    # Extract coordinates and calculate velocity and acceleration
    x_values, y_values, z_values = coordinates.get('x', []), coordinates.get('y', []), coordinates.get('z', [])
    dt = DATA_PROVIDED_TIME

    # Function to calculate velocity and acceleration
    def calculate_velocity_acceleration(values):
        velocity = [(values[i + 1] - values[i]) / dt for i in range(len(values) - 1)]
        acceleration = [(velocity[i + 1] - velocity[i]) / dt for i in range(len(velocity) - 1)]
        return velocity, acceleration

    # Calculating for each coordinate
    vx, ax = calculate_velocity_acceleration(x_values)
    vy, ay = calculate_velocity_acceleration(y_values)
    vz, az = calculate_velocity_acceleration(z_values)

    # Chair location ranges
    chair_x_range = chair_location.get('x', [])
    chair_y_range = chair_location.get('y', [])

    # Function to plot each coordinate
    def plot_coordinate_analysis(values, velocity, acceleration, chair_range, coord_label):
        plt.figure(figsize=(12, 8))

        # Location
        plt.subplot(3, 1, 1)
        plt.plot(values, label=f'{coord_label} Coordinate')
        plt.title(f'{coord_label} Coordinate')
        plt.xlabel('Frame')
        plt.ylabel(coord_label)
        if coord_label in ['X', 'Y']:
            plt.axhline(y=chair_range[0], color='r', linestyle='--', label=f'Chair {coord_label} Lower Bound')
            plt.axhline(y=chair_range[1], color='g', linestyle='--', label=f'Chair {coord_label} Upper Bound')
        plt.legend()

        # Velocity
        plt.subplot(3, 1, 2)
        plt.plot(velocity, label=f'{coord_label} Velocity')
        plt.title(f'{coord_label} Velocity')
        plt.xlabel('Frame')
        plt.ylabel('Velocity (m/s)')
        plt.axhline(y=0, color='b', linestyle='--', label='Zero Velocity')
        plt.legend()

        # Acceleration
        plt.subplot(3, 1, 3)
        plt.plot(acceleration, label=f'{coord_label} Acceleration')
        plt.title(f'{coord_label} Acceleration')
        plt.xlabel('Frame')
        plt.ylabel('Acceleration (m/s^2)')
        plt.axhline(y=0, color='b', linestyle='--', label='Zero Acceleration')
        plt.legend()

        plt.tight_layout()
        plt.show()

    # Plotting for X, Y, and Z
    plot_coordinate_analysis(x_values, vx, ax, chair_x_range, 'X')
    plot_coordinate_analysis(y_values, vy, ay, chair_y_range, 'Y')
    plot_coordinate_analysis(z_values, vz, az, [], 'Z')
