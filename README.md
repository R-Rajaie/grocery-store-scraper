# grocery-store-scraper
This is a collection of web scrapers for collecting the locations of grocery stores across the US. Namely the ones that do not post their locations online (so the only option is to scrape them yourself). 

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
