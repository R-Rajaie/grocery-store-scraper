# Store Location Scraper
This is a collection of web scrapers for collecting the locations of grocery stores across the US (and can work with many other types of chain stores with similarly formatted location selector pages when the code is properly tweaked). Namely the ones that do not post their locations online (so the only option is to scrape them yourself). 

These are created using Selenium (UI automation), Chromedriver (Chrome emulation), Pandas (data collection), and BeautifulSoup4 (html parsing)

## Requirements
You must set up a virtual Python environment in order to properly run these. 

### Directions to set up a virtual environment
```
python -m venv myenv
source myenv/bin/activate
```
This will create an environment file in your project (ensure you're cd'ed in the project). You must only create the environment once, but you must source it every time you open a new terminal to run any of the scripts. 

### Directions to install required dependencies
``` pip install -r requirements.txt ```
This should install all required dependencies. Ensure you're cd'ed in the project.


### Directions to run
To scrape, just run the corresponding file. To collect every Whole Foods, for example, run `whole_foods_locations.py`. 


## Disclaimer
This was made in part by AI. The code is not perfect, and I do not have a perfect understanding of the libraries I am using (specifically bs4). Therefore, there may be inefficiencies present in the code. Feel free to raise issues or push your own suggestions to improve stability and efficiency. 

Also feel free to use this code as a base for your own needs and customize it accordingly. There are fields I didn't bother to collect since they weren't relevant to me, but maybe they're useful for you. Similarly, you can repurpose this code for grocery store websites which aren't covered in this repo. Most store locators fall under the umbrella of a few different groups, so it should be relatively simple to slightly modify some fields and some logic to fit most situations. 
