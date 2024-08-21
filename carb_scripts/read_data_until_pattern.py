import pandas as pd


def read_data_until_pattern(file_path, pattern):
    '''
        Description: removes description of data from end of CARB sensor data.
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    end_index = next((i for i, line in enumerate(lines) if pattern in line), len(lines))
    data_lines = lines[:end_index]
    
    if not data_lines: # Empty datafile, e.g. from trying to get data from a date after today's date
        print("Empty CARB file at: " + file_path)
        return None
        
    else:
        data = pd.read_csv(pd.compat.StringIO(''.join(data_lines)))
        return data
