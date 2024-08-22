import os
#import openpyxl

from carb_scripts import carb_scraper
from carb_scripts import driver_startup
from carb_scripts import merge_files
from carb_scripts import data_cleanup


def main():
    '''
        Description: Pulls PM2.5, NO2, O3, and temperature readings from Davis-UCD sensor for 2018 Camp Fire project.
    '''
    pollutants = ["ozone", 
                 "pm_25", 
                 "no2", 
                 "temp_f"]
    
    if not os.path.exists(os.path.join(os.getcwd(), "pollutant_data")):
        os.makedirs(os.path.join(os.getcwd(), "pollutant_data"))
        
    os.chdir(os.path.join(os.getcwd(), "pollutant_data"))
        
    # Generates folders in local directory of ozone/pm_25/no2/temperature
    folder_list = [(os.path.join(os.getcwd(), "ozone")), 
                   (os.path.join(os.getcwd(), "pm_25")), 
                   (os.path.join(os.getcwd(), "no2")), 
                   (os.path.join(os.getcwd(), "temp_f"))]
    
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)
            
    
    websites = ["https://www.arb.ca.gov/aqmis2/display.php?report=SITE31D&site=2143&year=2024&mon=08&day=13&hours=all&statistic=HVAL&ptype=aqd&param=OZONE_ppm",
               "https://www.arb.ca.gov/aqmis2/display.php?report=SITE31D&site=2143&monitor=-&year=2024&mon=08&day=08&param=PM25&units=001&statistic=HVAL&ptype=aqd&o3switch=new&hours=all",
               "https://www.arb.ca.gov/aqmis2/display.php?report=SITE31D&site=2143&year=2024&mon=08&day=13&hours=all&statistic=HVAL&ptype=aqd&param=NO2",
               "https://www.arb.ca.gov/aqmis2/display.php?year=2018&mon=12&day=1&site=2143&hours=all&o3switch=new&units=015&ptype=met&param=TEMP&report=SITE31D&statistic=DAVG&order=&btnsubmit=Update+Display"]
    
    # Generates the master list of year + months for file naming / querying CARB sensors in YEAR-MONTH-DAY format
    date_list = []
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    
    for year in years:
        for month in months:
            date_list.append(str(year) + "_" + month + "_" + "1")
    
    print("\nProgram description:\nPulls PM2.5, NO2, O3, and temperature readings from Davis-UCD sensor between Jan 2017 and Dec 2024 for 2018 Camp Fire Project.\n\n")
    print("Pulling data on:\n" + str(pollutants) + "\n\n Between the dates of: \n" + str(date_list[0]) + " to " +
          str(date_list[len(date_list) - 1]) + "\n\nExporting to:\n" + os.getcwd())
    
    
    
    #[driver, download_dir] = driver_startup.driver_startup()
    #carb_scraper.carb_scraper(driver, websites, date_list, pollutants, download_dir)
    merge_files.merge_files(pollutants)


main()