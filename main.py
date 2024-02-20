import datetime, re, requests, json

# Temporary global variable with the current chair location

API_URI = "http://127.0.0.1:5000/api/chair/location"
PATH_LOG_FILE = "tracker_log.log"


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
    try:
        response = requests.get(API_URI)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


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


def calculate_total_time_in_chair_surface(log_data, chair_location):
    pass


def parse_log_file(file_path):
    measurements = []

    # Regular expressions to extract relevant data
    frame_pattern = re.compile(r'Process frame without interrupt: (\d+)')
    fps_pattern = re.compile(r'\[FPS\] Average last 1 frame FPS=(\d+\.\d+)')
    target_pattern = re.compile(r'Targets: (\d+)')
    target_data_pattern = re.compile(r't_id=(\d+) x=([+-]\d+\.\d+) y=([+-]\d+\.\d+) z=([+-]\d+\.\d+)')

    with open(file_path, 'r') as file:
        measurement = {}

        for line in file:
            frame_match = frame_pattern.search(line)
            fps_match = fps_pattern.search(line)
            target_match = target_pattern.search(line)
            target_data_match = target_data_pattern.search(line)

            if frame_match:
                measurement = {'frame': int(frame_match.group(1))}
            elif fps_match:
                measurement['fps'] = float(fps_match.group(1))
            elif target_match:
                measurement['targets'] = int(target_match.group(1))
            elif target_data_match:
                t_id = int(target_data_match.group(1))
                x = float(target_data_match.group(2))
                y = float(target_data_match.group(3))
                z = float(target_data_match.group(4))
                measurement[f'target_{t_id}_data'] = {'x': x, 'y': y, 'z': z}
            elif 'endOfFrame' in line:
                # End of a measurement, append to the list
                measurements.append(measurement)

    return measurements


def main():
    log_file_measurement = parse_log_file(PATH_LOG_FILE)

    current_location_range_json = get_current_chair_location()
    current_location_range_dict_str = json.dumps(current_location_range_json)
    current_location_range_dict = json.loads(current_location_range_dict_str)
    total_time_in_range_loc = calculate_total_time_in_chair_surface(log_file_measurement, current_location_range_dict)
    print(f'Total time in chair surface: {total_time_in_range_loc}')


if __name__ == '__main__':
    main()
