import pandas as pd
import os
from datetime import date

def daily_cum(pollutant_df, pollutant_name, pollutant_dir):
    #pollutant_df.columns = ['site', 'date', 'start_hour', 'value', 'variable', 'units', 'quality', 'prelim', 'name']
    
    daily_cum_exp = pollutant_df.groupby('date')['value'].sum().reset_index()
    
    daily_cum_exp['date'] = pd.to_datetime(daily_cum_exp['date'])
    daily_cum_exp = daily_cum_exp.sort_values(by='date').reset_index(drop=True)
    
    daily_cum_file_path = os.path.join(pollutant_dir, (str(pollutant_name) + '_dailycum.csv'))
    daily_cum_exp.to_csv(daily_cum_file_path, index=False)
    
    print(f"Daily cumulative exposure file for {pollutant_name} saved at {daily_cum_file_path}")
    