import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def driver_startup():
    '''
        Description: returns the download directory of the data and the driver necessary to scraper the CARB site.

    '''

    options = Options()
    options.binary_location = r'C:\Program Files\Firefox\firefox.exe'
    
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "pollutant_data_temp")
    
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

    return driver, download_dir

