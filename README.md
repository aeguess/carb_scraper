# Description
Ass part of the 2018 Camp Fire developmental response project, we need to scrape cal air sensor data to estimate exposure to our groups of interest. We're using CARB data from ([this](https://ww3.arb.ca.gov/qaweb/iframe_site.php?s_arb_code=57577)) site. We're scraping data on temperature, ozone, PM2.5, and NO2 to compare between a 2019 control group, a 2018 in-utero exposed group, and a 2017 infant exposed group.

# Software Prerequisites
This script executes on an outdated version of Firefox ([Version 56](https://www.mozilla.org/en-US/firefox/56.0/releasenotes/)) which should be downloaded prior to running the Python script. To assist in managing Python packages, install either mini or anaconda through either the terminal or app. Miniconda (a lighter version of Anaconda) can be found ([here](https://docs.anaconda.com/miniconda/)).

For a more in-depth guide on installing the software and setting up the virtual environment, see [here](https://github.com/lmillergrp/webvitals).

# Installing the virtual environment and executing the script
To build the environment using Conda, execute the following in your terminal:
```
conda env create -n webvitals2 -f environment.yml
```
followed by
```
conda activate webvitals2
```

To execute the script, execute the following in your terminal:
```
cd Downloads
```
followed by
```
python carb_scraper.py
```

The Python script will then begin executing, and will take a few hours to complete data scraping.
