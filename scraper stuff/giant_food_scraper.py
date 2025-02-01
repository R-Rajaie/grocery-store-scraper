# Food Lion, Stop & Shop, GIANT, Giant Food, and Hannaford are all part of Ahold Delhaize and have nearly identical store locators. They are also very similar to what Safeway and Albertsons have.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup 

# Boot up chromedriver, set up bs4
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
url = "https://stores.giantfood.com/"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(1)

all_stores = []

def get_info_one(location):
    address = location.find(class_="c-address-street-1").get_text() + ", " + location.find(class_="c-address-city").get_text() + " " + location.find(class_="c-address-state").get_text() + " " + location.find(class_="c-address-postal-code").get_text()
    phone = location.find(class_="c-phone-number-span c-phone-main-number-span").get_text()
    print(address + " " + phone)
    all_stores.append({"Address": address, "Phone": phone})

def get_info_multiple(page):
    locations = page.find_all(class_="LocationList-item l-col-xs-12 l-col-sm-6 l-col-md-3-up")
    for location in locations:
        suffix = location.find(class_="Link--primary").get('href')
        driver.get("https://stores.giantfood.com/" + suffix)
        time.sleep(1)
        get_info_one(BeautifulSoup(driver.page_source, 'html.parser'))


states = soup.find_all(class_="DirectoryList-item")
for state in states: 
    suffix = state.find(class_="DirectoryList-itemLink Link--secondary").get('href')
    driver.get(url + suffix)
    time.sleep(1)
    state_locs = BeautifulSoup(driver.page_source, 'html.parser')

    if driver.current_url == "https://stores.giantfood.com/dc/washington": 
        get_info_multiple(state_locs)

    cities = state_locs.find_all(class_="DirectoryList-item")

    for city in cities:
        suffix = city.find(class_="DirectoryList-itemLink Link--secondary").get('href')
        driver.get("https://stores.giantfood.com/" + suffix)
        time.sleep(1)
        info = BeautifulSoup(driver.page_source, 'html.parser')

        if(city.find(class_="DirectoryList-itemCount").get_text() == "(1)"):
            get_info_one(info)
        else:
            get_info_multiple(info)
        
df = pd.DataFrame(all_stores)
df.to_csv("giant_food_locations.csv", index=False)
driver.quit()