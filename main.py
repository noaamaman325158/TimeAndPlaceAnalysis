import datetime

# Temporary global variable with the current chair location



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


# Function to get the current chair location
def get_current_chair_location():
    return chair_current_location


# Function to parse a log entry and extract relevant information
def parse_log_entry(log_entry):
    entry_data = {}
    parts = log_entry.split()

    if "Process" in log_entry and "frame without interrupt" in log_entry:
        entry_data['frame_number'] = int(parts[4])
    elif "[FPS]" in log_entry:
        entry_data['fps_value'] = float(parts[6].split('=')[1])
    elif "Targets:" in log_entry:
        entry_data['number_of_targets'] = int(parts[1])
    elif "t_id=" in log_entry:
        entry_data['x_value'] = float(parts[4][2:])
        entry_data['y_value'] = float(parts[5][2:])
        entry_data['z_value'] = float(parts[6][2:])

    return entry_data


def convert_log_file_data_to_dict(log_file_data):
    log_data_dict = {}

    for log_entry in log_file_data:
        if 'endOfFrame' in log_entry:
            entry_data = parse_log_entry(log_entry)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_data_dict[timestamp] = entry_data

    return log_data_dict


def calculate_total_time_in_chair_surface(log_data, chair_location):
    total_time_duration = datetime.timedelta()
    prev_timestamp = None

    for timestamp, entry_data in sorted(log_data.items()):
        if prev_timestamp is not None:
            time_difference = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
                prev_timestamp, '%Y-%m-%d %H:%M:%S')

            x_value = entry_data['x_value']
            y_value = entry_data['y_value']

            if is_in_chair_surface((x_value, y_value), chair_location):
                total_time_duration += time_difference

        prev_timestamp = timestamp

    return total_time_duration


def main():
    log_file_data = [
        "Process frame without interrupt: 598",
        "[FPS] Average last 1 frame FPS=10.02",
        "Targets: 1",
        "t_id=0 x=+0.6 y=+0.7 z=+0.8",
        "endOfFrame",
        "Process frame without interrupt: 599",
        "[FPS] Average last 1 frame FPS=10.02",
        "Targets: 1",
        "t_id=0 x=+0.7 y=+0.7 z=+0.8",
        "endOfFrame",
        "Process frame without interrupt: 600",
        "[FPS] Average last 1 frame FPS=10.07",
        "Targets: 1",
        "t_id=0 x=+0.7 y=+0.7 z=+0.8",
        "endOfFrame"
    ]

    current_location = get_current_chair_location()
    log_data_dict = convert_log_file_data_to_dict(log_file_data)

    total_time_in_range_loc = calculate_total_time_in_chair_surface(log_data_dict, current_location)
    print(f'Total time in chair surface: {total_time_in_range_loc}')


if __name__ == '__main__':
    main()
