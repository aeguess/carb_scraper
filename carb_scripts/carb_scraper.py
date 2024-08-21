import time
import os
from selenium.webdriver.support.ui import Select


def carb_scraper(driver, websites, date_list, pollutants, download_dir):
    '''
        Description: primary function for program. Iteratively scrapes CARB site for each pollutant between dates of interest.
    '''
    
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
            
            original_file = os.path.join(download_dir, "datafile.txt")
            #original_file = os.path.join("Downloads/pollutant_data/datafile.txt")
            new_file = os.path.join(os.getcwd(), pollutants[index], current_date)

            os.rename(original_file, new_file) # Moves file into subfolder based on pollutant and renames file from datafile.txt to date_pollutant.csv
        
    