from constants import FRAME, FPS, TARGETS, END_OF_FRAME
import re
import pandas as pd

def extract_coordinates(log_file_measurement):
    """
    Extracts x and y coordinates from a list of log file measurements.

    Each measurement is expected to be a dictionary with keys for different target data.
    This function specifically looks for 'x' and 'y' coordinates of 'target_0_data'.

    Parameters:
    log_file_measurement (list of dict): A list of dictionaries, each representing a single measurement.

    Returns:
    dict: A dictionary with two keys, 'x' and 'y', each containing a list of coordinate values.
    """
    extracted_coordinates = {'x': [], 'y': [], 'z': []}

    for measurement in log_file_measurement:
        x_value = measurement.get('target_0_data', {}).get('x', None)
        y_value = measurement.get('target_0_data', {}).get('y', None)
        z_value = measurement.get('target_0_data', {}).get('z', None)

        if x_value is not None and y_value is not None:
            extracted_coordinates['x'].append(x_value)
            extracted_coordinates['y'].append(y_value)
            extracted_coordinates['z'].append(z_value)

    return extracted_coordinates


def parse_log_file(file_path):
    """
    Parses a log file to extract frame, FPS, target, and coordinate data.

    This function reads a log file line by line and uses regular expressions to find and extract
    relevant data, such as frame number, FPS value, number of targets, and their coordinates.

    Parameters:
    file_path (str): The path to the log file.

    Returns:
    list of dict: A list of dictionaries, each containing data for a single frame.
    """
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
                measurement = {FRAME: int(frame_match.group(1))}
            elif fps_match:
                measurement[FPS] = float(fps_match.group(1))
            elif target_match:
                measurement[TARGETS] = int(target_match.group(1))
            elif target_data_match:
                t_id = int(target_data_match.group(1))
                x = float(target_data_match.group(2))
                y = float(target_data_match.group(3))
                z = float(target_data_match.group(4))
                measurement[f'target_{t_id}_data'] = {'x': x, 'y': y, 'z': z}
            elif END_OF_FRAME in line:
                measurements.append(measurement)

    return measurements


def parse_log_file_to_dataframe(file_path):
    """
    Converts log file data into a pandas DataFrame.

    This function first parses a log file using `parse_log_file` to get a list of frame data
    and then converts this list into a pandas DataFrame for easier data manipulation and analysis.

    Parameters:
    file_path (str): The path to the log file.

    Returns:
    pandas.DataFrame: A DataFrame containing the parsed log file data.
    """
    data_rows = parse_log_file(file_path)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_rows)
    return df


def wrapper_get_dataframe_from_log(file_path):
    """
    Wrapper function to get DataFrame from log file.

    This function is a simple wrapper around `parse_log_file_to_dataframe`,
    used for obtaining a DataFrame directly from a log file path.

    Parameters:
    file_path (str): The path to the log file.

    Returns:
    pandas.DataFrame: A DataFrame containing the parsed log file data.
    """
    df = parse_log_file_to_dataframe(file_path)
    return df


def save_dataframe_to_csv(df, csv_file_name):
    """
    Saves a DataFrame to a CSV file.

    Parameters:
    df (pandas.DataFrame): The DataFrame to save.
    csv_file_name (str): The name of the CSV file to save the DataFrame to.

    Returns:
    None
    """
    df.to_csv(csv_file_name, index=False)
    print(f"Data saved to {csv_file_name}.")
