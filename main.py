import datetime

# temporary gloval variable with the current location with the range
chair_current_location = {
    'x': [-0.5, 0],
    'y': [1.8, 2.4]
}


# Get the current chair location from a third party that mangae the sensor
def get_current_chair_location():
    return chair_current_location


def point_in_range(location, point):
    x_lower_bound, x_upper_bound = location['x'][0], location['x'][1]
    y_lower_bound, y_upper_bound = location['y'][0], location['y'][1]

    x_value = point[0]
    y_value = point[1]

    in_x_range = x_lower_bound <= x_value <= x_upper_bound
    in_y_range = y_lower_bound <= y_value <= y_upper_bound

    return in_x_range and in_y_range


def is_in_chair_surface(point, chair_loc):
    return point_in_range(chair_loc, point)


def calculate_total_time_in_chair_surface(log_data, chair_location):
    pass



