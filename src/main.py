import datetime
import json
import requests

from Utils.data_operations import parse_log_file, extract_coordinates, wrapper_get_dataframe_from_log, \
    save_dataframe_to_csv
from Utils.data_visulization_utils import analyze_movement
from constants import API_URI, PATH_LOG_FILE, DATA_PROVIDED_TIME, FRAME, FPS, TARGETS, END_OF_FRAME, X, Y
from src.Utils.data_preparation import prepare_sensor_data


def point_in_range(location, point):
    """

    :param location:
    :param point:
    :return:
    """
    x_lower_bound, x_upper_bound = location[X][0], location[X][1]
    y_lower_bound, y_upper_bound = location[Y][0], location[Y][1]

    x_value = point[0]
    y_value = point[1]

    in_x_range = x_lower_bound <= x_value <= x_upper_bound
    in_y_range = y_lower_bound <= y_value <= y_upper_bound

    return in_x_range and in_y_range


def is_in_chair_surface(point, chair_loc):
    return point_in_range(chair_loc, point)


def get_current_chair_location():
    try:
        response = requests.get(API_URI)
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def parse_log_entry(log_entry):
    """

    :param log_entry:
    :return:
    """
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
    """

    :param log_data:
    :param chair_location:
    :return:
    """
    total_time_duration = datetime.timedelta()
    prev_frame_number = None

    for measurement in log_data:
        frame_number = measurement.get('frame')
        time_difference = datetime.timedelta(seconds=DATA_PROVIDED_TIME)

        if prev_frame_number is not None:
            for target_id in range(measurement.get('targets', 0)):
                target_key = f'target_{target_id}_data'
                if target_key in measurement:
                    x_value = measurement[target_key][X]
                    y_value = measurement[target_key][Y]

                    if is_in_chair_surface((x_value, y_value), chair_location):
                        total_time_duration += time_difference

        prev_frame_number = frame_number

    return total_time_duration


def calculate_time_in_chair_df(prepared_data, chair_location):
    """
    Calculates the total time a person was detected in the chair area.

    Parameters:
    prepared_data (DataFrame): The prepared DataFrame with sensor data.
    chair_location (dict): A dictionary with 'x' and 'y' keys, each containing a range [min, max].

    Returns:
    float: The total time in seconds that the person was in the chair area.
    """

    # Filter the DataFrame for rows where the person is within the chair location bounds
    in_chair_condition = (
            (prepared_data[X] >= chair_location[X][0]) & (prepared_data[Y] <= chair_location[X][1]) &
            (prepared_data[Y] >= chair_location[Y][0]) & (prepared_data[Y] <= chair_location[Y][1])
    )
    in_chair_data = prepared_data[in_chair_condition]

    # Calculate the time spent in the chair by counting the frames and dividing by the frame rate
    # Assuming each frame represents an equal interval of time and the fps is constant
    frames_in_chair = in_chair_data.shape[0]
    average_fps = prepared_data[FPS].mean()
    time_in_chair_seconds = frames_in_chair / average_fps

    return time_in_chair_seconds


def main():
    log_file_measurement = parse_log_file(PATH_LOG_FILE)

    current_location_range_json = get_current_chair_location()

    current_location_range_dict_str, current_location_range_dict = None, None
    if current_location_range_json is not None:
        current_location_range_dict_str = json.dumps(current_location_range_json)
        current_location_range_dict = json.loads(current_location_range_dict_str)
        total_time_in_range_loc = calculate_total_time_in_chair_surface(log_file_measurement,
                                                                        current_location_range_dict)
        print(f'Total time in chair surface: {total_time_in_range_loc}')
    else:
        print("Error: Failed to retrieve chair location.")

    # Analyzing and visualizing the data
    x_y = extract_coordinates(log_file_measurement)
    analyze_movement(x_y, current_location_range_dict)

    # Prepare the Data for Analysis steps
    after_preparations_df = prepare_sensor_data("assets/sensor_data.csv")
    print(after_preparations_df)
    chair_location = {

        'x': [-0.5, 0],

        'y': [1.8, 2.4]

    }

    # Calculate the time in chair using the prepared data and the chair location

    time_in_chair = calculate_time_in_chair_df(after_preparations_df, chair_location)
    print(time_in_chair)


if __name__ == '__main__':
    main()
