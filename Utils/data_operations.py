from constants import FRAME, FPS, TARGETS, END_OF_FRAME
import re


def extract_coordinates(log_file_measurement):
    extracted_coordinates = {'x': [], 'y': []}

    for measurement in log_file_measurement:
        x_value = measurement.get('target_0_data', {}).get('x', None)
        y_value = measurement.get('target_0_data', {}).get('y', None)

        if x_value is not None and y_value is not None:
            extracted_coordinates['x'].append(x_value)
            extracted_coordinates['y'].append(y_value)

    return extracted_coordinates


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
                # End of a measurement, append to the list
                measurements.append(measurement)

    return measurements
