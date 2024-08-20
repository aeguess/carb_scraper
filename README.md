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
