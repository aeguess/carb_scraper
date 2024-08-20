import time
import pandas as pd
import os
from os import rename, listdir
#import openpyxl
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options

from webdriver_manager.firefox import GeckoDriverManager



def carb_scraper(driver, websites, date_list, pollutants):
    
    for index, website in enumerate(websites):
        
        time.sleep(3) # 2s delay minimum for robots.txt https://www.arb.ca.gov/robots.txt
        driver.get(website)
        
        
        for date in date_list:
            
            time.sleep(3)
            
            curr_date = date.split("_")
            
            select = Select(driver.find_element_by_id('year'))
            select.select_by_visible_text(curr_date[0])
            
            select = Select(driver.find_element_by_id('mon'))
            select.select_by_visible_text(curr_date[1])
            
            select = Select(driver.find_element_by_id('day'))
            select.select_by_visible_text(curr_date[2])
            
            xpath='//*[@id="btnsubmit"]'
            driver.find_element_by_xpath(xpath).click() # update display with current date info
            
            #xpath + '//*[@id="content_area"]/center[2]/table[2]/tbody/tr[1]/td[2]'
            #if "No Data Available.  Please try your query again." in xpath:
            #    website = "https://www.arb.ca.gov/aqmis2/display.php?report=SITE31D&site=2143&monitor=-&year=2024&mon=08&day=08&param=PM25&units=001&statistic=HVAL&ptype=aqd&o3switch=new&hours=all"
            
            xpath='//*[@id="content_area"]/center[2]/table[2]/tbody/tr[2]/td[2]/a[1]'
            driver.find_element_by_xpath(xpath).click() # download data
            
            time.sleep(2) # delay for download to complete
            
            date = (date.split("_"))[0:2] # removes default date of "1" used to query CARB
            date = date[0] + "_" + date[1] # isolates year + month
            current_date = str(date) + "_" + str(pollutants[index]+'.csv')
            
            original_file = os.path.join(os.getcwd(), "datafile.txt")
            new_file = os.path.join(os.getcwd(), pollutants[index], current_date)

            os.rename(original_file, new_file) # Moves file into subfolder based on pollutant and renames file from datafile.txt to date_pollutant.csv
        
        
        
 


def driver_startup():

    options = Options()
    options.binary_location = r'C:\Program Files\Firefox\firefox.exe'
    
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "pollutant_data")
    
    profile = webdriver.FirefoxProfile()
    
    profile.set_preference("browser.download.folderList", 2)  # Use a custom download directory
    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")  # Ignores downloads popup for .txts
    profile.set_preference("pdfjs.disabled", True)  # Disable the built-in PDF viewer

	# Comment out the line below if you want to see what is going on in the browser when this runs
	#options.add_argument("--headless")

	# Install Geckodriver
    driver = webdriver.Firefox(executable_path=GeckoDriverManager(version="v0.20.0").install(), options=options, firefox_profile=profile)

    time.sleep(2)

    return driver



def read_data_until_pattern(file_path, pattern):
    '''
        Description: removes fluff from end of CARB sensor data.
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    end_index = next((i for i, line in enumerate(lines) if pattern in line), len(lines))
    data_lines = lines[:end_index]
    data = pd.read_csv(pd.compat.StringIO(''.join(data_lines)))

    return data



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
            master_df = master_df.set_index('date').combine_first(df.set_index('date')).reset_index()
        
    
        
        master_df['date'] = pd.to_datetime(master_df['date'], format='%Y-%m-%d')
        master_df = master_df.sort_values(by='date')
        master_df = master_df.reset_index(drop=True)
        
        
        master_file_path = os.path.join(pollutant_dir, (str(pollutant) + '_merged.csv'))
        master_df.to_csv(master_file_path, index=False)
        print(f"Merged file for {pollutant} saved at {master_file_path}")



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
    print("Pulling data on:\n" + str(pollutants) + "\n\n Between the dates of: \n" + str(date_list) + "\n\nExporting to:\n" + os.getcwd())
    
    
    
    driver = driver_startup()
    carb_scraper(driver, websites, date_list, pollutants)
    merge_files(pollutants)


main()