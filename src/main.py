import datetime
import json

import pandas as pd
import requests

from Utils.data_operations import parse_log_file, extract_coordinates, wrapper_get_dataframe_from_log, \
    save_dataframe_to_csv
from Utils.data_visulization_utils import analyze_movement
from constants import API_URI, PATH_LOG_FILE, DATA_PROVIDED_TIME, FRAME, FPS, TARGETS, END_OF_FRAME, X, Y
from src.Utils.data_preparation import prepare_sensor_data


def point_in_range(location, point):
    """
    This function is determined if some point is inside the range that we get from the API of the chair location
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
    """
    Wrapper function for the point_in_range function
    :param point:
    :param chair_loc:
    :return:
    """
    return point_in_range(chair_loc, point)


def get_current_chair_location():
    """
    This method is fetch the data from some external third party or more concisely mock api in this case
    :return:
    """
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
    This method is parsing the static schema that exists with the given log file
    every measurement is located inside some dictionary collection with the required attributes
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
    Calculates the total time a person was detected in the chair area, assuming each row in prepared_data
    represents a unique frame with a timestamp.

    Parameters:
    prepared_data (DataFrame): The prepared DataFrame with sensor data including timestamps.
    chair_location (dict): A dictionary with 'x' and 'y' keys, each containing a range [min, max].

    Returns:
    float: The total time in seconds that the person was in the chair area.
    """

    def is_in_chair(row):
        point = (row['x'], row['y'])  # Replace 'x' and 'y' with actual column names
        return is_in_chair_surface(point, chair_location)

    # Filter the data to include only rows where the person is in the chair
    in_chair_data = prepared_data[prepared_data.apply(is_in_chair, axis=1)]

    # Calculate the total time
    if 'timestamp' in in_chair_data.columns:
        in_chair_data['timestamp'] = pd.to_datetime(in_chair_data['timestamp'])
        time_differences = in_chair_data['timestamp'].diff().fillna(pd.Timedelta(seconds=DATA_PROVIDED_TIME))
        total_time = time_differences.sum().total_seconds()
    else:
        # Fallback to using FPS if timestamps are not available
        frames_in_chair = in_chair_data.shape[0]
        average_fps = prepared_data['fps'].mean()  # Replace 'fps' with actual column name
        total_time = frames_in_chair / average_fps

    return total_time



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
    x_y_z = extract_coordinates(log_file_measurement)
    analyze_movement(x_y_z, current_location_range_dict)

    # Calculate the time in chair using the second approach - Data Science Based Approach
    # Prepare the Data for Analysis steps
    # after_preparations_df = prepare_sensor_data("assets/sensor_data.csv")
    # time_in_chair = calculate_time_in_chair_df(after_preparations_df, current_location_range_dict)



if __name__ == '__main__':
    main()
