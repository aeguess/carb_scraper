import pandas as pd
import os
# from datetime import date

def data_cleanup(pollutant_df, pollutant_name, pollutant_dir):
    '''
    Description:
        Cleans up data to be imported into Prism for figure generation. Reuses some code from daily_cum.py
        
        
    Experimental groups:
        infant exposed: Nov 8, 2017 to June 4, 2022
        
        in utero exposed: Nov 8, 2018 to June 4, 2023
        
        ctrl exposed: Nov 8, 2019 to June 4, 2024
    '''
    
    
    daily_cum_exp = pollutant_df.groupby('date')['value'].sum().reset_index()
    
    daily_cum_exp['date'] = pd.to_datetime(daily_cum_exp['date'])
    daily_cum_exp = daily_cum_exp.sort_values(by='date').reset_index(drop=True)
    
    
    # Infant exposure
    
    mask = (daily_cum_exp['date'] >= '2017-11-8') & (daily_cum_exp['date'] <= '2022-7-4')
    infant_exposed = daily_cum_exp.loc[mask]
    
   # daily_cum_file_path = os.path.join(pollutant_dir, (str(pollutant_name) + '_infant_CLEANED.csv'))
   # infant_exposed.to_csv(daily_cum_file_path, index=False)
        
   # print(f"Daily cumulative exposure file for infant exposure to {pollutant_name} saved at {daily_cum_file_path}\n")


    # In Ut exposure
    
    mask = (daily_cum_exp['date'] >= '2018-11-8') & (daily_cum_exp['date'] <= '2023-7-4')
    in_ut_exp = daily_cum_exp.loc[mask]

   # daily_cum_file_path = os.path.join(pollutant_dir, (str(pollutant_name) + '_inutero_CLEANED.csv'))
    #in_ut_exp.to_csv(daily_cum_file_path, index=False)
        
   # print(f"Daily cumulative exposure file for in utero exposure to {pollutant_name} saved at {daily_cum_file_path}\n")
    
    
    # Ctrl exp
    
    mask = (daily_cum_exp['date'] >= '2019-11-8') & (daily_cum_exp['date'] <= '2024-7-4')
    ctrl_exp = daily_cum_exp.loc[mask]
    
   # daily_cum_file_path = os.path.join(pollutant_dir, (str(pollutant_name) + '_ctrl_CLEANED.csv'))
    #ctrl_exp.to_csv(daily_cum_file_path, index=False)
        
   # print(f"Daily cumulative exposure file for contrtol (2019) exposure to {pollutant_name} saved at {daily_cum_file_path}\n")
    
    # Combine the data into a single DataFrame
    
    combined_df = pd.DataFrame({
      #  'date': pd.to_datetime(daily_cum_exp['date']),
        'infant': infant_exposed['value'],
        'inutero': in_ut_exp['value'],
        'ctrl': ctrl_exp['value']
    }).reset_index(drop=True)
    
    combined_df.fillna(0, inplace=True)
    
    combined_file_path = os.path.join(pollutant_dir, f'{pollutant_name}_combined_CLEANED.csv')
    combined_df.to_csv(combined_file_path, index=False)
    
    print(f"Combined daily cumulative exposure file saved at {combined_file_path}\n")
        