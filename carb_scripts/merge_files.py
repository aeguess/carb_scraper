import pandas as pd
import os

from carb_scripts import read_data_until_pattern


def merge_files(pollutants):
    fluff = "Quality Flag Definition" # CARB .txt downloads come with 'fluff' at the end, marked by "Quality Flag Definition"

    for pollutant in pollutants:
        
        pollutant_dir = os.path.join(os.getcwd(), pollutant)
        print(pollutant_dir)
        
        if not os.path.exists(pollutant_dir):
            os.makedirs(pollutant_dir)
        
        all_files = [os.path.join(root, file)
                     for root, _, files in os.walk(pollutant_dir)
                     for file in files if file.endswith('.csv')]

        master_df = read_data_until_pattern(all_files[0], fluff)
        
        
        for filename in all_files[1:]:
            
            df = read_data_until_pattern(filename, fluff)
            
            if df is not None: # if df is a blank file, don't combine
                master_df = master_df.set_index('date').combine_first(df.set_index('date')).reset_index()
        
    
        
        master_df['date'] = pd.to_datetime(master_df['date'], format='%Y-%m-%d')
        master_df = master_df.sort_values(by='date')
        master_df = master_df.reset_index(drop=True)
        
        
        master_file_path = os.path.join(pollutant_dir, (str(pollutant) + '_merged.csv'))
        master_df.to_csv(master_file_path, index=False)
        print(f"Merged file for {pollutant} saved at {master_file_path}")

