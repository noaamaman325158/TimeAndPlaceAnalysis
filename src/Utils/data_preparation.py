import pandas as pd
import json

from src.Utils.data_operations import wrapper_get_dataframe_from_log, save_dataframe_to_csv
from src.constants import PATH_LOG_FILE, X, Y, Z


def generate_csv_file(path_to_log_file):
    df = wrapper_get_dataframe_from_log(path_to_log_file)

    save_dataframe_to_csv(df, "assets/sensor_data.csv")


def prepare_sensor_data(path_to_file):
    """
       Loads and prepares sensor data from a CSV file for analysis.

       Parameters:
       csv_file_path (str): The file path to the CSV file containing sensor data.

       Returns:
       DataFrame: A pandas DataFrame with the sensor data ready for analysis.
       """

    sensor_data = pd.read_csv(path_to_file)

    def safe_parse_json(json_str):
        try:
            return json.loads(json_str.replace("'", "\""))
        except (ValueError, AttributeError):
            return None

    # Apply the parsing function to the 'target_0_data' column
    sensor_data['parsed_target_data'] = sensor_data['target_0_data'].apply(safe_parse_json)

    target_data_keys = [X, Y, Z]
    for key in target_data_keys:
        sensor_data[key] = sensor_data['parsed_target_data'].apply(lambda row: row.get(key) if row else None)

    sensor_data.drop(columns=['target_0_data', 'parsed_target_data'], inplace=True)

    return sensor_data
